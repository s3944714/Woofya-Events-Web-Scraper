import subprocess
import os

# Define the path to the Scrapers directory
SCRAPER_PATH = os.path.join(os.getcwd(), 'Scrapers')

# List of all scraper files in the order you want to run them
scraper_files = [
    "Humantix.py",
    "HumantixPets.py",
    "eventbrite.py",
    "pupsy.py",
    "southAustralia.py",
    "visitNSW.py",
    "visitNSW_Hikes.py",
    "visitNSW_Phase2.py",
    "yappack.py"
]

def run_scraper(file_name):
    """
    Executes a single scraper script using subprocess.
    
    Args:
        file_name (str): The name of the scraper file to be executed.
    """
    file_path = os.path.join(SCRAPER_PATH, file_name)
    print(f"Running {file_name}...")
    try:
        # Run the scraper script
        subprocess.run(['python', file_path], check=True)
        print(f"{file_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {file_name}: {e}\n")

if __name__ == "__main__":
    print("Starting all scrapers...\n")

    # Run each scraper in the Scrapers directory
    for scraper in scraper_files:
        run_scraper(scraper)

    print("All scrapers have been executed.")
