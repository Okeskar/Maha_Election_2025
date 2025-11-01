import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse, parse_qs

# URL of the page
url = "https://www.pmc.gov.in/en/election?year=2025"

# Output folder
output_folder = r"C:\Onkar\Swapnil\Election maps\PMC_2025\Final Ward Formation"
os.makedirs(output_folder, exist_ok=True)

def convert_drive_link_to_direct(download_url):
    """
    Converts Google Drive file URL to direct download link.
    Example input:
    https://drive.google.com/file/d/FILE_ID/view
    Output:
    https://drive.google.com/uc?export=download&id=FILE_ID
    """
    parsed = urlparse(download_url)
    if 'drive.google.com' not in parsed.netloc:
        return download_url  # Not a Drive link, return as is
    
    # Extract file ID
    if '/file/d/' in parsed.path:
        file_id = parsed.path.split('/file/d/')[1].split('/')[0]
    else:
        # Try query param 'id'
        query_params = parse_qs(parsed.query)
        file_id = query_params.get('id', [None])[0]
    
    if file_id:
        direct_link = f"https://drive.google.com/uc?export=download&id={file_id}"
        return direct_link
    return download_url  # fallback

# Setup Selenium Chrome driver with webdriver-manager (auto downloads driver)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run browser in headless mode (no UI)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    time.sleep(5)  # Wait for page & JS to load; increase if needed

    # Find the element with the "Final Ward Formation" text
    section_header = None
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        headers = driver.find_elements(By.TAG_NAME, tag)
        for header in headers:
            if "Final Ward Formation" in header.text:
                section_header = header
                break
        if section_header:
            break

    if not section_header:
        print("Couldn't find 'Final Ward Formation' section on the page.")
        driver.quit()
        exit()

    # Get next siblings until next header at same or higher level to gather links
    pdf_links = []
    try:
        next_elem = section_header.find_element(By.XPATH, "following-sibling::*[1]")
    except:
        next_elem = None

    while next_elem:
        # Stop if next header of same or higher level is found
        if next_elem.tag_name.startswith('h') and next_elem.tag_name <= section_header.tag_name:
            break

        # Find all <a> elements in next_elem that link to PDFs or Google Drive files
        anchors = next_elem.find_elements(By.TAG_NAME, 'a')
        for a in anchors:
            href = a.get_attribute('href')
            if not href:
                continue
            href = href.strip()
            # Check for PDF or Google Drive links (commonly used for PDFs)
            if href.lower().endswith('.pdf') or 'drive.google.com/file/d/' in href:
                pdf_links.append(href)

        try:
            next_elem = next_elem.find_element(By.XPATH, "following-sibling::*[1]")
        except:
            break

    if not pdf_links:
        print("No PDF links found in 'Final Ward Formation' section.")
        driver.quit()
        exit()

    print(f"Found {len(pdf_links)} PDF files. Downloading...")

    # Download the PDF files
    for pdf_url in pdf_links:
        # Convert Google Drive links to direct download
        download_url = convert_drive_link_to_direct(pdf_url)

        filename = os.path.basename(urlparse(pdf_url).path)
        if not filename.lower().endswith('.pdf'):
            # Sometimes Google Drive URLs won't have a proper filename, so we create one
            filename = f"google_drive_file_{pdf_links.index(pdf_url)+1}.pdf"

        filepath = os.path.join(output_folder, filename)

        print(f"Downloading {filename} from {download_url} ...")

        r = requests.get(download_url, stream=True)
        r.raise_for_status()

        # For Google Drive files, sometimes confirmation is required due to virus scan warning.
        # This script does not handle that. For large files, consider using Google Drive API.

        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print("All downloads completed!")

finally:
    driver.quit()
