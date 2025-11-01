import os
import requests
from lxml import html
from urllib.parse import urlparse

# Target URL
url = "https://amravaticorporation.in/en/electoral-ward-structure-2025/"

# Folder to save the files
save_path = r"C:\\Onkar\\Swapnil\\Election maps\\Amravati"
os.makedirs(save_path, exist_ok=True)

# Fetch and parse the page
response = requests.get(url)
tree = html.fromstring(response.content)

# XPath to get download links from the table
links = tree.xpath('//*[@id="tablepress-34"]//a')

# Download each PDF
for link in links:
    file_url = link.get("href")

    # Extract filename from the URL itself
    path = urlparse(file_url).path
    file_name = os.path.basename(path)

    try:
        pdf_response = requests.get(file_url)
        pdf_response.raise_for_status()
        with open(os.path.join(save_path, file_name), "wb") as f:
            f.write(pdf_response.content)
        print(f"✅ Downloaded: {file_name}")
    except Exception as e:
        print(f"❌ Failed: {file_name} ({e})")
