import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_info_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraire le lien Google Maps
        google_maps_link = None
        google_maps_element = soup.find('a', href=True, text='Google Maps')
        if google_maps_element:
            google_maps_link = google_maps_element['href']

        # Extraire les horaires
        hours = None
        hours_element = soup.find('p', class_='opening-hours')  # Ajuster la classe en fonction de votre HTML
        if hours_element:
            hours = hours_element.text.strip()

        return google_maps_link, hours
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion à {url}: {e}")
        return None, None

def update_csv_with_extracted_info(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    data['Google Maps Link'] = ''
    data['Hours'] = ''

    for index, row in data.iterrows():
        url = row['URL']  # Assurez-vous que la colonne contenant les URL est nommée 'URL' dans votre CSV
        google_maps_link, hours = extract_info_from_url(url)
        data.at[index, 'Google Maps Link'] = google_maps_link
        data.at[index, 'Hours'] = hours

    data.to_csv(output_csv, index=False)
    print(f"Mise à jour du fichier CSV terminée et sauvegardée dans {output_csv}")

# Chemins vers les fichiers CSV
input_csv = 'spots.csv'  # Chemin vers le fichier CSV d'entrée
output_csv = 'activities_updated.csv'  # Chemin vers le fichier CSV de sortie

update_csv_with_extracted_info(input_csv, output_csv)
