import os
from bs4 import BeautifulSoup

SAVE_FOLDER = r"C:\Onkar\Swapnil\Election maps\Akola"
os.makedirs(SAVE_FOLDER, exist_ok=True)

HTML_FILE = r"C:\Onkar\Swapnil\Election maps\Akola\akola_page.html"

BASE_URL = "https://amcakola.in"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
pdf_links = soup.select("#divChildMenu a[href$='.pdf']")

print(f"Found {len(pdf_links)} PDF links.")

import requests
from urllib.parse import urljoin

for link in pdf_links:
    pdf_url = urljoin(BASE_URL, link["href"])
    pdf_name = os.path.basename(pdf_url)
    save_path = os.path.join(SAVE_FOLDER, pdf_name)
    
    print(f"Downloading: {pdf_url}")
    try:
        r = requests.get(pdf_url)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Failed to download {pdf_url} — {e}")

print("All done!")
