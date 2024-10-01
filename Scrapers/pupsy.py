import os
import json
import requests
from bs4 import BeautifulSoup

# Base URL of the Pupsy dog-friendly pubs and bars page
base_url = "https://pupsy.com.au/places/category/dog-friendly-pubs-bars/"

# Total number of pages to scrape (manually inspected, update if more pages exist)
total_pages = 2

# List to store all venue data
venues_list = []

# Loop through each page (if pagination is present)
for page in range(1, total_pages + 1):
    # Construct the URL for the current page (adjust if the site uses different pagination)
    url = f"{base_url}page/{page}/" if page > 1 else base_url
    print(f"Scraping page {page}: {url}")

    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all venue blocks using the appropriate class
        venue_blocks = soup.find_all('div', class_='fl-module-content')

        # If no venues are found, break the loop
        if not venue_blocks:
            print(f"No more venues found on page {page}. Stopping.")
            break

        # Loop through each venue block and extract details
        for index, venue in enumerate(venue_blocks):
            try:
                # Extract the title and link
                title_tag = venue.find('h2', class_='geodir-entry-title')
                if title_tag:
                    venue_name = title_tag.text.strip()
                    venue_link = title_tag.find('a')['href'] if title_tag.find('a') else "N/A"
                    
                    # Set the location and description to be identical to the title
                    location = venue_name
                    description = venue_name
                else:
                    # Skip the block if no title is found
                    print(f"Skipping a venue block due to missing title on page {page}. Block #{index}")
                    continue

                # Extract amenities such as "Dogs Welcome Inside" or "Covered Outdoor"
                amenities = []
                amenity_tags = venue.find_all('h5', class_='fl-callout-title')
                for amenity in amenity_tags:
                    amenities.append(amenity.text.strip().replace('<br>', ' '))

                # Store the venue data in a dictionary with title, description, and location set the same
                venue_data = {
                    'title': venue_name,
                    'description': description,  # Same as title
                    'link': venue_link,
                    'location': location,  # Same as title
                    'amenities': ", ".join(amenities) if amenities else "None"
                }

                # Append the venue data to the list
                venues_list.append(venue_data)

                # Debugging: Print each extracted venue to verify
                print(f"Title: {venue_name}, Description: {description}, Link: {venue_link}, Location: {location}, Amenities: {venue_data['amenities']}")

            except Exception as e:
                print(f"Error while parsing venue on page {page}: {e}")
    else:
        print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

# Specify the output directory and file name
output_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Raw_Data')  # Output folder outside the 'Scrapers' directory
output_file = os.path.join(output_directory, 'pupsytest.json')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the venue data to the JSON file
with open(output_file, 'w') as f:
    json.dump(venues_list, f, indent=4)

print(f"All venue data saved to {output_file}")
