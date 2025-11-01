import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ------------------- Configuration -------------------
BASE_URL = "https://www.jcmc.gov.in/election-ward-formation-final-2025-26.htm"
OUTPUT_DIR = r"C:\Onkar\Swapnil\Election maps\Jalgaon"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
FILE_EXTS = (".pdf",)

# ------------------- Fetch Page -------------------
print(f"🌐 Fetching page: {BASE_URL}")
resp = requests.get(BASE_URL, headers=HEADERS, timeout=30)
resp.raise_for_status()

# Let BeautifulSoup detect proper encoding
soup = BeautifulSoup(resp.content, "html.parser")

# ------------------- Extract Links -------------------
links = []

for li in soup.select("ul li"):
    a_tag = li.find("a", href=True)
    if a_tag:
        href = a_tag["href"]
        text = a_tag.get_text(strip=True)
        # If text is too generic like 'Click To View', use filename from URL
        if text.lower() in ["click to view", "view"]:
            text = os.path.basename(urlparse(href).path).replace("%20", " ")
        if any(href.lower().endswith(ext) for ext in FILE_EXTS):
            links.append((href, text))

print(f"🧩 Found {len(links)} files to download.\n")

# ------------------- Download Files -------------------
for i, (href, text) in enumerate(links, 1):
    file_url = urljoin(BASE_URL, href)
    
    # Replace only illegal Windows filename characters, keep Unicode intact
    filename = re.sub(r"[\\/:*?\"<>|]", "_", text) + ".pdf"
    save_path = os.path.join(OUTPUT_DIR, filename)
    
    if os.path.exists(save_path):
        print(f"{i:02d}. ⏩ Skipped (already exists): {filename}")
        continue

    try:
        print(f"{i:02d}. 📥 Downloading: {filename}")
        r = requests.get(file_url, headers=HEADERS, timeout=40)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Error downloading {file_url}: {e}")

print("\n🎯 All downloads completed!")
print(f"📂 Files saved to: {OUTPUT_DIR}")
