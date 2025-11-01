import os
import requests
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def sanitize_filename(name):
    # Removes or replaces characters not allowed in filenames
    return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in name).strip()

def download_file(url, folder, filename=None):
    os.makedirs(folder, exist_ok=True)

    if not filename:
        filename = os.path.basename(url.split("?")[0])
    else:
        filename = sanitize_filename(filename)
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

    dest = os.path.join(folder, filename)
    if os.path.exists(dest):
        print(f"Already exists: {filename}")
        return

    print(f"Downloading: {url} → {filename}")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()

        with open(dest, "wb") as f:
            for chunk in resp.iter_content(8192):
                if chunk:
                    f.write(chunk)

        print(f"  Saved: {dest}")
    except Exception as e:
        print(f"  Failed to download {url}: {e}")

def main():
    target_url = "https://kbmc.gov.in/election"
    output_folder = r"C:\Onkar\Swapnil\Election maps\Kulgaon-Badlapur Municipal Council\file"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Opening page: {target_url}")
        driver.get(target_url)
        time.sleep(5)  # wait for page to fully load

        # Get all content blocks that might contain an h6 + PDF link
        blocks = driver.find_elements(By.XPATH, '//*[@id="main-content"]/section/div/div/div/div/div/div/div/div')
        print(f"Found {len(blocks)} content blocks")

        for block in blocks:
            try:
                # Try to extract visible file name
                label_elem = block.find_element(By.XPATH, './h6')
                label = label_elem.text.strip()
                filename = sanitize_filename(label)

                # Try to find PDF link
                link_elem = block.find_element(By.XPATH, './/a[contains(@href, ".pdf")]')
                href = link_elem.get_attribute("href")

                if href:
                    full_url = urljoin(target_url, href)
                    download_file(full_url, output_folder, filename)

            except Exception as e:
                print(f"Skipping block due to error: {e}")
                continue

    finally:
        driver.quit()
        print("Done.")

if __name__ == "__main__":
    main()
