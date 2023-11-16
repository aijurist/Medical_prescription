import mysql.connector

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Helloworld1@",
    database="doctor_info"
)

cursor = db_connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    specialization VARCHAR(255),
    location VARCHAR(255)
)
"""

cursor.execute(create_table_query)
db_connection.commit()

doctors_data = [
    ("Dr. John Doe", "Cardiologist", "City Hospital"),
    ("Dr. Jane Smith", "Pediatrician", "Community Clinic"),
    ("Dr. David Johnson", "Orthopedic Surgeon", "Medical Center"),
    ("Dr. Sarah Williams", "Dermatologist", "Skin Care Clinic"),
    ("Dr. Michael Brown", "Ophthalmologist", "Eye Clinic"),
    ("Dr. Susan Lee", "Gynecologist", "Women's Health Center"),
]

insert_query = """
INSERT INTO doctors (name, specialization, location)
VALUES (%s, %s, %s)
"""

for data in doctors_data:
    cursor.execute(insert_query, data)

db_connection.commit()

select_query = "SELECT * FROM doctors"
cursor.execute(select_query)

print("Doctor Information:")
for doctor in cursor.fetchall():
    print(doctor)

cursor.close()
db_connection.close()
