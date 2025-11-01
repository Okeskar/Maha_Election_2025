import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ---- Configuration ----
url = "https://malegaoncorporation.org/mmc/wardwise-final-formation"
output_dir = r"C:\Onkar\Swapnil\Election maps\Malegaon"
os.makedirs(output_dir, exist_ok=True)

# ---- Fetch the webpage ----
print(f"Fetching: {url}")
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
response.raise_for_status()

# ---- Parse the HTML ----
soup = BeautifulSoup(response.text, "html.parser")

# ---- Find and download files ----
count = 0
for a in soup.find_all("a", href=True):
    link = a["href"].strip()
    if link.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
        # Ensure full URL
        full_url = urljoin(url, link)
        filename = os.path.basename(full_url.split("?")[0])
        filepath = os.path.join(output_dir, filename)

        try:
            print(f"📥 Downloading: {full_url}")
            r = requests.get(full_url, headers=headers, timeout=20)
            r.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"✅ Saved: {filepath}")
            count += 1
        except Exception as e:
            print(f"❌ Failed: {full_url} — {e}")

print(f"\n🎯 Download complete — {count} files saved in:\n{output_dir}")
