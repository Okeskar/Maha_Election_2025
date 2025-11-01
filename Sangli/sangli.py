import requests
import os

# Folder to save PDFs
save_folder = r"C:\Onkar\Swapnil\Election maps\Sangli SMKC"
os.makedirs(save_folder, exist_ok=True)

# Base URL for relative links
base_url = "https://smkc.gov.in/"

# List of PDFs (relative URLs and names)
pdf_links = []
for i in range(1, 21):
    rel_url = f"pdf/Election Final 2025/Map/Prabhag{i}.pdf"
    full_url = base_url + rel_url.replace(" ", "%20")  # encode spaces
    name = f"प्रभाग {i}"
    pdf_links.append((full_url, name))

# Download PDFs
for url, name in pdf_links:
    # Make Windows-safe filename
    filename = "".join(c for c in name if c not in r'\/:*?"<>|') + ".pdf"
    path = os.path.join(save_folder, filename)
    print(f"Downloading {filename} ...")
    r = requests.get(url)
    if r.status_code == 200:
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"Saved to {path}")
    else:
        print(f"Failed to download {filename}: Status {r.status_code}")

print("All PDFs processed!")
