import os
import requests
from urllib.parse import quote

base_url = "https://portal.mcgm.gov.in/irj/go/km/docs/documents/MCGM%20Department%20List/Assessment%20And%20Collection%20(Election)/Docs/Election%20Department/BMC%20General%20Election%202025/Ward%20Formation/Final/Final%20Prabhag%20Maps%202025/"

# All folders/zones confirmed from your list
folders = [
    "L",
    "M EAST", "M WEST",
    "N",
    "S", "T"
]

start_ward = 1
end_ward = 227  # Adjust if you know exact ward max for zones

download_base_dir = r"C:\Onkar\Swapnil\Election maps\BMC1"
os.makedirs(download_base_dir, exist_ok=True)

for folder in folders:
    print(f"\n📁 Processing folder: {folder}")

    local_folder = os.path.join(download_base_dir, folder.replace(" ", "_"))
    os.makedirs(local_folder, exist_ok=True)

    for ward_num in range(start_ward, end_ward + 1):
        file_name = f"Prabhag No._{ward_num}.pdf"  # Corrected filename pattern
        encoded_folder = quote(folder)
        encoded_file_name = quote(file_name)
        file_url = f"{base_url}{encoded_folder}/{encoded_file_name}"
        local_file_path = os.path.join(local_folder, file_name)

        try:
            response = requests.get(file_url, timeout=15)
            if response.status_code == 200:
                with open(local_file_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {file_name} from {folder}")
            else:
                # Uncomment below for debugging missing files
                # print(f"❌ Not found: {file_url} (Status: {response.status_code})")
                pass
        except Exception as e:
            print(f"⚠️ Error downloading {file_url}: {e}")

print("\n✅ All done.")
