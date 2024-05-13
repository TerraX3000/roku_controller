from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import time
import yaml 
import os 

def send_log_info_to_streamlit(log_info, streamlit_url):
    # Set up Selenium WebDriver
    config = get_app_config()
    chromedriver_path = config.get("chromedriver_path")
    if chromedriver_path:
        executable_path = chromedriver_path
    else:
        executable_path = binary_path
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    service = webdriver.ChromeService(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the Streamlit app
        driver.get(streamlit_url + "&log=" + log_info)
        # Wait for some time to ensure the request is completed
        time.sleep(5)

    finally:
        driver.quit()


def get_config_file_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file_name = "roku_controller_config.yaml"
    config_file_path = os.path.join(script_dir, config_file_name)
    return config_file_path

def get_app_config():
    config_file_path = get_config_file_path()
    print(config_file_path)
    with open(config_file_path) as f:
        config = yaml.safe_load(f)
    return config