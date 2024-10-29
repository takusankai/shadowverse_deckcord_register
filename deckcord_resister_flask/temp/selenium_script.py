from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_with_google():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--start-maximized')
    options.add_argument('--lang=ja-JP')
    options.add_argument(r'--user-data-dir=/mnt/c/Users/takus/AppData/Local/Google/Chrome/User Data')  # 既存のChromeプロファイルを使用
    options.add_argument('--profile-directory=Profile 5')  # プロファイルディレクトリを指定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # ユーザーエージェントを変更

    driver_path = ChromeDriverManager(driver_version="127.0.6533.120").install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('http://localhost:5000')

    login_button = driver.find_element(By.ID, 'login')
    login_button.click()

    # Googleログインページでの操作を自動化
    time.sleep(5)
    email_input = driver.find_element(By.ID, 'identifierId')
    email_input.send_keys('takusan9170@gmail.com')
    next_button = driver.find_element(By.ID, 'identifierNext')
    next_button.click()

    time.sleep(5)
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys('20022002 takusan')
    next_button = driver.find_element(By.ID, 'passwordNext')
    next_button.click()

    time.sleep(50)  # 認証が完了するまで待機

    # 認証後の処理
    print(driver.page_source)

    # driver.quit()

if __name__ == '__main__':
    login_with_google()