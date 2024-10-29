import pyautogui
import time

def main():
    print("スクリプトを開始します")

    # 画面全体のサイズを取得
    screenWidth, screenHeight = pyautogui.size()
    print(f"画面のサイズ: ({screenWidth}, {screenHeight})")

    # マウスの初期位置を取得して表示
    initialMouseX, initialMouseY = pyautogui.position()
    print(f"初期マウスの位置: ({initialMouseX}, {initialMouseY})")

    # 初めにマウス座標を画面の中心に移動
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
    time.sleep(1)  # 1秒待機

    # マウスの移動後の位置を取得して表示
    currentMouseX, currentMouseY = pyautogui.position()
    print(f"移動後のマウスの位置: ({currentMouseX}, {currentMouseY})")

    # 左クリック
    pyautogui.click()
    time.sleep(1)  # 1秒待機

    # キーボードのAキーを押す
    pyautogui.press('a')
    time.sleep(1)  # 1秒待機

    print("スクリプトを終了します")

# メイン処理
if __name__ == '__main__':
    main()