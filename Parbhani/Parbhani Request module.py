import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, filename, dst_folder):
    """Download a file and save it in dst_folder using the given filename."""
    os.makedirs(dst_folder, exist_ok=True)

    # create safe filename
    safe_name = filename.replace(" ", "_").replace("/", "_")
    extension = os.path.splitext(url)[1] or ".jpg"  # default extension if missing
    local_path = os.path.join(dst_folder, f"{safe_name}{extension}")

    print(f"⬇️ Downloading: {filename} → {local_path}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"✅ Saved: {local_path}")
    except Exception as e:
        print(f"❌ Failed to download {url} ({e})")

def scrape_and_download(page_url, dst_folder):
    """Fetch the page, parse the table, and download all files."""
    print(f"Fetching page: {page_url}")
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    # Loop through each data row (skip the header)
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[1].get_text(strip=True)
            link_tag = cols[2].find("a", href=True)
            if link_tag:
                file_url = urljoin(page_url, link_tag["href"])
                download_file(file_url, name, dst_folder)

if __name__ == "__main__":
    # Target webpage
    target_page = "https://pcmcparbhani.org/en/pcmc/election-2025"

    # Folder to save downloaded images
    download_folder = r"C:\Onkar\Swapnil\Election maps\Parbhani\1"

    scrape_and_download(target_page, download_folder)
