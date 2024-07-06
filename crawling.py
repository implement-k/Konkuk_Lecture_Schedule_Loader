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
    

def crawlSite(site, YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR):
    print(f'선택한 옵션  :\n 연도 : {YEAR}, 학년 : {GRADE}, 학기 : {SEMESTER}, ', end='')
    if limitMAJOR:
        print(f'학과 : {MAJOR}')
    else:
        print(f'학과 : 전체학과')

    UNIV = int(MAJOR[:2])
    MAJOR = int(MAJOR[2:])

    try:
        Select(site.find_element(By.ID, 'pYear')).select_by_visible_text(str(YEAR))
    except NoSuchElementException:
        print('해당 연도를 선택할 수 없음')
        exit(0)
    except:
        print('연도 오류')
        exit(0)

    try:
        Select(site.find_element(By.ID, 'pTerm')).select_by_index(SEMESTER-1)
    except NoSuchElementException:
        print('해당 학년를 선택할 수 없음')
        exit(0)
    except:
        print('학년 오류')
        exit(0)

    site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[2]/label[2]').click()

    time.sleep(0.1)
    select_univ = Select(site.find_element(By.ID, 'pUniv'))
    select_major = Select(site.find_element(By.ID, 'pSustMjCd'))

    if limitMAJOR:
        select_univ.select_by_index(UNIV)
        univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{UNIV}]')
        print(univ_element.text, end=' ')
        time.sleep(3)

        # select_major.select_by_visible_text('컴퓨터공학부')
        select_major.select_by_index(MAJOR)
        major_element = site.find_element(by.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{MAJOR}]')
        print(major_element.text)

        site.find_element(By.ID, 'btnSearch').click()
        time.sleep(0.5)

        print(site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text)
    else:
        univ = 1
        print('진행과정')
        while True:
            try: select_univ.select_by_index(univ)
            except: break

            univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{UNIV}]')
            print(select_element.text, end=' ')
            time.sleep(0.5)

            while True:
                select_major.select_by_index(MAJOR)
                major_element = site.find_element(by.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{MAJOR}]')
                print(major_element.text,end='\r')

                site.find_element(By.ID, 'btnSearch').click()
                time.sleep(0.5)
                print(site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text)


def makeLectures(YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR):
    site = readySelenium()

    #페이지 접속
    url = "https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp"
    site.get(url)
    print('접속 완료    : ' + site.title)

    time.sleep(0.1)

    lectures = crawlSite(site, YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR)
 
    
    return lectures




# lectures : {
#   [과목번호] : lecture
# }
# lecture : {
#   class:int, //이수구분
#   credit:int[0~21], //학점
#   lang:int[0~2^9] <1:한국어, 2:영어, 4:중국어, ..., 3:한국어+영어, ..., 7:한국어+영어+중국어, ...>, //언어유형
#   pmajors:[우선학과 리스트], //우선학과
#   instructor:string, //교강사
#   building:int[0~100], //건물번호
#   room:string //호실
#   num:int,
#   days:[],
#   starts:[],
#   ends:[],
#   exam:[],
# }
# print(search_box)

# /html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[2]
# /html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[3]
# /html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[16]


# /html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[3]/td[2]



#크롬 드라이버에 url 주소 넣고 실행


# driver.get("https://www.example.com")
# print(driver.title)

# driver.quit()
