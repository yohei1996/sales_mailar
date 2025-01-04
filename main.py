from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def google_search():
    # Chromeオプションの設定
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # ヘッドレスモードで実行する場合はコメントを外す
    
    # ChromeDriverServiceの設定
    service = Service(executable_path="./chromedriver")
    
    # Chromeドライバーの初期化
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Googleのトップページにアクセス
        driver.get("https://www.google.com")
        
        # 検索ボックスを見つけて「生成AI」と入力
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("生成AI")
        search_box.send_keys(Keys.RETURN)
        
        # 検索結果が表示されるまで少し待機
        time.sleep(3)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        # ブラウザを閉じる
        driver.quit()

if __name__ == "__main__":
    google_search()