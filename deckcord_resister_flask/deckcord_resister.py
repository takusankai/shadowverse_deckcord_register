import re
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import os
import sys
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# 定数としてURLとクラス名を定義
TARGET_URL = 'https://shadowverse-portal.com/deckbuilder/classes?lang=ja'
DECK_CODE_INPUT_ID = '#deckCode'
SUBMIT_BUTTON_ID = '#deckImport'
DECK_NAME_INPUT_SELECTOR = 'input[name="deck_name"]'
CONFIRM_BUTTON_SELECTOR = 'button.deckbuilder-deck-save-button'

def access_portal(deck_code, deck_name):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument(r"--user-data-dir=/mnt/c/Users/takus/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Profile 2")
    options.add_argument('--start-maximized')
    options.add_argument('--lang=ja-JP')  # ロケールを日本語に設定

    # ChromeDriverのバージョンを指定
    driver_path = ChromeDriverManager(driver_version="127.0.6533.120").install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # driver = webdriver.Chrome(r'C:\Users\takus\chromedriver.exe', options=options)
    # driver = webdriver.Chrome(executable_path=r'C:\Users\takus\chromedriver.exe', options=options)
    
    process_deck_input(driver, deck_code, deck_name)
    # check_portal(driver, deck_code, deck_name)

def process_deck_input(driver, deck_code, deck_name):
    if not re.match(r'^[a-z0-9]{4}$', deck_code):
        return 'エラー: デッキコードは4桁の英数字（小文字限定）ではありませんでした。', 400

    # クッキー情報を読み込む
    with open('cookie_data.json', 'r') as file:
        cookies = json.load(file)
        driver.get(TARGET_URL)  # クッキーを追加する前に一度サイトを開く必要がある
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                del cookie['sameSite']
            driver.add_cookie(cookie)

    driver.get(TARGET_URL)
    time.sleep(2)  # ページ遷移の待機

    deck_code_input = driver.find_element(By.CSS_SELECTOR, DECK_CODE_INPUT_ID)
    deck_code_input.send_keys(deck_code)

    submit_button = driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_ID)
    submit_button.click()
    time.sleep(10)  # ページ遷移の待機

    # 現在のURLを取得
    current_url = driver.current_url

    # 確認ページにアクセス
    driver.get(current_url)
    time.sleep(10)  # ページ遷移の待機

    # テキスト欄にデッキ名を入力
    deck_name_input = driver.find_element(By.CSS_SELECTOR, DECK_NAME_INPUT_SELECTOR)
    deck_name_input.send_keys(deck_name)

    # 確認ボタンをクリック
    confirm_button = driver.find_element(By.CSS_SELECTOR, CONFIRM_BUTTON_SELECTOR)
    confirm_button.click()

    # driver.quit()
    return f'{deck_code}を{deck_name}として正常に登録しました！'

def check_portal(driver, deck_code, deck_name):

    time.sleep(5)  # ページ遷移の待機

    driver.get('https://shadowverse-portal.com/signin?lang=ja')
    time.sleep(2)  # ページ遷移の待機

    google_login_button = driver.find_element(By.XPATH, '//a[@class="signin-button is-google"]')
    google_login_button.click()
    time.sleep(2000)  # ページ遷移の待機

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    deck_code = data.get('deck_code')
    deck_name = data.get('deck_name')
    return access_portal(deck_code, deck_name)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        cli_deck_code = sys.argv[1]
        cli_deck_name = sys.argv[2]
        if re.match(r'^[a-z0-9]{4}$', cli_deck_code):
            access_portal(cli_deck_code, cli_deck_name)
            print("access_portalを実行します。")
        else:
            print('エラー: デッキコードは4桁の英数字（小文字限定）ではありませんでした。')
    else:
        print('エラー: デッキコードとデッキ名の両方が指定されませんでした。')

    app.run(host='0.0.0.0', ssl_context='adhoc')