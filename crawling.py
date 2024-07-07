from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from subject_crawling import major_or_designated
from subject_crawling import other_subjects
import json


def readySelenium():
    options = Options()
    # gitpod에서 접속하기 위한 옵션
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--headless")  

    # Setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def crawlSite(site, YEAR, GRADE, SEMESTER):
    log = []
    lectures = {}

    print(f'선택한 옵션  : (연도 : {YEAR}, 학년 : {GRADE}, 학기 : {SEMESTER})')
    try:
        Select(site.find_element(By.ID, 'pYear')).select_by_visible_text(str(YEAR))
    except NoSuchElementException:
        print('오류     : 해당 연도를 선택할 수 없음')
        exit(0)
    except:
        print('오류     : 연도 오류')
        exit(0)

    try:
        Select(site.find_element(By.ID, 'pTerm')).select_by_index(SEMESTER-1)
    except NoSuchElementException:
        print('오류     : 해당 학년를 선택할 수 없음')
        exit(0)
    except:
        print('오류     : 학년 오류')
        exit(0)

    site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[2]/label[2]').click()

    select_class = Select(site.find_element(By.ID, 'pPobt'))
    select_univ = Select(site.find_element(By.ID, 'pUniv'))
    select_major = Select(site.find_element(By.ID, 'pSustMjCd'))
    time.sleep(0.1)

    print('진행과정 : 불러오기 시작')
    print('----------------------')
    print('진행과정 : 전선 시작')
    major_or_designated(0, site, lectures, select_class, select_univ, select_major, log) #전선
    print('진행과정 : 전선 완료                                     ')

    print('전선 저장')
    with open('checkpoint_전선.json', 'w', encoding='UTF-8') as f : 
	    json.dump(lectures, f, indent=4, ensure_ascii=False)

    print('진행과정 : 전필 시작')
    major_or_designated(1, site, lectures, select_class, select_univ, select_major, log) #전필
    print('진행과정 : 전필 완료                                     ')

    print('전필 저장')
    with open('checkpoint_전필.json', 'w', encoding='UTF-8') as f : 
	    json.dump(lectures, f, indent=4, ensure_ascii=False)

    print('진행과정 : 지교 시작')
    major_or_designated(2, site, lectures, select_class, select_univ, select_major, log) #지교
    print('진행과정 : 지교 완료                                     ')

    print('지교 저장')
    with open('checkpoint_지교.json', 'w', encoding='UTF-8') as f : 
	    json.dump(lectures, f, indent=4, ensure_ascii=False)

    print('진행과정 : 지필 시작')
    major_or_designated(3, site, lectures, select_class, select_univ, select_major, log) #지필
    print('진행과정 : 지필 완료                                     ')

    print('지필 저장')
    with open('checkpoint_지필.json', 'w', encoding='UTF-8') as f : 
	    json.dump(lectures, f, indent=4, ensure_ascii=False)

    print('진행과정 : 일선 시작')
    other_subjects(4, site, lectures, select_class, log)  #일선
    print('진행과정 : 일선 완료                                     ')
    print('진행과정 : 교직 시작')
    other_subjects(5, site, lectures, select_class, log)  #교직
    print('진행과정 : 교직 완료                                     ')
    print('진행과정 : 기교 시작')
    other_subjects(6, site, lectures, select_class, log)  #기교
    print('진행과정 : 기교 완료                                     ')
    print('진행과정 : 심교 시작')
    other_subjects(7, site, lectures, select_class, log)  #심교
    print('진행과정 : 심교 완료                                     ')

    # print('진행과정 : 융필 시작')
    # convergence_required(8, site, lectures)  #융필
    # print('진행과정 : 융필 완료')
    # print('진행과정 : 융선 시작')
    # convergenct_elective(9, site, lectures)  #융선
    # print('진행과정 : 융선 완료')
    
    print('진행과정 : 완료!')
    with open('dub_log.json', 'w', encoding='UTF-8') as f : 
	    json.dump(log, f, indent=4, ensure_ascii=False)

    return lectures


def makeLectures(YEAR, GRADE, SEMESTER):
    site = readySelenium()

    #페이지 접속
    url = "https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp"
    site.get(url)
    print('접속 완료    : ' + site.title)

    time.sleep(0.1)

    lectures = crawlSite(site, YEAR, GRADE, SEMESTER)

    return lectures