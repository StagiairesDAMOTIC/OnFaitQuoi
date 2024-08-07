import csv
import json

# Chemins des fichiers
csv_file_path = 'activities_updated.csv'  # Remplace 'data.csv' par le chemin vers ton fichier CSV
json_file_path = 'activities_updated.json'  # Remplace 'data.json' par le chemin vers ton fichier JSON de sortie

# Colonnes à conserver
selected_columns = ['name', 'location', 'image', 'Google Maps Link', 'Hours']  # Remplace par les colonnes souhaitées

def extract_lat_long(google_maps_link):
    try:
        # Vérifier si le lien contient '='
        if '=' in google_maps_link:
            coords_part = google_maps_link.split('=')[1]
            # Vérifier si la partie coords contient une virgule
            if ',' in coords_part:
                latitude, longitude = coords_part.split(',')
                return float(latitude), float(longitude)
            else:
                raise ValueError("Le lien ne contient pas les coordonnées attendues.")
        else:
            raise ValueError("Le lien ne contient pas le caractère '='.")
    except Exception as e:
        print(f"Erreur lors de l'extraction des coordonnées : {e} - Lien: {google_maps_link}")
        return None, None

def parse_hours(hours_str):
    try:
        # Exemple de format attendu: "Lundi(09:00-18:00)/Mardi(09:00-18:00)/..."
        hours_parts = hours_str.split('/')
        hours_dict = {}
        for part in hours_parts:
            if part:
                day, times = part.split('(')
                day = day.strip()
                times = times.strip(')')
                if times == "Fermé":
                    hours_dict[day] = {"open": None, "close": None}
                else:
                    open_time, close_time = times.split('-')
                    hours_dict[day] = {"open": open_time, "close": close_time}
        return hours_dict
    except Exception as e:
        print(f"Erreur lors de l'extraction des horaires : {e} - Horaires: {hours_str}")
        return {}


# Lire le fichier CSV et convertir en JSON avec les colonnes sélectionnées
data = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Filtrer les colonnes sélectionnées
        filtered_row = {col: row[col] for col in selected_columns if col in row}
        
        # Extraire latitude et longitude et les ajouter au dictionnaire
        if 'Google Maps Link' in filtered_row:
            latitude, longitude = extract_lat_long(filtered_row['Google Maps Link'])
            if latitude and longitude:
                filtered_row['latitude'] = latitude
                filtered_row['longitude'] = longitude
            del filtered_row['Google Maps Link']  # Supprimer l'ancienne colonne
        
        # Convertir les horaires au format JSON souhaité
        if 'Hours' in filtered_row:
            filtered_row['opening_hours'] = parse_hours(filtered_row['Hours'])
            del filtered_row['Hours']  # Supprimer l'ancienne colonne
        
        data.append(filtered_row)

# Écrire les données JSON dans le fichier
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Les données des colonnes sélectionnées ont été extraites du fichier CSV et sauvegardées dans {json_file_path}.")
