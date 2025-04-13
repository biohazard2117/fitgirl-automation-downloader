import os
import time
import logging
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
log_file = "downloader.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Function to read URLs from a text file
def get_urls_from_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.askopenfilename(title="Select a text file with URLs", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return []

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    return urls

# Get URLs from the file
urls = get_urls_from_file()

# Display the URLs for clarification
if not urls:
    logging.error("No URLs provided. Exiting...")
    exit()

logging.info("URLs to process:")
for url in urls:
    logging.info(url)

# Prompt user to select download directory
root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

# Select and validate the download directory
download_path = filedialog.askdirectory(title="Select Download Folder")
if not download_path:
    logging.error("No download folder selected. Exiting...")
    exit()

# Normalize and validate download path
download_path = os.path.abspath(download_path)
if not os.path.exists(download_path):
    logging.error(f"Invalid download path: {download_path}. Exiting...")
    exit()

logging.info(f"Selected download path: {download_path}")

options = webdriver.EdgeOptions()
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

# Block popups, ads, and specific URLs
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

# Disable the Downloads Hub popup
options.add_argument("--disable-features=msDownloadsHub")

# Block specific URLs by enabling DevTools Protocol commands
options.add_argument("--remote-debugging-port=9222")

# Initialize WebDriver
driver = webdriver.Edge(options=options)

# def close_unwanted_tabs():
#     while len(driver.window_handles) > 1:
#         for handle in driver.window_handles:
#             logging.info(f"List of all the windows currently open before closing: {handle}")
#         driver.switch_to.window(driver.window_handles[-1])
#         if "https://fuckingfast.co/" not in driver.current_url:
#             driver.close()
#         driver.switch_to.window(driver.window_handles[0])

def close_unwanted_tabs():
    """
    Close all tabs except the one with the desired URL.
    """
    try:
        logging.info("Starting to close unwanted tabs...")
        # Get the current list of open tabs
        open_tabs = driver.window_handles
        logging.info(f"Currently open tabs: {open_tabs}")

        # Iterate through all open tabs
        for handle in open_tabs:
            driver.switch_to.window(handle)
            current_url = driver.current_url
            logging.info(f"Checking tab with URL: {current_url}")
            
            # Ignore Edge internal tabs (e.g., edge://downloads/hub)
            if current_url.startswith("edge://"):
                logging.info(f"Ignoring Edge internal tab with URL: {current_url}")
                continue

            # Close the tab if it doesn't match the desired URL
            if "https://fuckingfast.co/" not in current_url:
                logging.info(f"Closing tab with URL: {current_url}")
                driver.close()

        # Switch back to the first remaining tab
        remaining_tabs = driver.window_handles
        if remaining_tabs:
            driver.switch_to.window(remaining_tabs[0])
            logging.info(f"Switched to remaining tab: {driver.current_url}")
        else:
            logging.warning("No tabs remaining after closing unwanted tabs.")

    except Exception as e:
        logging.error(f"Error while closing unwanted tabs: {e}")

def wait_for_downloads_to_complete(download_path):
    logging.info("Waiting for all downloads to complete...")
    while True:
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload') or f.endswith('.part')]
        if not downloading_files:  # No more temporary download files
            logging.info("All downloads completed.")
            break
        else:
            logging.info(f"Still downloading: {downloading_files}")
        time.sleep(5)

def monitor_downloads_and_continue():
    while True:
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload')]
        if len(downloading_files) <= 1:  # If only one file is downloading, start the next batch
            logging.info("Only one download remaining. Starting new batch...")
            break
        else:
            logging.info("Waiting until one download remains...")
        time.sleep(5)

def retry_on_error_with_restart(url, retries=3, wait_time=10):
    for i in range(retries):
        try:
            logging.info(f"Tabs before navigation: {len(driver.window_handles)}")
            driver.get(url)
            logging.info(f"Tabs after navigation: {len(driver.window_handles)}")
            # logging.info("Closing unwanted tabs 1st time...")
            # close_unwanted_tabs()  # Close any unwanted tabs
            logging.info(f"Retrying URL: {url}, Attempt {i+1}")

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'link-button') and contains(text(), 'DOWNLOAD')]"))
            ).click()
            
            logging.info("Clicked 'Download' button.")
            logging.info("Waiting for 7 seconds after clicking download first time...")
            time.sleep(7)
            
            # Close unwanted tabs
            logging.info("Closing unwanted tabs...")
            close_unwanted_tabs()
            
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

# Counter to track progress
file_counter = 0

# Process each URL
for url in urls:
    try:
        if not retry_on_error_with_restart(url):
            logging.error(f"Failed to process URL after retries: {url}")
            continue

        file_counter += 1

        if file_counter % 3 == 0:
            logging.info("Monitoring downloads before starting new batch...")
            monitor_downloads_and_continue()

    except Exception as e:
        logging.error(f"Unexpected error for URL {url}: {e}")
    finally:
        logging.info(f"Finished processing URL: {url}")

# Wait for all downloads to complete before closing the browser
wait_for_downloads_to_complete(download_path)

# Close the browser after processing all URLs
driver.quit()
logging.info("Browser closed. All tasks completed.")