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

class Hyundai_Faq:
    def get_hyundai_faq(self):
        URL = "https://www.hyundai.com/kr/ko/e/customer/center/faq"
    
        driver = webdriver.Chrome()
        driver.get(URL)
        # 리스트에 딕셔너리로 내용 저장
        hyundai_faq_data = []
        
        for page_id in range(4):
            for question_id in range(1,11):
                try:
                    #엘리먼트 찾기
                    faq_list = driver.find_element(By.CSS_SELECTOR, "div[data-v-28d34f54].list-wrap")
        
                    try:
                        # 플로팅 메뉴 제거
                        floating_menu = driver.find_element(By.CSS_SELECTOR, "div[data-v-1ea4ba2d].inner_wrap")
                        driver.execute_script("arguments[0].remove();", floating_menu)
                    except:
                        pass
                    faq_title = faq_list.find_elements(By.CSS_SELECTOR,f"div[data-id='{question_id}'] button.list-title")
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",faq_title[0])
                    time.sleep(0.5)
        
                    #질문타이틀 클릭하기
                    faq_title[0].click()
                    time.sleep(0.5)
        
                    #질문타이틀 텍스트 받아오기
                    faq_question = faq_title[0].find_element(By.CSS_SELECTOR, "span.list-content[data-v-28d34f54]")
                    faq_question_text = faq_question.text
                    #print(faq_question_text)
        
                    #질문답변 텍스트 받아오기
                    faq_answer = driver.find_element(By.CLASS_NAME, "conts")
                    faq_answer_text = faq_answer.text
                    #print("전체 답변:", faq_answer_text)
                    
                    hyundai_faq_data.append({"hyundai_question": faq_question_text, "hyundai_answer": faq_answer_text})
        
                except TimeoutException:
                    print("Timed out waiting for page to load")
                except NoSuchElementException:
                    print("Could not find the element")
                except IndexError:
                    pass
        
            next_button = driver.find_element(By.CSS_SELECTOR, "button.btn-next")
            next_button.click()
            time.sleep(1)
            driver.quit()
        return hyundai_faq_data
            
    def hyundai_faq_preprocessing(self, hyundai_faq_data):
        hyundai_faq_df = pd.DataFrame(hyundai_faq_data)
        return hyundai_faq_df

    def get_hyundai_faq_df(self):
        return self.hyundai_faq_df

    def __init__(self):
        self.hyundai_faq_df = self.hyundai_faq_preprocessing(self.get_hyundai_faq())