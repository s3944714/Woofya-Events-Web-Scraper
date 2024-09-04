import requests
from bs4 import BeautifulSoup
import json

def fetch_html(url):
    """
    Fetches the HTML content of the given URL.
    
    :param url: URL of the webpage to fetch.
    :return: HTML content if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return None

def parse_stella_insurance_experiences(html_content):
    """
    Parses the HTML content from Stella Insurance to extract dog-friendly experiences details.
    
    :param html_content: HTML content of the webpage.
    :return: A list of dog-friendly experiences details.
    """
    experiences = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Print a portion of the HTML for debugging
        print("HTML snippet for debugging:")
        print(html_content[:2000])  # Print first 2000 characters
        
        # Find all experience containers
        experience_items = soup.find_all('h2', class_='wp-block-heading')
        
        for experience in experience_items:
            # Extract the title
            title = experience.get_text(strip=True)
            
            # Extract the description
            description_tag = experience.find_next('p')
            description = description_tag.get_text(strip=True) if description_tag else "No description found"
            
            # Extract the location
            location_tag = experience.find_next('a')
            location = location_tag.get_text(strip=True) if location_tag else "No location found"
            
            experiences.append({
                'title': title,
                'description': description,
                'location': location
            })
    
    except Exception as e:
        print(f"Error parsing HTML from Stella Insurance: {e}")
    
    return experiences

def save_to_json(data, filename):
    """
    Saves the list of data to a JSON file.
    
    :param data: List of data details.
    :param filename: Name of the JSON file to save, including directory path.
    """
    try:
        # Ensure the directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename} successfully.")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

def display_experiences(experiences):
    """
    Displays the list of dog-friendly experiences in the specified format.
    
    :param experiences: List of experience details.
    """
    for experience in experiences:
        print(f"Title: {experience['title']}")
        print(f"Description: {experience['description']}")
        print(f"Location: {experience['location']}")
        print("-" * 40)

def scrape_stella_insurance_experiences():
    url = 'https://www.stellainsurance.com.au/16-of-the-best-dog-friendly-experiences-in-australia/'
    
    print(f"Fetching HTML content from {url}...")
    html_content = fetch_html(url)
    
    if html_content:
        print("HTML content fetched successfully!\n")
        print("Parsing dog-friendly experiences from Stella Insurance...")
        experiences = parse_stella_insurance_experiences(html_content)
        
        if experiences:
            print(f"Found {len(experiences)} experiences:\n")
            display_experiences(experiences)
            
            # Save experiences to JSON file
            save_to_json(experiences, 'data/stella_experiences.json')
        else:
            print("No experiences found or an error occurred during parsing.")
    else:
        print("Failed to fetch HTML content.")

def main():
    print("Starting web scrapers...\n")
    
    # Scrape Stella Insurance experiences
    scrape_stella_insurance_experiences()
    
    print("\nAll scraping tasks completed.")

if __name__ == "__main__":
    main()
