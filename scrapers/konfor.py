from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import get_product_by_url, insert_product, update_product, insert_price, insert_variant, delete_variants
import time
import random


def scrape_konfor():
    driver = webdriver.Chrome(
        service=Service(
            executable_path="./chromedriver"
        )
    )

    driver.set_page_load_timeout(300)

    driver.get("https://konfor.pk/")
    
    
    category_id = "t4s-nav-ul"
    product_name = "t4s-product__title"
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, category_id))
    )
    
    category_element = driver.find_element(By.ID, category_id)
    
    category_links = category_element.find_elements(By.TAG_NAME, "a")
    
    categories = []
    links = []
    product_data = []
    
    for item in category_links[:8]:
        category_name = item.get_attribute("textContent").strip()
        category_href = item.get_attribute("href")
        
        categories.append({
            'Category': category_name,
            'Link': category_href
        })
        
    for link in categories:
        driver.get(link['Link'])
        
        time.sleep(random.uniform(2, 4))
        
        products = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.t4s-full-width-link[href]"))
        )
        
        for p in products:
            product_link = p.get_attribute("href")
            links.append({
                'URL': product_link,
                'Category': link['Category']
            })
    
    for item in links:
        driver.get(item['URL'])
        
        time.sleep(random.uniform(2, 4))
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_name))
        )
        
        name = driver.find_element(By.CLASS_NAME, product_name).text
        
        sale_price = driver.find_element(By.CSS_SELECTOR, "div.t4s-product-price ins").text
        
        original_price = driver.find_element(By.CSS_SELECTOR, "div.t4s-product-price del").text
        
        variant_elements = driver.find_elements(By.CSS_SELECTOR, '[data-swatch-item]')

        variants = []

        for v in variant_elements:

            variant_name = v.get_attribute("data-value")
            classes = v.get_attribute("class")

            if "is--soldout" in classes:
                stock_status = "out of stock"
            else:
                stock_status = "in stock"

            variants.append({
                "variant": variant_name,
                "stock_status": stock_status
            })

        description = driver.find_element(By.CSS_SELECTOR, "div.t4s-rte.t4s-tab-content").text
        
        product_data.append({
            'Name': name,
            'URL': item['URL'],
            'Category': item['Category'],
            'Price': sale_price,
            'Original Price': original_price,
            'Variants': variants,
            'Description': description
        })
        
        existing_product = get_product_by_url(item['URL'])
        
        if existing_product:
            product_id = existing_product[0]
            update_product(product_id, name, description, item['Category'])
            insert_price(product_id, sale_price, original_price)
            delete_variants(product_id)
            
            for var in variants:
                insert_variant(product_id, var['variant'], var['stock_status'])
        else:
            product_id = insert_product(name, item['URL'], description, item['Category'])
            insert_price(product_id, sale_price, original_price)
            
            for var in variants:
                insert_variant(product_id, var['variant'], var['stock_status'])
    
    for c in categories:
        print(c)
    print(f'Total Categories: {len(categories)}')
    
    for l in links:
        print(l)
    print(f'Total Product Links: {len(links)}')
    
    for p in product_data:
        print(p)
    print(f'Total Products: {len(product_data)}')
    
    driver.quit()