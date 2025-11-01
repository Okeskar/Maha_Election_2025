import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configuration
url = "https://web.cmcchandrapur.com/ongoing_projects?marathi=true"
download_dir = r"C:\Onkar\Swapnil\Election maps\Chandrapur 2"
os.makedirs(download_dir, exist_ok=True)

# Helper: sanitize filenames
def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

# Fetch page
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Find all <td> tags that contain a title + are followed by a download link
tds = soup.find_all("td", style="color:black;")
print(f"Found {len(tds)} candidate <td> blocks")

downloads = []

for i in range(len(tds)):
    td = tds[i]
    title = td.get_text(strip=True)
    next_td = td.find_next_sibling("td")

    if next_td:
        link = next_td.find("a", href=True)
        if link and "uploads/files" in link["href"]:
            file_url = link["href"]
            if not file_url.startswith("http"):
                file_url = "https://web.cmcchandrapur.com" + file_url

            ext = os.path.splitext(urlparse(file_url).path)[1]
            if not ext:
                ext = ".pdf"

            filename = sanitize(title) + ext
            filepath = os.path.join(download_dir, filename)

            print(f"⬇️ Downloading: {title}")
            print(f"    From: {file_url}")
            print(f"    To:   {filepath}")

            try:
                file_data = requests.get(file_url)
                file_data.raise_for_status()
                with open(filepath, "wb") as f:
                    f.write(file_data.content)
                print("    ✅ Saved.")
                downloads.append((title, file_url))
            except Exception as e:
                print("    ❌ Failed to download:", e)

print(f"\n✅ Done. Total downloaded: {len(downloads)} files.")
