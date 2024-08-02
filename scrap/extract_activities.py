import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
url = 'https://guidedugolfe.com/spot/'

# Function to extract information from each spot
def extract_spot_info(spot):
    name = spot.find('p', class_='text-sm mt-0.5 3xs:font-semibold tracking-tight leading-tight line-clamp-1').text.strip()
    description = spot.find('p', class_='text-gray-500 text-xs 3xs:text-sm font-light tracking-tight leading-tight mt-0.5 3xs:mt-1 2xs:mt-2 line-clamp-2 sm:line-clamp-3 text-elipsis overflow-hidden').text.strip()
    location = spot.find('p', class_='truncate font-light text-gray-500').text.strip()
    status = spot.find('p', class_='text-green-600 mr-1').text.strip()
    href = spot['href']
    image_tag = spot.find('img', class_='h-full w-full rounded-md object-cover')
    image = image_tag['src'] if image_tag else ''

    return {
        'name': name,
        'description': description,
        'location': location,
        'status': status,
        'url': href,
        'image': image
    }

# Function to scrape the page and save data to CSV
def scrape_to_csv(url, output_csv):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    spots = soup.select('a[title][class="relative bg-white rounded-md h-32 3xs:h-40 w-full shadow-md drop-shadow flex flex-row"]')

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'description', 'location', 'status', 'url', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for spot in spots:
            spot_info = extract_spot_info(spot)
            writer.writerow(spot_info)

    print(f"Data has been extracted and saved to '{output_csv}'")

# Call the function to scrape the page and save data to CSV
scrape_to_csv(url, 'spots.csv')
