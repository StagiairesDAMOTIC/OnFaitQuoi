import csv
import requests
from bs4 import BeautifulSoup
import time

def extract_info_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Google Maps link
        google_maps_link = None
        for a in soup.find_all('a', href=True):
            if 'google.com/maps' in a['href']:
                google_maps_link = a['href']
                break

        # Extract opening hours
        hours = {}
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        hours_elements = soup.select('dl.divide-y > div')
        
        for element in hours_elements:
            day_element = element.find('dt')
            if day_element:
                day = day_element.get_text(strip=True)
                times = element.find_all('span', class_='text-cyan-600')
                if times:
                    hours[day] = [time.get_text(strip=True) for time in times]
                else:
                    hours[day] = ['Fermé']

        # Format hours into the desired format
        hours_str = ""
        for day in days:
            if day in hours:
                if hours[day] == ['Fermé']:
                    hours_str += f"{day}(Fermé)/"
                else:
                    if len(hours[day]) == 1:
                        hours_str += f"{day}({hours[day][0]})/"
                    elif len(hours[day]) >= 2:
                        hours_str += f"{day}({hours[day][0]}-{hours[day][1]})/"
            else:
                hours_str += f"{day}(Inconnu)/"

        hours_str = hours_str.rstrip('/')

        return google_maps_link, hours_str
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        return None, None

def update_csv_with_extracted_info(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Google Maps Link', 'Hours']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            url = row['url']
            print(f"Processing URL: {url}")
            google_maps_link, hours = extract_info_from_url(url)
            row['Google Maps Link'] = google_maps_link
            row['Hours'] = hours
            writer.writerow(row)
            time.sleep(1)  # Sleep to respect rate limits

    print(f"CSV file updated and saved as {output_csv}")

# Paths to the CSV files
input_csv = 'spots.csv'  # Path to the input CSV file
output_csv = 'activities_updated.csv'  # Path to the output CSV file

update_csv_with_extracted_info(input_csv, output_csv)
