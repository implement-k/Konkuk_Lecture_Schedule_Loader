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


def readySelenium():
    options = Options()
    # gitpod에서 접속하기 위한 옵션
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--headless")  

    # Setup ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
    

def iterTable(site, lectures):
    #TODO 10: 해설[TODO 영어 한국어 해설도 조사] -> 현재는 비활성
    #TODO 4: 강의번호 누를시 강의 계획서 팝업 으로 강의 계획서 수집 -> 현재는 강의번호만
    #TODO 16: info 변경 -> days, starts, ends

    r = 2
    moreRow = True
    id_dict = {
        2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
        9: 'lang', 10: '해설', 11: 'note', 12: 'class_elective', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'info'
        }
    order = [i for i in range(2, 17)]
    order = [order[2]] + order[:2] + order[3:]    #4->2->3->5->6->...

    while True:
        lecnum = 0
        lecture = {}
        print(r)
        for c in order:
            try: 
                i = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]')
            except:
                moreRow = False
                break

            if c == 4:
                lecnum = int(site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]/button').text)
                
                if lecnum in lectures:
                    print('이미 있는 강의번호   : '+str(lecnum))
                    break

                continue
        
            lecture[id_dict[c]] = i.text
        
        if not moreRow:
            break

        r += 1
        lectures[lecnum] = lecture.copy()


def crawlSite(site, YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR):
    lectures = {}

    print(f'선택한 옵션  : (연도 : {YEAR}, 학년 : {GRADE}, 학기 : {SEMESTER}, ', end='')

    if limitMAJOR:
        print(f'학과 : {MAJOR})')
    else:
        print(f'학과 : 전체학과)')

    UNIV = int(MAJOR[:2])
    MAJOR = int(MAJOR[2:])

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

    time.sleep(0.1)
    select_univ = Select(site.find_element(By.ID, 'pUniv'))
    select_major = Select(site.find_element(By.ID, 'pSustMjCd'))

    print('진행과정 : 불러오기 시작')

    if limitMAJOR:
        try:
            select_univ.select_by_index(UNIV)
        except NoSuchElementException:
            print('오류     : 해당 대학을 선택할 수 없음')
            exit(0)
        except:
            print('오류     : 대학 오류')
            exit(0)

        univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{UNIV+1}]')
        print('진행과정 : '+univ_element.text, end=' ')
        time.sleep(3)

        try:
            select_major.select_by_index(MAJOR)
        except NoSuchElementException:
            print('오류     : 해당 학과을 선택할 수 없음')
            exit(0)
        except:
            print('오류     : 학과 오류')
            exit(0)

        major_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{MAJOR+1}]')
        print(major_element.text)
        
        site.find_element(By.ID, 'btnSearch').click()
        time.sleep(1)

        iterTable(site, lectures)
    else:
        univ = 1
        while True:
            try: select_univ.select_by_index(univ)
            except: break

            univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{UNIV}]')
            print('진행과정 : '+select_element.text, end=' ')
            time.sleep(0.5)

            while True:
                try: select_major.select_by_index(MAJOR)
                except: break

                major_element = site.find_element(by.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{MAJOR}]')
                print(major_element.text,end='\r')

                site.find_element(By.ID, 'btnSearch').click()
                time.sleep(1)
                iterTable(site, lectures)
    
    print('진행과정 : 완료!')

    return lectures


def makeLectures(YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR):
    site = readySelenium()

    #페이지 접속
    url = "https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp"
    site.get(url)
    print('접속 완료    : ' + site.title)

    time.sleep(0.1)

    lectures = crawlSite(site, YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR)

    return lectures