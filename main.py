import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://humanitix.com/au/search?query=dogs&page=0"

# Send a GET request to fetch the HTML content of the page
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store the event data
    events_list = []

    # Find all event blocks
    events = soup.find_all('a', class_='sc-eb5cf798-0')

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

    # Save the event data to a JSON file
    with open('events.json', 'w') as f:
        json.dump(events_list, f, indent=4)

    print("Events data saved to events.json")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
