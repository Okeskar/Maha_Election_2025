import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs_from_url(page_url, local_folder):
    # Make sure the folder exists
    os.makedirs(local_folder, exist_ok=True)

    print(f"Fetching page: {page_url}")
    resp = requests.get(page_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find all <a> tags with href ending in .pdf
    pdf_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            full_url = urljoin(page_url, href)
            pdf_links.append(full_url)

    print(f"Found {len(pdf_links)} PDF links")

    for pdf_url in pdf_links:
        filename = os.path.basename(pdf_url)
        local_path = os.path.join(local_folder, filename)

        print(f"Downloading {pdf_url} -> {local_path}")
        r = requests.get(pdf_url, stream=True)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("All downloads complete.")

if __name__ == "__main__":
    url = "https://kdmc.gov.in/kdmc/SectionInformation.html?editForm&rowId=740&page="
    folder = r"C:\Onkar\Swapnil\Election maps\KDMC"
    download_pdfs_from_url(url, folder)
