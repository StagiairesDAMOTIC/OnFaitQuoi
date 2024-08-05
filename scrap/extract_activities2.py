import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
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
        hours = None
        hours_element = soup.find('p', class_='opening-hours')  # Adjust class based on your HTML structure
        if hours_element:
            hours = hours_element.get_text(strip=True)

        return google_maps_link, hours
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        return None, None

def update_csv_with_extracted_info(input_csv, output_csv):
    data = pd.read_csv(input_csv)
    print("Columns available in CSV:", data.columns)  # Debugging line to print column names
    
    # Add new columns for the extracted information
    data['Google Maps Link'] = ''
    data['Hours'] = ''

    for index, row in data.iterrows():
        url = row['url']  # Use the correct column name based on your CSV file
        print(f"Processing URL: {url}")  # Debugging line to print the current URL being processed
        google_maps_link, hours = extract_info_from_url(url)
        data.at[index, 'Google Maps Link'] = google_maps_link
        data.at[index, 'Hours'] = hours
        time.sleep(1)  # Sleep to respect rate limits

    data.to_csv(output_csv, index=False)
    print(f"CSV file updated and saved as {output_csv}")

# Paths to the CSV files
input_csv = 'spots.csv'  # Path to the input CSV file
output_csv = 'activities_updated.csv'  # Path to the output CSV file

update_csv_with_extracted_info(input_csv, output_csv)
