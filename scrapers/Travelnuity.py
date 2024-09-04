import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        events = []

        # Extract headings and descriptions
        headings = soup.find_all('h2', class_='wp-block-heading')
        descriptions = soup.find_all('p')

        for heading in headings:
            event = {}
            event['location_name'] = heading.get_text(strip=True)
            
            # Extract the brief description related to the heading
            next_element = heading.find_next_sibling('p')
            if next_element:
                event['description'] = next_element.get_text(strip=True)
            else:
                event['description'] = "No description available."

            events.append(event)

        return events
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []

def save_to_json(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

def main():
    url = 'https://www.travelnuity.com/dog-friendly-day-trips-melbourne/'
    html_content = fetch_html(url)
    if html_content:
        events = parse_html(html_content)
        save_to_json(events, 'data/travelnuity.json')

if __name__ == '__main__':
    # Ensure the directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
