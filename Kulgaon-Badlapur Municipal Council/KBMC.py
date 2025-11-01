import os
import requests
import time
from urllib.parse import urljoin, urlparse, unquote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    filename = unquote(filename)
    if not filename:
        filename = "downloaded_file"
    return filename

def download_file(url, folder):
    os.makedirs(folder, exist_ok=True)
    filename = get_filename_from_url(url)
    dest = os.path.join(folder, filename)
    if os.path.exists(dest):
        print(f"Already exists: {filename}")
        return
    print(f"Downloading: {url} → {filename}")
    resp = requests.get(url, stream=True)
    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"  Failed = HTTP {resp.status_code} : {url}")
        return
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)
    print(f"  Saved: {dest}")

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
        time.sleep(5)  # allow things to load

        # Try the specific XPATH you gave
        xpath_primary = '//*[@id="main-content"]/section/div/div/div/div/div[1]/div/div/div/div[2]/a'
        link_elems = driver.find_elements(By.XPATH, xpath_primary)
        print(f"Primary XPath found {len(link_elems)} link(s)")

        # Also include a broader fallback to catch **all** PDF links
        fallback = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')
        print(f"Fallback found {len(fallback)} PDF link(s) in total")

        # Combine unique hrefs
        urls = set()
        for a in link_elems + fallback:
            href = a.get_attribute("href")
            if href:
                full = urljoin(target_url, href)
                if full.lower().endswith(".pdf"):
                    urls.add(full)

        print(f"Total unique PDF file URLs to download: {len(urls)}")

        for u in urls:
            download_file(u, output_folder)

    finally:
        driver.quit()
        print("Done.")

if __name__ == "__main__":
    main()
