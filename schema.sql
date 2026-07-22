-- Database Setup for TrafficGuard AI

CREATE DATABASE IF NOT EXISTS trafficguard;
USE trafficguard;

-- 1. Users / Roles Table (optional if we only have two fixed roles, but good for scaling)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Officers / Users Table
CREATE TABLE IF NOT EXISTS officers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    officer_id VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- 3. Vehicles & Drivers Table
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL UNIQUE,
    owner_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    vehicle_type VARCHAR(50),
    is_repeat_offender BOOLEAN DEFAULT FALSE,
    total_offences INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Fine Rules Configuration
CREATE TABLE IF NOT EXISTS fine_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    violation_type VARCHAR(100) NOT NULL UNIQUE,
    base_fine_amount DECIMAL(10, 2) NOT NULL
);

-- 5. Violations Table
CREATE TABLE IF NOT EXISTS violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT,
    officer_id INT,
    violation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    gps_location VARCHAR(255),
    violation_type VARCHAR(100),
    fine_amount DECIMAL(10, 2) NOT NULL,
    ai_confidence FLOAT,
    evidence_image_path VARCHAR(255),
    payment_status ENUM('PENDING', 'PAID', 'FAILED', 'OVERDUE') DEFAULT 'PENDING',
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY (officer_id) REFERENCES officers(id)
);

-- 6. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    violation_id INT,
    transaction_id VARCHAR(100) UNIQUE,
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50),
    receipt_url VARCHAR(255),
    FOREIGN KEY (violation_id) REFERENCES violations(id)
);

-- Initial Data Seed
INSERT IGNORE INTO roles (role_name) VALUES ('ADMIN'), ('OFFICER');
INSERT IGNORE INTO fine_rules (violation_type, base_fine_amount) VALUES
('Helmet Missing', 500.00),
('Seatbelt Missing', 1000.00),
('Signal Jump', 1500.00),
('Speeding', 2000.00),
('Triple Riding', 1000.00),
('Wrong Lane', 1000.00);
