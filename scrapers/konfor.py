from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, category_id))
    )
    
    category_element = driver.find_element(By.ID, category_id)
    
    category_links = category_element.find_elements(By.TAG_NAME, "a")
    
    categories = []
    
    for item in category_links:
        category_name = item.get_attribute("textContent").strip()
        category_href = item.get_attribute("href")
        
        categories.append({
            'Category': category_name,
            'Link': category_href
        })
    
    for c in categories:
        print(c)
    print(f'Total Categories: {len(categories)}')
    
    
    driver.quit()