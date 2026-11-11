# Fake Internship & Course Scam Detector

## Features
- Scans internship text for scam indicators (urgent hiring, registration fees, free domains, unrealistic salary).
- Provides a clean, modern UI in the browser extension.

## 1. Run the Backend API
The backend requires Python and Flask to analyze the text.

1. Open a terminal and navigate to the `backend` folder:
   `cd d:\Harshit\FakeInternshipDetector\backend`

2. (Optional) Create and activate a virtual environment:
   `python -m venv venv`
   `.\venv\Scripts\Activate.ps1`

3. Install dependencies:
   `pip install -r requirements.txt`

4. Run the Flask server:
   `python app.py`
   The backend will start at `http://127.0.0.1:5000`. Keep this terminal window open.

## 2. Install the Browser Extension
1. Open your Chromium-based browser (Chrome, Edge, Brave, etc.).
2. Go to `chrome://extensions/` (or `edge://extensions/`).
3. Enable **Developer mode** (usually a toggle in the top right corner).
4. Click **Load unpacked** and select the `d:\Harshit\FakeInternshipDetector\extension` folder.
5. The Scam Detector extension will be added to your browser. You can pin it for quick access!

## Usage
- Click on the extension icon.
- Paste any suspicious internship offer text.
- Click **Analyze Offer**.
- Get instant feedback on whether the offer looks Safe, Suspicious, or like a Scam.
