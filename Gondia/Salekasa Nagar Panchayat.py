import os
import requests
from lxml import html
from urllib.parse import urljoin
from pathlib import Path

# URL to scrape
url = 'https://gondia.gov.in/en/final-ward-wise-maps-municipal-counsil-general-election-2025/'

# Set base directory for storing files
base_directory = r'C:\Onkar\Swapnil\Election maps\Gondia\Salekasa Nagar Panchayat'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Send a request to fetch the page content
response = requests.get(url)
tree = html.fromstring(response.content)

# Base URL for the relative links
base_url = 'https://gondia.gov.in'

# XPath to extract the required section of the page
xpath = '//*[@id="post-33112"]/section/div[5]/div/div/div'

# Function to download a PDF and save it in the correct folder
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

# Extract the content based on XPath
section_content = tree.xpath(xpath)

# Check if the section is found
if section_content:
    # Find all the <a> tags with the PDFs
    links = tree.xpath(f'{xpath}//a[@href]')

    # Loop through each link and download the PDFs
    for link in links:
        pdf_url = link.get('href')
        
        # Ensure we have a full URL
        if not pdf_url.startswith('http'):
            pdf_url = urljoin(base_url, pdf_url)

        # Get the file name from the link text (or URL if no text)
        file_name = link.text.strip().replace(' ', '_') + '.pdf' if link.text else pdf_url.split("/")[-1]

        # Check the section name from the link's surrounding text (e.g., Notification, Maps)
        section_name = link.xpath('ancestor::div[1]//p/strong/span/text()')
        
        # If section name not found, explicitly handle the "Final Ward Wise Maps" section
        if not section_name:
            section_name = 'Unknown'
            # Special check for Final Ward Wise Maps section
            if 'Final Ward Wise Maps' in link.text:
                section_name = 'Final_Ward_Wise_Maps'
        
        # Ensure section_name is a string and not a list
        if isinstance(section_name, list):
            section_name = section_name[0] if section_name else 'Unknown'
        
        # Download the PDF
        download_pdf(pdf_url, section_name, file_name)
else:
    print("No relevant section found.")

print("Download completed!")
