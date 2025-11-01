import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re

# URL of the webpage
url = "https://www.umc.gov.in/general-election"

# XPaths for PDF link and file name (from the 'वर्णन' column)
pdf_xpath = '//*[@id="collapse0"]/div/div/table/tbody/tr/td[3]/a'  # PDF links (assumed to be in the 3rd column)
filename_xpath = '//*[@id="collapse0"]/div/div/table/tbody/tr/td[2]'  # 'वर्णन' column for filenames (2nd column)

# Function to download the PDF file and save it
def download_pdf(pdf_url, file_name, folder_path="C:\\Onkar\\Swapnil\\Election maps\\Ulhasnagar"):
    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Clean the filename to ensure there are no illegal characters
    file_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)  # Replace invalid characters
    file_name = file_name.strip()  # Remove leading/trailing spaces
    
    # If filename is empty, use a default name
    if not file_name:
        file_name = "untitled_file"
    
    # Send a request to fetch the PDF
    pdf_response = requests.get(pdf_url)

    if pdf_response.status_code == 200:
        # Construct the full path to save the PDF
        file_path = os.path.join(folder_path, file_name + ".pdf")
        
        # Write the PDF content to the file
        with open(file_path, 'wb') as f:
            f.write(pdf_response.content)
        
        print(f"Downloaded: {file_name}.pdf")
    else:
        print(f"Failed to download {file_name}.pdf")

# Convert Google Drive URL to direct download link
def convert_to_drive_direct_link(pdf_url):
    # Extract the file ID from the URL
    file_id = re.search(r"/d/([^/]+)", pdf_url)
    if file_id:
        file_id = file_id.group(1)
        # Construct the direct download link
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return pdf_url  # If not a Google Drive link, return the URL as is

# Function to fetch PDFs using Selenium (handles JS-loaded content)
def fetch_pdfs_with_selenium(url):
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless (no GUI)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for the page to fully load (optional sleep time)
    sleep(5)  # Adjust the sleep time if necessary
    
    # Get all PDF links and filenames from the page
    pdf_elements = driver.find_elements(By.XPATH, pdf_xpath)
    filename_elements = driver.find_elements(By.XPATH, filename_xpath)
    
    # Check if we found any PDFs
    if not pdf_elements or not filename_elements:
        print("No PDFs found on the page.")
        driver.quit()
        return []

    # Create a list of (filename, pdf_url) tuples
    pdf_files = []
    for filename_element, pdf_element in zip(filename_elements, pdf_elements):
        pdf_url = pdf_element.get_attribute("href")  # Get PDF URL from the "href" attribute
        file_name = filename_element.text.strip()  # Get the file name text from 'वर्णन' column
        
        # Debug: Print the raw extracted filename
        print(f"Raw extracted filename: '{file_name}'")
        
        # Clean the filename to remove unwanted characters
        file_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)  # Replace invalid characters
        file_name = file_name.strip()  # Remove leading/trailing spaces
        
        # If filename is empty, use default names
        if not file_name:
            file_name = f"untitled_file_{len(pdf_files) + 1}"
        
        # Convert Google Drive URL to direct download link
        pdf_url = convert_to_drive_direct_link(pdf_url)
        
        # Debug: Print final filename and URL
        print(f"Final Filename: '{file_name}', PDF URL: {pdf_url}")
        
        pdf_files.append((file_name, pdf_url))
    
    # Close the driver
    driver.quit()
    
    return pdf_files

# Main function to fetch and download all PDFs
def main():
    pdf_files = fetch_pdfs_with_selenium(url)
    
    if not pdf_files:
        return

    for file_name, pdf_url in pdf_files:
        download_pdf(pdf_url, file_name)

if __name__ == "__main__":
    main()
