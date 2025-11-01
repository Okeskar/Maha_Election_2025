import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL of the page
url = "https://www.pcmcindia.gov.in/info.php"

# Folder to save PDFs
save_folder = r"C:\Onkar\Swapnil\Election maps\PCMC Pradhikaran"
os.makedirs(save_folder, exist_ok=True)

# Request page content
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
        full_link = urljoin(url, href)  # Make full URL if relative
        pdf_links.append(full_link)

# Download PDFs
for link in pdf_links:
    pdf_name = link.split("/")[-1].split("?")[0]  # Remove any query params
    pdf_path = os.path.join(save_folder, pdf_name)
    print(f"Downloading {pdf_name} ...")
    r = requests.get(link, headers=headers)
    with open(pdf_path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {pdf_path}")

print("All PDFs downloaded successfully!")
