import requests
import os

# Folder to save PDFs
save_folder = r"C:\Onkar\Swapnil\Election maps\Nashik"
os.makedirs(save_folder, exist_ok=True)

# List of PDF URLs and names (extracted from HTML)
pdf_links = [
    ("https://nmc.gov.in/assets/admin/upload/download/nmcelection2025-26/NMC_election_2025_draft_Ward.pdf", "प्रारूप अधिसूचना २२-८-२०२५"),
    ("https://nmc.gov.in/assets/admin/upload/download/nmcelection2025-26/NASHIK_2025_ALL_MAP_PDF.pdf", "एकत्रिक प्रारूप प्रभाग रचना नकाशा"),
]

# Adding ward PDFs 1-31 dynamically
base_url = "https://nmc.gov.in/assets/admin/upload/download/nmcelection2025-26/"
for i in range(1, 32):
    pdf_links.append((f"{base_url}{i}.pdf", f"प्रभाग {i}"))

# Download PDFs
for url, name in pdf_links:
    # Make Windows-safe filename
    filename = "".join(c for c in name if c not in r'\/:*?"<>|') + ".pdf"
    path = os.path.join(save_folder, filename)
    print(f"Downloading {filename} ...")
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Saved to {path}")

print("All PDFs downloaded successfully!")
