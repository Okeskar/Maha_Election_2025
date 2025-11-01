import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- Configuration ---
url = "https://election.nagpurnmc.in/nmc_yearwise_news/1"
output_dir = r"C:\Onkar\Swapnil\Election maps\Nagpur"
os.makedirs(output_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

# --- Fetch Page ---
print(f"Fetching: {url}")
response = requests.get(url, headers=headers)
response.raise_for_status()

# --- Parse HTML ---
soup = BeautifulSoup(response.text, "html.parser")

# --- Find all PDF links ---
count = 0
for a in soup.find_all("a", href=True):
    href = a["href"].strip()
    text = a.get_text(strip=True)

    if href.lower().endswith(".pdf"):
        file_url = urljoin(url, href)
        file_name = text if text else os.path.basename(href)
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"

        # Clean filename
        file_name = "".join(c for c in file_name if c not in "\\/:*?\"<>|")
        save_path = os.path.join(output_dir, file_name)

        try:
            print(f"📥 Downloading: {file_name}")
            r = requests.get(file_url, headers=headers, timeout=20)
            r.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(r.content)
            print(f"✅ Saved to: {save_path}")
            count += 1
        except Exception as e:
            print(f"❌ Failed: {file_name} ({e})")

print(f"\n🎯 Done! {count} PDF files downloaded to:\n{output_dir}")
