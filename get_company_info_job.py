import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_company_info():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # ヘッドレスモードで実行する場合はコメントを外す
    
    service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # ◆ CSVを読み込み、まだ会社名が取得されていないURLのみ抽出
    df = pd.read_csv('company_info_job.csv', encoding='utf-8')
    if '会社名' not in df.columns:
        df['会社名'] = None
    if '会社事業内容' not in df.columns:
        df['会社事業内容'] = None
    if 'ホームページリンク' not in df.columns:
        df['ホームページリンク'] = None

    df_no_company_name = df[df['会社名'].isna()]
    urls = df_no_company_name['URL'].tolist()
    
    for url in urls:
        driver.get(url)
        try:
            # Extract the company name
            company_name_element = driver.find_elements(By.XPATH, "//div[@class='job-detail-box-data']//dt[contains(text(),'社名')]/following-sibling::dd/p")
            company_name = company_name_element[0].text.strip() if company_name_element else "N/A"

            # Extract the business content
            business_content_element = driver.find_elements(By.XPATH, "//div[@class='job-detail-box-data']//dt[text()='会社事業内容']/following-sibling::dd/p")
            company_business = business_content_element[0].text.strip() if business_content_element else "N/A"

            # Extract the homepage link
            homepage_link_element = driver.find_elements(By.XPATH, "//div[@class='job-detail-box-data']//dt[text()='ホームページリンク']/following-sibling::dd/a")
            homepage_link = homepage_link_element[0].get_attribute('href') if homepage_link_element else "N/A"

            # データフレームへ反映
            df.loc[df['URL'] == url, '会社名'] = company_name
            df.loc[df['URL'] == url, '会社事業内容'] = company_business
            df.loc[df['URL'] == url, 'ホームページリンク'] = homepage_link

            print(f"[SUCCESS] {url} の情報を取得しました。")

        except Exception as e:
            print(f"[ERROR] {url} のスクレイピング中にエラー: {e}")
            continue

    driver.quit()

    # ◆ CSVファイルを上書き
    df.to_csv('company_info_job.csv', index=False, encoding='utf-8')
    print("すべてのURLに対してスクレイプを試行し、結果を company_info.csv に保存しました。")

if __name__ == "__main__":
    extract_company_info()