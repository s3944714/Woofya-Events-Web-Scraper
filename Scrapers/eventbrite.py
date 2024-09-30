import os
import json
from requests_html import HTMLSession

# Base URL for Eventbrite search results (Australia Dog Events)
base_url = "https://www.eventbrite.com.au/d/australia/dog/?page="

# Initialize an HTML session
session = HTMLSession()

# Number of pages to scrape
total_pages = 6  # Adjust based on the number of pages available on the site

# List to store all event data
events_list = []

# Loop through each page
for page in range(1, total_pages + 1):
    # Construct the URL for the current page
    url = f"{base_url}{page}"
    print(f"Scraping page {page}: {url}")

    # Send a GET request to fetch the HTML content and render JavaScript
    response = session.get(url)
    response.html.render(sleep=3)  # Render the JavaScript to load dynamic content

    # Check if the content was successfully rendered
    if response.status_code == 200:
        # Parse the rendered HTML content
        soup = response.html

        # Find all <section> tags with class 'event-card-details' that represent event cards
        event_sections = soup.find('section.event-card-details')

        if not event_sections:
            print(f"No events found on page {page}.")
        else:
            for event in event_sections:
                try:
                    # Extract the event link
                    link_tag = event.find('a.event-card-link', first=True)
                    event_link = link_tag.attrs['href'] if link_tag else "N/A"

                    # Extract the event title (inside <h3> tag)
                    title_tag = event.find('h3', first=True)
                    title = title_tag.text.strip() if title_tag else "N/A"

                    # Extract the event date (inside the first <p> tag)
                    date_tag = event.find('p', first=True)
                    date = date_tag.text.strip() if date_tag else "N/A"

                    # Extract the event location (inside the second <p> tag)
                    location_tag = event.find('p:nth-of-type(2)', first=True)
                    location = location_tag.text.strip() if location_tag else "N/A"

                    # Extract the event price (inside the <div> tag with class 'priceWrapper')
                    price_tag = event.find('div.DiscoverHorizontalEventCard-module__priceWrapper___3rOUY p', first=True)
                    price = price_tag.text.strip() if price_tag else "Free"  # Default to Free if no price is listed

                    # Store the event data in a dictionary
                    event_data = {
                        'title': title,
                        'link': event_link,
                        'date': date,
                        'location': location,
                        'price': price
                    }

                    # Append the event data to the list
                    events_list.append(event_data)

                except Exception as e:
                    print(f"Error while parsing event on page {page}: {e}")
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Specify the output directory and file name
output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data')  # Output folder outside the 'Scrapers' directory
output_file = os.path.join(output_directory, 'Eventbrite_Dog_Events.json')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the event data to the JSON file
with open(output_file, 'w') as f:
    json.dump(events_list, f, indent=4)

print(f"All event data saved to {output_file}")
