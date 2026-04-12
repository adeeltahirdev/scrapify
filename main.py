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
product = "grid-product__link"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, shops))
)

shop = driver.find_element(By.CLASS_NAME, shops)
shop.click()

products = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, product))
)

i = 1

for p in products:
    href = p.get_attribute("href")
    print(f"Link_{i}: {href}")
    i += 1
    
    

time.sleep(10)
print(driver.title)
driver.quit()