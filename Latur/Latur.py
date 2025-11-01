from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time
import requests

# --------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------
PAGE_URL = "https://mclatur.org/general-election-2025/"
SAVE_FOLDER = r"C:\Onkar\Swapnil\Election maps\Latur"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# --------------------------------------------------------
# START SELENIUM
# --------------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

print("Opening page...")
driver.get(PAGE_URL)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.dataTable"))
)
time.sleep(2)

# --------------------------------------------------------
# FUNCTION: SCRAPE A TABLE (WITH JS PAGINATION CLICK)
# --------------------------------------------------------
def scrape_table(table_id):
    all_links = []
    page_index = 1

    while True:
        # Wait until table is visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"#{table_id} tbody tr"))
        )
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.select_one(f"table#{table_id}")
        if not table:
            print(f"⚠️ Table {table_id} not found.")
            break

        # Collect all file URLs on this page
        page_links = [a["href"] for a in table.select("tbody a[href]")]
        all_links.extend(page_links)
        print(f"📄 Page {page_index}: {len(page_links)} new, {len(all_links)} total")

        # Try to go to next page
        try:
            next_btn = driver.find_element(
                By.CSS_SELECTOR, f"#{table_id}_wrapper .dt-paging .next"
            )

            if "disabled" in next_btn.get_attribute("class"):
                print(f"✅ Finished pagination for {table_id}")
                break

            # Get first row text for comparison
            old_first_row = driver.find_element(
                By.CSS_SELECTOR, f"#{table_id} tbody tr:first-child"
            ).text

            # Scroll and click via JS (more reliable)
            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            driver.execute_script("arguments[0].click();", next_btn)

            # Wait for table content to change
            WebDriverWait(driver, 15).until_not(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, f"#{table_id} tbody tr:first-child"),
                    old_first_row,
                )
            )

            page_index += 1
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Pagination ended or failed for {table_id}: {e}")
            break

    return all_links

# --------------------------------------------------------
# SCRAPE ALL TABLES
# --------------------------------------------------------
table_ids = ["tablepress-52", "tablepress-40", "tablepress-41"]
all_files = []

for tid in table_ids:
    print(f"\n🔍 Scraping table {tid} ...")
    links = scrape_table(tid)
    print(f"✅ Found {len(links)} files in {tid}.")
    all_files.extend(links)

driver.quit()

# --------------------------------------------------------
# DOWNLOAD FILES (SKIP EXISTING)
# --------------------------------------------------------
print(f"\nTotal unique files found: {len(all_files)}")
all_files = list(set(all_files))  # remove duplicates

for url in all_files:
    filename = os.path.basename(url)
    save_path = os.path.join(SAVE_FOLDER, filename)

    if os.path.exists(save_path):
        print(f"⏭️ Skipping (already exists): {filename}")
        continue

    print(f"⬇️ Downloading: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {save_path}")
    except Exception as e:
        print(f"❌ Failed: {url} ({e})")

print("\n🎉 All downloads complete (including paginated pages).")
