import os
import requests
from lxml import html
from urllib.parse import urlparse

# Target page
url = "https://vvcmc.in/en/election/"

# Output folder
save_path = r"C:\Onkar\Swapnil\Election maps\Vasai Virar MC"
os.makedirs(save_path, exist_ok=True)

# Add headers to avoid 403 error
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0 Safari/537.36"
}

# Get page
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse HTML
tree = html.fromstring(response.content)

# Use the provided XPath to find all <a> links in the <section>
links = tree.xpath('/html/body/section//a[@href]')

# Loop through each link
for link in links:
    file_url = link.get("href")
    if file_url.lower().endswith(".pdf"):
        # Handle relative URLs
        if file_url.startswith("/"):
            file_url = "https://vvcmc.in" + file_url

        # Extract filename from URL
        file_name = os.path.basename(urlparse(file_url).path)

        try:
            print(f"Downloading {file_name}...")
            pdf = requests.get(file_url, headers=headers)
            pdf.raise_for_status()
            with open(os.path.join(save_path, file_name), "wb") as f:
                f.write(pdf.content)
            print(f"✅ Saved: {file_name}")
        except Exception as e:
            print(f"❌ Failed: {file_name} ({e})")
