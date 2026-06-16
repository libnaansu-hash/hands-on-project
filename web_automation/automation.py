# lab3_form_automation.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)   # wait up to 10 seconds

try:
    # ── 1. Open form page ────────────────────────────────
    driver.get('https://demoqa.com/automation-practice-form')
    print('Page loaded:', driver.title)

    # ── 2. Fill First Name ────────────────────────────────
    first_name = wait.until(EC.presence_of_element_located((By.ID, 'firstName')))
    first_name.send_keys('Aspire')

    # ── 3. Fill Last Name ─────────────────────────────────
    driver.find_element(By.ID, 'lastName').send_keys('Student')

    # ── 4. Fill Email ─────────────────────────────────────
    driver.find_element(By.ID, 'userEmail').send_keys('student@aspireai.com')

    # ── 5. Select Gender ─────────────────────────────────
    # Click the Male radio button using JavaScript (avoids click interception)
    male_radio = driver.find_element(By.CSS_SELECTOR, 'label[for="gender-radio-1"]')
    driver.execute_script('arguments[0].click();', male_radio)

    # ── 6. Fill Mobile Number ─────────────────────────────
    driver.find_element(By.ID, 'userNumber').send_keys('9876543210')

    # ── 7. Fill Current Address ───────────────────────────
    driver.find_element(By.ID, 'currentAddress').send_keys(
        '123 Automation Street, Python City, 600001'
    )

    # ── 8. Take a screenshot before submitting ───────────
    driver.save_screenshot('lab3_before_submit.png')
    print('Form filled — screenshot saved')

    # ── 9. Scroll to and click Submit ─────────────────────
    submit_btn = driver.find_element(By.ID, 'submit')
    driver.execute_script('arguments[0].scrollIntoView();', submit_btn)
    time.sleep(0.5)
    driver.execute_script('arguments[0].click();', submit_btn)

    # ── 10. Verify success modal appeared ─────────────────
    success = wait.until(EC.visibility_of_element_located((By.ID, 'example-modal-sizes-title-lg')))
    print('Success message:', success.text)
    driver.save_screenshot('lab3_success.png')

except Exception as e:
    print('Error:', e)
    driver.save_screenshot('lab3_error.png')

finally:
    time.sleep(2)
    driver.quit()
    print('Done!')
