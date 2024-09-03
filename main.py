
import requests
from bs4 import BeautifulSoup
import EventURLlist
import time
# Define the URL of the event
url = 'https://www.eventbrite.com.au/d/australia/dog/'

def fetch_event_info(url):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract meta tags for Open Graph
    event_title = soup.find('meta', property='og:title')
    event_description = soup.find('meta', property='og:description')
    event_image = soup.find('meta', property='og:image')
    event_url = soup.find('meta', property='og:url')

    # Extract content from meta tags
    event_title_text = event_title['content'] if event_title else 'Title not found'
    event_description_text = event_description['content'] if event_description else 'Description not found'
    event_image_url = event_image['content'] if event_image else 'Image URL not found'
    event_url_text = event_url['content'] if event_url else 'Event URL not found'

    # Extract location
    location_div = soup.find('div', class_='location-info__address')
    location_text = location_div.get_text(strip=True) if location_div else 'Location not found'

    # Extract time slots
    time_slots = soup.find_all('li', class_='child-event-dates-item')
    time_slots_text = []
    for slot in time_slots:
        time_span = slot.find('time')
        if time_span:
            date_time = time_span.get('datetime')
            time_slots_text.append(date_time)


    # Return the extracted data as a dictionary
    return {
        'Title': event_title_text,
        'Description': event_description_text,
        'Image URL': event_image_url,
        'Event URL': event_url_text,
        'Location': location_text,
        'Available Dates': time_slots_text
    }

def process_event_urls(event_urls, delay=2):
    event_details_list = []
    for index, url in enumerate(event_urls):
        print(f"Processing {index + 1}/{len(event_urls)}: {url}")
        event_details = fetch_event_info(url)
        event_details_list.append(event_details)
        time.sleep(delay)  # Delay between requests to avoid 429 error
    return event_details_list

# Example usage
event_urls = EventURLlist.gather_event_urls_with_selenium(url)
result = process_event_urls(event_urls)
for event in result:
    print(event)
