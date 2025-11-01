import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- Configuration ---
BASE_URL = "https://wardha.gov.in/en/wardha-district-maps-and-regional-plans/"
OUTPUT_DIR = r"C:\Onkar\Swapnil\Election maps\Wardha"  # change if needed
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
FILE_EXTS = (".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".doc", ".docx", ".xls", ".xlsx", ".zip")

# --- Fetch main page ---
print(f"🌐 Fetching main page: {BASE_URL}")
resp = requests.get(BASE_URL, headers=HEADERS, timeout=30)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# --- Collect all candidate links ---
links = set()
for tag in soup.find_all(["a", "img"], href=True):
    links.add(tag["href"])
for tag in soup.find_all("img", src=True):
    links.add(tag["src"])

# --- Also catch CDN or media URLs via regex ---
cdn_links = re.findall(r'https?://[^\s"\']+(?:' + "|".join(FILE_EXTS) + r')', resp.text)
for link in cdn_links:
    links.add(link)

# --- Normalize and filter ---
final_links = []
for href in links:
    abs_url = urljoin(BASE_URL, href)
    if abs_url.lower().endswith(FILE_EXTS):
        final_links.append(abs_url)

# --- Download ---
print(f"🧩 Found {len(final_links)} downloadable files.\n")

for i, file_url in enumerate(final_links, 1):
    file_name = os.path.basename(urlparse(file_url).path)
    file_name = re.sub(r"[\\/:*?\"<>|]", "_", file_name)

    save_path = os.path.join(OUTPUT_DIR, file_name)
    if os.path.exists(save_path):
        print(f"{i:02d}. ⏩ Skipped (already exists): {file_name}")
        continue

    try:
        print(f"{i:02d}. 📥 Downloading: {file_name}")
        r = requests.get(file_url, headers=HEADERS, timeout=40)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Error downloading {file_url}: {e}")

print("\n🎯 Download completed successfully!")
print(f"📂 Files saved to: {OUTPUT_DIR}")
