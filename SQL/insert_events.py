import json
import pyodbc
import os

def insert_data_into_db(json_file, connection_string):
    """
    Inserts data from a JSON file into the events table in the SQL Server database.
    
    Parameters:
    - json_file: Path to the JSON file to be inserted.
    - connection_string: The connection string to connect to the SQL Server database.
    """
    # Print the current working directory for debugging
    print(f"Current Working Directory: {os.getcwd()}")

    # Step 1: Read the JSON data from the file
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            events = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the JSON file path is correct.")
        return

    # Step 2: Establish a connection to the SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Step 3: Insert each event into the events table
    for event in events:
        title = event.get('title', '')
        location = event.get('location', '')
        description = event.get('description', '')

        # Check if the features field is a list before joining
        features = event.get('features', [])
        if not isinstance(features, list):
            features = [features] if isinstance(features, str) else []  # Convert string to list, or use empty list
        features = ', '.join(features)  # Convert features list to comma-separated string

        date_range = event.get('date_range', '')
        link = event.get('link', '')

        # Execute the insert command
        cursor.execute("""
            INSERT INTO events (title, location, description, features, date_range, link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, title, location, description, features, date_range, link)

    # Step 4: Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Data successfully inserted into the database.")

# Define the connection string for your SQL Server
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-9UFQHR5\\WOOFYASERVER;"  # Update with your server name
    "Database=events_db;"                     # Update with your database name
    "Trusted_Connection=yes;"                 # Use Windows Authentication (no username and password required)
)

# Use the absolute path for the cleaned JSON file
current_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's current directory
json_file = os.path.join(current_directory, "../SQL/cleaned_combined_data.json")  # Updated file path

# Run the script to insert data
insert_data_into_db(json_file, connection_string)
