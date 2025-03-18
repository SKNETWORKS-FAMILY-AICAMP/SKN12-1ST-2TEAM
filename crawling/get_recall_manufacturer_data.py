from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
import time

class Recall_Manufacturer_Data:
    def get_manufacturer_data(self):
        url = 'https://www.car.go.kr/rs/stats/rcList.do'
        driver = webdriver.Chrome()
        driver.get(url)
        search_year = ['2022','2023','2024']
        manufacturer_data = []
        for i in search_year:
            fromyear = Select(driver.find_element(By.XPATH, '//*[@id="recallYear"]'))
            fromyear.select_by_value(f'{i}')
            time.sleep(1)
            
            button = driver.find_element(By.XPATH, '//*[@id="srchBtn"]')
            button.click()
            time.sleep(1)
            
            button = driver.find_element(By.XPATH, '//*[@id="openTwoBtn"]')
            button.click()
            time.sleep(1)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            datas = soup.select('#openTrTwo > tr')
            
            for tr in datas:
                values = [i+'년'] + [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
                manufacturer_data.append(values)
        
        driver.quit()
        return manufacturer_data
    
    def manufacturer_data_preprocessing(self, manufacturer_data):
        manufacturer_df = pd.DataFrame(data=manufacturer_data, columns=['recall_year','recall_month','car_model','car_num'])
        manufacturer_df = manufacturer_df.dropna()
        manufacturer_df['recall_month'] = manufacturer_df['recall_month'].replace('소계 +소계 -', '총합')
        manufacturer_df['car_num'] = manufacturer_df['car_num'].str.replace(',','').astype(int)
        return manufacturer_df

    def get_manufacturer_df(self):
        return self.manufacturer_df

    def __init__(self):
        self.manufacturer_df = self.manufacturer_data_preprocessing(self.get_manufacturer_data())