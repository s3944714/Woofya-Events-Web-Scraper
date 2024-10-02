import os
import json
from requests_html import HTMLSession
import pyppeteer

# Base URL for the event search
base_url = "https://www.visitnsw.com/search?query=dogs&type=events&page="

# List to store all event data
events_list = []

# Initialize an HTML session to render the page
session = HTMLSession()

# Limit the scraper to run only for 12 pages
max_pages = 12
max_retries = 3  # Maximum number of retries for each page

# Phase 1: Scrape event links and basic information
for page in range(1, max_pages + 1):
    # Construct the full URL for the current page
    url = f"{base_url}{page}"
    print(f"Scraping page {page}: {url}")

    # Send a GET request to fetch the HTML content
    response = session.get(url)

    # Retry mechanism for rendering JavaScript
    for attempt in range(max_retries):
        try:
            # Render the JavaScript (this is what handles dynamic content)
            response.html.render(sleep=3, timeout=20)  # Adjust timeout as needed
            break  # Exit loop if successful
        except pyppeteer.errors.TimeoutError:
            print(f"Timeout on page {page}, attempt {attempt + 1} of {max_retries}")
    else:
        print(f"Failed to render page {page} after {max_retries} attempts. Skipping.")
        continue

    # Parse the HTML content
    soup = response.html

    # Find all event blocks within the <li> tags (class 'search__page-result')
    event_sections = soup.find('li.search__page-result')

    # If no events are found on the page, stop the loop
    if not event_sections:
        print(f"No more events found on page {page}. Stopping.")
        break

    # Loop through each event and extract the relevant details
    for event in event_sections:
        try:
            # Extract the event link
            event_link_tag = event.find('a.opensearch__result-link', first=True)
            event_link = event_link_tag.attrs['href'] if event_link_tag else "N/A"

            # Extract the title (inside <h2> tag)
            title_tag = event.find('h2', first=True)
            title = title_tag.text.strip() if title_tag else "N/A"

            # Extract the description (inside <p> tag)
            description_tag = event.find('p', first=True)
            description = description_tag.text.strip() if description_tag else "N/A"

            # Extract the image URL (inside <img> tag)
            image_tag = event.find('img', first=True)
            image_url = image_tag.attrs['src'] if image_tag else "N/A"

            # Store the event data in a dictionary (basic data only)
            event_data = {
                'title': title,
                'link': event_link,
                'description': description,
                'image': image_url,
                
            }

            # Append the event data to the list
            events_list.append(event_data)

        except Exception as e:
            print(f"Error while parsing event on page {page}: {e}")

# Specify the output directory and file name
# Define the path to the existing 'Data' directory outside of 'Scrapers'
output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Raw_Data')  # Output folder outside the 'Scrapers' directory

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Define the output file path in the existing 'Data' directory
output_file = os.path.join(output_directory, 'VisitNSW_Events_with_Details.json')

# Save the event data to the JSON file
with open(output_file, 'w') as f:
    json.dump(events_list, f, indent=4)

print(f"All event data saved to {output_file}")
