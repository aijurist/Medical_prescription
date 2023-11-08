from twilio.rest import Client
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

from main import chatbot
from web_scraper import get_headache_info
from location_finder import find_hospitals_near_me
from patient_info import insert_patient, update_diagnosis, get_patient_details_secure, get_all_patients
from appointment import doctors_data, extract_doctor_name, get_doctors_data, show_available_doctors, book_appointment


account_sid = "AC700c21d089a2c5e6c316b9732ba40216"
auth_token = "e5da3d2418f3cd2a87cf8ea7f539d482"
client = Client(account_sid, auth_token)
twilio_number = "whatsapp:+14155238886"
recipient_number = "whatsapp:+917871252414"


def extract_keywords(user_input):
    words = word_tokenize(user_input)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    keywords = [word for word, pos in nltk.pos_tag(filtered_words) if pos in ['NN', 'NNS', 'JJ', 'JJR', 'JJS']]

    return keywords


def send_whatsapp_message(to, body):
    message = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to
    )
    print(f"Message sent with SID: {message.sid}")


def check_for_text_message(message):
    # Check if the message contains text
    if message.body:
        return True
    else:
        return False


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def receive_message():
    incoming_message = request.values.get("Body", "").strip()

    response = MessagingResponse()

    if check_for_text_message(request.values):
        response.message("You entered text: " + incoming_message)
    else:
        response.message("You didn't enter any text.")

    return str(response)


if __name__ == "__main__":
    app.run()

