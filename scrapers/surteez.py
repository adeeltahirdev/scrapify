from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        product_data.append({
            'Name': name,
            'URL': item['URL'],
            'Category': item['Category']
        })
        
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