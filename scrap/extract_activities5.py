import requests
from bs4 import BeautifulSoup
import re
import json

# URLs of the activity pages to scrape
urls = [
    'https://guidedugolfe.com/en/spot/sun-force',
    'https://guidedugolfe.com/en/spot/energie-sport-danse-cavalaire',
    'https://guidedugolfe.com/en/spot/energie-sport-danse-gassin',
    'https://guidedugolfe.com/en/spot/pampelonne-nautic-club',
    'https://guidedugolfe.com/en/spot/wellness-saint-tropez1'
]

activities = []

def extract_activity(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract specific information based on CSS classes
    name = soup.title.string if soup.title else "N/A"
    description_tag = soup.find('meta', {'name': 'description'})
    description = description_tag['content'] if description_tag else "N/A"
    image_tag = soup.find('meta', {'property': 'og:image'})
    image = image_tag['content'] if image_tag else "N/A"

    # Extract latitude and longitude from the script tag
    latitude, longitude = "N/A", "N/A"
    for script in soup.find_all('script'):
        if script.string and 'latitude' in script.string:
            script_content = script.string
            latitude_match = re.search(r'"latitude":\s*(-?\d+\.\d+)', script_content)
            longitude_match = re.search(r'"longitude":\s*(-?\d+\.\d+)', script_content)
            if latitude_match and longitude_match:
                latitude = latitude_match.group(1)
                longitude = longitude_match.group(1)
                break

    # Extract other information if needed
    # For example, activities listed on the page
    activities_list = soup.select('.flex-1.space-y-1.px-2 a')
    activities_names = [activity.get_text(strip=True) for activity in activities_list]

    activity = {
        "name": name,
        "description": description,
        "image": image,
        "latitude": float(latitude) if latitude != "N/A" else None,
        "longitude": float(longitude) if longitude != "N/A" else None,
        "activities": activities_names
    }

    activities.append(activity)

for url in urls:
    extract_activity(url)

# Save the extracted data to a JSON file
with open('activities5.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=4)

print("Data has been extracted and saved to 'activities5.json'")
