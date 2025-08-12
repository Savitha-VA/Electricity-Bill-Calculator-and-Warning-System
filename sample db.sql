-- Create database
CREATE DATABASE IF NOT EXISTS electricity_bills;
USE electricity_bills;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
);

-- Appliances table
CREATE TABLE IF NOT EXISTS appliances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    appliance_name VARCHAR(255),
    watts_consumed INT,
    hours_used INT
);

-- Bill history table
CREATE TABLE IF NOT EXISTS bill_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appliance_name VARCHAR(255),
    unit_consumption FLOAT,
    total_bill FLOAT,
    date TIMESTAMP
);


