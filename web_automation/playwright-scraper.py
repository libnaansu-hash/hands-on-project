# lab5_playwright_scraper.py
import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_books():
    all_books = []

    async with async_playwright() as p:
        # Launch headless Chromium
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for page_num in range(1, 4):
            url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
            await page.goto(url)
            print(f'Scraping page {page_num}...')

            # ── Playwright auto-waits — no WebDriverWait needed! ──
            await page.wait_for_selector('article.product_pod')

            books = await page.query_selector_all('article.product_pod')

            for book in books:
                # Title
                title_el = await book.query_selector('h3 > a')
                title = await title_el.get_attribute('title')

                # Price
                price_el = await book.query_selector('.price_color')
                price = await price_el.inner_text()

                # Rating
                rating_el = await book.query_selector('p.star-rating')
                rating_class = await rating_el.get_attribute('class')
                rating = rating_class.split()[-1]

                # Availability
                avail_el = await book.query_selector('.availability')
                avail = (await avail_el.inner_text()).strip()

                all_books.append({
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': avail,
                    'page': page_num
                })

        await browser.close()
    return all_books


async def main():
    print('Starting Playwright scraper...')
    books = await scrape_books()
    print(f'Total books scraped: {len(books)}')

    # ── Export to CSV ─────────────────────────────────────
    with open('books_playwright.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title','price','rating','availability','page'])
        writer.writeheader()
        writer.writerows(books)

    print('Saved to books_playwright.csv')

    # ── Stats ─────────────────────────────────────────────
    prices = [float(b['price'].replace('£','')) for b in books]
    by_rating = {}
    for b in books:
        by_rating[b['rating']] = by_rating.get(b['rating'], 0) + 1
    print('Books by rating:', by_rating)
    print(f'Average price: £{sum(prices)/len(prices):.2f}')


asyncio.run(main())
