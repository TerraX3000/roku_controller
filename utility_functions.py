from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import time
import yaml 


def send_log_info_to_streamlit(log_info, streamlit_url):
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the Streamlit app
        driver.get(streamlit_url + "&log=" + log_info)
        # Wait for some time to ensure the request is completed
        time.sleep(5)

    finally:
        driver.quit()

def get_app_config():
    with open("roku_controller_config.yaml") as f:
        config = yaml.safe_load(f)
    return config