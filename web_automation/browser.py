# lab2_selenium_browser.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ── 1. Launch Chrome ────────────────────────────────────
# ChromeDriverManager downloads the right driver automatically
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment to run without window
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print('Browser launched!')

# ── 2. Navigate to a page ────────────────────────────────
driver.get(''https://books.toscrape.com')
print('Page title:', driver.title)

# ── 3. Find elements ─────────────────────────────────────
# Find the first book title on the page
first_book = driver.find_element(By.CSS_SELECTOR, 'article.product_pod h3 a')
print('First book:', first_book.get_attribute('title'))

# Find ALL book price elements
prices = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod .price_color')
print(f'Found {len(prices)} prices on this page')
print('First price:', prices[0].text)

# ── 4. Interact — scroll to the element ──────────────────
driver.execute_script('arguments[0].scrollIntoView();', first_book)
time.sleep(1)   # brief pause so we can see it

# ── 5. Take a screenshot ─────────────────────────────────
driver.save_screenshot('lab2_screenshot.png')
print('Screenshot saved as lab2_screenshot.png')

# ── 6. Clean up ──────────────────────────────────────────
driver.quit()
print('Browser closed. Lab 2 complete!')
