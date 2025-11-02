from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import requests

# -------------------------------
# Configuration
# -------------------------------
PORTAL_URL = "https://amc.gov.in/en/election/"
DOWNLOAD_DIR = r"C:\Onkar\AMC_Election"  # base folder to save PDFs
WAIT_TIME = 5  # seconds to wait for page load

# -------------------------------
# Setup Chrome driver
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # optional: run browser in background
chrome_options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(PORTAL_URL)
time.sleep(WAIT_TIME)  # wait for page to load

# -------------------------------
# Step 1: Get all rows in the table
# -------------------------------
rows = driver.find_elements(By.XPATH, '//*[@id="tablepress-106"]/tbody/tr')
print(f"Found {len(rows)} rows in the table.")

# -------------------------------
# Step 2: Loop through each row and download PDF
# -------------------------------
for idx, row in enumerate(rows, start=1):
    try:
        # Get category/date from 2nd column
        category = row.find_element(By.XPATH, './td[2]').text.strip()
        if not category:
            category = "General"

        # Get link from 3rd column
        link_elem = row.find_element(By.XPATH, './td[3]/a')
        file_url = link_elem.get_attribute("href")
        file_name = link_elem.text.strip()

        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"

        # Append row index to ensure unique filename
        file_name_unique = f"{idx}_{file_name}"

        # Prepare folder path
        folder_path = os.path.join(DOWNLOAD_DIR, category)
        os.makedirs(folder_path, exist_ok=True)

        save_path = os.path.join(folder_path, file_name_unique)

        # Download file using requests
        print(f"Downloading: {file_name_unique} ...")
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved: {save_path}")
        else:
            print(f"❌ Failed to download {file_name_unique}, status code: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Row {idx} skipped due to error: {e}")

driver.quit()
print("✅ All files downloaded successfully!")
