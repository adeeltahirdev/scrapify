from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import get_product_by_url, insert_product, update_product, insert_price, insert_variant, delete_variants, connect_db, create_tables, db_close


connect_db()
create_tables()

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
variant = "variant-input"
stock = "data-product-inventory"
description = "rte"

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
    
for ct in categories:
    print(ct)
print(len(categories))

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
    
    variants = []
    
    variant_container = driver.find_elements(By.CLASS_NAME, variant)
    
    for v in variant_container:
        value = v.get_attribute("data-value")
        
        v.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[{stock}]'))
        )
        stock_status = driver.find_element(By.CSS_SELECTOR, f'[{stock}]').text
        
        if stock_status == '':
            stock_status = 'out of stock'
        
        variants.append({
            'variant': value,
            'stock_status': stock_status
        })
        
    descriptions = ""
    
    description_elements = driver.find_elements(By.CLASS_NAME, description)

    for desc in description_elements: 
        text = desc.text.strip() 
        if len(text) > 50: 
            descriptions = text 
            break
        
            
    print(descriptions)
    
    products_data.append({
        'name': name,
        'price': final_price,
        'original_price': original_price,
        'url': items['URL'],
        'category': items['Category'],
        'Variants': variants,
        'Description': descriptions
    })
    
    existing_product = get_product_by_url(items['URL'])
    
    if existing_product:
        product_id = existing_product[0]
        update_product(product_id, name, descriptions, items['Category'])
        insert_price(product_id, final_price, original_price)
        delete_variants(product_id)
        
        for var in variants:
            insert_variant(product_id, var['variant'], var['stock_status'])
    else:
        product_id = insert_product(name, items['URL'], descriptions, items['Category'])
        insert_price(product_id, final_price, original_price)
        
        for var in variants:
            insert_variant(product_id, var['variant'], var['stock_status'])
    
for data in products_data:
    print(data)
print(len(products_data))
        
driver.quit()
db_close()