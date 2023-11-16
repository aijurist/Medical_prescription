import spacy
import mysql.connector

def get_doctors_data(db_config):
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    select_query = "SELECT name, specialization, location FROM doctors"
    cursor.execute(select_query)
    doctors_data = cursor.fetchall()
    db_connection.close()
    return doctors_data

def extract_doctor_name(user_input):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(user_input)
    doctor_name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            doctor_name = ent.text
            break
    return doctor_name

def book_appointment(doctor_name, appointment_time):
    appointment_confirmation = f"Appointment booked with {doctor_name} at {appointment_time}"
    return appointment_confirmation

def show_available_doctors(doctors_data):
    doctor_list = ["Here is a list of available doctors:"]
    for doctor in doctors_data:
        doctor_info = f"Doctor Name: {doctor[0]}, Specialization: {doctor[1]}, Location: {doctor[2]}"
        doctor_list.append(doctor_info)
    return '\n'.join(doctor_list)
def handle_user_request(user_input, doctors_data):
    if any(word in user_input.lower() for word in ['book an appointment', 'schedule an appointment', 'appointment booking']):
        while True:
            doctor_name = extract_doctor_name(user_input)

            if doctor_name:
                matching_doctor = None
                for doctor in doctors_data:
                    if doctor_name.lower() in doctor[0].lower():
                        matching_doctor = doctor
                        break

                if matching_doctor:
                    print(f"Doctor Name: {matching_doctor[0]}")
                    print(f"Specialization: {matching_doctor[1]}")
                    print(f"Location: {matching_doctor[2]}")
                    appointment_time = input("Please enter the appointment time: ")
                    book_appointment(matching_doctor[0], appointment_time)
                    break  # Exit the loop after a successful booking
                else:
                    print(f"The doctor '{doctor_name}' is not present in the database. Please try again or type 'quit' to exit.")
            else:
                show_available_doctors(doctors_data)
                selected_doctor = input("Please enter the doctor's name to book an appointment: ")
                if selected_doctor.lower() == 'quit':
                    print("Exiting appointment booking.")
                    break  # Exit the loop if the user decides to quit
                else:
                    matching_doctor = None
                    for doctor in doctors_data:
                        if selected_doctor.lower() in doctor[0].lower():
                            matching_doctor = doctor
                            break

                    if matching_doctor:
                        print(f"Doctor Name: {matching_doctor[0]}")
                        print(f"Specialization: {matching_doctor[1]}")
                        print(f"Location: {matching_doctor[2]}")
                        appointment_time = input("Please enter the appointment time: ")
                        book_appointment(matching_doctor[0], appointment_time)
                        break
                    else:
                        print(f"The doctor is not present in the database. Please try again.")
    else:
        print("Other user requests or available commands can be handled here.")


db_config = {
            "host": "localhost",
            "user": "root",
            "password": "Helloworld1@",
            "database": "doctor_info"
        }
doctors_data = get_doctors_data(db_config)
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Helloworld1@",
        "database": "doctor_info"
    }
    doctors_data = get_doctors_data(db_config)

    while True:
        user_input = input("Please enter your request: ")
        handle_user_request(user_input, doctors_data)
