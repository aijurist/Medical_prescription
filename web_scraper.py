import requests
from bs4 import BeautifulSoup
import re
def clean_extracted_info(extracted_info):
    info_lines = extracted_info.split('\n')
    filtered_lines = [line for line in info_lines if not any(unwanted_word in line.lower() for unwanted_word in ['uk:', 'us:'])]
    cleaned_info = '\n'.join(filtered_lines)
    cleaned_info = re.sub(r'\[\d+\]', '', cleaned_info)
    return cleaned_info

def get_headache_info(headache_type):
    wikipedia_urls = {
        'migraine': 'https://en.wikipedia.org/wiki/Migraine',
        'tension headache': 'https://en.wikipedia.org/wiki/Tension_headache',
        'cluster headache': 'https://en.wikipedia.org/wiki/Cluster_headache',
        'sinus headache': 'https://en.wikipedia.org/wiki/Sinusitis'
    }

    if headache_type.lower() in wikipedia_urls:
        url = wikipedia_urls[headache_type.lower()]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            info_div = soup.find('div', class_='mw-content-container')
            content = info_div.find_all('p')
            extracted_text = []
            for element in content:
                extracted_text.append(element.get_text())
            extracted_info = '\n'.join(extracted_text)
            extracted_info = clean_extracted_info(extracted_info)
                        
            return extracted_info
        else:
            return "I couldn't find information about that type of headache at the moment."
    else:
        return "I'm not familiar with that type of headache."
