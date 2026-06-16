# lab1_verify.py — Verify your setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright

print('Selenium import: OK')

# Quick Playwright check
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    print('Playwright launched:', page.title())
    browser.close()

print('Setup complete! You are ready for Lab 2.')
