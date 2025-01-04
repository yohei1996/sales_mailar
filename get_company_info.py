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
    df = pd.read_csv('company_info.csv', encoding='utf-8')
    df_no_company_name = df[df['会社名'].isna()]
    urls = df_no_company_name['URL'].tolist()
    
    for url in urls:
        driver.get(url)
        try:
            # 会社名
            company_name_element = driver.find_elements(By.XPATH, '//*[@id="main"]/div[1]/div/h1')
            company_name = company_name_element[0].text if company_name_element else "N/A"

            # 会社URL
            company_url_element = driver.find_elements(By.XPATH, '//*[@id="main"]/div[1]/div/section[1]//tr[th[text()="URL"]]/td')
            company_url = company_url_element[0].text if company_url_element else "N/A"

            # 売上
            sales_element = driver.find_elements(By.XPATH, '//div[@class="company__info__item"]//div[span[text()="売上"]]/span[@class="td"]')
            sales = sales_element[0].text if sales_element else "N/A"

            # 従業員数
            employees_element = driver.find_elements(By.XPATH, '//div[@class="company__info__item"]//div[span[text()="従業員数"]]/span[@class="td"]')
            employees = employees_element[0].text if employees_element else "N/A"

            # 会社情報
            company_info_element = driver.find_elements(By.XPATH, '//*[@id="main"]/div[1]/div/section[1]')
            company_info = company_info_element[0].text if company_info_element else "N/A"

            # 結果をdfに反映
            df.loc[df['URL'] == url, '会社名'] = company_name
            df.loc[df['URL'] == url, '会社URL'] = company_url
            df.loc[df['URL'] == url, '売上'] = sales
            df.loc[df['URL'] == url, '従業員数'] = employees
            df.loc[df['URL'] == url, '会社情報'] = company_info

        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue

    driver.quit()

    df.to_csv('company_info.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    extract_company_info()