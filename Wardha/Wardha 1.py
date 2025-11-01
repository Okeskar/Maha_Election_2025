from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Import the Service class
from selenium.webdriver.chrome.options import Options  # If you want to customize the browser options

# Specify the path to your chromedriver
chromedriver_path = r"C:\path\to\chromedriver.exe"  # Replace with the actual path to your chromedriver

# Set up the Chrome Service
service = Service(chromedriver_path)

# Set up Chrome options (optional)
options = Options()
# options.add_argument("--headless")  # Uncomment to run Chrome in headless mode

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=options)

# Open the target URL
driver.get("YOUR_TARGET_URL")  # Replace with your target URL

# Find all image elements by their XPath
image_elements = driver.find_elements(By.XPATH, 'YOUR_IMAGE_XPATH')  # Replace with the correct XPath

# Loop through all images and process them
for idx, img_element in enumerate(image_elements):
    try:
        # Extract image URL
        img_url = img_element.get_attribute('src')
        
        if img_url:
            print(f"Image {idx + 1} URL: {img_url}")  # Debugging line to print the URL
            
            # Ensure the URL is valid and format it if necessary
            img_url = urljoin(driver.current_url, img_url)  # Handle relative URLs

            # Make sure the URL is a string
            if isinstance(img_url, str):
                # Download the image
                img_data = requests.get(img_url).content

                # Save image locally
                file_name = f"image_{idx + 1}.jpg"
                with open(file_name, 'wb') as file:
                    file.write(img_data)
                print(f"Saved: {file_name}")
            else:
                print(f"Invalid URL type for image {idx + 1}: {type(img_url)}")
        else:
            print(f"Image {idx + 1} does not have a valid 'src' attribute.")
    
    except Exception as e:
        print(f"Error processing image {idx + 1}: {e}")

# Clean up and close the driver
driver.quit()
