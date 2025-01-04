from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pandas as pd

def extract_company_info():
    # Chromeオプションの設定
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # ヘッドレスモードで実行する場合はコメントを外す
    service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://biz-maps.com/s/prefs/13")
        user_input = input("URLを取得を開始しますか？ (y/n): ")
        if user_input.lower() != 'y':
            print("URL取得をキャンセルしました。")
            return

        urls = []
        page_count = 0
        while page_count < 5:
            company_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'results__item')]//a"))
            )
            urls.extend([el.get_attribute('href') for el in company_elements])

            try:
                time.sleep(2)  # ページがロードされるのを待つ
                next_button = driver.find_element(By.XPATH, "//li[@class='page-item next']/a")
                next_button_url = next_button.get_attribute('href')
                driver.get(next_button_url)
                page_count += 1
            except Exception as e:
                print("次のページが見つかりません。終了します。")
                break

        df = pd.read_csv('company_info.csv', encoding='utf-8')
        new_urls = [url for url in urls if url not in df['URL'].values]
        new_df = pd.DataFrame(new_urls, columns=['URL'])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv('company_info.csv', index=False, encoding='utf-8')

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        # ブラウザを閉じる
        driver.quit()

if __name__ == "__main__":
    extract_company_info()