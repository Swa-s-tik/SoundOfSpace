from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import urllib

def get_user_input():
    """Get coordinates from user"""
    return input("Enter coordinates in format of 161.265, -59.685: ")

def setup_driver():
    """Set up Chrome driver"""
    service = Service(executable_path="chromedriver.exe")
    return webdriver.Chrome(service=service)

def navigate_to_skyview(driver):
    """Navigate to SkyView website"""
    driver.get("https://skyview.gsfc.nasa.gov/current/cgi/query.pl")

def input_coords(driver, coords):
    """Input coordinates into text field"""
    input_element = driver.find_element(By.ID, "object")
    input_element.send_keys(coords)

def select_dataset(driver):
    """Select Fermi 5 dataset"""
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ROSATw/sources class=")))
    select_element = driver.find_element(By.ID, "ROSATw/sources class=")
    select = Select(select_element)
    select.select_by_visible_text("RASS-Cnt Broad")

def submit_query(driver):
    """Submit query"""
    submit_button = driver.find_element(By.XPATH, "//input[@value='Submit Request']")
    submit_button.click()

def switch_to_results_page(driver):
    """Switch to results page"""
    driver.switch_to.window(driver.window_handles[1])

def download_image(driver):
    img_element = driver.find_element(By.ID, "img1")
    # Get the image URL
    img_url = img_element.get_attribute("src")
    # Download the image
    urllib.request.urlretrieve(img_url, "image.jpg")

def main():
    coords = get_user_input()
    driver = setup_driver()
    navigate_to_skyview(driver)
    input_coords(driver, coords)
    select_dataset(driver)
    submit_query(driver)
    switch_to_results_page(driver)
    # Now you can access the results page
    print(driver.title)
    time.sleep(10)
    download_image(driver)
    driver.quit()

if __name__ == "__main__":
    main()
