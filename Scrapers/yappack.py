import os
import json
import requests
from bs4 import BeautifulSoup

# Base URL for the event pages (excluding the page parameter)
base_url = "https://theyappack.com.au/dog-friendly-events/page/"

# Total number of pages to scrape (change based on site structure)
total_pages = 2

# List to store all event data
events_list = []

# Loop through each page
for page in range(1, total_pages + 1):
    # Construct the URL for the current page
    url = f"{base_url}{page}"
    print(f"Scraping page {page}: {url}")

    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all event cards based on the common container class for each event
        event_cards = soup.find_all('div', class_='card h-100 p-0 m-0 mw-100 border-0')

        # If no events are found on the page, stop the loop
        if not event_cards:
            print(f"No more events found on page {page}. Stopping.")
            break

        # Loop through each event card and extract the relevant details
        for event in event_cards:
            try:
                # Extract the event title and link using the updated class names
                title_tag = event.find('h3', class_='geodir-entry-title')
                link_tag = title_tag.find('a') if title_tag else None
                title = link_tag['title'].strip() if link_tag and link_tag.has_attr('title') else link_tag.text.strip() if link_tag else "N/A"
                event_link = link_tag['href'] if link_tag else "N/A"

                # Extract the start and end dates (inside <div> tags with class 'event-date')
                start_date_tag = event.find('div', class_='geodir-field-event_start_date')
                end_date_tag = event.find('div', class_='geodir-field-event_end_date')
                start_date = start_date_tag.text.strip() if start_date_tag else "N/A"
                end_date = end_date_tag.text.strip() if end_date_tag else "N/A"
                date_range = f"{start_date} - {end_date}" if start_date != "N/A" and end_date != "N/A" else start_date

                # Extract the event description (inside <div> class 'excerpt')
                description_tag = event.find('div', class_='excerpt')
                description = description_tag.text.strip() if description_tag else "N/A"

                # Extract the location (inside <div> class 'geodir-field-suburb')
                location_tag = event.find('div', class_='geodir-field-suburb')
                location = location_tag.text.strip() if location_tag else "N/A"

                # Store the event data in a dictionary
                event_data = {
                    'title': title,
                    'link': event_link,
                    'date_range': date_range,
                    'description': description,
                    'location': location
                }

                # Append the event data to the list
                events_list.append(event_data)

                # Debugging: Print each extracted event to verify
                print(f"Title: {title}, Link: {event_link}, Date Range: {date_range}, Location: {location}")

            except Exception as e:
                print(f"Error while parsing event on page {page}: {e}")
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Specify the output directory and file name
output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Raw_Data')    # Output folder outside the 'Scrapers' directory
output_file = os.path.join(output_directory, 'Yappack_Dog_Events_Updated.json')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the event data to the JSON file
with open(output_file, 'w') as f:
    json.dump(events_list, f, indent=4)

print(f"All event data saved to {output_file}")
