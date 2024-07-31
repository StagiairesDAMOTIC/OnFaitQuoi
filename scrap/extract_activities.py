import requests
from bs4 import BeautifulSoup
import json

# URL des pages d'activités à scraper
urls = [
    'https://guidedugolfe.com/en/spot/sun-force',
    'https://guidedugolfe.com/en/spot/energie-sport-danse-cavalaire',
    'https://guidedugolfe.com/en/spot/energie-sport-danse-gassin',
    'https://guidedugolfe.com/en/spot/pampelonne-nautic-club',
    'https://guidedugolfe.com/en/spot/wellness-saint-tropez1'
]

activities = []

def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def extract_activity(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la requête vers {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extractions basées sur la structure des pages du site
    name = soup.select_one('h1').text.strip()
    address = soup.select_one('.location').text.strip() if soup.select_one('.location') else "N/A"
    
    opening_hours_div = soup.select_one('.hours')
    opening_hours = {}
    if opening_hours_div:
        for line in opening_hours_div.select('p'):
            parts = line.text.split(': ')
            if len(parts) == 2:
                day, hours = parts
                opening_hours[day.strip()] = hours.strip()

    # Localisation et autres détails
    latitude = soup.select_one('.latitude').text.strip() if soup.select_one('.latitude') else "N/A"
    longitude = soup.select_one('.longitude').text.strip() if soup.select_one('.longitude') else "N/A"

    activity = {
        "name": name,
        "address": address,
        "latitude": safe_float(latitude),
        "longitude": safe_float(longitude),
        "opening_hours": opening_hours
    }

    activities.append(activity)

for url in urls:
    extract_activity(url)

# Enregistrer les données dans un fichier JSON
with open('activities2.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=4)

print("Les données ont été extraites et enregistrées dans 'activities2.json'")
