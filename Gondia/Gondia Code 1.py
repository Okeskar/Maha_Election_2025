import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Config
base_url = "https://gondia.gov.in/en/draft-ward-wise-maps-municipal-counsil-general-election-2025/"
download_base_folder = r"C:\Onkar\Swapnil\Election maps\Gondia 1"

print(f"Base download folder: {download_base_folder}")

# Create base folder if needed
if not os.path.exists(download_base_folder):
    try:
        os.makedirs(download_base_folder, exist_ok=True)
        print(f"Created base folder: {download_base_folder}")
    except Exception as e:
        print(f"Error creating base folder: {e}")
        exit(1)

# Fetch the page
try:
    resp = requests.get(base_url, timeout=30)
    resp.raise_for_status()
except Exception as e:
    print(f"Failed to fetch {base_url}: {e}")
    exit(1)

soup = BeautifulSoup(resp.text, "html.parser")
print("Fetched and parsed webpage.")

# Find section headings — adjust tag list if needed
heading_tags = ['h2', 'h3', 'strong']  # maybe strong if headings are bold
all_headings = []
for tag in heading_tags:
    found = soup.find_all(tag)
    print(f"Found {len(found)} tags of type {tag}")
    all_headings.extend(found)

if not all_headings:
    print("Warning: No headings found for categorisation — will fallback to base folder only.")

downloaded_count = 0

# Find all links once (you could refine per heading but simpler: download all PDFs into base)
links = soup.find_all("a", href=True)
print(f"Found {len(links)} links.")

# Function to sanitize file names
def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

# Loop through all found links and download PDFs
for link in links:
    href = link['href'].strip()
    if href.lower().startswith("javascript:") or href.lower().startswith("mailto:"):
        continue

    full_url = urljoin(base_url, href)
    parsed = urlparse(full_url)

    # Check if it's a PDF link
    if parsed.path.lower().endswith(".pdf"):
        # Extract the file name from the URL
        filename = os.path.basename(parsed.path)
    elif ".pdf" in parsed.path.lower():
        filename = os.path.basename(parsed.path)
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"
    else:
        continue

    # Get the nearest heading for categorization
    folder_for_file = download_base_folder

    # Extract the title from the nearest heading
    title = None
    for heading in all_headings:
        if heading and heading.get_text(strip=True):
            # Look for the first heading before this link
            title = heading.get_text(strip=True)
            break

    if title:
        # Use the heading title for folder categorization or as part of the filename
        folder_for_file = os.path.join(download_base_folder, sanitize(title))
        os.makedirs(folder_for_file, exist_ok=True)
        filename = sanitize(title) + "_" + filename

    # Full save path for the file
    save_path = os.path.join(folder_for_file, filename)
    print(f"Preparing to download: {full_url} → {filename} in folder: {folder_for_file}")

    try:
        r2 = requests.get(full_url, timeout=30)
        r2.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r2.content)
        print(f"Downloaded: {save_path}")
        downloaded_count += 1
    except Exception as e:
        print(f"Error downloading {full_url}: {e}")

print(f"Done. Total downloaded: {downloaded_count}")
