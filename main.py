from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = Options()
# gitpod에서 접속하기 위한 옵션
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--headless")  

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#페이지 접속
url = "https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp"

driver.get(url)
print(driver.title)

time.sleep(1)

#종강시 옵션 선택
select_term = driver.find_element(By.ID, 'pTerm')
select_term.select_by_index(1)

option = driver.find_element(By.ID, 'pSearchGb2')
option.click()

select_univ = driver.find_element(By.ID, 'pUniv')
select_univ.select_by_index(2)

# select_major = driver.find_element(By.ID, 'pSustMjCd')
# select_mafor.select_by_index(1)

search_box = driver.find_element(By.ID, 'btnSearch')
search_box.click()

time.sleep(1)

a = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]')
print(a.get_text())

# print(search_box)



#크롬 드라이버에 url 주소 넣고 실행


# driver.get("https://www.example.com")
# print(driver.title)

# driver.quit()
