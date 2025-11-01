import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, filename, dst_folder):
    """Download and save a file with a clean name."""
    os.makedirs(dst_folder, exist_ok=True)
    safe_name = filename.replace(" ", "_").replace("/", "_")
    extension = os.path.splitext(url)[1] or ".pdf"
    local_path = os.path.join(dst_folder, f"{safe_name}{extension}")

    print(f"⬇️ Downloading: {filename}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"✅ Saved: {local_path}\n")
    except Exception as e:
        print(f"❌ Failed to download {url} ({e})\n")

def scrape_and_download(base_url, dst_folder):
    """Scrape all Ward PDFs and extra maps from the given URL."""
    print(f"Fetching: {base_url}\n")
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> tags that point to PDFs
    pdf_links = soup.find_all("a", href=lambda href: href and href.lower().endswith(".pdf"))

    for tag in pdf_links:
        file_url = urljoin(base_url, tag["href"])
        text = tag.get_text(strip=True)

        # Clean up the name — if empty, use filename from URL
        name = text if text else os.path.splitext(os.path.basename(file_url))[0]

        download_file(file_url, name, dst_folder)

if __name__ == "__main__":
    # Webpage to scrape
    target_url = "https://www.pcmcindia.gov.in/election"

    # Folder to save PDFs
    download_folder = r"C:\Onkar\Swapnil\Election maps\PCMC"

    scrape_and_download(target_url, download_folder)
