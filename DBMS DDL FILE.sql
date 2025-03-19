CREATE DATABASE Patient_Management_System;

USE Patient_Management_System;

-- Patients Table
CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    address VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

-- Doctors Table
CREATE TABLE Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialty VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

-- Medical History Table
CREATE TABLE Medical_History (
    medical_history_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    medical_condition VARCHAR(255),
    diagnosis_date DATE,
    treatment VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);

-- Prescriptions Table
CREATE TABLE Prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    prescription_date DATE,
    medication VARCHAR(255),
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);

-- Insurance Companies Table
CREATE TABLE Insurance_Companies (
    insurance_company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    policy_number VARCHAR(50)
);

-- Insurance Policies Table
CREATE TABLE Insurance_Policies (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    insurance_company_id INT,
    policy_number VARCHAR(50),
    coverage_start_date DATE,
    coverage_end_date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (insurance_company_id) REFERENCES Insurance_Companies(insurance_company_id) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10, 2),
    payment_date DATE,
    payment_method VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);

-- Lab Tests Table
CREATE TABLE Lab_Tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    test_name VARCHAR(100),
    test_date DATE,
    result VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE
);

-- Appointments Table
CREATE TABLE Appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_date DATE,
    appointment_time TIME,
    doctor_id INT,
    reason_for_visit VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);

-- Notes Table
CREATE TABLE Notes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    note_date DATE,
    note_content TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) ON DELETE CASCADE
);

