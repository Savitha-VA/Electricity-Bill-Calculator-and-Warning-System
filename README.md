
#  Electricity Bill Calculator and Warning System


The **Electricity Bill Calculator with Warning System** is a desktop-based Python application that helps users **calculate, monitor, and manage** their electricity consumption effectively.
It features **user authentication**, **appliance management**, **real-time bill calculation**, **bill history storage**, and **visual data representation** using pie charts.

Built with:

* **Python** (`tkinter` for GUI, `matplotlib` for charts)
* **MySQL** (data storage for users, appliances, and bill history)

---

## Features

* **User Registration & Login**

  * Secure account creation.
  * Login validation before accessing the main system.

* **Appliance Management**

  * Add, edit, and remove appliances with their wattage and daily usage hours.
  * Bill limit input to set consumption thresholds.

* **Bill Calculation**

  * Calculates total units (kWh) and total bill using a tiered tariff system.
  * Alerts users when consumption exceeds the bill limit.

* **Bill History Storage**

  * Saves calculated bill data into a MySQL database.
  * Displays history with appliance name, consumption, bill amount, and date.

* **Visualization**

  * Interactive **pie chart** showing the percentage consumption of each appliance.

---

## Output

1. **Registration Page**
   
    <img width="1198" height="909" alt="Screenshot 2025-08-13 020005" src="https://github.com/user-attachments/assets/2beec114-43e4-40a8-9ab6-9acc92194a64" />

3. **Login Page**
   
    <img width="1201" height="903" alt="Screenshot 2025-08-13 020046" src="https://github.com/user-attachments/assets/d3d76c67-1122-4265-888a-52529d334815" />

5. **Appliance Management**
   
    <img width="1198" height="913" alt="Screenshot 2025-08-13 020136" src="https://github.com/user-attachments/assets/27939131-3fbe-4a51-b0cb-be666f26d010" />

    <img width="1231" height="938" alt="Screenshot 2025-08-13 020153" src="https://github.com/user-attachments/assets/2f96ed7d-6898-4d49-a363-004da46db30d" />

    <img width="1196" height="906" alt="Screenshot 2025-08-13 020541" src="https://github.com/user-attachments/assets/d9724cbb-4579-44c7-a958-cee6bf8bc7d7" />

    <img width="879" height="556" alt="Screenshot 2025-08-13 020626" src="https://github.com/user-attachments/assets/8a0b93a3-2c9a-4466-8d26-34cc8adc375d" />



7. **Visualization Page**
   
    <img width="1231" height="943" alt="Screenshot 2025-08-13 020604" src="https://github.com/user-attachments/assets/210d1bf4-1476-49ac-8636-ac6d0a2409b5" />
    <img width="520" height="410" alt="image" src="https://github.com/user-attachments/assets/203bd34d-0d5e-44f7-a185-54d446ec4e2c" />



---

## Technologies Used

* **Programming Language:** Python 3.12
* **GUI Library:** Tkinter
* **Database:** MySQL
* **Visualization:** Matplotlib


---




##  Database Schema

### 1. `users`

| Column   | Type         | Description              |
| -------- | ------------ | ------------------------ |
| id       | INT (PK)     | User ID  |
| username | VARCHAR(255) | Username                 |
| password | VARCHAR(255) | Password                 |

### 2. `appliances`

| Column          | Type         | Description       |
| --------------- | ------------ | ----------------- |
| id              | INT (PK)     | Appliance ID      |
| user\_id        | INT          | Linked user ID    |
| appliance\_name | VARCHAR(255) | Name of appliance |
| watts\_consumed | INT          | Wattage           |
| hours\_used     | INT          | Daily usage hours |

### 3. `bill_history`

| Column            | Type         | Description                |
| ----------------- | ------------ | -------------------------- |
| id                | INT (PK)     | Bill record ID             |
| appliance\_name   | VARCHAR(255) | Name of appliance          |
| unit\_consumption | FLOAT        | Units consumed (kWh)       |
| total\_bill       | FLOAT        | Total bill in INR          |
| date              | TIMESTAMP    | Date & time of calculation |

---


