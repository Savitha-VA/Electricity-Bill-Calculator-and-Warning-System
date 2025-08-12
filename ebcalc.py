import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------
# MySQL Connection
# --------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",         # change if needed
    database="electricity_bills"
)
cursor = db.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS appliances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    appliance_name VARCHAR(255),
    watts_consumed INT,
    hours_used INT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appliance_name VARCHAR(255),
    unit_consumption FLOAT,
    total_bill FLOAT,
    date TIMESTAMP
)
""")

# --------------------
# Global Variables
# --------------------
appliances_data = []
total_bill = 0.0

# --------------------
# Functions
# --------------------
def register_user():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get().strip()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Error", "Username already exists")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        messagebox.showinfo("Success", "Registration Successful!")

def login():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    if cursor.fetchone():
        messagebox.showinfo("Success", f"Welcome {username}!")
        notebook.select(appliance_management_frame)
    else:
        messagebox.showerror("Login Error", "Invalid credentials")

def refresh_appliance_table():
    for row in appliance_tree.get_children():
        appliance_tree.delete(row)
    for appliance in appliances_data:
        appliance_tree.insert("", "end", values=(
            appliance["appliance_name"], appliance["watts_consumed"], appliance["hours_used"]
        ))

def open_add_appliance_window(edit_index=None):
    add_win = tk.Toplevel(root)
    add_win.title("Add Appliance" if edit_index is None else "Edit Appliance")
    add_win.geometry("340x200")
    add_win.resizable(False, False)

    ttk.Label(add_win, text="Appliance Name:").grid(row=0, column=0, padx=12, pady=8, sticky="e")
    name_entry = ttk.Entry(add_win, width=28)
    name_entry.grid(row=0, column=1, pady=8)

    ttk.Label(add_win, text="Watts Consumed:").grid(row=1, column=0, padx=12, pady=8, sticky="e")
    watts_entry = ttk.Entry(add_win, width=28)
    watts_entry.grid(row=1, column=1, pady=8)

    ttk.Label(add_win, text="Hours Used (per day):").grid(row=2, column=0, padx=12, pady=8, sticky="e")
    hours_entry = ttk.Entry(add_win, width=28)
    hours_entry.grid(row=2, column=1, pady=8)

    # If editing, pre-fill the fields
    if edit_index is not None:
        appliance = appliances_data[edit_index]
        name_entry.insert(0, appliance["appliance_name"])
        watts_entry.insert(0, appliance["watts_consumed"])
        hours_entry.insert(0, appliance["hours_used"])

    def save_appliance():
        try:
            name = name_entry.get().strip()
            watts = int(watts_entry.get())
            hours = int(hours_entry.get())
            if not name:
                messagebox.showerror("Error", "Appliance name cannot be empty")
                return
            data = {
                "appliance_name": name,
                "watts_consumed": watts,
                "hours_used": hours
            }
            if edit_index is None:
                appliances_data.append(data)
            else:
                appliances_data[edit_index] = data
            refresh_appliance_table()
            add_win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values for Watts and Hours")

    ttk.Button(add_win, text="Save", command=save_appliance, width=18).grid(row=3, column=0, columnspan=2, pady=12)

def remove_selected_appliance():
    selected = appliance_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select an appliance to remove")
        return
    index = appliance_tree.index(selected[0])
    del appliances_data[index]
    refresh_appliance_table()

def edit_selected_appliance():
    selected = appliance_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select an appliance to edit")
        return
    index = appliance_tree.index(selected[0])
    open_add_appliance_window(edit_index=index)

def calculate_total_bill():
    global total_bill
    if not appliances_data:
        messagebox.showwarning("No Appliances", "Add at least one appliance before calculating the bill.")
        return

    try:
        bill_limit = float(bill_limit_entry.get()) if bill_limit_entry.get().strip() else None
    except ValueError:
        messagebox.showerror("Error", "Bill limit must be a number")
        return

    total_bill = 0.0
    total_units = 0.0

    for appliance in appliances_data:
        watts = appliance["watts_consumed"]
        hours = appliance["hours_used"]
        units = (watts * hours * 30) / 1000.0
        appliance["unit_consumption"] = units
        total_units += units

    billed_amount = 0.0
    if total_units > 100:
        remain = total_units - 100
        if remain <= 300:
            billed_amount += remain * 4.5
            remain = 0
        else:
            billed_amount += 300 * 4.5
            remain -= 300

        if remain > 0:
            take = min(remain, 100)
            billed_amount += take * 6
            remain -= take

        if remain > 0:
            take = min(remain, 100)
            billed_amount += take * 8
            remain -= take

        if remain > 0:
            take = min(remain, 200)
            billed_amount += take * 9
            remain -= take

        if remain > 0:
            take = min(remain, 200)
            billed_amount += take * 10
            remain -= take

        if remain > 0:
            billed_amount += remain * 11

    total_bill = round(billed_amount, 2)

    if bill_limit is not None and total_bill > bill_limit:
        messagebox.showwarning("Bill Limit Exceeded", f"Total bill ₹{total_bill:.2f} exceeds set limit ₹{bill_limit}")
    else:
        messagebox.showinfo("Bill Calculation", f"Total Units: {total_units:.2f} kWh\nTotal Bill: ₹{total_bill:.2f}")

def store_bill_history():
    if not appliances_data:
        messagebox.showwarning("No Data", "No appliance data to store.")
        return
    if any("unit_consumption" not in a for a in appliances_data):
        messagebox.showwarning("Not Calculated", "Please calculate the bill first.")
        return

    for appliance in appliances_data:
        date = datetime.now()
        cursor.execute(
            "INSERT INTO bill_history (appliance_name, unit_consumption, total_bill, date) VALUES (%s, %s, %s, %s)",
            (appliance['appliance_name'], appliance['unit_consumption'], total_bill, date)
        )
    db.commit()
    messagebox.showinfo("Saved", "Bill history stored successfully")

def display_bill_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("Bill History")
    hist_win.geometry("700x420")

    tree = ttk.Treeview(hist_win, columns=("Name", "Units", "Bill", "Date"), show="headings", height=16)
    tree.heading("Name", text="Appliance Name")
    tree.heading("Units", text="Units (kWh)")
    tree.heading("Bill", text="Total Bill (INR)")
    tree.heading("Date", text="Date")

    tree.column("Name", width=220, anchor="w")
    tree.column("Units", width=120, anchor="center")
    tree.column("Bill", width=140, anchor="center")
    tree.column("Date", width=200, anchor="center")

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cursor.execute("SELECT appliance_name, unit_consumption, total_bill, date FROM bill_history ORDER BY date DESC")
    for row in cursor.fetchall():
        dt = row[3].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row[3], datetime) else str(row[3])
        tree.insert("", "end", values=(row[0], f"{row[1]:.2f}", f"₹{row[2]:.2f}", dt))

def display_pie_chart():
    if not appliances_data or any("unit_consumption" not in a for a in appliances_data):
        messagebox.showwarning("No Data", "Please calculate the bill first.")
        return

    names = [a["appliance_name"] for a in appliances_data]
    units = [a["unit_consumption"] for a in appliances_data]

    fig, ax = plt.subplots()
    ax.pie(units, labels=names, autopct='%1.1f%%', startangle=90)
    ax.set_title("Appliance Consumption (Current Session)")

    chart_win = tk.Toplevel(root)
    chart_win.title("Consumption Pie Chart")
    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.get_tk_widget().pack(expand=True, fill="both")
    canvas.draw()

# --------------------
# GUI Setup
# --------------------
root = tk.Tk()
root.title("⚡ Electricity Bill Management System")
root.geometry("960x700")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 11), background="#f4f4f4")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background="#f4f4f4", foreground="#2a2a2a")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=12, pady=12)

# Register Frame
reg_frame = ttk.Frame(notebook)
notebook.add(reg_frame, text="📝 Register")
ttk.Label(reg_frame, text="User Registration", style="Header.TLabel").pack(pady=14)

form_frame_reg = tk.Frame(reg_frame, bg="#f4f4f4")
form_frame_reg.pack(pady=6)
ttk.Label(form_frame_reg, text="Username:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
reg_username_entry = ttk.Entry(form_frame_reg, width=34)
reg_username_entry.grid(row=0, column=1, pady=6)
ttk.Label(form_frame_reg, text="Password:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
reg_password_entry = ttk.Entry(form_frame_reg, show="*", width=34)
reg_password_entry.grid(row=1, column=1, pady=6)
ttk.Button(reg_frame, text="Register", command=register_user, width=24).pack(pady=12)

# Login Frame
login_frame = ttk.Frame(notebook)
notebook.add(login_frame, text="🔑 Login")
ttk.Label(login_frame, text="User Login", style="Header.TLabel").pack(pady=14)

form_frame_login = tk.Frame(login_frame, bg="#f4f4f4")
form_frame_login.pack(pady=6)
ttk.Label(form_frame_login, text="Username:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
login_username_entry = ttk.Entry(form_frame_login, width=34)
login_username_entry.grid(row=0, column=1, pady=6)
ttk.Label(form_frame_login, text="Password:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
login_password_entry = ttk.Entry(form_frame_login, show="*", width=34)
login_password_entry.grid(row=1, column=1, pady=6)
ttk.Button(login_frame, text="Login", command=login, width=24).pack(pady=12)

# Appliance Management Frame
appliance_management_frame = ttk.Frame(notebook)
notebook.add(appliance_management_frame, text="💡 Appliance Management")
ttk.Label(appliance_management_frame, text="Bill Limit (INR):", style="TLabel").pack(pady=(8,0))
bill_limit_entry = ttk.Entry(appliance_management_frame, width=20)
bill_limit_entry.pack(pady=(0,10))

btn_frame_top = tk.Frame(appliance_management_frame, bg="#f4f4f4")
btn_frame_top.pack(pady=8)
buttons = [
    ("Add Appliance", open_add_appliance_window),
    ("Edit Appliance", edit_selected_appliance),
    ("Remove Appliance", remove_selected_appliance),
    ("Calculate Bill", calculate_total_bill),
    ("Store Bill History", store_bill_history),
    ("Display Bill History", display_bill_history),
    ("Display Pie Chart", display_pie_chart),
]

for i, (txt, cmd) in enumerate(buttons):
    row_num = i // 4   # first 4 buttons on row 0, rest on row 1
    col_num = i % 4
    ttk.Button(btn_frame_top, text=txt, command=cmd, width=18).grid(row=row_num, column=col_num, padx=6, pady=4)



appliance_tree = ttk.Treeview(appliance_management_frame, columns=("Name", "Watts", "Hours"), show="headings", height=12)
appliance_tree.heading("Name", text="Appliance Name")
appliance_tree.heading("Watts", text="Watts")
appliance_tree.heading("Hours", text="Hours Used")
appliance_tree.column("Name", width=300, anchor="w")
appliance_tree.column("Watts", width=100, anchor="center")
appliance_tree.column("Hours", width=120, anchor="center")
appliance_tree.pack(padx=12, pady=8, fill="x")

root.mainloop()
