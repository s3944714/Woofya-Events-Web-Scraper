import os
import requests
from bs4 import BeautifulSoup
import json

# Base URL of the page to scrape
base_url = "https://humanitix.com/au/search?query=dogs&page="

# List to store all event data from all pages
all_events_list = []

# Loop through multiple pages (change the range as needed or set a stopping condition)
for page_num in range(0, 5):  # Change 5 to the number of pages you want to scrape or dynamically stop when no results
    url = f"{base_url}{page_num}"
    
    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all event blocks
        events = soup.find_all('a', class_='sc-eb5cf798-0')

        # If there are no events on the page, stop scraping
        if not events:
            print(f"No events found on page {page_num}, stopping.")
            break

        # List to store the event data for the current page
        events_list = []

        for event in events:
            try:
                # Extract the title
                title = event.find('h6').text.strip()

                # Extract the description (date and time)
                description = event.find('p', class_='sc-8821f522-0').text.strip()

                # Extract the location
                location = event.find_all('p', class_='sc-8821f522-0')[1].text.strip()

                # Store the event data in a dictionary
                event_data = {
                    'title': title,
                    'description': description,
                    'location': location
                }

                # Append the event data to the list
                events_list.append(event_data)

            except Exception as e:
                print(f"Error while parsing event: {e}")

        # Add events from the current page to the all_events_list
        all_events_list.extend(events_list)

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        break

# Specify the output directory and file name
output_directory = os.path.join('..', 'Data')  # Go one level up and enter 'Data' folder
output_file = os.path.join(output_directory, 'Humantix.json')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save all event data from all pages to the JSON file
with open(output_file, 'w') as f:
    json.dump(all_events_list, f, indent=4)

print(f"Events data saved to {output_file}")
