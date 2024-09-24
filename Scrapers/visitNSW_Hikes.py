import os
import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://www.visitnsw.com/articles/dog-friendly-hikes-and-walks-in-nsw"

# Send a GET request to fetch the HTML content of the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store all hike data
    hikes_list = []

    # Find all hike sections (h2 tags that include hike titles and p tags for details)
    hike_sections = soup.find_all('h2')

    for section in hike_sections:
        try:
            # Extract the title of the hike (inside <h2> tag with a link <a>)
            title_tag = section.find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = "https://www.visitnsw.com" + title_tag['href']  # Full link
            else:
                continue  # Skip this iteration if no title is found

            # Initialize description and details
            description = ""
            distance = "N/A"
            time = "N/A"
            leash_policy = "N/A"
            
            # Find the next <p> tags containing description, distance, time, and leash policy
            current_p_tag = section.find_next_sibling('p')
            while current_p_tag and current_p_tag.name == 'p':
                # Extract distance, time, leash policy from <strong> tags
                strong_tag = current_p_tag.find('strong')
                if strong_tag:
                    strong_text = strong_tag.text.lower()
                    if 'distance' in strong_text:
                        distance = current_p_tag.text.replace("Distance:", "").strip()
                    elif 'time' in strong_text:
                        time = current_p_tag.text.replace("Time:", "").strip()
                    elif 'on-leash' in strong_text:
                        leash_policy = current_p_tag.text.replace("On-leash?", "").strip()
                else:
                    # Accumulate the general description from the paragraph
                    description += current_p_tag.text.strip() + " "
                
                # Move to the next <p> tag
                current_p_tag = current_p_tag.find_next_sibling('p')

            # Only append if a title is present and at least one description or detail is found
            hike_data = {
                'title': title,
                'link': link,
                'description': description.strip(),
                'distance': distance.strip(),
                'time': time.strip(),
                'leash_policy': leash_policy.strip()
            }

            # Append the hike data to the list
            hikes_list.append(hike_data)

        except Exception as e:
            print(f"Error while parsing hike: {e}")

    # Specify the output directory and file name
    output_directory = os.path.join('Data')  # Output folder
    output_file = os.path.join(output_directory, 'VisitNSW_Hikes.json')

    # Ensure the directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save the hike data to the JSON file
    with open(output_file, 'w') as f:
        json.dump(hikes_list, f, indent=4)

    print(f"All hikes data saved to {output_file}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
