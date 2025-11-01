import requests
from bs4 import BeautifulSoup
import os

# URL of the page containing the PDFs
url = "https://www.satara.gov.in/en/notice/zilla-parishad-and-panchayat-samiti-general-elections-2025-final-ward-composition-maps/"

# Folder to save PDFs
save_folder = r"C:\Onkar\Swapnil\Election maps\Satara"
os.makedirs(save_folder, exist_ok=True)

# Get the page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all PDF links
pdf_links = []
for a in soup.find_all("a", href=True):
    href = a['href']
    if href.lower().endswith(".pdf"):
        pdf_links.append(href)

# Download each PDF
for link in pdf_links:
    pdf_name = link.split("/")[-1]
    pdf_path = os.path.join(save_folder, pdf_name)
    print(f"Downloading {pdf_name} ...")
    r = requests.get(link, headers=headers)
    with open(pdf_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {pdf_path}")

print("All PDFs downloaded successfully!")
