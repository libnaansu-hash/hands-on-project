# lab6_price_monitor.py  — Simple price monitor
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

# ── Configuration ────────────────────────────────────────
TARGET_BOOK_URL = (
    'https://books.toscrape.com/catalogue/'
    'a-light-in-the-attic_1000/index.html'
)
PRICE_ALERT_THRESHOLD = 55.00   # Alert if price drops below £55
CHECK_INTERVAL_SECONDS = 30     # Check every 30 seconds (demo mode)


async def get_price(page) -> float:
    """Navigate to the book page and extract the current price."""
    await page.goto(TARGET_BOOK_URL)
    await page.wait_for_selector('.price_color')
    price_text = await page.inner_text('.price_color')
    return float(price_text.replace('£', '').strip())


async def monitor():
    print('Price Monitor Started!')
    print(f'Checking: {TARGET_BOOK_URL}')
    print(f'Alert threshold: £{PRICE_ALERT_THRESHOLD}')
    print(f'Check interval: every {CHECK_INTERVAL_SECONDS}s')
    print('-' * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        checks = 0

        try:
            while checks < 5:   # Run 5 checks for demo
                checks += 1
                now = datetime.now().strftime('%H:%M:%S')

                try:
                    price = await get_price(page)
                    print(f'[{now}] Check #{checks}  Price: £{price:.2f}', end='  ')

                    if price < PRICE_ALERT_THRESHOLD:
                        print('  🔔 ALERT! Price dropped below threshold!')
                    else:
                        print(f'  (above threshold of £{PRICE_ALERT_THRESHOLD})')

                except Exception as e:
                    print(f'[{now}] Error fetching price: {e}')

                if checks < 5:
                    print(f'  Waiting {CHECK_INTERVAL_SECONDS}s before next check...')
                    await asyncio.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print('Monitor stopped by user.')

        finally:
            await browser.close()
            print('Monitor complete!')


asyncio.run(monitor())
