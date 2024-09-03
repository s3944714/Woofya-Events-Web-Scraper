import requests
from bs4 import BeautifulSoup

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
    Parses the HTML content from The Yappack to extract event details.
    
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
            
            # Extract the location
            location_tag = event.find('div', class_='geodir_post_meta suburb')
            location = location_tag.get_text(strip=True) if location_tag else "No location found"
            
            events.append({
                'title': title,
                'description': description,
                'location': location
            })
    
    except Exception as e:
        print(f"Error parsing HTML from The Yappack: {e}")
    
    return events

def display_events(events):
    """
    Displays the list of events in the specified format.
    
    :param events: List of event details.
    """
    for event in events:
        print(f"Title: {event['title']}")
        print(f"Description: {event['description']}")
        print(f"Location: {event['location']}")
        print("-" * 40)

def scrape_yappack_events():
    url = 'https://theyappack.com.au/dog-friendly/pack-places/off-leash-areas/'
    
    print(f"Fetching HTML content from {url}...")
    html_content = fetch_html(url)
    
    if html_content:
        print("HTML content fetched successfully!\n")
        print("Parsing event details from The Yappack...")
        events = parse_yappack_events(html_content)
        
        if events:
            print(f"Found {len(events)} events:\n")
            display_events(events)
        else:
            print("No events found or an error occurred during parsing.")
    else:
        print("Failed to fetch HTML content.")

def main():
    print("Starting web scrapers...\n")
    
    # Scrape The Yappack events
    scrape_yappack_events()
    
    # Future websites can be added here
    # scrape_another_website()
    
    print("\nAll scraping tasks completed.")

if __name__ == "__main__":
    main()
