# Fitgirl Automation Downloader

⚠️ Note: Currently only work for DataNodes links

## Overview
This project automates the downloading of files from a list of URLs using Selenium. It dynamically monitors downloads, handles errors, and prevents unwanted ads and popups. The user can select both the download folder and the file containing the list of URLs through a graphical interface.

## Features
- **Dynamic Download Folder Selection:** Allows users to choose their preferred download folder.
- **Batch Downloads with Monitoring:** Downloads files in batches and starts new batches as soon as earlier downloads are complete.
- **Retry Mechanism:** Automatically retries downloads in case of errors, restarting from the beginning.
- **Ad and Popup Blocker:** Closes unwanted tabs and blocks ads.
- **Dynamic URL Input:** Users can select a text file containing URLs to process.

## Requirements
- Python 3.x
- Google Chrome Browser
- ChromeDriver (matching the installed Chrome version)
- Required Python Libraries:
  - selenium
  - tkinter

## Installation
1. Clone this repository:
```
git clone https://github.com/stephan-rz/fitgirl-automation-downloader.git
```
2. Navigate to the project folder:
```
cd fitgirl-automation-downloader
```
3. Install the required libraries:
```
pip install selenium
```

## Usage
1. Run the script:
```
python downloader.py
```
2. Select the download folder when prompted.
3. Select the text file containing URLs (one per line).
4. The script will automatically process the URLs and handle downloads.

## Pre-Release Executable
- For users who do not want to install Python or dependencies, an **executable file** is available in the **Pre-Releases** section of this repository.
- Simply download the `.exe` file and run it directly.
- No additional setup is required. Just follow the prompts to select your download folder and input file.

## Notes
- Ensure **ChromeDriver** is compatible with your Chrome browser version.
- The text file containing URLs should list one URL per line.
- Downloads are automatically saved in the selected folder.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

