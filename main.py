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
product_original_price = "product__price--compare"
product_sale_price = "sale-price"
product_price = "product__price"
ul_tag = "tags--vertical"

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, shops))
)

shop = driver.find_element(By.CLASS_NAME, shops)
shop.click()

ctg = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, ul_tag))
)


ctg_links = ctg.find_elements(By.TAG_NAME, "a")


categories = []
links = []
products_data = []

for c in ctg_links:
    ctg_name = c.text.strip()
    ctg_href = c.get_attribute("href")
    categories.append({
        'Category': ctg_name,
        'Link': ctg_href
    })
    
print(len(categories))
for ct in categories:
    print(ct)

for lnks in categories:
    driver.get(lnks['Link'])
    
    products = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, product))
    )
    
    for p in products:
        product_href = p.get_attribute("href")
        links.append(product_href)

for l in links:
    print(f"Product_Links: {l}")
print(len(links))

for link in links:
    driver.get(link)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, product_name))
    )
    
    name = driver.find_element(By.CLASS_NAME, product_name).text
    
    sale_element = driver.find_element(By.CLASS_NAME, product_sale_price)
    
    if sale_element:
        original_price = driver.find_element(By.CLASS_NAME, product_original_price).text
        sale_price = driver.find_element(By.CLASS_NAME, product_sale_price).text

        products_data.append({
            'Product Name': name,
            'Original Price': original_price,
            'Sale Price': sale_price,
            'Product Link': link
        })
        
for data in products_data:
    print(data)
print(len(products_data))
        
driver.quit()