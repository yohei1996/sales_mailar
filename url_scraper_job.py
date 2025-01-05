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
        # ◆ 対象サイトをTownWorkに変更
        driver.get("https://townwork.net/tokyo/jc_003/")
        user_input = input("URLを取得を開始しますか？ (y/n): ")
        if user_input.lower() != 'y':
            print("URL取得をキャンセルしました。")
            return

        # ◆ すでに保存されたURLを重複チェックするために読み込む
        df = pd.read_csv('company_info_job.csv', encoding='utf-8')
        existing_urls = set(df['URL'].values)

        urls = []
        page_count = 0

        # ◆ ここではサンプルとして5ページ分だけ取得する
        while page_count < 5:
            # ◆ 「詳細を見る」のリンクをXPathで取得
            #   以下では例として「* 詳細を見る」あるいは「詳細を見る」のテキストを含む aタグをすべてピックアップ
            detail_links = driver.find_elements(By.XPATH, "//a[contains(text(),'詳細を見る')]")

            # ◆ 各リンクのhrefを抽出してリストに追加
            for link_el in detail_links:
                url = link_el.get_attribute('href')
                if url and url not in existing_urls:
                    urls.append(url)

            # ◆ 次のページがある場合はクリックor getする（TownWorkの場合）
            #   例: //a[contains(text(),'次のページへ')] を想定
            try:
                time.sleep(2)  # ページがロードされるのを待つ(任意)
                next_button = driver.find_element(By.XPATH, "//a[contains(text(),'次のページへ')]")
                if next_button:
                    next_url = next_button.get_attribute('href')
                    driver.get(next_url)
                    page_count += 1
                else:
                    print("次のページリンクが見つかりません。終了します。")
                    break
            except Exception:
                print("次のページが見つからないか、読み込みに失敗しました。終了します。")
                break

        # ◆ 取得したURLを新規に DataFrame にまとめる
        new_urls_df = pd.DataFrame(urls, columns=['URL'])
        # ◆ CSVに書き込む前に既存行と結合し重複排除
        updated_df = pd.concat([df, new_urls_df], ignore_index=True).drop_duplicates(subset=['URL'], keep='first')
        updated_df.to_csv('company_info_job.csv', index=False, encoding='utf-8')
        print(f"{len(urls)} 件の新規URLを取得しました。 company_info.csv へ追加済みです。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        # ブラウザを閉じる
        driver.quit()

if __name__ == "__main__":
    extract_company_info()