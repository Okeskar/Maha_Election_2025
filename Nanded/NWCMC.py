import os
import requests
from bs4 import BeautifulSoup

# HTML snippet you provided — ideally, you'd fetch this from the site live
HTML_SNIPPET = """
<div class="card-container">
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/94609.jpg" target="_blank" class="card">प्रभाग क्र. 01 - तरोडा खुर्द</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/61016.jpg" target="_blank" class="card">प्रभाग क्र. 02 - तरोडा बु</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/90539.jpg" target="_blank" class="card">प्रभाग क्र. 03 - सांगवी</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/48447.jpg" target="_blank" class="card">प्रभाग क्र. 04 - हनुमानगढ</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/36220.jpg" target="_blank" class="card">प्रभाग क्र. 05 - भाग्यनगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/52419.jpg" target="_blank" class="card">प्रभाग क्र. 06 - गणेशनगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/48953.jpg" target="_blank" class="card">प्रभाग क्र. 07 - जयभींनगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/28346.jpg" target="_blank" class="card">प्रभाग क्र. 08 - शिवाजीनगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/16511.jpg" target="_blank" class="card">प्रभाग क्र. 09 - नवामोंढा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/72612.jpg" target="_blank" class="card">प्रभाग क्र. 10 - दत्तनगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/92808.jpg" target="_blank" class="card">प्रभाग क्र. 11 - हैदरबाग</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/82136.jpg" target="_blank" class="card">प्रभाग क्र. 12 - उमर कॉलनी</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/41920.jpg" target="_blank" class="card">प्रभाग क्र. 13 - मंढई / चौफाळा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/48898.jpg" target="_blank" class="card">प्रभाग क्र. 14 - इतवारा / मदिनानगर</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/97940.jpg" target="_blank" class="card">प्रभाग क्र. 15 - होळी</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/60739.jpg" target="_blank" class="card">प्रभाग क्र. 16 - वजिराबाद / गाडीपुरा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/37182.jpg" target="_blank" class="card">प्रभाग क्र. 17 - गुरुद्वारा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/44155.jpg" target="_blank" class="card">प्रभाग क्र. 18 - खडकपुरा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/74828.jpg" target="_blank" class="card">प्रभाग क्र. 19 - वसरणी / कौठा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/39699.jpg" target="_blank" class="card">प्रभाग क्र. 20 - सिडको / वाघाळा</a>
  <a href="https://nwcmc.gov.in/web/upload_files/website/election_docs/53999.pdf" target="_blank" class="card">एकत्रित नकाशा</a>
</div>
"""

# Output folder
output_folder = r"C:\Onkar\Swapnil\Election maps\NWCMC"
os.makedirs(output_folder, exist_ok=True)

# Parse the HTML
soup = BeautifulSoup(HTML_SNIPPET, "html.parser")
links = soup.find_all("a", class_="card")

# Download each file
for link in links:
    url = link['href']
    name = link.get_text(strip=True)

    # Get file extension
    ext = os.path.splitext(url)[1]
    safe_name = name.replace("/", "-").replace("\\", "-").replace(":", "-")
    filename = f"{safe_name}{ext}"
    filepath = os.path.join(output_folder, filename)

    try:
        print(f"Downloading: {filename}")
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"Saved: {filepath}")
        else:
            print(f"Failed to download {url} — HTTP {resp.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

print("✅ All files processed.")
