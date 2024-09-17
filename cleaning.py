import json
import pandas as pd

# Load the JSON files
with open("/Users/alanlok/Desktop/SEM2/ProgrammingProject1/scrapers/data/travelnuity.json", "r") as f:
    travelnuity_data = json.load(f)

with open("/Users/alanlok/Desktop/SEM2/ProgrammingProject1/scrapers/data/yappack_events.json", "r") as f:
    yappack_events_data = json.load(f)

with open("/Users/alanlok/Desktop/SEM2/ProgrammingProject1/scrapers/data/yappack_parks.json", "r") as f:
    yappack_parks_data = json.load(f)

with open("/Users/alanlok/Desktop/SEM2/ProgrammingProject1/scrapers/data/stella_experiences.json", "r") as f:
    stella_experiences_data = json.load(f)

# Convert JSON to DataFrame
travelnuity_df = pd.DataFrame(travelnuity_data)
yappack_events_df = pd.DataFrame(yappack_events_data)
yappack_parks_df = pd.DataFrame(yappack_parks_data)
stella_experiences_df = pd.DataFrame(stella_experiences_data)

def identify_duplicates(df, name_col):
    
    # Check for duplicates based on the specified column
    duplicates = df[df.duplicated(subset=[name_col], keep=False)]
    return duplicates

duplicate_entries_travelnuity = identify_duplicates(travelnuity_df, 'location_name')
print("Duplicate Entries in Travelnuity Dataset:")
print(duplicate_entries_travelnuity)

duplicate_entries_yappack_events = identify_duplicates(yappack_events_df, 'title')
print("Duplicate Entries in Yappack Events Dataset:")
print(duplicate_entries_yappack_events)

duplicate_entries_yappack_parks = identify_duplicates(yappack_parks_df, 'name')
print("\nDuplicate Entries in Yappack Parks Dataset:")
print(duplicate_entries_yappack_parks)

duplicate_entries_stella_experiences = identify_duplicates(stella_experiences_df, 'title')
print("\nDuplicate Entries in Stella Experiences Dataset:")
print(duplicate_entries_stella_experiences)

# Function to remove duplicates
def remove_duplicates(df, col_name):
   # Remove duplicates, keeping the first occurrence
    unique_df = df.drop_duplicates(subset=[col_name], keep='first')
    return unique_df

# Remove duplicates from all four dataframes
cleaned_travelnuity = remove_duplicates(travelnuity_df, 'location_name')
cleaned_yappack_events = remove_duplicates(yappack_events_df, 'title')
cleaned_yappack_parks = remove_duplicates(yappack_parks_df, 'name')
cleaned_stella_experiences = remove_duplicates(stella_experiences_df, 'title')

# Save the cleaned data to new CSV files
cleaned_travelnuity.to_csv("cleaned_travelnuity.csv", index=False)
cleaned_yappack_events.to_csv("cleaned_yappack_events.csv", index=False)
cleaned_yappack_parks.to_csv("cleaned_yappack_parks.csv", index=False)
cleaned_stella_experiences.to_csv("cleaned_stella_experiences.csv", index=False)