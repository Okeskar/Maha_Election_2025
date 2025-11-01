import requests
import os

# URLs for Annexures and Maps
annexure_2_url = "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592240163834.pdf"
goregaon_url = "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592235925196.pdf"

# URLs for Final Ward Wise Maps
ward_urls = [
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592246759972.jpg",  # Ward 1
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592246816288.jpg",  # Ward 2
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592246899045.jpg",  # Ward 3
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592246962056.jpg",  # Ward 4
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247041377.jpg",  # Ward 5
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247107478.jpg",  # Ward 6
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247178092.jpg",  # Ward 7
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247228187.jpg",  # Ward 8
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247294109.jpg",  # Ward 9
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247363600.jpg",  # Ward 10
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247422328.jpg",  # Ward 11
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247495249.jpg",  # Ward 12
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247559891.jpg",  # Ward 13
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247613750.jpg",  # Ward 14
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247667176.jpg",  # Ward 15
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247723514.jpg",  # Ward 16
    "https://cdn.s3waas.gov.in/s346922a0880a8f11f8f69cbb52b1396be/uploads/2025/09/17592247796609.jpg"   # Ward 17
]

# Base directory for saving files
base_directory = r'C:\Onkar\Swapnil\Election maps\Gondia\Goregaon Nagar Panchayat'

# Function to download the file
def download_file(url, folder_name, file_name):
    folder_path = os.path.join(base_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    response = requests.get(url)

    # Check if the response is valid
    if response.status_code == 200:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {file_name} from {url}")

# Download the Annexure 2 and Goregaon PDF
download_file(annexure_2_url, 'Annexures', 'Annexure_2.pdf')
download_file(goregaon_url, 'Maps', 'Goregaon_Nagar_Panchayat.pdf')

# Download the Ward Wise Maps
for i, url in enumerate(ward_urls, 1):
    download_file(url, 'Final Ward Wise Maps', f'Ward_Ward_{i}.jpg')

print("Download completed!")
