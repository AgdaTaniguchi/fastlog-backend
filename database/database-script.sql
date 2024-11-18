DROP DATABASE IF EXISTS fastlog;
CREATE DATABASE IF NOT EXISTS fastlog;

USE fastlog;

CREATE TABLE IF NOT EXISTS delivery (
    tracking_number INT PRIMARY KEY AUTO_INCREMENT,
    estimated_date DATETIME
);

CREATE TABLE IF NOT EXISTS delivery_update (
    id INT PRIMARY KEY AUTO_INCREMENT,
    delivery_status ENUM('approved', 'shipped', 'delivered'),
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    tracking_number INT,
    FOREIGN KEY (tracking_number) REFERENCES delivery(tracking_number)
);