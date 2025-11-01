import os
import requests

base_url = "https://dm.mcgm.gov.in/assets/pdf/All%20Maps/"
download_path = r"C:\Onkar\Swapnil\Election maps\BMC\Disaster management maps Mumbai"
os.makedirs(download_path, exist_ok=True)

# Mapping of ward full names to exact file names
ward_file_map = {
    "Ward A": "A.pdf",
    "Ward B": "B.pdf",
    "Ward C": "C.pdf",
    "Ward D": "D.pdf",
    "Ward E": "E.pdf",
    "Ward F North": "FN.pdf",
    "Ward F South": "FS.pdf",
    "Ward G North": "GN.pdf",
    "Ward G South": "GS.pdf",
    "Ward H East": "HE.pdf",
    "Ward H West": "HW.pdf",
    "Ward K East": "KE.pdf",
    "Ward K West": "KW.pdf",
    "Ward L": "L.pdf",
    "Ward M East": "ME.pdf",
    "Ward M West": "MW.pdf",
    "Ward N": "N.pdf",
    "Ward P North": "PN.pdf",
    "Ward P South": "PS.pdf",
    "Ward R North": "RN.pdf",
    "Ward R South": "RS.pdf",
    "Ward R Central": "RC.pdf",
    "Ward S": "S.pdf",
    "Ward T": "T.pdf"
}

def is_valid_pdf(content: bytes) -> bool:
    return content.startswith(b'%PDF')

for ward, filename in ward_file_map.items():
    url = base_url + filename
    local_file = os.path.join(download_path, f"{ward}.pdf")
    print(f"Downloading {ward} from {url} ...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if is_valid_pdf(response.content):
                with open(local_file, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Saved {ward}.pdf")
            else:
                print(f"⚠️ Invalid PDF content for {ward}, skipping.")
        else:
            print(f"❌ HTTP {response.status_code} error for {ward}")
    except Exception as e:
        print(f"❌ Error downloading {ward}: {e}")
