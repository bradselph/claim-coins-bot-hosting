import os
import sys
import time
import winreg
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def get_chrome_path():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe')
        chrome_path = winreg.QueryValue(registry_key, None)
        winreg.CloseKey(registry_key)
        return chrome_path
    except Exception as e:
        print(f"Failed to get Chrome path: {e}")
        sys.exit(1)

def get_user_data_path():
    user_profile = os.getenv("USERPROFILE")
    default_path = os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data")
    if os.path.exists(default_path):
        return default_path
    else:
        print(f"Default Chrome user data path not found: {default_path}")
        sys.exit(1)

def main():
    try:
        # Install required packages
        install_package('selenium')
        install_package('webdriver-manager')

        # Prompt the user for the hCaptcha accessibility token
        accessibility_token = input("Please enter your hCaptcha accessibility token: ")

        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        user_data_path = get_user_data_path()
        chrome_options.add_argument(f'--user-data-dir={user_data_path}')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36')

        # Get the Chrome binary path
        chrome_path = get_chrome_path()
        chrome_options.binary_location = chrome_path

        # Set up ChromeDriver using webdriver-manager
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Add your hCaptcha accessibility token to the browser's cookies
        driver.get('https://www.hcaptcha.com/')
        driver.add_cookie({'name': 'hc_accessibility', 'value': accessibility_token})
        driver.get('https://bot-hosting.net/panel/earn')
        time.sleep(5)
        
        while True:
            check_break = False
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'You can claim free coins again in')]")
                check_break = True
            except:
                pass
            if check_break:
                break

            check_captcha = False
            try:
                driver.find_element(By.CSS_SELECTOR, "[data-hcaptcha-widget-id]")
                check_captcha = True
            except:
                pass

            if check_captcha:
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

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
