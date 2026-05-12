from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import get_product_by_url, insert_product, update_product, insert_price, insert_variant, delete_variants
import time
import random



def scrape_surteez():
    driver = webdriver.Chrome(
        service=Service(
            executable_path="./chromedriver"
        )
    )

    driver.set_page_load_timeout(300)

    driver.get("https://surteez.com/")

    menu_btn = ".mobile-menu__button--burger"
    all_products = ".main-buttons__item"
    category = "list-collections-section__container"
    product_link_class = "product__media__holder"
    product_name = "product__title"
    variant = ".select-popout__option"
    description_class = "product__description"

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "app-embed-container-783829"))
        )
        
        overlay = driver.find_element(By.ID, "app-embed-container-783829")
        driver.execute_script("arguments[0].style.display = 'none';", overlay)
        
        print('overlay removed')
        
    except:
        print('overlay not found')
        
        
    menu_butn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, menu_btn))
    )

    menu_butn.click()

    products_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, all_products))
    )

    driver.execute_script("arguments[0].click();", products_btn)

    category_elements = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, category))
    )

    category_links = category_elements.find_elements(By.TAG_NAME, "a")

    categories = []
    links = []
    product_data = []

    for item in category_links:
        category_name = item.get_attribute("textContent").strip()
        category_href = item.get_attribute("href")
        categories.append({
            'Category': category_name,
            'Link': category_href
        })
        
    for link in categories:
        driver.get(link['Link'])
        
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, product_link_class))
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
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_name))
        )
        
        name = driver.find_element(By.CLASS_NAME, product_name).text
        
        try:
            sale_price = driver.find_element(
                By.CLASS_NAME,
                "product__price--regular"
            ).text.strip()

            try:
                original_price = driver.find_element(
                    By.CLASS_NAME,
                    "product__price--compare"
                ).text.strip()
            except:
                original_price = None

        except:
            sale_price = driver.find_element(
                By.CLASS_NAME,
                "product__price"
            ).text.strip()

            original_price = None
            
        variant_elements = driver.find_elements(By.CSS_SELECTOR, variant)
        
        variants = []
        
        for v in variant_elements:
            variant_name = v.get_attribute("data-value")
            classes = v.get_attribute("class")
            
            if "unavailable" in classes:
                stock_status = "out of stock"
            else:
                stock_status = "in stock"
                
            variants.append({
                'variant': variant_name,
                'stock_status': stock_status
            })
            
        description = driver.find_element(By.CLASS_NAME, description_class).text.strip()

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
    print(f'Toatal Categories: {len(categories)}')
    
    for l in links:
        print(l)
    print(f'Total Products: {len(links)}')
    
    for p in product_data:
        print(p)
    print(f'Total Products Data: {len(product_data)}')

    driver.quit()