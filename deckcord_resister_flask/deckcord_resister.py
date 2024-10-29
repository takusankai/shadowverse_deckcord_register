import re
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    options.add_argument("--profile-directory=Profile 5") # どのプロフィールでも上手くいかない
    options.add_argument('--start-maximized')
    options.add_argument('--lang=ja-JP')

    # ChromeDriverのパスを指
    # driver_path = ChromeDriverManager(driver_version="127.0.6533.120").install()
    driver_path = r'/mnt/c/Users/takus/Downloads/develops/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    service = Service(driver_path, log_path='/mnt/c/Users/takus/Downloads/develops/chromedriver-win64/chromedriver.log')
    driver = webdriver.Chrome(service=service, options=options)

    # 上記がchroniumの起動だが上手くいかない、バージョン変更しても駄目、直にzip展開して指定しても上手く起動せず
    # とにかく一度たりともgmailすら開けない、ログアウトしてしまう現象も確認
    
    process_deck_input(driver, deck_code, deck_name)

def process_deck_input(driver, deck_code, deck_name):
    if not re.match(r'^[a-z0-9]{4}$', deck_code):
        return 'エラー: デッキコードは4桁の英数字（小文字限定）ではありませんでした。', 400

    driver.get(TARGET_URL)
    time.sleep(1)  # ページ遷移の待機

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