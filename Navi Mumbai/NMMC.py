import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import quote

# -----------------------------
# Configuration
# -----------------------------
BASE_URL = "http://nmmc.gov.in/other-info/resources/nmmc-elections"
DOWNLOAD_FOLDER = r"C:\Onkar\Swapnil\Election maps\NMMC\PDFs"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Fetch the page
# -----------------------------
response = requests.get(BASE_URL)
response.raise_for_status()  # fail if page not loaded
html = response.text

soup = BeautifulSoup(html, "html.parser")

# -----------------------------
# Extract PDF paths
# -----------------------------
pdf_urls = []

# look for Angular 'ng-click' containing the filePath
for el in soup.select("[ng-click^='openFile']"):
    try:
        ng_click_value = el["ng-click"]
        # extract file path from openFile('...') string
        file_path = ng_click_value.split("'")[1]
        pdf_url = "https://app.nmmconline.in/backend/common/api/file/preview?filePath=" + quote(file_path)
        pdf_urls.append(pdf_url)
    except Exception as e:
        print("⚠️ Could not parse element:", e)
        continue

print(f"Found {len(pdf_urls)} PDFs.")

# -----------------------------
# Download PDFs
# -----------------------------
for i, pdf_url in enumerate(pdf_urls, start=1):
    try:
        file_name = os.path.basename(pdf_url.split("filePath=")[1])
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        
        # skip if already downloaded
        if os.path.exists(file_path):
            print(f"[{i}] Already downloaded: {file_name}")
            continue

        print(f"[{i}] Downloading: {file_name}")
        pdf_data = requests.get(pdf_url).content
        with open(file_path, "wb") as f:
            f.write(pdf_data)
    except Exception as e:
        print(f"⚠️ Row {i} error: {e}")

print("\n✅ All PDFs downloaded!")
