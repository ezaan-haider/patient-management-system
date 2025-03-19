import streamlit as st
import mysql.connector
import pandas as pd
import streamlit as st

st.markdown(
    """
    <style>
    /* Sidebar container */
    .css-1d391kg {
        background-color: #add8e6; /* Light blue background */
        color: #ffffff; /* White text color */
    }
    .css-1d391kg a {
        color: #ffffff; /* White link color */
    }
    .css-1d391kg a:hover {
        color: #007bff; /* Blue link hover color */
    }

    /* Main content */
    .css-1outpf7 {
        background-color: #ffffff; /* White background */
        padding: 20px;
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }

    /* Custom styles */
    .stMarkdown {
        text-align: center;
    }

    #sistema-de-clientes {
        font-weight: bold;
    }

    .css-1q8dd3e {
        background: transparent;
        box-sizing: border-box;
        border-radius: 0.6rem;
        align-self: center;
        font-size: 17px;
        font-weight: 400 bold;
        text-align: center;
        color: aliceblue;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        cursor: pointer;
        border: 2px solid aqua;
        width: 60px;
        height: 30px;
        font-size: 15px;
    }

    .css-1q8dd3e:hover {
        color: aqua;
        box-shadow: 3px 3px 20px #03e9f4,
        3px 2px 20px #03e9f4;
        border: 2px solid aqua;
    }

    #sistema-de-clientes {
        background-color: #000;
        border: 1px solid #dbd56e;
        color: #fff;
        border-radius: 12px;
    }

    /* Hide Streamlit's default menu, footer, and header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="*******",
    password="******",
    database="Patient_Management_System"
)
cursor = db_connection.cursor()

# Helper functions
def run_query(query, params=None):
    cursor.execute(query, params)
    return cursor.fetchall()

def run_query_no_return(query, params=None):
    cursor.execute(query, params)
    db_connection.commit()

def get_last_inserted_id():
    cursor.execute("SELECT LAST_INSERT_ID()")
    return cursor.fetchone()[0]

def fetch_query(query, params=None):
    cursor.execute(query, params)
    columns = cursor.column_names
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=columns)
    return df

# Streamlit UI for CRUD operations
st.title("Patient Management System")

# Sidebar for CRUD operations
option = st.sidebar.selectbox("Select Action", ["Insert", "Update", "Delete", "Search", "Fetch"])


def insert_ui(table_name):
    if table_name == "Patients":
        first_name = st.text_input("First Name", key="insert_patient_first_name")
        last_name = st.text_input("Last Name", key="insert_patient_last_name")
        date_of_birth = st.date_input("Date of Birth", key="insert_patient_dob")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="insert_patient_gender")
        address = st.text_area("Address", key="insert_patient_address")
        phone_number = st.text_input("Phone Number", key="insert_patient_phone")
        email = st.text_input("Email", key="insert_patient_email")
        if st.button("Add Patient", key="insert_patient_button"):
            run_query_no_return("INSERT INTO Patients (first_name, last_name, date_of_birth, gender, address, phone_number, email) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                                (first_name, last_name, date_of_birth, gender, address, phone_number, email))
            patient_id = get_last_inserted_id()
            st.success(f"Patient added successfully! Patient ID: {patient_id}")

    elif table_name == "Appointments":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_appointment_patient_id")
        appointment_date = st.date_input("Appointment Date", key="insert_appointment_date")
        appointment_time = st.time_input("Appointment Time", key="insert_appointment_time")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="insert_appointment_doctor_id")
        reason_for_visit = st.text_area("Reason for Visit", key="insert_appointment_reason")
        if st.button("Add Appointment", key="insert_appointment_button"):
            run_query_no_return("INSERT INTO Appointments (patient_id, appointment_date, appointment_time, doctor_id, reason_for_visit) VALUES (%s, %s, %s, %s, %s)", 
                                (patient_id, appointment_date, appointment_time, doctor_id, reason_for_visit))
            appointment_id = get_last_inserted_id()
            st.success(f"Appointment added successfully! Appointment ID: {appointment_id}")

    elif table_name == "Doctors":
        first_name = st.text_input("First Name", key="insert_doctor_first_name")
        last_name = st.text_input("Last Name", key="insert_doctor_last_name")
        specialty = st.text_input("Specialty", key="insert_doctor_specialty")
        phone_number = st.text_input("Phone Number", key="insert_doctor_phone")
        email = st.text_input("Email", key="insert_doctor_email")
        if st.button("Add Doctor", key="insert_doctor_button"):
            run_query_no_return("INSERT INTO Doctors (first_name, last_name, specialty, phone_number, email) VALUES (%s, %s, %s, %s, %s)", 
                                (first_name, last_name, specialty, phone_number, email))
            doctor_id = get_last_inserted_id()
            st.success(f"Doctor added successfully! Doctor ID: {doctor_id}")

    elif table_name == "Medical History":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_medical_history_patient_id")
        medical_condition = st.text_input("Medical Condition", key="insert_medical_history_condition")
        diagnosis_date = st.date_input("Diagnosis Date", key="insert_medical_history_diagnosis_date")
        treatment = st.text_input("Treatment", key="insert_medical_history_treatment")
        if st.button("Add Medical History", key="insert_medical_history_button"):
            run_query_no_return("INSERT INTO Medical_History (patient_id, medical_condition, diagnosis_date, treatment) VALUES (%s, %s, %s, %s)", 
                                (patient_id, medical_condition, diagnosis_date, treatment))
            medical_history_id = get_last_inserted_id()
            st.success(f"Medical history added successfully! History ID: {medical_history_id}")

    elif table_name == "Prescriptions":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_prescription_patient_id")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="insert_prescription_doctor_id")
        prescription_date = st.date_input("Prescription Date", key="insert_prescription_date")
        medication = st.text_input("Medication", key="insert_prescription_medication")
        dosage = st.text_input("Dosage", key="insert_prescription_dosage")
        frequency = st.text_input("Frequency", key="insert_prescription_frequency")
        if st.button("Add Prescription", key="insert_prescription_button"):
            run_query_no_return("INSERT INTO Prescriptions (patient_id, doctor_id, prescription_date, medication, dosage, frequency) VALUES (%s, %s, %s, %s, %s, %s)", 
                                (patient_id, doctor_id, prescription_date, medication, dosage, frequency))
            prescription_id = get_last_inserted_id()
            st.success(f"Prescription added successfully! Prescription ID: {prescription_id}")

    elif table_name == "Insurance Companies":
        company_name = st.text_input("Company Name", key="insert_insurance_company_name")
        policy_number = st.text_input("Policy Number", key="insert_insurance_policy_number")
        if st.button("Add Insurance Company", key="insert_insurance_company_button"):
            run_query_no_return("INSERT INTO Insurance_Companies (company_name, policy_number) VALUES (%s, %s)", 
                                (company_name, policy_number))
            insurance_company_id = get_last_inserted_id()
            st.success(f"Insurance company added successfully! Company ID: {insurance_company_id}")

    elif table_name == "Insurance Policies":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_insurance_policy_patient_id")
        insurance_company_id = st.number_input("Insurance Company ID", min_value=1, step=1, key="insert_insurance_policy_company_id")
        policy_number = st.text_input("Policy Number", key="insert_insurance_policy_number")
        coverage_start_date = st.date_input("Coverage Start Date", key="insert_insurance_policy_start_date")
        coverage_end_date = st.date_input("Coverage End Date", key="insert_insurance_policy_end_date")
        if st.button("Add Insurance Policy", key="insert_insurance_policy_button"):
            run_query_no_return("INSERT INTO Insurance_Policies (patient_id, insurance_company_id, policy_number, coverage_start_date, coverage_end_date) VALUES (%s, %s, %s, %s, %s)", 
                                (patient_id, insurance_company_id, policy_number, coverage_start_date, coverage_end_date))
            policy_id = get_last_inserted_id()
            st.success(f"Insurance policy added successfully! Policy ID: {policy_id}")

    elif table_name == "Payments":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_payment_patient_id")
        amount = st.number_input("Amount", min_value=0.0, step=0.01, key="insert_payment_amount")
        payment_date = st.date_input("Payment Date", key="insert_payment_date")
        payment_method = st.text_input("Payment Method", key="insert_payment_method")
        if st.button("Add Payment", key="insert_payment_button"):
            run_query_no_return("INSERT INTO Payments (patient_id, amount, payment_date, payment_method) VALUES (%s, %s, %s, %s)", 
                                (patient_id, amount, payment_date, payment_method))
            payment_id = get_last_inserted_id()
            st.success(f"Payment added successfully! Payment ID: {payment_id}")

    elif table_name == "Lab Tests":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_lab_test_patient_id")
        test_name = st.text_input("Test Name", key="insert_lab_test_name")
        test_date = st.date_input("Test Date", key="insert_lab_test_date")
        result = st.text_input("Result", key="insert_lab_test_result")
        if st.button("Add Lab Test", key="insert_lab_test_button"):
            run_query_no_return("INSERT INTO Lab_Tests (patient_id, test_name, test_date, result) VALUES (%s, %s, %s, %s)", 
                                (patient_id, test_name, test_date, result))
            test_id = get_last_inserted_id()
            st.success(f"Lab test added successfully! Test ID: {test_id}")
    elif table_name == "Notes":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="insert_note_patient_id")
        note_date = st.date_input("Note Date", key="insert_note_date")
        note_content = st.text_area("Note Content", key="insert_note_content")
        if st.button("Add Note", key="insert_note_button"):
            run_query_no_return("INSERT INTO Notes (patient_id, note_date, note_content) VALUES (%s, %s, %s)", 
                            (patient_id, note_date, note_content))
            note_id = get_last_inserted_id()
            st.success(f"Note added successfully! Note ID: {note_id}")



def update_ui(table_name):
    if table_name == "Patients":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_patient_id")
        first_name = st.text_input("First Name", key="update_patient_first_name")
        last_name = st.text_input("Last Name", key="update_patient_last_name")
        date_of_birth = st.date_input("Date of Birth", key="update_patient_dob")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="update_patient_gender")
        address = st.text_area("Address", key="update_patient_address")
        phone_number = st.text_input("Phone Number", key="update_patient_phone")
        email = st.text_input("Email", key="update_patient_email")
        if st.button("Update Patient", key="update_patient_button"):
            run_query_no_return("UPDATE Patients SET first_name=%s, last_name=%s, date_of_birth=%s, gender=%s, address=%s, phone_number=%s, email=%s WHERE patient_id=%s", 
                                (first_name, last_name, date_of_birth, gender, address, phone_number, email, patient_id))
            st.success("Patient updated successfully!")

    elif table_name == "Appointments":
        appointment_id = st.number_input("Appointment ID", min_value=1, step=1, key="update_appointment_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_appointment_patient_id")
        appointment_date = st.date_input("Appointment Date", key="update_appointment_date")
        appointment_time = st.time_input("Appointment Time", key="update_appointment_time")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="update_appointment_doctor_id")
        reason_for_visit = st.text_area("Reason for Visit", key="update_appointment_reason")
        if st.button("Update Appointment", key="update_appointment_button"):
            run_query_no_return("UPDATE Appointments SET patient_id=%s, appointment_date=%s, appointment_time=%s, doctor_id=%s, reason_for_visit=%s WHERE appointment_id=%s", 
                                (patient_id, appointment_date, appointment_time, doctor_id, reason_for_visit, appointment_id))
            st.success("Appointment updated successfully!")

    elif table_name == "Doctors":
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="update_doctor_id")
        first_name = st.text_input("First Name", key="update_doctor_first_name")
        last_name = st.text_input("Last Name", key="update_doctor_last_name")
        specialty = st.text_input("Specialty", key="update_doctor_specialty")
        phone_number = st.text_input("Phone Number", key="update_doctor_phone")
        email = st.text_input("Email", key="update_doctor_email")
        if st.button("Update Doctor", key="update_doctor_button"):
            run_query_no_return("UPDATE Doctors SET first_name=%s, last_name=%s, specialty=%s, phone_number=%s, email=%s WHERE doctor_id=%s", 
                                (first_name, last_name, specialty, phone_number, email, doctor_id))
            st.success("Doctor updated successfully!")

    elif table_name == "Medical History":
        medical_history_id = st.number_input("History ID", min_value=1, step=1, key="update_medical_history_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_medical_history_patient_id")
        medical_condition = st.text_input("Medical Condition", key="update_medical_history_condition")
        diagnosis_date = st.date_input("Diagnosis Date", key="update_medical_history_diagnosis_date")
        treatment = st.text_input("Treatment", key="update_medical_history_treatment")
        if st.button("Update Medical History", key="update_medical_history_button"):
            run_query_no_return("UPDATE Medical_History SET patient_id=%s, medical_condition=%s, diagnosis_date=%s, treatment=%s WHERE medical_history_id=%s", 
                                (patient_id, medical_condition, diagnosis_date, treatment, medical_history_id))
            st.success("Medical history updated successfully!")

    elif table_name == "Prescriptions":
        prescription_id = st.number_input("Prescription ID", min_value=1, step=1, key="update_prescription_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_prescription_patient_id")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="update_prescription_doctor_id")
        prescription_date = st.date_input("Prescription Date", key="update_prescription_date")
        medication = st.text_input("Medication", key="update_prescription_medication")
        dosage = st.text_input("Dosage", key="update_prescription_dosage")
        frequency = st.text_input("Frequency", key="update_prescription_frequency")
        if st.button("Update Prescription", key="update_prescription_button"):
            run_query_no_return("UPDATE Prescriptions SET patient_id=%s, doctor_id=%s, prescription_date=%s, medication=%s, dosage=%s, frequency=%s WHERE prescription_id=%s", 
                                (patient_id, doctor_id, prescription_date, medication, dosage, frequency, prescription_id))
            st.success("Prescription updated successfully!")

    elif table_name == "Insurance Companies":
        insurance_company_id = st.number_input("Insurance Company ID", min_value=1, step=1, key="update_insurance_company_id")
        company_name = st.text_input("Company Name", key="update_insurance_company_name")
        policy_number = st.text_input("Policy Number", key="update_insurance_company_policy_number")
        if st.button("Update Insurance Company", key="update_insurance_company_button"):
            run_query_no_return("UPDATE Insurance_Companies SET company_name=%s, policy_number=%s WHERE insurance_company_id=%s", 
                                (company_name, policy_number, insurance_company_id))
            st.success("Insurance company updated successfully!")

    elif table_name == "Insurance Policies":
        policy_id = st.number_input("Policy ID", min_value=1, step=1, key="update_insurance_policy_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_insurance_policy_patient_id")
        insurance_company_id = st.number_input("Insurance Company ID", min_value=1, step=1, key="update_insurance_policy_company_id")
        policy_number = st.text_input("Policy Number", key="update_insurance_policy_number")
        coverage_start_date = st.date_input("Coverage Start Date", key="update_insurance_policy_start_date")
        coverage_end_date = st.date_input("Coverage End Date", key="update_insurance_policy_end_date")
        if st.button("Update Insurance Policy", key="update_insurance_policy_button"):
            run_query_no_return("UPDATE Insurance_Policies SET patient_id=%s, insurance_company_id=%s, policy_number=%s, coverage_start_date=%s, coverage_end_date=%s WHERE policy_id=%s", 
                                (patient_id, insurance_company_id, policy_number, coverage_start_date, coverage_end_date, policy_id))
            st.success("Insurance policy updated successfully!")

    elif table_name == "Payments":
        payment_id = st.number_input("Payment ID", min_value=1, step=1, key="update_payment_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_payment_patient_id")
        amount = st.number_input("Amount", min_value=0.0, step=0.01, key="update_payment_amount")
        payment_date = st.date_input("Payment Date", key="update_payment_date")
        payment_method = st.text_input("Payment Method", key="update_payment_method")
        if st.button("Update Payment", key="update_payment_button"):
            run_query_no_return("UPDATE Payments SET patient_id=%s, amount=%s, payment_date=%s, payment_method=%s WHERE payment_id=%s", 
                                (patient_id, amount, payment_date, payment_method, payment_id))
            st.success("Payment updated successfully!")

    elif table_name == "Lab Tests":
        test_id = st.number_input("Test ID", min_value=1, step=1, key="update_lab_test_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_lab_test_patient_id")
        test_name = st.text_input("Test Name", key="update_lab_test_name")
        test_date = st.date_input("Test Date", key="update_lab_test_date")
        result = st.text_input("Result", key="update_lab_test_result")
        if st.button("Update Lab Test", key="update_lab_test_button"):
            run_query_no_return("UPDATE Lab_Tests SET patient_id=%s, test_name=%s, test_date=%s, result=%s WHERE test_id=%s", 
                                (patient_id, test_name, test_date, result, test_id))
            st.success("Lab test updated successfully!")

    elif table_name == "Notes":
        note_id = st.number_input("Note ID", min_value=1, step=1, key="update_note_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_note_patient_id")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="update_note_doctor_id")
        note_date = st.date_input("Note Date", key="update_note_date")
        note_content = st.text_area("Note Content", key="update_note_content")
        if st.button("Update Note", key="update_note_button"):
            run_query_no_return("UPDATE Notes SET patient_id=%s, doctor_id=%s, note_date=%s, note_content=%s WHERE note_id=%s", 
                                (patient_id, doctor_id, note_date, note_content, note_id))
            st.success("Note updated successfully!")
    elif table_name == "Notes":
        note_id = st.number_input("Note ID", min_value=1, step=1, key="update_note_id")
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="update_note_patient_id")
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="update_note_doctor_id")
        note_date = st.date_input("Note Date", key="update_note_date")
        note_content = st.text_area("Note Content", key="update_note_content")
        if st.button("Update Note", key="update_note_button"):
           run_query_no_return("UPDATE Notes SET patient_id=%s, doctor_id=%s, note_date=%s, note_content=%s WHERE note_id=%s", 
                            (patient_id, doctor_id, note_date, note_content, note_id))
           st.success("Note updated successfully!")
# Delete entries from tables
def delete_entry(table_name):
    if table_name == "Patients":
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="delete_patient_id")
        if st.button("Delete Patient", key="delete_patient_button"):
            run_query_no_return("DELETE FROM Patients WHERE patient_id=%s", (patient_id,))
            st.success("Patient deleted successfully!")

    elif table_name == "Appointments":
        appointment_id = st.number_input("Appointment ID", min_value=1, step=1, key="delete_appointment_id")
        if st.button("Delete Appointment", key="delete_appointment_button"):
            run_query_no_return("DELETE FROM Appointments WHERE appointment_id=%s", (appointment_id,))
            st.success("Appointment deleted successfully!")

    elif table_name == "Doctors":
        doctor_id = st.number_input("Doctor ID", min_value=1, step=1, key="delete_doctor_id")
        if st.button("Delete Doctor", key="delete_doctor_button"):
            run_query_no_return("DELETE FROM Doctors WHERE doctor_id=%s", (doctor_id,))
            st.success("Doctor deleted successfully!")

    elif table_name == "Medical History":
        history_id = st.number_input("History ID", min_value=1, step=1, key="delete_medical_history_id")
        if st.button("Delete Medical History", key="delete_medical_history_button"):
            run_query_no_return("DELETE FROM Medical_History WHERE history_id=%s", (history_id,))
            st.success("Medical history deleted successfully!")

    elif table_name == "Prescriptions":
        prescription_id = st.number_input("Prescription ID", min_value=1, step=1, key="delete_prescription_id")
        if st.button("Delete Prescription", key="delete_prescription_button"):
            run_query_no_return("DELETE FROM Prescriptions WHERE prescription_id=%s", (prescription_id,))
            st.success("Prescription deleted successfully!")

    elif table_name == "Insurance Companies":
        insurance_company_id = st.number_input("Insurance Company ID", min_value=1, step=1, key="delete_insurance_company_id")
        if st.button("Delete Insurance Company", key="delete_insurance_company_button"):
            run_query_no_return("DELETE FROM Insurance_Companies WHERE insurance_company_id=%s", (insurance_company_id,))
            st.success("Insurance company deleted successfully!")

    elif table_name == "Insurance Policies":
        policy_id = st.number_input("Policy ID", min_value=1, step=1, key="delete_insurance_policy_id")
        if st.button("Delete Insurance Policy", key="delete_insurance_policy_button"):
            run_query_no_return("DELETE FROM Insurance_Policies WHERE policy_id=%s", (policy_id,))
            st.success("Insurance policy deleted successfully!")

    elif table_name == "Payments":
        payment_id = st.number_input("Payment ID", min_value=1, step=1, key="delete_payment_id")
        if st.button("Delete Payment", key="delete_payment_button"):
            run_query_no_return("DELETE FROM Payments WHERE payment_id=%s", (payment_id,))
            st.success("Payment deleted successfully!")

    elif table_name == "Lab Tests":
        test_id = st.number_input("Test ID", min_value=1, step=1, key="delete_lab_test_id")
        if st.button("Delete Lab Test", key="delete_lab_test_button"):
            run_query_no_return("DELETE FROM Lab_Tests WHERE test_id=%s", (test_id,))
            st.success("Lab test deleted successfully!")

    elif table_name == "Notes":
        note_id = st.number_input("Note ID", min_value=1, step=1, key="delete_note_id")
        if st.button("Delete Note", key="delete_note_button"):
            run_query_no_return("DELETE FROM Notes WHERE note_id=%s", (note_id,))
            st.success("Note deleted successfully!")

def search_ui():
    search_option = st.selectbox("Search by", ["Patient ID", "Patient Name", "Doctor Name", "Appointment Date"])

    base_query = """
        SELECT Patients.patient_id, Patients.first_name AS patient_first_name, Patients.last_name AS patient_last_name, 
               Appointments.appointment_date, Doctors.first_name AS doctor_first_name, Doctors.last_name AS doctor_last_name, 
               Prescriptions.medication, Medical_History.medical_condition, Notes.note_date, Notes.note_content, 
               Lab_Tests.test_name
        FROM Patients
        LEFT JOIN Appointments ON Patients.patient_id = Appointments.patient_id
        LEFT JOIN Doctors ON Appointments.doctor_id = Doctors.doctor_id
        LEFT JOIN Prescriptions ON Patients.patient_id = Prescriptions.patient_id
        LEFT JOIN Medical_History ON Patients.patient_id = Medical_History.patient_id
        LEFT JOIN Notes ON Patients.patient_id = Notes.patient_id
        LEFT JOIN Lab_Tests ON Patients.patient_id = Lab_Tests.patient_id
    """

    if search_option == "Patient ID":
        patient_id = st.number_input("Enter Patient ID", min_value=1, step=1)
        if st.button("Search"):
            query = base_query + " WHERE Patients.patient_id = %s"
            results = run_query(query, (patient_id,))
            columns = ["Patient ID", "Patient First Name", "Patient Last Name", "Appointment Date", 
                       "Doctor First Name", "Doctor Last Name", "Medication", "Medical Condition", 
                       "Note Date", "Note Content", "Test Name"]
            results_df = pd.DataFrame(results, columns=columns)
            st.dataframe(results_df)

    elif search_option == "Patient Name":
        first_name = st.text_input("Enter Patient First Name")
        last_name = st.text_input("Enter Patient Last Name")
        if st.button("Search"):
            query = base_query + " WHERE Patients.first_name = %s AND Patients.last_name = %s"
            results = run_query(query, (first_name, last_name))
            columns = ["Patient ID", "Patient First Name", "Patient Last Name", "Appointment Date", 
                       "Doctor First Name", "Doctor Last Name", "Medication", "Medical Condition", 
                       "Note Date", "Note Content", "Test Name"]
            results_df = pd.DataFrame(results, columns=columns)
            st.dataframe(results_df)

    elif search_option == "Doctor Name":
        doctor_first_name = st.text_input("Enter Doctor First Name")
        doctor_last_name = st.text_input("Enter Doctor Last Name")
        if st.button("Search"):
            query = base_query + " WHERE Doctors.first_name = %s AND Doctors.last_name = %s"
            results = run_query(query, (doctor_first_name, doctor_last_name))
            columns = ["Patient ID", "Patient First Name", "Patient Last Name", "Appointment Date", 
                       "Doctor First Name", "Doctor Last Name", "Medication", "Medical Condition", 
                       "Note Date", "Note Content", "Test Name"]
            results_df = pd.DataFrame(results, columns=columns)
            st.dataframe(results_df)

    elif search_option == "Appointment Date":
        appointment_date = st.date_input("Enter Appointment Date")
        if st.button("Search"):
            query = base_query + " WHERE Appointments.appointment_date = %s"
            results = run_query(query, (appointment_date,))
            columns = ["Patient ID", "Patient First Name", "Patient Last Name", "Appointment Date", 
                       "Doctor First Name", "Doctor Last Name", "Medication", "Medical Condition", 
                       "Note Date", "Note Content", "Test Name"]
            results_df = pd.DataFrame(results, columns=columns)
            st.dataframe(results_df)

def fetch_all_records():
    tables = ["Patients", "Appointments", "Doctors", "Medical_History", "Prescriptions", 
              "Insurance_Companies", "Insurance_Policies", "Payments", "Lab_Tests", "Notes"]
    all_data = {}
    
    for table in tables:
        query = f"SELECT * FROM {table}"
        df = fetch_query(query)
        all_data[table] = df
    
    return all_data

# UI to fetch and display all records
def fetch_ui():
    if st.button("Fetch All Records"):
        all_data = fetch_all_records()
        for table, df in all_data.items():
            st.subheader(table)
            st.write(df)



if option == "Insert":
    st.header("Insert Data")
    insert_option = st.selectbox("Select Table", ["Patients", "Appointments", "Doctors", "Medical History", "Prescriptions", "Insurance Companies", "Insurance Policies", "Payments", "Lab Tests", "Notes"])
    insert_ui(insert_option)

elif option == "Update":
    st.header("Update Data")
    update_option = st.selectbox("Select Table", ["Patients", "Appointments", "Doctors", "Medical History", "Prescriptions", "Insurance Companies", "Insurance Policies", "Payments", "Lab Tests", "Notes"])
    update_ui(update_option)

elif option == "Delete":
    st.header("Delete Data")
    delete_option = st.selectbox("Select Table", ["Patients", "Appointments", "Doctors", "Medical History", "Prescriptions", "Insurance Companies", "Insurance Policies", "Payments", "Lab Tests", "Notes"])
    delete_entry(delete_option)

elif option == "Search":
    st.header("Search Data")
    search_ui()

elif option == "Fetch":
    fetch_ui()


# Close database connection
db_connection.close()

