# 웹 드라이버 설정
from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager 

# 대기 관련 라이브러리
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

# 웹 요소 찾기 관련 라이브러리
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import Select  
from selenium.webdriver.common.keys import Keys  
import chromedriver_autoinstaller


# 그 외 
import time 
import warnings
warnings.filterwarnings('ignore')
from bs4 import BeautifulSoup 
import numpy as np  
import pandas as pd 
from tqdm import tqdm  


# 여기에 이름(파일명) 이 들어갑니다. 
이름 = '지선' 

original_res_df = pd.read_excel(f'data/restaurant_info_data(2)/{이름}.xlsx')
original_df = original_res_df.copy()


# 시작 인덱스 
start_num = 0
# 한번에 돌아갈 분량
num = 200  
# 마지막에 바꿔줘야하는 end_num 
end_num = start_num + num


res_df = original_df[start_num:] 
res_df = res_df.reset_index(drop=True)

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

restaurant_name_list = []
category_name_list = []
address_list = []
menu_list = []
price_list = []
visitor_review_list =[]
blog_review_list =[]


for i in range(len(res_df)):
       
    name = res_df['검색어'][i]
    driver.get('https://map.naver.com/p/search/{}'.format(name))
    time.sleep(3)  

    try :
        if driver.find_elements(By.ID,'entryIframe') :
            entryIframe = driver.find_element(By.ID,'entryIframe')
            driver.switch_to.frame(entryIframe)
            time.sleep(3) 

            restaurant_name = driver.find_element(By.CLASS_NAME,'Fc1rA').text
            category_name = driver.find_element(By.CLASS_NAME,'DJJvD').text
            address = driver.find_element(By.CLASS_NAME,'LDgIH').text
            if driver.find_elements(By.CLASS_NAME,'ihmWt') :
                menu = driver.find_element(By.CLASS_NAME,'ihmWt').text
                price = driver.find_element(By.CLASS_NAME,'mkBm3').text
            elif driver.find_elements(By.CLASS_NAME,'VQvNX') :
                menu = driver.find_element(By.CLASS_NAME,'VQvNX').text
                price = driver.find_element(By.CLASS_NAME,'Yrsei').text
            else : 
                menu = '메뉴없음'
                price = "가격없음"
            
            # 리뷰 긁어오기 
            pxmot_elements = driver.find_elements(By.CLASS_NAME, 'PXMot')
            visitor_review = 0
            blog_review = 0

            # PXMot 가 존재할 때 (별점 방문자 블로그 중  뭐라도 존재)
            if pxmot_elements:
                for element in pxmot_elements:
                    element_text = element.text
                    if element_text.startswith('별점'):
                        # 별점이 있으면 다음 요소 검사
                        continue
                    elif element_text.startswith('방문자리뷰'):
                        # 방문자 리뷰가 존재하는 경우
                        review_text = element_text.replace('방문자리뷰', '')
                        # 쉼표(,) 제거 후 정수로 변환
                        try : 
                            visitor_review = int(review_text.replace(',', '')) if ',' in review_text else int(review_text)
                        except ValueError :
                            visitor_review = 0
                    elif element_text.startswith('블로그리뷰'):
                        # 블로그 리뷰가 존재하는 경우
                        review_text = element_text.replace('블로그리뷰', '')
                        # 쉼표(,) 제거 후 정수로 변환
                        try :
                            blog_review = int(review_text.replace(',', '')) if ',' in review_text else int(review_text)
                        except ValueError :
                            blog_review = 0
            # PXMot 가 없을 때(별점 방문자 블로그 중  뭐라도 존재x)
            else  : 
                visitor_review = 0
                blog_review = 0      
        else: 
            searchIframe = driver.find_element(By.ID,'searchIframe')
            driver.switch_to.frame(searchIframe)


            ## 클릭 
            driver.find_element(By.CLASS_NAME,'YwYLL').click()
            time.sleep(1)
            driver.switch_to.default_content()
        
            entryIframe = driver.find_element(By.ID,'entryIframe')
            driver.switch_to.frame(entryIframe)
            time.sleep(3) 

            # 가게 이름, 변수로 지정
            restaurant_name = driver.find_element(By.CLASS_NAME,'Fc1rA').text
            category_name = driver.find_element(By.CLASS_NAME,'DJJvD').text
            address = driver.find_element(By.CLASS_NAME,'LDgIH').text

            # 메뉴와 가격이 존재하는지의 여부를 고려 
            # 매장마다 메뉴를 보여주는 테마가 2가지 존재하기 때문에 이를 고려
            if driver.find_elements(By.CLASS_NAME,'ihmWt') :
                menu = driver.find_element(By.CLASS_NAME,'ihmWt').text
                price = driver.find_element(By.CLASS_NAME,'mkBm3').text
            elif driver.find_elements(By.CLASS_NAME,'VQvNX') :
                menu = driver.find_element(By.CLASS_NAME,'VQvNX').text
                price = driver.find_element(By.CLASS_NAME,'Yrsei').text
            else : 
                menu = '메뉴없음'
                price = "가격없음"

            # 리뷰 수 긁어오기
            pxmot_elements = driver.find_elements(By.CLASS_NAME, 'PXMot')
        
            if pxmot_elements:
                for element in pxmot_elements:
                    element_text = element.text
                    if element_text.startswith('별점'):
                        # 별점이 있으면 다음 요소 검사
                        continue
                    elif element_text.startswith('방문자리뷰'):
                        # 방문자 리뷰가 존재하는 경우
                        review_text = element_text.replace('방문자리뷰', '')
                        # 쉼표(,) 제거 후 정수로 변환
                        try : 
                            visitor_review = int(review_text.replace(',', '')) if ',' in review_text else int(review_text)
                        except ValueError :
                            visitor_review = 0
                    elif element_text.startswith('블로그리뷰'):
                        # 블로그 리뷰가 존재하는 경우
                        review_text = element_text.replace('블로그리뷰', '').strip()
                        # 쉼표(,) 제거 후 정수로 변환
                        try :
                            blog_review = int(review_text.replace(',', '')) if ',' in review_text else int(review_text)
                        except ValueError :
                            blog_review = 0
            # PXMot 가 없을 때(별점 방문자 블로그 중  뭐라도 존재x)
            else  : 
                visitor_review = 0
                blog_review = 0        

    except Exception as e : 
        restaurant_name = name 
        category_name = '전처리필요'
        address = '전처리필요'
        menu = '메뉴없음'
        price = "가격없음"
        visitor_review = 0
        blog_review = 0
        print(f"에러 메시지: {str(e)}")


    restaurant_name_list.append(restaurant_name)
    category_name_list.append(category_name)
    address_list.append(address)
    menu_list.append(menu)
    price_list.append(price)
    visitor_review_list.append(visitor_review)
    blog_review_list.append(blog_review)

res_info_df = pd.DataFrame({'식당이름':restaurant_name_list ,
                             '업태구분' :category_name_list ,
                             '주소' :address_list ,
                             '메뉴': menu_list,
                             '가격':price_list,
                             '방문자리뷰':visitor_review_list,
                             '블로그리뷰':blog_review_list,
                             })
driver.quit()

res_info_df['검색어'] = res_df['검색어']
res_info_df.to_excel(f'./data/restaurant_info_data(2)/restaurant_info_data/restaurant_tag_df_{이름}_{start_num}_{end_num}.xlsx', index=False)