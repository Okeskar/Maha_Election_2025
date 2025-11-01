import os
import re
import time
import requests
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def sanitize_filename(name):
    # Clean filename for Windows
    name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    if not name:
        name = "downloaded_file"
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return name

def download_file(url, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        print(f"Already exists: {filename}")
        return
    print(f"Downloading: {url} → {filename}")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    target_url = "https://www.mbmc.gov.in/en/mbmc/final-ward-wise-map-1-to-24"
    output_folder = r"C:\Onkar\Swapnil\Election maps\Mira Bhayandar\file"  # Update if needed

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Opening page: {target_url}")
        driver.get(target_url)
        time.sleep(5)

        # Get all content blocks under the main container
        blocks = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[2]/div/div')
        print(f"Found {len(blocks)} blocks")

        for block in blocks:
            try:
                # Get label and link inside the block
                label_elem = block.find_element(By.XPATH, './/span[2]')
                label_text = label_elem.text.strip()
                filename = sanitize_filename(label_text)

                link_elem = label_elem.find_element(By.XPATH, './a')
                href = link_elem.get_attribute("href")
                if href and href.lower().endswith(".pdf"):
                    full_url = urljoin(target_url, href)
                    download_file(full_url, output_folder, filename)
                else:
                    print(f"No valid PDF link for: {label_text}")

            except Exception as e:
                print(f"Error processing block: {e}")
                continue

    finally:
        driver.quit()
        print("Done.")

if __name__ == "__main__":
    main()
