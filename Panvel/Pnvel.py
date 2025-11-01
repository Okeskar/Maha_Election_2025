import os
import requests

# Base URL and image names
base_url = "https://www.panvelcorporation.com/public/map/"
image_names = [
    "PB1 (1).jpg",
    *[f"PB{i}.jpg" for i in range(2, 21)],
    "full_election.jpg"
]

# Create a folder to save the images
output_folder = r"C:\Onkar\Swapnil\Election maps\Panvel corporation"
os.makedirs(output_folder, exist_ok=True)

# Download each image
for name in image_names:
    url = base_url + name
    filename = os.path.join(output_folder, name.replace(" ", "_"))  # remove space in filename
    print(f"Downloading {url} ...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved to {filename}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")

print("\n🎉 All downloads attempted.")
