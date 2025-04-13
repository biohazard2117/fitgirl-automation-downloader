import os
import time
import logging

def wait_for_downloads_to_complete(download_path):
    logging.info("Waiting for all downloads to complete...")
    while True:
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload') or f.endswith('.part')]
        if not downloading_files:
            logging.info("All downloads completed.")
            break
        else:
            logging.info(f"Still downloading: {downloading_files}")
        time.sleep(5)

def monitor_downloads_and_continue(download_path):
    while True:
        downloading_files = [f for f in os.listdir(download_path) if f.endswith('.crdownload')]
        if len(downloading_files) <= 1:
            logging.info("Only one download remaining. Starting new batch...")
            break
        else:
            logging.info("Waiting until one download remains...")
        time.sleep(5)