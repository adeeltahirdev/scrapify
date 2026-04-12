from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(
    service=Service(
        executable_path="./chromedriver"
    )
)
driver.get("https://radstore.pk/")

shops = "site-nav__link"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, shops))
)

shop = driver.find_element(By.CLASS_NAME, shops)
shop.click()

time.sleep(10)
print(driver.title)
driver.quit()