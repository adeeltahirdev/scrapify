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

for item in categories:
    driver.get(item['Link'])
    
    products = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, product))
    )
    
    for p in products:
        product_href = p.get_attribute("href")
        links.append({
            'URL': product_href,
            'Category': item['Category']
        })

for l in links:
    print(f"Product_Links: {l}")
print(len(links))

for items in links:
    driver.get(items['URL'])
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, product_name))
    )
    
    name = driver.find_element(By.CLASS_NAME, product_name).text
    
    sale_elements = driver.find_elements(By.CLASS_NAME, product_sale_price)

    if sale_elements:
        
        sale_price = driver.find_element(By.CLASS_NAME, product_sale_price).text
        original_elements = driver.find_elements(By.CLASS_NAME, product_original_price)

        original_price = original_elements[0].text if original_elements else None

        final_price = sale_price
    else:
        
        price = driver.find_element(By.CLASS_NAME, product_price).text

        final_price = price
        original_price = None


    products_data.append({
        'name': name,
        'price': final_price,
        'original_price': original_price,
        'url': items['URL'],
        'category': items['Category']
    })
        
for data in products_data:
    print(data)
print(len(products_data))
        
driver.quit()