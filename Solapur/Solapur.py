import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, unquote

def get_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    filename = unquote(filename)
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    return filename

def download_file(url, folder):
    filename = get_filename_from_url(url)
    filepath = os.path.join(folder, filename)
    print(f"Downloading {url} as {filename}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded: {filepath}")

def main():
    output_folder = r"C:\Onkar\Swapnil\Election maps\Solapur"
    os.makedirs(output_folder, exist_ok=True)

    options = Options()
    # Uncomment below line to run browser headless
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://www.solapurcorporation.gov.in/smc/election_details_marathi"
        print(f"Opening URL: {url}")
        driver.get(url)

        driver.implicitly_wait(5)

        # Find all <a> elements with href containing .pdf inside the GridView1 table
        links_xpath = '//*[@id="ContentPlaceHolder1_GridView1"]//a[contains(@href, ".pdf")]'
        links = driver.find_elements(By.XPATH, links_xpath)
        print(f"Found {len(links)} PDF links")

        for link in links:
            file_url = link.get_attribute("href")
            if file_url and file_url.endswith(".pdf"):
                download_file(file_url, output_folder)

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
