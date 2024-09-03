from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import TotalPageFinder

def gather_event_urls_with_selenium(base_url):
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_event_urls = []
    max_pages = TotalPageFinder.get_number_of_pages_selenium(base_url)
    try:
        for page in range(1, max_pages + 1):
            # Open the URL for the current page
            page_url = f"{base_url}?page={page}"
            driver.get(page_url)

            # Wait until the events container is present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.search-results-panel-content__events'))
            )

            # Get all event elements on the current page
            event_elements = driver.find_elements(By.CSS_SELECTOR, 'div.search-results-panel-content__events a.event-card-link')

            for event in event_elements:
                href = event.get_attribute('href')
                if href:
                    all_event_urls.append(href)

            print(f"Page {page} scraped. Found {len(event_elements)} events.")

    finally:
        driver.quit()

    # Remove duplicates
    all_event_urls = list(set(all_event_urls))

    return all_event_urls

# Example usage
url = 'https://www.eventbrite.com.au/d/australia/dog/'
event_urls = gather_event_urls_with_selenium(url)
print(f"Collected {len(event_urls)} event URLs.")
for u in event_urls:
    print(u)
