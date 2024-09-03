from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_number_of_pages (url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for efficiency
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        driver.implicitly_wait(10)  # Wait for elements to load

        # Try to find the pagination element
        try:
            pagination_element = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="pagination-parent"]')
            pagination_text = pagination_element.text
            print(f"Pagination text: {pagination_text}")  # Debugging output

            # Extract total pages from text
            total_pages = pagination_text.split(' of ')[-1]
            return int(total_pages)
        except Exception as e:
            print(f"Pagination element not found or error occurred: {e}")
            return None

    finally:
        driver.quit()

# Example usage
url = 'https://www.eventbrite.com.au/d/australia/dog/'
number_of_pages = get_number_of_pages(url)
if number_of_pages is not None:
    print(f"Number of pages: {number_of_pages}")
else:
    print("Failed to retrieve number of pages.")
