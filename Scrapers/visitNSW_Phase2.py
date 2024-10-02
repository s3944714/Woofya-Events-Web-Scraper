import os
import json
import aiohttp
import asyncio
from requests_html import AsyncHTMLSession

# Path to the JSON file created by Phase 1
input_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'VisitNSW_Events_with_Details.json')

# Load the events data from the JSON file
def load_events():
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            return json.load(f)
    else:
        print(f"File not found: {input_file}")
        return []

# Asynchronous function to scrape event details concurrently
async def fetch_event_details(session, event):
    try:
        event_link = event['link']
        print(f"Scraping event details from {event_link}")

        # Send an asynchronous request to get event details
        async with session.get(event_link) as response:
            content = await response.text()
            event_soup = AsyncHTMLSession().html
            event_soup.feed(content)
            await event_soup.arender(sleep=1)

            # Extract date and location
            date_tag = event_soup.find('span.event-date', first=True)
            location_tag = event_soup.find('span.event-location', first=True)

            # Update event data with the date and location
            event['date'] = date_tag.text.strip() if date_tag else "TBD"
            event['location'] = location_tag.text.strip() if location_tag else "TBD"

    except Exception as e:
        print(f"Error while scraping details for event {event['title']}: {e}")
        # Mark the event as failed
        event['date'] = 'Failed to Scrape'
        event['location'] = 'Failed to Scrape'

# Phase 2: Scrape date and location using asyncio and aiohttp
async def gather_event_details(events):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for event in events:
            tasks.append(fetch_event_details(session, event))
        await asyncio.gather(*tasks)

# Save the successfully scraped events
def save_successful_events(events):
    output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'VisitNSW_Successful_Events.json')
    successful_events = [event for event in events if event['date'] != 'Failed to Scrape']
    with open(output_file, 'w') as f:
        json.dump(successful_events, f, indent=4)
    print(f"Successfully scraped events saved to {output_file}")

# Save the failed events
def save_failed_events(events):
    output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'VisitNSW_Failed_Events.json')
    failed_events = [event for event in events if event['date'] == 'Failed to Scrape']
    with open(output_file, 'w') as f:
        json.dump(failed_events, f, indent=4)
    print(f"Failed events saved to {output_file}")

# Main function to run the scraping process
async def main():
    events_list = load_events()
    if events_list:
        await gather_event_details(events_list)
        save_successful_events(events_list)
        save_failed_events(events_list)
    else:
        print("No events to process.")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
