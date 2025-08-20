from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

TXT_FILE = 'name of the text file in the same folder as your code.txt'
DOWNLOAD_DIR = 'your/download/directory'
URL = 'url of the target site/page'  
#Optional-CORS workaround for skipping security stuff
#PROXY_URL = "https://cors-anywhere.herokuapp.com/"
#AD_SERVER_URL = 'https://vid.pubmatic.com/AdServer/AdServerServlet?adId=6243092&adtype=13&pubId=160998&siteId=1267822&vapi=2+7&vfmt=1+4+5+6&vadFmt=2+3+4+5+6+7+8&vtype=1&vpos=1&vw=640&vh=360&sec=1&cachebuster=15665486879682&placement=1&vplay=1+2+3+5+6&schain=1.0,1!impactify.io,2227,1,,,&vminl=1&vmaxl=90&gdpr=0&kadpageurl=https%3A%2F%2Fwww.font-generator.com%2Ffonts%2FKomikaTitle2%2F%23google_vignette'

#Chrome
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--incognito")  
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "Your download directory",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
# chrome_options.add_argument("--headless")  # Uncomment if you want headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#Open website
driver.get(URL)

#Enable if skipping CORS stuff
#cors_url = PROXY_URL + AD_SERVER_URL
#driver.get(cors_url)

with open(TXT_FILE, 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "font-preview-text")))  # Wait for the input box

for line in lines:
    try:
        #first interact/text input
        input_box = driver.find_element(By.ID, 'change this to the input field ID for the text box')
        input_box.clear()
        input_box.send_keys(line)

        #Enter button if there is any/ delete this part if there isn't
        submit_button = driver.find_element(By.ID, 'change to ID of the enter button')  
        submit_button.click()

        #Doenload button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'change to ID of the download button')) 
        )

        #Scrolls to download button if necessary
        download_button = driver.find_element(By.ID, 'change to ID of the download button') 
        driver.execute_script("arguments[0].scrollIntoView();", download_button)

        download_button.click()

        # wait for the download to complete
        time.sleep(5)

    except Exception as e:
        print(f"error '{line}': {e}")

driver.quit()
print("Donezo.")
