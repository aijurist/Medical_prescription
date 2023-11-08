import nltk
from nltk.chat.util import Chat
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import random

lemmatizer = WordNetLemmatizer()


def lemmatize_input(user_input):
    words = word_tokenize(user_input)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)


pairs = [
    ("(hi|hello|hey)", [
        "Hi there! How can I assist you?"
    ]),

    ("(.*)(headache|pain in head)(.*)", [
        "I'm sorry to hear about your headache. Can you describe it in more detail?",
        "What specific symptoms are you experiencing during your headache?"
    ]),

    ("(.*)(migraine|tension headache|cluster headache|sinus headache)", [
        "Based on your description, it could be a specific type of headache. Let's narrow it down.",
        "Can you describe the pain in more detail?"
    ]),

    (
        "(.*)(throbbing|pulsating|one-sided|both sides|eye pain|nausea|vomiting|sensitivity to light|sound|nasal congestion|watery eyes|pain in my (eye|eyes))",
        [
            "I see. Based on the symptoms you've mentioned, it could be a migraine.",
            "Migraine headaches often involve throbbing pain, nausea, vomiting, and sensitivity to light and sound.",
            "Can you provide more information about your symptoms?"
        ]),

    # Questions to narrow down migraine
    (
    "(.*)(throb|pulsat|hammer|pound|intense|severe|one-sided|eye pain|nausea|vomit|sensitiv|light|sound|nasal congestion|watery eyes)",
    [
        "I see. Migraine headaches often involve throbbing, intense, and one-sided pain, along with symptoms like nausea, vomiting, and sensitivity to light and sound.",
        "Are you experiencing any of these symptoms?"
    ]),

    (
    "(.*)(aura|visual disturbances|visual changes|flashes of light|zigzag lines|blind spots|numbness|tingling|weakness|before the headache)",
    [
        "Migraines sometimes have a pre-headache phase called an aura. This can include visual disturbances like flashes of light, zigzag lines, blind spots, or other sensory changes.",
        "Have you noticed any aura or visual disturbances before your headaches?"
    ]),

    (
    "(.*)(recurrent|headache attacks|last several hours|up to 72 hours|days|associated with|dizziness|vomiting|exacerbated by physical activity|triggered by|common triggers)",
    [
        "Migraines are often recurrent, with headache attacks that can last several hours to up to 72 hours. They are typically associated with symptoms like dizziness, vomiting, and can be exacerbated by physical activity.",
        "Do your headaches fit this pattern, and have you identified any common triggers?"
    ]),

    ("(.*)(family history|migraine|relatives|family members)", [
        "Migraines can sometimes run in families. Do you have any family history of headaches or migraines? Have your relatives experienced similar issues?"
    ]),

    ("no", [
        "I understand. Let's continue exploring your symptoms to get a clearer picture. Can you provide more information about your current headache?"
    ]),

    ("yes", [
        "Thank you for sharing that. It's helpful to know. Do you experience other migraine symptoms, or is there something else you'd like to share about your condition?"
    ]),

    (
    "(.*)(constant|pressure|band-like|both sides|stress|muscle tension|sensitivity to light|sound|nasal congestion|watery eyes)",
    [
        "I see. Based on the symptoms you've mentioned, it could be a tension headache.",
        "Tension headaches often involve constant pressure or a band-like sensation around the head, and they may be related to stress or muscle tension.",
        "Can you provide more information about your symptoms?"
    ]),

    ("(.*)(severe|excruciating|one-sided|eye pain|nasal congestion|watery eyes|restlessness)", [
        "I see. Based on the symptoms you've mentioned, it could be a cluster headache.",
        "Cluster headaches are known for their severe, excruciating pain, often on one side of the head, along with eye-related symptoms.",
        "Can you provide more information about your symptoms?"
    ]),

    ("(.*)(facial pressure|forehead|cheeks|nasal congestion|watery eyes)", [
        "I see. Based on the symptoms you've mentioned, it could be a sinus headache.",
        "Sinus headaches are typically associated with facial pressure, often in the forehead or cheeks, and may involve nasal congestion and watery eyes.",
        "Can you provide more information about your symptoms?"
    ]),

    ("(.*)(intensity|scale|1-10|1 to 10|intense)", [
        "On a scale of 1 to 10, how would you rate the intensity of the pain?"
    ]),

    ("(.*)(duration|how long|hours|whole day)", [
        "How long have you been experiencing these headaches?"
    ]),

    ("(.*)(triggers|cause|foods|stress|sleep)", [
        "Have you noticed any specific triggers that seem to cause your headaches, such as certain foods, stress, or lack of sleep?"
    ])
]

fever_pairs = [
    ("(.*)(fever|high temperature|temperature|body temperature)(.*)", [
        "I'm sorry to hear that you have a fever. Can you tell me more about your symptoms?",
        "How high is your temperature, and have you noticed any other symptoms along with the fever?"
    ]),

    ("(.*)(temperature|thermometer|readings|degrees|Celsius|Fahrenheit)", [
        "What's the current reading on your thermometer, and how are you measuring your temperature (in Celsius or Fahrenheit)?"
    ]),

    ("(.*)(chills|sweating|shivering)(.*)", [
        "Fever can often be accompanied by chills, sweating, or shivering. Are you experiencing any of these symptoms?"
    ]),

    ("(.*)(cough|sore throat|runny nose|shortness of breath|fatigue|muscle aches)", [
        "Fever can be a symptom of various illnesses. Have you noticed any other symptoms like cough, sore throat, runny nose, shortness of breath, fatigue, or muscle aches?"
    ]),

    ("(.*)(recent travel|exposure|contact|COVID-19)(.*)", [
        "Given the current health concerns, have you recently traveled to a high-risk area or been in close contact with someone who has tested positive for COVID-19?"
    ]),

    ("(.*)(duration|how long|hours|days)(.*)", [
        "How long have you had this fever? Is it a recent onset, or has it been ongoing for several days?"
    ]),

    ("(.*)(medications|home remedies|doctor|medical advice)(.*)", [
        "It's important to monitor your fever. Have you taken any medications or tried home remedies to manage it, or have you consulted a doctor for medical advice?"
    ]),

    ("(.*)(seek medical attention|emergency|worsening symptoms)(.*)", [
        "If your fever is high and accompanied by severe symptoms, it's crucial to seek immediate medical attention. Please don't hesitate to call for help if you're experiencing worsening symptoms."
    ])
]
ext = [
    ("(.*)(fever|high temperature|temperature|body temperature)(.*)", [
        "I'm sorry to hear that you have a fever. Can you tell me more about your symptoms?",
        "How high is your temperature, and have you noticed any other symptoms along with the fever?"
    ]),
    ("(.*)(tired|fatigued|exhausted|lack of energy)(.*)", [
        "I'm sorry to hear that you're feeling tired. Can you describe your tiredness in more detail?",
        "What other symptoms are you experiencing along with feeling tired?"
    ]),
]
pairs += fever_pairs
pairs += ext
chatbot = Chat(pairs)

