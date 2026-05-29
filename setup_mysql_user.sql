-- Run this in MySQL Workbench (Sales Data connection -> SQL tab -> Execute)
-- Creates a local app user for the Python dashboard

CREATE DATABASE IF NOT EXISTS sales;

CREATE USER IF NOT EXISTS 'sales_app'@'localhost' IDENTIFIED BY 'sales123';
GRANT ALL PRIVILEGES ON sales.* TO 'sales_app'@'localhost';

CREATE USER IF NOT EXISTS 'sales_app'@'127.0.0.1' IDENTIFIED BY 'sales123';
GRANT ALL PRIVILEGES ON sales.* TO 'sales_app'@'127.0.0.1';

FLUSH PRIVILEGES;

SELECT 'Done! Use sales_app / sales123 in your .env file' AS status;
