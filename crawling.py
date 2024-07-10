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
NOW = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")


def crawlSite(site, YEAR, SEMESTER, CHECKPOINT):
    log = []
    lectures = {'checkpoint':0}
    checkpoint = 0

    print(f'선택한 옵션  : (연도 : {YEAR}, 학기 : {SEMESTER}, ',end='')

    if CHECKPOINT:
        print(f'체크포인트 : {CHECKPOINT})')

        try:
            with open(CHECKPOINT, 'r') as f:
                lectures = json.load(f)
        except FileNotFoundError:
            print('오류     : 해당 파일을 찾을 수 없음')
            exit(0)
        except:
            print('오류     : 경로 오류')
            exit(0)
        
        if 'checkpoint' in lectures:
            checkpoint = lectures['checkpoint']
        else:
            print('이미 완성된 파일')
    else:
        print(f'체크포인트 : 없음)')

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
    if checkpoint < 1:
        print('진행과정 : 전선 시작')
        major_or_designated(0, site, lectures, select_class, select_univ, select_major, log) #전선
        print('진행과정 : 전선 완료                                     ')
        lectures['checkpoint'] = 1

        print('전선 저장')
        with open(f'checkpoint/checkpoint_전선_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)

    if checkpoint < 2:
        print('진행과정 : 전필 시작')
        major_or_designated(1, site, lectures, select_class, select_univ, select_major, log) #전필
        print('진행과정 : 전필 완료                                     ')
        lectures['checkpoint'] = 2

        print('전필 저장')
        with open(f'checkpoint/checkpoint_전필_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)

    if checkpoint < 3:
        print('진행과정 : 지교 시작')
        major_or_designated(2, site, lectures, select_class, select_univ, select_major, log) #지교
        print('진행과정 : 지교 완료                                     ')
        lectures['checkpoint'] = 3

        print('지교 저장')
        with open(f'checkpoint/checkpoint_지교_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)

    if checkpoint < 4:
        print('진행과정 : 지필 시작')
        major_or_designated(3, site, lectures, select_class, select_univ, select_major, log) #지필
        print('진행과정 : 지필 완료                                     ')
        lectures['checkpoint'] = 4

        print('지필 저장')
        with open(f'checkpoint/checkpoint_지필_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)

    if checkpoint < 5:
        print('진행과정 : 일선 시작')
        other_subjects(4, site, lectures, select_class, log)  #일선
        print('진행과정 : 일선 완료                                     ')
        print('진행과정 : 교직 시작')
        other_subjects(5, site, lectures, select_class, log)  #교직
        print('진행과정 : 교직 완료                                     ')
        lectures['checkpoint'] = 5

        print('일선, 교직 저장')
        with open(f'checkpoint/checkpoint_일선_교직_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)

    if checkpoint < 6:
        print('진행과정 : 기교 시작')
        other_subjects(6, site, lectures, select_class, log)  #기교
        print('진행과정 : 기교 완료                                     ')
        lectures['checkpoint'] = 6

        print('기교 저장')
        with open(f'checkpoint/checkpoint_일선_교직_{NOW}.json', 'w', encoding='UTF-8') as f : 
            json.dump(lectures, f, indent=4, ensure_ascii=False)
    
    if checkpoint < 7:
        print('진행과정 : 심교 시작')
        other_subjects(7, site, lectures, select_class, log)  #심교
        print('진행과정 : 심교 완료                                     ')
        del lectures['checkpoint']

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


def readySelenium():
    options = Options()
    # gitpod에서 접속하기 위한 옵션
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--headless")  

    # Setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def makeLectures(YEAR, SEMESTER, CHECKPOINT, URL):
    site = readySelenium()

    #페이지 접속
    site.get(URL)
    print('접속 완료    : ' + site.title)
    time.sleep(0.1)

    lectures = crawlSite(site, YEAR, SEMESTER, CHECKPOINT)

    return lectures