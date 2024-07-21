from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from subject_crawling import major_or_designated
from subject_crawling import other_subjects
import json, datetime, time

options = Options()
# gitpod에서 접속하기 위한 옵션
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--headless")  

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
site = webdriver.Chrome(service=service, options=options)

#페이지 접속
site.get('https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp')
print('접속 완료    : ' + site.title)

Select(site.find_element(By.ID, 'pYear')).select_by_visible_text('2024')
Select(site.find_element(By.ID, 'pTerm')).select_by_index(0)
site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[2]/label[2]').click()
select_class = Select(site.find_element(By.ID, 'pPobt')).select_by_index(0)
time.sleep(1)
# site.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]').click()
select_univ = Select(site.find_element(By.ID, 'pUniv')).select_by_index(1)
select_major = Select(site.find_element(By.ID, 'pSustMjCd')).select_by_index(1)
time.sleep(1)
site.find_element(By.ID, 'btnSearch').click()
time.sleep(1)

site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[4]/button').click()

site.switch_to.window(site.window_handles[1])
text = site.find_element(By.XPATH, '/html/body/div/div/div[1]/table/tbody/tr[5]/td').text
print(text)
site.close()
site.switch_to.window(site.window_handles[0])

