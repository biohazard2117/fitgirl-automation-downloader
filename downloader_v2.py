import os
import time
import logging
from utils.browser_utils import initialize_driver, close_unwanted_tabs
from utils.file_utils import get_urls_from_file, select_download_directory
from utils.download_utils import wait_for_downloads_to_complete, monitor_downloads_and_continue
from utils.logging_utils import configure_logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Configure logging
configure_logging()

# Get URLs from the file
urls = get_urls_from_file()
if not urls:
    logging.error("No URLs provided. Exiting...")
    exit()

# Select and validate the download directory
download_path = select_download_directory()
if not download_path:
    logging.error("No download folder selected. Exiting...")
    exit()

# Initialize WebDriver
driver = initialize_driver(download_path)

def retry_on_error_with_restart(url, retries=3, wait_time=10):
    for i in range(retries):
        try:
            driver.get(url)
            logging.info(f"Retrying URL: {url}, Attempt {i+1}")

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'link-button') and contains(text(), 'DOWNLOAD')]"))
            ).click()
            
            logging.info("Clicked 'Download' button.")
            logging.info("Waiting for 7 seconds...")
            time.sleep(7)
            
            # Close unwanted tabs
            close_unwanted_tabs(driver)
            
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'link-button') and contains(text(), 'DOWNLOAD')]"))
            ).click()
            time.sleep(7)
            return True

        except Exception as e:
            logging.error(f"Attempt {i+1} failed for URL: {url}. Retrying in {wait_time} seconds...")
            logging.error(f"Error: {e}")
            time.sleep(wait_time)
    return False

# Process each URL
file_counter = 0
for url in urls:
    try:
        if not retry_on_error_with_restart(url):
            logging.error(f"Failed to process URL after retries: {url}")
            continue

        file_counter += 1

        if file_counter % 3 == 0:
            logging.info("Monitoring downloads before starting new batch...")
            monitor_downloads_and_continue(download_path)

    except Exception as e:
        logging.error(f"Unexpected error for URL {url}: {e}")
    finally:
        logging.info(f"Finished processing URL: {url}")

# Wait for all downloads to complete before closing the browser
wait_for_downloads_to_complete(download_path)

# Close the browser after processing all URLs
driver.quit()
logging.info("Browser closed. All tasks completed.")