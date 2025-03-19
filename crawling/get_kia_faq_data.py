from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

class Kia_Faq:
    def get_kia_faq(self):
        url = 'https://www.kia.com/kr/customer-service/center/faq'
        driver = webdriver.Chrome()
        driver.get(url)
        
        # 차량 구매 관련 FAQ 탭 클릭 (탭 변경)
        try:
            wait = WebDriverWait(driver, 10)
            purchase_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-list"]/li[3]/button')))
            purchase_tab.click()
            time.sleep(1)  # 탭 변경 후 대기
        except Exception as e:
            print(" '차량 구매' 탭 클릭이 되지 않았습니다!!!:", e)
            driver.quit()
            exit()
        
        # 데이터 저장용 리스트
        kia_faq_data = []
        
        # 차량 구매 관련 FAQ 1~4페이지 크롤링 루프
        for page in range(1, 4):  # 1~3 페이지 반복
            # print(f"현재 {page}페이지 크롤링 중...")
        
            # 현재 페이지의 FAQ 목록 가져오기
            faq_items = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
        
            for i, item in enumerate(faq_items):
                try:
                    # 질문 버튼 찾기
                    question_btn = item.find_element(By.CLASS_NAME, "cmp-accordion__button")
        
                    # 스크롤 동작 및 대기
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", question_btn)
                    time.sleep(1.5) 
        
                    # 클릭해서 펼치기
                    question_btn.click()
                    time.sleep(1)  # 답변이 펼쳐질 시간 대기
        
                    # 질문 가져오기
                    question = question_btn.text.strip()
        
                    # 답변 긁어오기 cmp-accordion__panel
                    answer_panel = item.find_element(By.CLASS_NAME, "cmp-accordion__panel")
                    answer = answer_panel.text.strip()
        
                    kia_faq_data.append({"kia_question": question, "kia_answer": answer})
        
                    # print(f" {page}페이지 {i+1}번째 질문 크롤링 완료") 
        
                except Exception as e:
                    print(f" {page}페이지 {i+1}번째 질문 크롤링 오류:", e)
                    continue
        
            # 다음 페이지로 이동 (4페이지에서는 이동하지 않는다)
            if page < 4:
                try:
                    next_page_xpath = f'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/ul/li[{page+1}]/a'
                    next_page_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_page_xpath)))
        
                    # 스크롤 이동 및 대기
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_page_btn)
                    time.sleep(1.5) 
        
                    next_page_btn.click()
                    time.sleep(1)  # 페이지 로딩 대기
                except Exception as e:
                    print(f" {page}페이지에서 {page+1}페이지로 이동 실패:", e)
                    break
        
        # FAQ 페이지로 돌아가서 '신차' 검색
        try:
            # FAQ 페이지로 돌아가서 검색창에 "신차" 입력
            search_box_xpath = '//*[@id="searchName"]'  # 검색창의 XPATH
            search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))
            
            # 기존 텍스트 삭제 후 "신차" 입력
            search_box.clear()
            search_box.send_keys("신차")
            search_box.send_keys(Keys.ENTER)  # Enter 키 입력
            
            time.sleep(3)  # 검색 결과 로딩 대기
            #print("'신차' 검색 완료!")
        
            # 신차 검색 결과 크롤링 루프
            faq_items = driver.find_elements(By.CLASS_NAME, "cmp-accordion__item")
        
            for i, item in enumerate(faq_items):
                try:
                    # 질문 버튼 찾기
                    question_btn = item.find_element(By.CLASS_NAME, "cmp-accordion__button")
        
                    # 스크롤 동작 및 대기
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", question_btn)
                    time.sleep(1.5) 
        
                    # 클릭해서 펼치기
                    question_btn.click()
                    time.sleep(1)  # 답변이 펼쳐질 시간 대기
        
                    # 질문 가져오기
                    question = question_btn.text.strip()
        
                    # 답변 긁어오기 cmp-accordion__panel
                    answer_panel = item.find_element(By.CLASS_NAME, "cmp-accordion__panel")
                    answer = answer_panel.text.strip()
        
                    kia_faq_data.append({"kia_question": question, "kia_answer": answer})
        
                    # print(f"신차 검색 결과 {i+1}번째 질문 크롤링 완료") 
        
                except Exception as e:
                    print(f"신차 검색 결과 {i+1}번째 질문 크롤링 오류:", e)
                    continue
        
        except Exception as e:
            print("'신차' 검색 오류:", e)
        driver.quit()
        return kia_faq_data
    
    def kia_faq_preprocessing(self, kia_faq_data):
        kia_faq_df = pd.DataFrame(kia_faq_data)
        
        # 필요없는 텍스트 제거
        kia_faq_df['kia_answer'] = kia_faq_df['kia_answer'].str.replace('바로가기 >', '')
        kia_faq_df['kia_answer'] = kia_faq_df['kia_answer'].str.replace('자세한 내용은 아래 링크를 클릭해 주세요.', '')
        kia_faq_df['kia_answer'] = kia_faq_df['kia_answer'].str.replace('EV & PBV 카탈로그/가격표 ', '')
        kia_faq_df['kia_answer'] = kia_faq_df['kia_answer'].str.replace('(구매보조금 지급 상한액은 아래표를 참고해주세요.)', '')
        kia_faq_df['kia_answer'] = kia_faq_df['kia_answer'].str.replace('시승 신청 바로가기 >', '')
        return kia_faq_df

    def get_kia_faq_df(self):
        return self.kia_faq_df

    def __init__(self):
        self.kia_faq_df = self.kia_faq_preprocessing(self.get_kia_faq())