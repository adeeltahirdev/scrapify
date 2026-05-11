from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    service=Service(
        executable_path="../chromedriver"
    )
)

driver.set_page_load_timeout(300)

driver.get("https://surteez.com/")

menu_btn = ".mobile-menu__button--burger"
all_products = ".main-buttons__item"
category = "list-collections-section__container"

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

products_btn.click()

category_elements = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, category))
)

category_links = category_elements.find_elements(By.TAG_NAME, "a")

categories = []

for item in category_links:
    category_name = item.text.strip()
    category_href = item.get_attribute("href")
    categories.append({
        'Category': category_name,
        'Link': category_href
    })
    
for c in categories:
    print(c)
print(f'Toatal Categories: {len(categories)}')

driver.quit()