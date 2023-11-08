import sqlite3

conn = sqlite3.connect('patient_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        gender TEXT,
        diagnosis TEXT
    )
''')


def insert_patient(first_name, last_name, age, gender, diagnosis):
    cursor.execute('''
        INSERT INTO patients (first_name, last_name, age, gender, diagnosis)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, age, gender, diagnosis))
    conn.commit()
    return cursor.lastrowid


def update_diagnosis(patient_id, new_diagnosis):
    cursor.execute('''
        UPDATE patients
        SET diagnosis = ?
        WHERE id = ?
    ''', (new_diagnosis, patient_id))
    conn.commit()



def get_all_patients():
    cursor.execute('SELECT * FROM patients')
    return cursor.fetchall()


def get_patient_details_secure(patient_id, first_name, last_name):
    cursor.execute('SELECT * FROM patients WHERE id = ? AND first_name = ? AND last_name = ?', (patient_id, first_name, last_name))
    return cursor.fetchone()



patient_records = [
    ("Sunil", "Kumar", 21, "Male", "Fever"),
    ("Santosh", "Kumar", 23, "Male", "Flu"),
    ("Ram", "Kumar", 35, "Male", "Sore Throat"),
    ("Vishaal", "H", 18, "Male", "Headache"),
    ("Aakash", "Kumar", 20, "Male", "Cold"),
    ("Rob", "Miller", 50, "Male", "Asthma"),
    ("Tom", "Anderson", 30, "Male", "Allergies"),
    ("Ashwath", "M", 18, "Male", "Back Pain"),
    ("Bhavanish", "Raj", 19, "Male", "Migraine"),
    ("Jack", "Davis", 33, "Male", "Stomachache")
]

for record in patient_records:
    insert_patient(*record)

conn.close()
