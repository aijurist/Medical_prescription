from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollBar, QTextBrowser, QInputDialog
from PyQt5.QtCore import QTimer, QThread, Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import mysql.connector
import spacy
from datetime import datetime

from main import chatbot
from web_scraper import get_headache_info
from location_finder import find_hospitals_near_me
from patient_info import insert_patient, update_diagnosis, get_patient_details_secure, get_all_patients
from appointment import doctors_data, extract_doctor_name, get_doctors_data, show_available_doctors, book_appointment

scrollbar_style = """
    QScrollBar:vertical {
        border: 2px solid #128C7E;
        background: #F5F5F5;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }

    QScrollBar::handle:vertical {
        background: #128C7E;
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::add-line:vertical {
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical {
        height: 0px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
"""


class TypingThread(QThread):
    typing_signal = pyqtSignal(str)

    def run(self):
        messages = [
            "Typing.",
            "Typing..",
            "Typing...",
        ]
        for message in messages:
            self.typing_signal.emit(message)
            self.msleep(500)


class ChatbotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation_area = None
        self.initUI()
        self.delayed_response_timer = QTimer()
        self.delayed_response_timer.timeout.connect(self.process_delayed_response)
        self.delayed_response_message = ""
        self.patient_id = None
        self.first_name = None
        self.last_name = None
        self.typing_thread = TypingThread()
        self.typing_thread.typing_signal.connect(self.display_typing)
        self.scroll_bar_position = 0
        self.nlp = spacy.load("en_core_web_sm")
        self.doctors_data = doctors_data

    def initUI(self):
        self.setWindowTitle('CareBot')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        title_label = QLabel('CareBot')
        title_label.setStyleSheet(
            'background-color: #128C7E; color: white; font-size: 24px; padding: 10px; text-align: center;'
            'font-family: Arial, sans-serif; border-radius: 10px;'
        )
        layout.addWidget(title_label)

        quicksand_font = QFont("Quicksand Light", 14)
        self.conversation_area = QTextBrowser()
        self.conversation_area.setOpenExternalLinks(True)
        self.conversation_area.setOpenLinks(True)
        self.conversation_area.setReadOnly(True)
        self.conversation_area.setFont(quicksand_font)
        self.conversation_area.setFixedHeight(400)

        '''self.conversation_area.setStyleSheet(
            'background-color: #F5F5F5; padding: 20px; border: 1px solid #128C7E; border-radius: 10px; font-family: Arial, sans-serif; font-size: 16px; color: #333333;'
        )'''

        font = QFont()
        font.setPointSize(12)
        self.conversation_area.setFont(font)

        self.conversation_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.conversation_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.conversation_area.setStyleSheet(scrollbar_style)
        layout.addWidget(self.conversation_area)

        input_label = QLabel('Type your message:')
        input_label.setStyleSheet('font-family: Arial, sans-serif; color: #333333;')
        layout.addWidget(input_label)

        self.user_input = QTextEdit()
        self.user_input.setFixedHeight(60)
        self.user_input.setStyleSheet(
            'background-color: #E0E0E0; padding: 10px; border: 1px solid #128C7E; border-radius: 10px; font-family: Arial, sans-serif; font-size: 16px; color: #333333;'
        )
        self.user_input.setPlaceholderText('Start typing here...')
        layout.addWidget(self.user_input)

        send_button = QPushButton('Send')
        send_button.setStyleSheet(
            'background-color: #128C7E; color: white; border: none; border-radius: 20px; padding: 15px; min-width: 60px; font-family: Arial, sans-serif; font-size: 16px;'
        )
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

        intro_message = "Hi there, I'm CareBot, your health care assistant.\n\n"
        intro_message += "You can use the following commands:\n"
        intro_message += "- 'ok' or 'great': To get information about your health.\n"
        intro_message += "- 'find hospitals near me': To find hospitals within 2km distance.\n"
        intro_message += "- 'Retrieve health records': To retrieve your latest health record"
        self.conversation_area.append(intro_message)

    def retrieve_patient_details_secure(self, patient_id, first_name, last_name):
        patient_details = get_patient_details_secure(patient_id, first_name, last_name)
        if patient_details:
            patient_info = "MediBot: Here are your patient details:\n"
            for key, value in patient_details.items():
                patient_info += f"{key}: {value}\n"
            return patient_info
        else:
            return "CareBot: Sorry, we couldn't find your patient details."

    def update_conversation_area(self, message):
        self.conversation_area.append(message)

    def send_message(self):
        user_message = self.user_input.toPlainText()
        attr = ['patient id', 'first name', 'last name']
        user_message_html = f'''
        <div style="
            width: 240px;
            background: #f5f5f5;
            border-radius: 4px;
            position: relative;
            margin: 0 0 25px;
            overflow-wrap: break-word;
            word-wrap: break-word;
            hyphens: auto;
        ">
            <div class="txt" style="padding: 8px 55px 8px 14px;">
                <p class="name" style="font-weight: 600; font-size: 20px; margin: 0 0 4px; color: #3498db;">You</p>
                <p class="message" style="font-size: 20px; margin: 0; color: #2b2b2b;">{user_message}</p>
            </div>
            <div class="bubble-arrow" style="position: absolute; width: 0; bottom: 42px; left: -16px; height: 0;">
                <div class="bubble-arrow" style="position: absolute; border: 0 solid transparent; border-top: 9px solid #f5f5f5; border-radius: 0 20px 0; width: 15px; height: 30px; transform: rotate(145deg);">
                </div>
            </div>
        </div>
        '''

        self.conversation_area.append(user_message_html)

        if user_message.lower() == 'find hospitals near me':
            hospitals_near_me = find_hospitals_near_me(radius=3000)
            self.display_hospitals_response(hospitals_near_me)

        booking_keywords = ['book an appointment', 'schedule an appointment', 'appointment booking']

        if any(word in user_message.lower() for word in booking_keywords):
            self.conversation_area.append(f'User: {user_message}')
            self.handle_user_request(user_message, doctors_data)

        elif user_message.lower() in ['yes', 'ok', 'great']:
            headache_type = "migraine"
            web_response = get_headache_info(headache_type)
            self.display_web_response(web_response)

        elif user_message.lower() == 'retrieve health records':
            for self.step in range(3):
                self.conversation_area.append(f'Please enter your {attr[self.step]}:')
                setattr(self, attr[self.step].replace(' ', '_'), user_message)
                if self.step == 2:
                    patient_details = self.retrieve_patient_details_secure(self.patient_id, self.first_name, self.last_name)
                    self.display_patient_details(patient_details)
                    self.conversation_area.append('Thank you. Your details have been recorded.')
                    self.user_input.clear()

        else:
            self.delayed_response_message = chatbot.respond(user_message)
            self.delayed_response_timer.start(1000)

        # Clear the user's input
        self.user_input.clear()

    def process_delayed_response(self):
        self.delayed_response_timer.stop()
        if self.delayed_response_message:
            chatbot_response_html = f'''
                            <div class="bubble alt">
                                <div class="txt">
                                    <p class="name alt" style="font-weight: 600; font-size: 20px; margin: 0 0 4px; color: #3498db;">CareBot</p>
                                    <p class="message">{self.delayed_response_message}</p>
                                </div>
                                <div class="bubble-arrow alt"></div>
                            </div>
                            '''
            self.conversation_area.append(chatbot_response_html)
            self.delayed_response_message = ""

    def display_web_response(self, web_response):
        response_lines = web_response.split('\n')[:5]
        response_text = '\n'.join(response_lines)
        response_html = '<div style="background-color: #F5F5F5; border-radius: 20px; max-width: 70%; padding: 10px; margin: 10px 0; text-align: left; color: #333333;">' + response_text + '</div>'
        self.conversation_area.append(response_html)

    def display_patient_details(self, patient_details):
        if patient_details:
            patient_info = "CareBot: Here are your patient details:\n"
            for key, value in patient_details.items():
                patient_info += f"{key}: {value}\n"
            self.conversation_area.append(patient_info)
        else:
            self.conversation_area.append("CareBot: Sorry, we couldn't find your patient details.")

    def display_hospitals_response(self, hospitals_near_me):
        if hospitals_near_me:
            hospitals_html = ''
            self.conversation_area.append(
                '<div style="color: #3498db;font-weight: 600;">CareBot</div>: Sure i can find you hospitals which are within 1000 meters from your current location.')
            for hospital in hospitals_near_me:
                hospital_html = f'''
                            <div class="bubble alt">
                                <div class="txt">
                                    <p class="message">{hospital['name']}, Distance: {hospital['distance']:.2f} meters</p>
                                </div>
                                <div class="bubble-arrow alt"></div>
                            </div>
                            '''
                hospitals_html += hospital_html
            self.conversation_area.append(hospitals_html)
        else:
            self.conversation_area.append('No hospitals found near your location.')

    def display_typing(self, message):
        if message:
            typing_html = '<div style="background-color: transparent; border-radius: 20px; max-width: 70%; padding: 10px; margin: 10px 0; text-align: left; color: #333333;">' + f'CareBot: {message}' + '</div>'
            self.typing_message = typing_html
            self.conversation_area.append(typing_html)
        else:
            if self.typing_message:
                self.conversation_area.textCursor().clearSelection()
                self.conversation_area.textCursor().removeSelectedText()

    def handle_user_request(self, user_input, doctors_data):
        if any(word in user_input.lower() for word in
               ['book an appointment', 'schedule an appointment', 'appointment booking']):
            doctor_name = extract_doctor_name(user_input)

            if doctor_name:
                matching_doctor = None
                for doctor in doctors_data:
                    if doctor_name.lower() in doctor[0].lower():
                        matching_doctor = doctor
                        break

                if matching_doctor:
                    response = f"Doctor Name: {matching_doctor[0]}\n"
                    response += f"Specialization: {matching_doctor[1]}\n"
                    response += f"Location: {matching_doctor[2]}\n"
                    response += self.conversation_area.append("Please enter the appointment time: ")
                    appointment_time = self.user_input.toPlainText()
                    response += f"Appointment booked with {matching_doctor[0]} at {appointment_time}"
                    self.conversation_area.append(response)
            else:
                self.conversation_area.append(show_available_doctors(doctors_data))
                selected_doctor = "The doctor's name you selected"
                if selected_doctor.lower() == 'quit':
                    response = "Exiting appointment booking."
                    self.conversation_area.append(response)
                else:
                    matching_doctor = None
                    for doctor in doctors_data:
                        if selected_doctor.lower() in doctor[0].lower():
                            matching_doctor = doctor
                            break

                    if matching_doctor:
                        response = f"Doctor Name: {matching_doctor[0]}\n"
                        response += f"Specialization: {matching_doctor[1]}\n"
                        response += f"Location: {matching_doctor[2]}\n"
                        appointment_time = input("Please enter the appointment time: ")
                        response += f"Appointment booked with {matching_doctor[0]} at {appointment_time}"
                        self.conversation_area.append(response)
                    else:
                        response = "The doctor is not present in the database. Please try again."
                        self.conversation_area.append(response)


def main():
    app = QApplication(sys.argv)
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Helloworld1@",
        "database": "doctor_info"
    }
    doctors_data = get_doctors_data(db_config)
    window = ChatbotGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
