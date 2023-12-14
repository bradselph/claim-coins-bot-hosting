from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import sys
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-data-dir=YOUR_USER_DATA_PATH')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36')
chrome_path = r'YOUR_CHROME_PATH'
chrome_options.binary_location = chrome_path
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://bot-hosting.net/panel/earn')
time.sleep(5)
while True:
    check_break = False
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'You can claim free coins again in')]")
        check_break = True
    except:
        pass
    if check_break == True:
        break

    check_captcha = False
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-hcaptcha-widget-id]")
        check_captcha = True
    except:
        pass

    if check_captcha == True:
        print("Press any key when done captcha...")
        os.system("pause >nul")
        button = driver.find_element(By.XPATH, "//button[@class='btn green']")
        button.click()
        close = driver.find_element(By.XPATH, "//div[@class='modal-content']").find_element(By.TAG_NAME, 'span')
        close.click()

    else:
        button = driver.find_element(By.XPATH, "//button[@class='btn green']")
        button.click()
        close = driver.find_element(By.XPATH, "//div[@class='modal-content']").find_element(By.TAG_NAME, 'span')
        close.click()

    for i in range(16, 0, -1):
        if i == 1:
            clock = f"Waiting for {i} second."
        else:
            clock = f"Waiting for {i} seconds."
        sys.stdout.write("\r" + clock)
        sys.stdout.flush()
        time.sleep(1)

    verify = driver.find_element(By.XPATH, "//button[@class='swal-button swal-button--confirm']")
    verify.click()

    os.system("cls")
driver.quit()
print("Done!")
os.system("pause")
