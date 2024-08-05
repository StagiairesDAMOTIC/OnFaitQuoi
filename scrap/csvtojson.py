import csv
import json

# Chemins des fichiers
csv_file_path = 'data.csv'  # Remplace 'data.csv' par le chemin vers ton fichier CSV
json_file_path = 'data.json'  # Remplace 'data.json' par le chemin vers ton fichier JSON de sortie

# Colonnes à conserver
selected_columns = ['name', 'location', 'url']  # Remplace par les colonnes souhaitées

# Lire le fichier CSV et convertir en JSON avec les colonnes sélectionnées
data = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Filtrer les colonnes sélectionnées
        filtered_row = {col: row[col] for col in selected_columns if col in row}
        data.append(filtered_row)

# Écrire les données JSON dans le fichier
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Les données des colonnes sélectionnées ont été extraites du fichier CSV et sauvegardées dans {json_file_path}.")
