from bs4 import BeautifulSoup
import csv
import os

# Path of the local HTML file
file_path = r'C:\Users\Eloi\Documents\GitHub\StagiairesDAMOTIC\Guide du Golfe de Saint-Tropez.html'

# Normalize the file path to avoid issues with backslashes
file_path = os.path.normpath(file_path)

# Function to extract information from each spot
def extract_spot_info(spot):
    name_tag = spot.find('p', class_='text-sm mt-0.5 3xs:font-semibold tracking-tight leading-tight line-clamp-1')
    name = name_tag.text.strip() if name_tag else 'N/A'

    description_tag = spot.find('p', class_='text-gray-500 text-xs 3xs:text-sm font-light tracking-tight leading-tight mt-0.5 3xs:mt-1 2xs:mt-2 line-clamp-2 sm:line-clamp-3 text-elipsis overflow-hidden')
    description = description_tag.text.strip() if description_tag else 'N/A'

    location_tag = spot.find('p', class_='truncate font-light text-gray-500')
    location = location_tag.text.strip() if location_tag else 'N/A'

    status_tag = spot.find('p', class_='text-green-600 mr-1')
    status = status_tag.text.strip() if status_tag else 'N/A'

    href = spot['href']
    image_tag = spot.find('img', class_='h-full w-full rounded-md object-cover')
    image = image_tag['src'] if image_tag else 'N/A'

    return {
        'name': name,
        'description': description,
        'location': location,
        'status': status,
        'url': href,
        'image': image
    }

# Function to scrape the page and save data to CSV
def scrape_to_csv(file_path, output_csv):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    spots = soup.select('a[title][class="relative bg-white rounded-md h-32 3xs:h-40 w-full shadow-md drop-shadow flex flex-row"]')

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'description', 'location', 'status', 'url', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for spot in spots:
            spot_info = extract_spot_info(spot)
            writer.writerow(spot_info)

    print(f"Data has been extracted and saved to '{output_csv}'")

# Path to your local HTML file and the output CSV file
file_path = r'C:\Users\Eloi\Documents\GitHub\StagiairesDAMOTIC\Guide du Golfe de Saint-Tropez.html'  # Change this to your local HTML file path
file_path = os.path.normpath(file_path)
output_csv = 'spots.csv'

# Call the function to scrape the page and save data to CSV
scrape_to_csv(file_path, output_csv)
