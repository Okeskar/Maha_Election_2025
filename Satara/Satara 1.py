import requests
from bs4 import BeautifulSoup
import os
import re

# URL of the page containing the PDFs
url = "https://www.satara.gov.in/en/notice/zilla-parishad-and-panchayat-samiti-general-elections-2025-final-ward-composition-maps/"

# Folder to save PDFs
save_folder = r"C:\Onkar\Swapnil\Election maps\Satara\PDF"
os.makedirs(save_folder, exist_ok=True)

# Get the page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Function to make filename safe
def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", text).strip().replace(" ", "_")

# Find and download all PDFs
pdf_count = 0
for a in soup.find_all("a", href=True):
    href = a['href']
    if href.lower().endswith(".pdf"):
        link_text = a.get_text(strip=True)
        if not link_text:
            link_text = f"file_{pdf_count + 1}"
        file_name = sanitize_filename(link_text) + ".pdf"
        file_path = os.path.join(save_folder, file_name)
        
        print(f"Downloading '{file_name}' ...")
        r = requests.get(href, headers=headers)
        with open(file_path, "wb") as f:
            f.write(r.content)
        print(f"Saved to {file_path}")
        pdf_count += 1

print(f"All {pdf_count} PDFs downloaded successfully!")
