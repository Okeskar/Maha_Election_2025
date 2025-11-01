import os
import requests
import urllib.parse

# Output directory
output_dir = r"C:\Onkar\Swapnil\Election maps\NMMC\PDFs"
os.makedirs(output_dir, exist_ok=True)

# List of working URLs
urls = [
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-15_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%B0%E0%A5%82%E0%A4%AA%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A4%A8%E0%A4%BE.pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-15_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%B0%E0%A5%82%E0%A4%AA%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%A8%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A4%BE%20(%E0%A4%8F%E0%A4%95%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%A4).pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-15_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%BE%E0%A4%B0%E0%A5%82%E0%A4%AA%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%E0%A4%A8%E0%A4%BF%E0%A4%B9%E0%A4%BE%E0%A4%AF%20%E0%A4%A8%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A5%87.pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-15_%E0%A4%85%E0%A4%82%E0%A4%A4%E0%A4%BF%E0%A4%AE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BF%E0%A4%A6%E0%A5%8D%E0%A4%A6%E0%A5%80%E0%A4%9A%E0%A5%80%20%E0%A4%9C%E0%A4%BE%E0%A4%B9%E0%A5%80%E0%A4%B0%20%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A4%A8%E0%A4%BE.pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-16_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%85%E0%A4%82%E0%A4%A4%E0%A4%BF%E0%A4%AE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%A8%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A4%BE%20(%E0%A4%8F%E0%A4%95%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%A4)%20(1).pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-16_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%85%E0%A4%82%E0%A4%A4%E0%A4%BF%E0%A4%AE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%E0%A4%A8%E0%A4%BF%E0%A4%B9%E0%A4%BE%E0%A4%AF%20%E0%A4%A8%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A5%87.pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-16_%E0%A4%AA%E0%A4%B0%E0%A4%BF%E0%A4%B6%E0%A4%BF%E0%A4%B7%E0%A5%8D%E0%A4%9F%2014%20%E0%A4%B5%2015.pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-16_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%85%E0%A4%82%E0%A4%A4%E0%A4%BF%E0%A4%AE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%A8%E0%A4%95%E0%A4%BE%E0%A4%B6%E0%A4%BE%20(%E0%A4%8F%E0%A4%95%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%A4)%20(2).pdf",
    "https://app.nmmconline.in/backend/common/api/file/preview?filePath=/var/nmmc/docs/contentManagement/_17-10-2025-18-58-16_%E0%A4%A8%E0%A4%AE%E0%A5%81%E0%A4%82%E0%A4%AE%E0%A4%AA%E0%A4%BE%20%E0%A4%B8%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%B5%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%95%20%E0%A4%A8%E0%A4%BF%E0%A4%B5%E0%A4%A1%E0%A4%A3%E0%A5%82%E0%A4%95%202025%20%E0%A4%85%E0%A4%82%E0%A4%A4%E0%A4%BF%E0%A4%AE%20%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%AD%E0%A4%BE%E0%A4%97%20%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%20%E0%A4%85%E0%A4%A7%E0%A4%BF%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A4%A8%E0%A4%BE.pdf"
]

# Download loop
for url in urls:
    try:
        # Parse and decode file path from URL
        parsed = urllib.parse.urlparse(url)
        file_path_encoded = urllib.parse.parse_qs(parsed.query).get('filePath', [None])[0]
        if not file_path_encoded:
            print(f"Invalid file path in URL: {url}")
            continue

        file_path = urllib.parse.unquote(file_path_encoded)
        original_filename = os.path.basename(file_path)

        # Remove prefix like "_17-10-2025-18-58-15_" from filename
        parts = original_filename.split("_", 2)  # Keep only the 3rd part onwards
        clean_filename = parts[2] if len(parts) >= 3 else original_filename

        output_path = os.path.join(output_dir, clean_filename)

        # Download the PDF
        print(f"Downloading: {clean_filename}")
        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to: {output_path}\n")

    except Exception as e:
        print(f"❌ Failed to download from {url}\nError: {e}\n")
