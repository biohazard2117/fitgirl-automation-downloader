from selenium import webdriver
import logging

def initialize_driver(download_path):
    options = webdriver.EdgeOptions()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_argument("--disable-features=msDownloadsHub")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Edge(options=options)
    return driver

def close_unwanted_tabs(driver):
    try:
        logging.info("Starting to close unwanted tabs...")
        open_tabs = driver.window_handles
        logging.info(f"Currently open tabs: {open_tabs}")

        for handle in open_tabs:
            driver.switch_to.window(handle)
            current_url = driver.current_url
            logging.info(f"Checking tab with URL: {current_url}")

            if current_url.startswith("edge://"):
                logging.info(f"Ignoring Edge internal tab with URL: {current_url}")
                continue

            if "https://fuckingfast.co/" not in current_url:
                logging.info(f"Closing tab with URL: {current_url}")
                driver.close()

        remaining_tabs = driver.window_handles
        if remaining_tabs:
            driver.switch_to.window(remaining_tabs[0])
            logging.info(f"Switched to remaining tab: {driver.current_url}")
        else:
            logging.warning("No tabs remaining after closing unwanted tabs.")

    except Exception as e:
        logging.error(f"Error while closing unwanted tabs: {e}")