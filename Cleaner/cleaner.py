import os
import pandas as pd
import re
import json
from datetime import datetime

# Define paths for input and output files relative to the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(current_dir, "../SQL/combined_data.json")
output_file_path = os.path.join(current_dir, "../SQL/cleaned_combined_data.json")

def load_json_file(file_path):
    """
    Loads a JSON file into a pandas DataFrame.
    Parameters:
        file_path (str): The file path to the JSON file.
    Returns:
        DataFrame: DataFrame with the loaded data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def save_to_json(df, output_file_path):
    """
    Saves a DataFrame as a JSON file.
    Parameters:
        df (DataFrame): DataFrame to be saved.
        output_file_path (str): Path to save the output JSON file.
    """
    df.to_json(output_file_path, orient='records', indent=4)
    print(f"Data has been cleaned and saved to {output_file_path}")

def remove_duplicates(df):
    """
    Removes duplicate entries based on event name and date.
    Parameters:
        df (DataFrame): The input DataFrame with event details.
    Returns:
        DataFrame: DataFrame with duplicates removed.
    """
    # If date is not present, create an empty column
    if 'date' not in df.columns:
        df['date'] = ''
    
    # Remove duplicates based on 'title' and 'date'
    df_unique = df.drop_duplicates(subset=['title', 'date'], keep='first')
    return df_unique

def standardize_date_format(date_str):
    """
    Standardizes the date format to ISO 8601 (YYYY-MM-DD).
    Parameters:
        date_str (str): Input date string.
    Returns:
        str: Standardized date string in 'YYYY-MM-DD' format or original if not recognized.
    """
    if not isinstance(date_str, str):
        return None  # Return None if the input is not a string
    
    # Define common date formats
    date_formats = [
        "%a, %d %b %Y", "%a, %d %b, %Y", "%d %b %Y", "%b %d, %Y",
        "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%m-%d-%Y",
        "%A, %d %B %Y", "%A, %B %d, %Y"
    ]

    for date_format in date_formats:
        try:
            # Attempt to parse and convert to standardized format
            standardized_date = datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
            return standardized_date
        except ValueError:
            continue
    return date_str  # Return original string if no format matches

def validate_schema(df, required_columns=['title', 'location']):
    """
    Validates the transformed data against the schema.
    Parameters:
        df (DataFrame): The DataFrame with event details.
        required_columns (list): List of required columns for validation.
    Returns:
        bool: True if the schema is valid, False otherwise.
    """
    # Check if all required columns are present
    for column in required_columns:
        if column not in df.columns:
            print(f"Missing required column: {column}")
            return False
    return True

def display_entry_count(original_df, cleaned_df):
    """
    Displays the number of entries in the original and cleaned JSON files.
    Parameters:
        original_df (DataFrame): The original DataFrame loaded from the JSON file.
        cleaned_df (DataFrame): The cleaned DataFrame after transformations.
    """
    original_count = len(original_df)
    cleaned_count = len(cleaned_df)
    print(f"Number of entries in the original JSON file: {original_count}")
    print(f"Number of entries in the cleaned JSON file: {cleaned_count}")

# Main function to clean the data
def clean_event_data(file_path, output_file_path):
    """
    Main function to clean the event data from a JSON file and save the cleaned version.
    1. Loads the JSON file into a DataFrame.
    2. Removes duplicate entries.
    3. Standardizes date formats.
    4. Validates the schema.
    5. Saves the cleaned data to a new JSON file.
    
    Parameters:
        file_path (str): Path to the input JSON file.
        output_file_path (str): Path to save the cleaned JSON file.
    """
    # Step 1: Load the JSON file
    df = load_json_file(file_path)

    # Step 2: Remove duplicates based on title and date
    df_cleaned = remove_duplicates(df)

    # Step 3: Standardize date formats
    if 'date' in df_cleaned.columns:
        df_cleaned['date'] = df_cleaned['date'].apply(standardize_date_format)

    # Step 4: Validate the transformed data against the schema
    if validate_schema(df_cleaned):
        # Step 5: Save the cleaned data to a new JSON file
        save_to_json(df_cleaned, output_file_path)
        
        # Display the number of entries before and after cleaning
        display_entry_count(df, df_cleaned)
    else:
        print("Schema validation failed. Please review the input data.")

# Run the cleaning process to create the cleaned JSON file inside SQL folder
clean_event_data(input_file_path, output_file_path)
