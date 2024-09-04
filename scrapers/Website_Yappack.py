import requests
from bs4 import BeautifulSoup
import json

def fetch_html(url):
    """
    Fetches the HTML content of the given URL.
    
    :param url: URL of the webpage to fetch.
    :return: HTML content if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return None

def parse_yappack_events(html_content):
    """
    Parses the HTML content from The Yappack events page to extract event details.
    
    :param html_content: HTML content of the webpage.
    :return: A list of event details.
    """
    events = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all event containers
        event_items = soup.find_all('div', class_='geodir-post')
        
        for event in event_items:
            # Extract the title
            title_tag = event.find('h3', class_='geodir-entry-title')
            title = title_tag.get_text(strip=True) if title_tag else "No title found"
            
            # Extract the description
            description_tag = event.find('div', class_='excerpt')
            description = description_tag.get_text(strip=True) if description_tag else "No description found"
            
            # Extract the location with link
            location_tag = event.find('a', href=True)
            location = location_tag.get_text(strip=True) if location_tag else "No location found"
            location_url = location_tag['href'] if location_tag else "No URL found"
            
            events.append({
                'title': title,
                'description': description,
                'location': location,
                'location_url': location_url
            })
    
    except Exception as e:
        print(f"Error parsing HTML from The Yappack events page: {e}")
    
    return events

def parse_off_leash_areas(html_content):
    """
    Parses the HTML content from The Yappack off-leash areas page to extract park details.
    
    :param html_content: HTML content of the webpage.
    :return: A list of park details.
    """
    parks = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all park containers
        park_items = soup.find_all('div', class_='geodir-post')
        
        for park in park_items:
            # Extract the name
            name_tag = park.find('h3', class_='geodir-entry-title')
            name = name_tag.get_text(strip=True) if name_tag else "No name found"
            
            # Extract the description
            description_tag = park.find('div', class_='excerpt')
            description = description_tag.get_text(strip=True) if description_tag else "No description found"
            
            # Extract the location
            location_tag = park.find('div', class_='geodir_post_meta')
            location = location_tag.get_text(strip=True) if location_tag else "No location found"
            
            parks.append({
                'name': name,
                'description': description,
                'location': location
            })
    
    except Exception as e:
        print(f"Error parsing HTML from The Yappack off-leash areas page: {e}")
    
    return parks

def save_to_json(data, filename):
    """
    Saves the list of data to a JSON file.
    
    :param data: List of data details.
    :param filename: Name of the JSON file to save, including directory path.
    """
    try:
        # Ensure the directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename} successfully.")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

def display_events(events):
    """
    Displays the list of events in the specified format.
    
    :param events: List of event details.
    """
    for event in events:
        print(f"Title: {event['title']}")
        print(f"Description: {event['description']}")
        print(f"Location: {event['location']}")
        print(f"Location URL: {event['location_url']}")
        print("-" * 40)

def display_parks(parks):
    """
    Displays the list of parks in the specified format.
    
    :param parks: List of park details.
    """
    for park in parks:
        print(f"Name: {park['name']}")
        print(f"Description: {park['description']}")
        print(f"Location: {park['location']}")
        print("-" * 40)

def scrape_yappack_events():
    url = 'https://theyappack.com.au/travel-and-local-dog-guides/melbournes-top-dog-friendly-events/'
    
    print(f"Fetching HTML content from {url}...")
    html_content = fetch_html(url)
    
    if html_content:
        print("HTML content fetched successfully!\n")
        print("Parsing event details from The Yappack...")
        events = parse_yappack_events(html_content)
        
        if events:
            print(f"Found {len(events)} events:\n")
            display_events(events)
            
            # Save events to JSON file
            save_to_json(events, 'data/yappack_events.json')
        else:
            print("No events found or an error occurred during parsing.")
    else:
        print("Failed to fetch HTML content.")

def scrape_off_leash_areas():
    url = 'https://theyappack.com.au/dog-friendly/pack-places/off-leash-areas/'
    
    print(f"Fetching HTML content from {url}...")
    html_content = fetch_html(url)
    
    if html_content:
        print("HTML content fetched successfully!\n")
        print("Parsing off-leash area details from The Yappack...")
        parks = parse_off_leash_areas(html_content)
        
        if parks:
            print(f"Found {len(parks)} parks:\n")
            display_parks(parks)
            
            # Save parks to JSON file
            save_to_json(parks, 'data/yappack_parks.json')
        else:
            print("No parks found or an error occurred during parsing.")
    else:
        print("Failed to fetch HTML content.")

def main():
    print("Starting web scrapers...\n")
    
    # Scrape The Yappack events
    scrape_yappack_events()
    
    # Scrape The Yappack off-leash areas
    scrape_off_leash_areas()
    
    print("\nAll scraping tasks completed.")

if __name__ == "__main__":
    main()
