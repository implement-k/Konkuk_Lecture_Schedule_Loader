import time, threading
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

#저장 key들
#구버전
#TODO 삭제
# id_dict = {
#         2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
#         9: 'lang', 10: '해설', 11: 'note', 12: 'class_elective', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'info'
#         }

#신버전 + notice
id_dict = {
        2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
        9: 'lang', 10: 'commentary', 11: 'note', 12: 'liberal_arts_area', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'time'
        }

order = [4, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

options = Options()
# gitpod에서 접속하기 위한 옵션
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--headless")  

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())

# 락(Lock) 객체 생성
lock = threading.Lock()

# 각 행 처리 함수
def process_row(site, r, lectures, year, term, u='', m=''):
    global options, service
    lecture = {}
    lecnum = 0
    isExist = False

    #순서
    for c in order:
        #해당 칸의 내용 i에 저장
        try:
            text = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]').text
        except NoSuchElementException:
            return False

        #과목 해설일 경우 건너뛰기
        #TODO 해설창에서 영문명 불러오기.
        if c == 10:
            continue

        #과목번호
        if c == 4:
            lecnum = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[4]/button').text

            # 중복 확인
            with lock:
                if lecnum in lectures and 'course_num' in lectures[lecnum]:
                    isExist = True
                    break
            
            #팝업창 제어
            tmp = webdriver.Chrome(service=service, options=options)
            tmp.get("https://sugang.konkuk.ac.kr/")
            tmp.execute_script(\
                f'window.open("https://sugang.konkuk.ac.kr/sugang/search?attribute=lectPlan&fake=1722002027694&pYear={year}&pTerm={term}&pSbjtId={lecnum}")')
            tmp.switch_to.window(tmp.window_handles[1])

            # 강의계획서 수강신청 유의사항 저장
            try:
                lecture['notice'] = tmp.find_element(By.XPATH, '/html/body/div/div/div[1]/table/tbody/tr[5]/td').text
            except:
                print(f"알림     : {u} {m} {r} {lecnum} 수강신청 유의사항 없음      ")
                lecture['notice'] = ''
                pass

            tmp.quit

        lecture[id_dict[c]] = text
    
    return True

    #lectures에 행 정보 추가
    with lock:
        if not isExist:
            lectures[lecnum] = lecture.copy()


# 멀티스레드 클래스
class ProcessRowThread(threading.Thread):
    def __init__(self, site, lectures, year, term, u='', m='', r_start=2, r_end=2):
        threading.Thread.__init__(self)
        self.site = site
        self.lectures = lectures
        self.year = year
        self.term = term
        self.u = u
        self.m = m
        self.r_start = r_start
        self.r_end = r_end

    def run(self):
        r = self.r_start

        while r < self.r_end:
            print(self.u, self.m, str(r), '                            ')
            # print(self.u, self.m, str(r), '                            ', end='\r')

            moreRow = process_row(self.site, r, self.lectures, self.year, self.term, self.u, self.m)
            if not moreRow: break
            r += 1


def iterTable(mt, site, lectures, year, univ_name, major_name):
    if mt == 1:
        r = 2

        #테이블 순회
        while True:
            moreRow = process_row(site, r, lectures, year, u=univ_name, m=major_name)
            if not moreRow: break
            r += 1
        return

    threads = []
    isDone = [False] * mt
    limit_seeds = [2, 3, 4, 5, 8, 11, 15, 18, 22, 27, 31, 35, 38]
    limits = [seed * mt + 2 for seed in limit_seeds]
    limit = 2

    #테이블의 행의 길이가 대략 어느정도인지 확인
    for l in limits:
        try:
            site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{l}]/td[1]')
        except NoSuchElementException:
            limit = l
            break

    interval = (limit - 2) // mt

    for i in range(mt):
        start_row = i * interval + 2
        end_row = (i + 1) * interval + 2

        thread = ProcessRowThread(site, lectures, year, u=univ_name, m=major_name, r_start=start_row, r_end=end_row)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


#전선,전필,지교,지필
def major_or_designated(idx, site, lectures, select_class, select_univ, select_major, year, mt):
    #이수구분 선택
    select_class.select_by_index(idx)
    time.sleep(1)

    #대학 필수 알림 뜰 시 확인 클릭
    try: site.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]').click()
    except: pass

    #대학들 순회
    univ = 0
    while True:
        #대학 선택
        try: select_univ.select_by_index(univ)
        except NoSuchElementException: break

        #대학 이름 확인
        univ_name = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{univ+1}]').text

        #학과 순회
        isVisited = set()
        major = 0
        while True:
            #학과 선택
            try: select_major.select_by_index(major)
            except: break

            #학과 이름 확인
            major_name = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{major+1}]').text

            #학과 이미 방문 했는지 확인
            if major_name not in isVisited:
                isVisited.add(major_name)
            else:
                major+=1
                continue

            #검색 버튼 클릭
            site.find_element(By.ID, 'btnSearch').click()
            time.sleep(2)

            #검색 결과 테이블 순회
            iterTable(mt, site, lectures, year, univ_name, major_name)

            major+=1
        univ+=1


# #일선, 교직, 기교, 심교, 융필, 융선
def other_subjects(idx, site, lectures, select_class, year, mt):
    #이수 구분 선택
    select_class.select_by_index(idx)
    time.sleep(1)

    #검색 버튼 클릭
    site.find_element(By.ID, 'btnSearch').click()
    time.sleep(5)

    #검색 결과 테이블 순회
    #멀티쓰레딩
    threads = []
    isDone = [True]*6

    if mt == 1:
        r = 2
        moreRow = True
        while moreRow:
            moreRow = process_row(site, r, lectures, year, u=univ_element.text, m=major_name)
    else:
        end_limit = 350 // mt + 1

        for i in range(mt):
            if i != 0 and isDone[i-1]:
                break

            start_row = i * end_limit + 2
            end_row = (i + 1) * end_limit if i < mt else 350
            thread = ProcessRowThread(site, lectures, year, i, isDone, u=univ_element.text, m=major_name, r_start=start_row, r_end=end_row)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()