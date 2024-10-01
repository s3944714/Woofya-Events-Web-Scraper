import json
import os

def count_entries(json_file):
    # Read the combined JSON file
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

    # Optional: Count occurrences of specific keys or attributes
    location_count = {}
    for entry in data:
        location = entry.get("location", "Unknown Location")
        location_count[location] = location_count.get(location, 0) + 1

    print(f"\nLocation Counts:")
    for loc, count in location_count.items():
        print(f"{loc}: {count}")
    
    return total_entries, location_count

# Example usage:
if __name__ == '__main__':
    combined_json_file = os.path.join(os.path.dirname(__file__), 'combined_data.json')
    count_entries(combined_json_file)
