from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
import time

class Recall_Year_Data:
    def get_year_data(self):
        url = 'https://www.car.go.kr/rs/stats/rcList.do'
        driver = webdriver.Chrome()
        driver.get(url)
        search_year = ['2022','2023','2024']
        year_data = []
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
            datas = soup.select('#openTrOne > tr')
            
            for tr in datas:
                values = [i+'년'] + [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
                year_data.append(values)
        
        driver.quit()
        return year_data
    
    def year_data_preprocessing(self, year_data):
        yaer_df = pd.DataFrame(data=year_data, columns=['recall_year','recall_month','kr_recall_car','kr_recall_num','us_recall_car','us_recall_num','total_recall_car','total_recall_num'])
    
        # dtype : str -> int
        for col in ['kr_recall_car','kr_recall_num','us_recall_car','us_recall_num','total_recall_car','total_recall_num']:
            yaer_df[col] = yaer_df[col].str.replace(',','').astype(int)
        return yaer_df

    def get_year_df(self):
        return self.recall_year_df

    def __init__(self):
        self.recall_year_df = self.year_data_preprocessing(self.get_year_data())