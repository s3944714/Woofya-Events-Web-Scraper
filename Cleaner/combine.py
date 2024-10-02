import os
import json

def combine_json_files(input_dir, output_file):
    combined_data = []

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):  # Check for JSON files only
            file_path = os.path.join(input_dir, filename)
            
            # Read each JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        combined_data.extend(data)  # Append data if it's a list
                    else:
                        combined_data.append(data)  # Append the whole object if not a list
                except json.JSONDecodeError as e:
                    print(f"Error loading {filename}: {e}")
    
    # Construct the output file path in the SQL directory
    output_file_path = os.path.join(os.path.dirname(input_dir), 'SQL', output_file)

    # Write the combined data to a single JSON file in the SQL directory
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(combined_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"Combined JSON data written to {output_file_path}")

# Set the input directory to the absolute path of Raw_Data
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
input_directory = os.path.join(current_dir, '..', 'Raw_Data')  # Correctly construct the path to Raw_Data
output_file = 'combined_data.json'  # Output file name

combine_json_files(input_directory, output_file)
