import requests
from bs4 import BeautifulSoup
import re
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

def extract_coordinates_from_script(script_content):
    latitude_match = re.search(r'latitude\s*:\s*([0-9.]+)', script_content)
    longitude_match = re.search(r'longitude\s*:\s*([0-9.]+)', script_content)
    latitude = float(latitude_match.group(1)) if latitude_match else None
    longitude = float(longitude_match.group(1)) if longitude_match else None
    return latitude, longitude

def extract_activity(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la requête vers {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extractions basées sur la structure des pages du site
    name = soup.find('h1').text.strip()
    address = soup.find('div', class_='location').text.strip() if soup.find('div', class_='location') else "N/A"
    opening_hours_div = soup.find('div', class_='hours')
    opening_hours = {}
    if opening_hours_div:
        for line in opening_hours_div.find_all('p'):
            parts = line.text.split(': ')
            if len(parts) == 2:
                day, hours = parts
                opening_hours[day.strip()] = hours.strip()

    # Extraction du contenu JavaScript
    scripts = soup.find_all('script')
    latitude, longitude = None, None
    for script in scripts:
        script_content = script.string
        if script_content and 'latitude' in script_content and 'longitude' in script_content:
            latitude, longitude = extract_coordinates_from_script(script_content)
            break

    activity = {
        "name": name,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "opening_hours": opening_hours
    }

    activities.append(activity)

for url in urls:
    extract_activity(url)

# Enregistrer les données dans un fichier JSON
with open('activities3.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=4)

print("Les données ont été extraites et enregistrées dans 'activities3.json'")
