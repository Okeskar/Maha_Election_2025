from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time
import requests
from urllib.parse import urljoin

# --- Setup Chrome ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- Open page ---
url = "https://web.kolhapurcorporation.gov.in/getElectionListByYear?ele_ele_yr_id=4"
driver.get(url)
time.sleep(5)  # wait for table to load

# --- Folder to save PDFs ---
save_folder = r"C:\Onkar\Kolhapur_PDFs"
os.makedirs(save_folder, exist_ok=True)

# --- Find all PDF links ---
pdf_elements = driver.find_elements(By.XPATH, "//tbody//a[@href and contains(@href, 'getDownloadPdfFile')]")

for a in pdf_elements:
    href = a.get_attribute("href")
    filename = a.get_attribute("download")  # Use the meaningful Hindi name
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    full_url = urljoin(url, href)  # in case it's relative
    pdf_path = os.path.join(save_folder, filename)
    
    print(f"Downloading {filename} ...")
    r = requests.get(full_url)
    with open(pdf_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {pdf_path}")

print("All PDFs downloaded successfully!")
driver.quit()
