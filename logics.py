import mysql.connector
import spacy
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from main import chatbot
from web_scraper import get_headache_info
from location_finder import find_hospitals_near_me
from patient_info import insert_patient, update_diagnosis, get_patient_details_secure, get_all_patients
from appointment import doctors_data, extract_doctor_name, get_doctors_data, show_available_doctors, book_appointment


class ChatbotCore:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.doctors_data = doctors_data
        self.patient_id = None
        self.first_name = None
        self.last_name = None

    def retrieve_patient_details_secure(self, patient_id, first_name, last_name):
        patient_details = get_patient_details_secure(patient_id, first_name, last_name)
        if patient_details:
            patient_info = "MediBot: Here are your patient details:\n"
            for key, value in patient_details.items():
                patient_info += f"{key}: {value}\n"
            return patient_info
        else:
            return "CareBot: Sorry, we couldn't find your patient details."

    def handle_user_request(self, user_input):
        if user_input.lower() == 'find hospitals near me':
            hospitals_near_me = find_hospitals_near_me(radius=3000)
            return hospitals_near_me

        elif user_input.lower() in ['yes', 'ok', 'great']:
            headache_type = "migraine"
            return get_headache_info(headache_type)

        elif user_input.lower() == 'retrieve health records':
            attr = ['patient id', 'first name', 'last name']
            for step in range(3):
                setattr(self, attr[step].replace(' ', '_'), user_input)
                if step == 2:
                    patient_details = self.retrieve_patient_details_secure(self.patient_id, self.first_name,
                                                                           self.last_name)
                    return patient_details

        elif any(word in user_input.lower() for word in
                 ['book an appointment', 'schedule an appointment', 'appointment booking']):
            doctor_name = extract_doctor_name(user_input)

            if doctor_name:
                matching_doctor = None
                for doctor in self.doctors_data:
                    if doctor_name.lower() in doctor[0].lower():
                        matching_doctor = doctor
                        break

                if matching_doctor:
                    response = f"Doctor Name: {matching_doctor[0]}\n"
                    response += f"Specialization: {matching_doctor[1]}\n"
                    response += f"Location: {matching_doctor[2]}\n"
                    response += "Please enter the appointment time: "
                    appointment_time = input()
                    response += f"Appointment booked with {matching_doctor[0]} at {appointment_time}"
                    return response

                else:
                    return show_available_doctors(self.doctors_data)

        else:
            return chatbot.respond(user_input)


chatbot_core = ChatbotCore()

app = Flask(__name__)
CORS(app)
@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    user_input = data['message']

    response = chatbot_core.handle_user_request(user_input)

    return jsonify({'response': response})


def main():
    app.run(debug=True)


if __name__ == '__main__':
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Helloworld1@",
        "database": "doctor_info"
    }
    doctors_data = get_doctors_data(db_config)
    main()