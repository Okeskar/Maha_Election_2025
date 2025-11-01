import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

# URL to scrape
url = 'https://gondia.gov.in/en/final-ward-wise-maps-municipal-counsil-general-election-2025/'

# Set base directory for storing files
base_directory = r'C:\Onkar\Swapnil\Election maps\Gondia'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Send a request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Function to download a file and save it in the correct folder
def download_pdf(pdf_url, folder_name, file_name):
    # Construct full path for the folder
    folder_path = os.path.join(base_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Get the file content
    pdf_response = requests.get(pdf_url)

    # Define the full file path
    file_path = os.path.join(folder_path, file_name)

    # Save the PDF content to the specified file
    with open(file_path, 'wb') as f:
        f.write(pdf_response.content)
    print(f"Downloaded: {file_path}")

# Find all relevant sections (heading + PDF links)
sections = [
    ('Notification', soup.find('p', text='Notification')),
    ('Annexures', soup.find('p', text='Annexures')),
    ('Maps', soup.find('p', text='Maps')),
    ('Final Ward Wise Maps', soup.find('p', text='Final Ward Wise Maps')),
]

# Iterate through each section and extract PDF links
for section_name, section_tag in sections:
    # Extract links under this section
    if section_tag:
        # Find the parent element that contains the PDF links
        parent_div = section_tag.find_parent('div')
        table = parent_div.find_next('table')
        rows = table.find_all('tr')

        # Loop through each row and extract the links
        for row in rows:
            columns = row.find_all('td')
            for col in columns:
                # Check if the column contains a link
                a_tag = col.find('a', href=True)
                if a_tag:
                    pdf_url = a_tag['href']
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(url, pdf_url)  # Make sure the URL is absolute

                    # Get the file name (e.g., "Ward 1", "Annexure 1", etc.)
                    file_name = a_tag.text.strip().replace(' ', '_') + '.pdf'

                    # Download the PDF and store it in the correct folder
                    download_pdf(pdf_url, section_name, file_name)

print("Download completed!")
