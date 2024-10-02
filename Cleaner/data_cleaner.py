import json
from datetime import datetime
from collections import defaultdict
import os

# Task 3.1 and 3.2: Remove duplicate entries based on event name and date.
def remove_duplicates(data):
    """
    Identify and remove duplicate entries based on event title and date.
    :param data: List of event dictionaries.
    :return: List of unique event dictionaries.
    """
    unique_events = {}
    for event in data:
        # Create a unique key based on title and date
        title = event.get("title", "").strip().lower()
        date = event.get("date", "").strip().lower()
        event_key = f"{title}_{date}"

        # If not already in unique_events, add it
        if event_key not in unique_events:
            unique_events[event_key] = event

    # Convert the dictionary back to a list
    return list(unique_events.values())

# Task 3.6: Standardize date formats to ISO 8601 (YYYY-MM-DD)
def standardize_date(date_str):
    """
    Standardize different date formats into ISO 8601 (YYYY-MM-DD).
    :param date_str: Original date string.
    :return: Standardized date string or original string if unable to parse.
    """
    date_formats = [
        "%Y-%m-%d",    # 2024-10-01
        "%d/%m/%Y",    # 01/10/2024
        "%B %d, %Y",   # October 1, 2024
        "%d %B %Y",    # 1 October 2024
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str  # Return original if unable to parse

# Task 3.7: Standardize common location names
def standardize_location(location):
    """
    Standardize common location names.
    :param location: Original location string.
    :return: Standardized location string.
    """
    location_mapping = {
        "sydney": "Sydney, NSW",
        "melbourne": "Melbourne, VIC",
        "yorke peninsula": "Yorke Peninsula, SA",
        "brisbane": "Brisbane, QLD",
    }

    # Convert location to lowercase and trim spaces
    clean_location = location.strip().lower()

    # Return standardized location if it exists in the mapping
    return location_mapping.get(clean_location, location)

# Main function to clean data
def clean_data(input_file, output_file):
    """
    Clean the input data by removing duplicates and standardizing formats.
    :param input_file: Path to the input JSON file.
    :param output_file: Path to the output JSON file.
    """
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as infile:
        try:
            data = json.load(infile)
        except json.JSONDecodeError as e:
            print(f"Error reading {input_file}: {e}")
            return

    # Step 1: Remove duplicates
    data = remove_duplicates(data)

    # Step 2: Standardize date formats and locations
    for event in data:
        event["date"] = standardize_date(event.get("date", ""))
        event["location"] = standardize_location(event.get("location", ""))

    # Save cleaned data
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print(f"Data cleaned and saved to {output_file}")

# Optional: Function to count entries and print summary (Task 3.3)
def count_entries(json_file):
    """
    Count entries in the cleaned JSON file.
    :param json_file: Path to the JSON file.
    :return: Total entries and count per location.
    """
    if not os.path.exists(json_file):
        print(f"File {json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {e}")
            return

    # Check if the data is a list of entries
    if not isinstance(data, list):
        print("Invalid data format. Expected a list of entries.")
        return

    total_entries = len(data)
    print(f"Total entries: {total_entries}")

    # Count occurrences of locations
    location_count = defaultdict(int)
    for entry in data:
        location = entry.get("location", "Unknown Location")
        location_count[location] += 1

    print(f"\nLocation Counts:")
    for loc, count in location_count.items():
        print(f"{loc}: {count}")

    return total_entries, location_count

# Run as a script
if __name__ == '__main__':
    input_file = os.path.join(os.path.dirname(__file__), '..', 'Raw_Data', 'combined_data.json')
    output_file = os.path.join(os.path.dirname(__file__), 'cleaned_data.json')

    # Clean the combined data
    clean_data(input_file, output_file)

    # Optional: Count entries in the cleaned data
    count_entries(output_file)
