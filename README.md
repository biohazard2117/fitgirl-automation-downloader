# Web Automation Downloader

This monorepo contains a web application that automates the process of downloading files from a list of URLs. Built using Next.js for the frontend and Python with Selenium for the backend automation, this tool hides the underlying complexity and provides a simple, user-friendly interface with real-time progress tracking.

## Features
- **Batch File Downloads**: Upload a list of URLs and automate the download process.
- **Retry Mechanism**: Automatically retries failed downloads after a delay.
- **Progress Tracking**: Displays real-time progress for each file.
- **Ad Blocker**: Automatically blocks ads during automation.
- **Browser Extensions**: Installs necessary extensions (e.g., IDM, AdBlock) automatically.
- **User-Friendly Interface**: Simplified frontend with a progress bar and status updates.

## Tech Stack
- **Frontend**: Next.js, TailwindCSS
- **Backend**: Python, Selenium, Flask (API)
- **Automation**: Selenium WebDriver with ChromeDriver

## Project Structure
```
web-automation-downloader/
├── apps/
│   ├── frontend/        # Next.js application
│   └── backend/         # Flask API and Selenium scripts
├── packages/
│   ├── shared/          # Shared utilities and constants
│   └── extensions/      # Browser extensions (e.g., AdBlock, IDM)
├── .gitignore           # Git ignore rules
├── LICENSE              # Open-source license
├── README.md            # Project documentation
└── package.json         # Monorepo dependencies
```

## Getting Started

### Prerequisites
- Node.js (v16 or later)
- Python (v3.8 or later)
- Google Chrome
- ChromeDriver (compatible with your Chrome version)

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/web-automation-downloader.git
   cd web-automation-downloader
   ```

2. Install dependencies:
   ```bash
   # Install frontend dependencies
   cd apps/frontend
   npm install

   # Install backend dependencies
   cd ../backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the .env file with your configuration
   ```

4. Run the application:
   ```bash
   # Start the backend
   cd apps/backend
   python app.py

   # Start the frontend
   cd ../frontend
   npm run dev
   ```

5. Access the application at `http://localhost:3000`.

## Contributing
Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This tool is intended for educational purposes only. Ensure compliance with the terms of service of the websites being automated. Use responsibly and ethically.
