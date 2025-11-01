import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Your Google API key here (must have Drive API enabled)
API_KEY = "YOUR_GOOGLE_API_KEY"

URL = "https://www.umc.gov.in/general-election"
XPATH = '//*[@id="collapse0"]/div/div/table/tbody/tr/td[3]/a'
SAVE_FOLDER = r"C:\Onkar\Swapnil\Election maps\UMC"

def get_filename_from_drive(file_id):
    """Get the real file name from Google Drive API."""
    api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name&key={API_KEY}"
    resp = requests.get(api_url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("name")
    else:
        print(f"Failed to get filename for {file_id}, status: {resp.status_code}")
        return None

def download_file_from_gdrive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"Opening URL: {URL}")
    driver.get(URL)
    time.sleep(3)

    links = driver.find_elements(By.XPATH, XPATH)

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    print(f"Found {len(links)} links")

    for link in links:
        href = link.get_attribute('href')
        if not href:
            continue

        file_id = None
        if "drive.google.com/file/d/" in href:
            try:
                file_id = href.split("/d/")[1].split("/")[0]
            except IndexError:
                pass
        
        if not file_id:
            print(f"Could not extract file ID from link: {href}")
            continue

        filename = get_filename_from_drive(file_id)
        if not filename:
            # fallback to file_id.pdf if cannot get real name
            filename = f"{file_id}.pdf"

        save_path = os.path.join(SAVE_FOLDER, filename)

        if os.path.exists(save_path):
            print(f"File already exists, skipping: {filename}")
            continue

        print(f"Downloading {filename} ...")
        try:
            download_file_from_gdrive(file_id, save_path)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
