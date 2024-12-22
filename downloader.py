import os
import time
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    print("No URLs provided. Exiting...")
    driver.quit()
    exit()

print("URLs to process:")
for url in urls:
    print(url)

# Prompt user to select download directory
root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

# Select and validate the download directory
download_path = filedialog.askdirectory(title="Select Download Folder")
if not download_path:
    print("No download folder selected. Exiting...")
    exit()

# Normalize and validate download path
download_path = os.path.abspath(download_path)
if not os.path.exists(download_path):
    print(f"Invalid download path: {download_path}. Exiting...")
    exit()

print(f"Selected download path: {download_path}")

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

# Block popups, ads, and specific URLs
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

# Block specific URLs by enabling DevTools Protocol commands
options.add_argument("--remote-debugging-port=9222")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Block unwanted tabs and ads function
def close_unwanted_tabs():
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        if "https://loadingfreerar.top/two/" in driver.current_url:
            driver.close()
        driver.switch_to.window(driver.window_handles[0])


# Monitor downloads and start new batch if only one download remains
def monitor_downloads_and_continue():
    while True:
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload')]
        if len(downloading_files) <= 1:  # If only one file is downloading, start the next batch
            print("Only one download remaining. Starting new batch...")
            break
        else:
            print("Waiting until one download remains...")
        time.sleep(5)


# Retry logic for download steps with full restart
def retry_on_error_with_restart(url, retries=3, wait_time=10):
    for i in range(retries):
        try:
            driver.get(url)
            close_unwanted_tabs()  # Close any unwanted tabs
            print(f"Retrying URL: {url}, Attempt {i+1}")

            # Step 1: Click "Continue to Download" button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "method_free"))).click()
            close_unwanted_tabs()
            print("Clicked 'Continue to Download' button.")

            # Step 2: Wait for the "Download" button to appear
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-blue-600') and contains(text(), 'Download')]"))).click()
            close_unwanted_tabs()
            print("Clicked 'Download' button.")

            # Step 3: Wait for 7 seconds (avoiding intermediate loading time)
            print("Waiting for 7 seconds...")
            time.sleep(7)

            # Step 4: Click the "Continue" button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-blue-600') and contains(text(), 'Continue')]"))).click()
            close_unwanted_tabs()
            print("Clicked 'Continue' button. Download started.")
            return True

        except Exception as e:
            print(f"Attempt {i+1} failed for URL: {url}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    return False


# Counter to track progress
file_counter = 0

# Process each URL
for url in urls:
    try:
        # Retry entire process if errors occur
        if not retry_on_error_with_restart(url):
            print(f"Failed to process URL after retries: {url}")
            continue

        # Increment file counter
        file_counter += 1

        # Monitor downloads and start new batch if only one remains
        if file_counter % 3 == 0:
            print("Monitoring downloads before starting new batch...")
            monitor_downloads_and_continue()

    except Exception as e:
        print(f"Unexpected error for URL {url}: {e}")
    finally:
        print(f"Finished processing URL: {url}")


# Close the browser after processing all URLs
driver.quit()