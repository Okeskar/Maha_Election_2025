import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIG ---
DOWNLOAD_FOLDER = r"C:\Onkar\Swapnil\Election maps\Ichalkaranji"
MAIN_URL = "https://ichalkaranjimnp.in/प्रभागनिहाय-नकाशा-७-ते-११/"
TABLE_BUTTON_XPATH = "//a[contains(text(),'View Table') or contains(text(),'View PDFs')]"  # adjust if needed

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# --- START SELENIUM ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run without opening browser window
driver = webdriver.Chrome(options=options)

try:
    # Open main page
    driver.get(MAIN_URL)
    print("Opened main page...")

    # Wait for table link/button and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, TABLE_BUTTON_XPATH))
    ).click()
    print("Opened table page...")

    # Wait for table to load
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.tablepress"))
    )

    # --- SCRAPE PDF LINKS AND NAMES ---
    pdf_rows = table.find_elements(By.XPATH, ".//tr")[1:]  # skip header
    pdf_data = []

    for row in pdf_rows:
        try:
            link = row.find_element(By.XPATH, ".//td[3]/a")
            url = link.get_attribute("href")
            name = link.text.strip()
            # sanitize filename
            safe_name = "".join(c if c.isalnum() or c in " -_." else "_" for c in name)
            if not safe_name.lower().endswith(".pdf"):
                safe_name += ".pdf"
            pdf_data.append((url, safe_name))
        except:
            continue

    print(f"Found {len(pdf_data)} PDFs in the table. Downloading...")

    # --- DOWNLOAD PDFs ---
    for url, name in pdf_data:
        local_path = os.path.join(DOWNLOAD_FOLDER, name)
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(r.content)
            print(f"Downloaded: {local_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

finally:
    driver.quit()
    print("Selenium driver closed.")
