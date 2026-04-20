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
product_name = "product-single__title"
product_price = "product__price"
product_original_price = "product__price--compare"
product_sale_price = "sale-price"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, shops))
)

shop = driver.find_element(By.CLASS_NAME, shops)
shop.click()

products = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, product))
)

i = 1

links = []
products_data = []

for p in products:
    href = p.get_attribute("href")
    links.append(href)
    i += 1
    
print(len(links))

for link in links:
    driver.get(link)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, product_name))
    )
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, product_sale_price))
    )
    name = driver.find_element(By.CLASS_NAME, product_name).text
    if not product_sale_price:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_price))
        )
        price = driver.find_element(By.CLASS_NAME, product_price).text
        products_data.append({'Name': name, 'Price': price, 'URL': link})
    else:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_sale_price))
        )
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_original_price))
        )
        original_price = driver.find_element(By.CLASS_NAME, product_original_price).text
        sale_price = driver.find_element(By.CLASS_NAME, product_sale_price).text

        products_data.append({'Name': name, 'Original Price': original_price, 'Sale Price': sale_price, 'URL': link})
    

for data in products_data:
    print(data)
    
print(len(products_data))

driver.quit()