import os
import json
from requests_html import HTMLSession

# Base URL for the event search (excluding the page parameter)
base_url = "https://southaustralia.com/search?Search=&q=dogs&page="

# Initialize an HTML session
session = HTMLSession()

# Number of pages to scrape
total_pages = 6

# List to store all service data
services_list = []

# Loop through each page
for page in range(1, total_pages + 1):
    # Construct the URL for the current page
    url = f"{base_url}{page}"
    print(f"Scraping page {page}: {url}")

    # Send a GET request to fetch the HTML content and render JavaScript
    response = session.get(url)
    response.html.render(sleep=3)  # Render the JavaScript, adjust sleep time if necessary

    # Check if the content was successfully rendered
    if response.status_code == 200:
        # Parse the rendered HTML content
        soup = response.html

        # Find all <div> tags with class 'product-card__content' that represent service cards
        service_cards = soup.find('div.product-card__content')

        if not service_cards:
            print(f"No services found on page {page}.")
        else:
            for service in service_cards:
                try:
                    # Extract the title (inside <h4> tag with class 'product-card__title')
                    title_tag = service.find('h4.product-card__title', first=True)
                    title = title_tag.text.strip() if title_tag else "N/A"

                    # Extract the location (inside <span> tag with class 'product-card__location')
                    location_tag = service.find('span.product-card__location', first=True)
                    location = location_tag.text.strip() if location_tag else "N/A"

                    # Extract the features (inside <ul> tag with class 'product-card__features')
                    features_tag = service.find('ul.product-card__features', first=True)
                    features = []
                    if features_tag:
                        features = [feature.text.strip() for feature in features_tag.find('li.product-card__features-item')]

                    # Store the service data in a dictionary
                    service_data = {
                        'title': title,
                        'location': location,
                        'features': features
                    }

                    # Append the service data to the list
                    services_list.append(service_data)

                except Exception as e:
                    print(f"Error while parsing service on page {page}: {e}")
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Specify the output directory and file name
output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Raw_Data')  # Output folder outside the 'Scrapers' directory
output_file = os.path.join(output_directory, 'SouthAustralia_Dog_Services.json')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the service data to the JSON file
with open(output_file, 'w') as f:
    json.dump(services_list, f, indent=4)

print(f"All service data saved to {output_file}")
