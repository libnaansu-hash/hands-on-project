# lab4_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# ── Setup ────────────────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run without opening a window
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
wait = WebDriverWait(driver, 10)

all_books = []   # Store all scraped books here

try:
    # ── Loop through first 3 pages ───────────────────────
    for page_num in range(1, 4):
        url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
        driver.get(url)
        print(f'Scraping page {page_num}...')

        # Wait for book items to load
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'article.product_pod')
        ))

        # Get all book cards on this page
        books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')

        for book in books:
            # ── Extract title ─────────────────────────────
            title_el = book.find_element(By.CSS_SELECTOR, 'h3 > a')
            title = title_el.get_attribute('title')

            # ── Extract price ─────────────────────────────
            price = book.find_element(By.CSS_SELECTOR, '.price_color').text

            # ── Extract rating ────────────────────────────
            rating_el = book.find_element(By.CSS_SELECTOR, 'p.star-rating')
            rating_class = rating_el.get_attribute('class')  # e.g. 'star-rating Three'
            rating_word = rating_class.split()[-1]           # e.g. 'Three'

            # ── Extract availability ──────────────────────
            availability = book.find_element(By.CSS_SELECTOR, '.availability').text.strip()

            all_books.append({
                'title': title,
                'price': price,
                'rating': rating_word,
                'availability': availability,
                'page': page_num
            })

        time.sleep(0.5)   # polite delay between pages

    print(f'Total books scraped: {len(all_books)}')

except Exception as e:
    print('Scraping error:', e)

finally:
    driver.quit()

# ── Export to CSV ────────────────────────────────────────
if all_books:
    with open('books_data.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'price', 'rating', 'availability', 'page']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books)
    print('Data saved to books_data.csv')
    print('Open this file in Excel or Google Sheets!')

    # ── Quick summary ──────────────────────────────────
    prices = [float(b['price'].replace('£','')) for b in all_books]
    print(f'Cheapest book: £{min(prices):.2f}')
    print(f'Most expensive: £{max(prices):.2f}')
    print(f'Average price: £{sum(prices)/len(prices):.2f}')
