from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import re
import time

# Liste des URL à scraper
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
    # Configuration de Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en mode sans tête (optionnel)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(url)
    
    # Attendre que le contenu dynamique se charge
    time.sleep(5)  # Ajuste le temps d'attente si nécessaire
    
    try:
        # Extraction des données
        name = driver.find_element_by_css_selector('h1').text.strip()
        address = driver.find_element_by_css_selector('.location').text.strip() if driver.find_elements_by_css_selector('.location') else "N/A"
        
        opening_hours = {}
        try:
            opening_hours_div = driver.find_element_by_css_selector('.hours')
            for line in opening_hours_div.find_elements_by_tag_name('p'):
                parts = line.text.split(': ')
                if len(parts) == 2:
                    day, hours = parts
                    opening_hours[day.strip()] = hours.strip()
        except:
            opening_hours = {}

        # Extraction du contenu JavaScript
        scripts = driver.find_elements_by_tag_name('script')
        latitude, longitude = None, None
        for script in scripts:
            script_content = script.get_attribute('innerHTML')
            if 'latitude' in script_content and 'longitude' in script_content:
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
    except Exception as e:
        print(f"Erreur lors de l'extraction pour {url}: {e}")
    
    driver.quit()

for url in urls:
    extract_activity(url)

# Enregistrer les données dans un fichier JSON
with open('activities1.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=4)

print("Les données ont été extraites et enregistrées dans 'activities1.json'")
