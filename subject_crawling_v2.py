import time, threading
from selenium.webdriver.common.by import By

#저장 key들
#구버전
# id_dict = {
#         2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
#         9: 'lang', 10: '해설', 11: 'note', 12: 'class_elective', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'info'
#         }

#신버전 + notice, syllabus_url, commentary_url
id_dict = {
        2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
        9: 'lang', 10: 'commentary', 11: 'note', 12: 'liberal_arts_area', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'time'
        }

order = [i for i in range(2, 17)]
order = [order[2]] + order[:2] + order[3:]    #4->2->3->5->6->...

import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 락(Lock) 객체 생성
lock = threading.Lock()

# 각 행 처리 함수
def process_row(site, r, lectures, year, term, u='', m=''):
    lecture = {}
    lecnum = 0
    isExist = False

    #순서
    for c in order:
        try:
            i = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]').text
        except:
            return False # 처리할 행이 없음
        
        if c == 10:
            continue
        
        if c == 4:
            lecnum = int(site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[4]/button').text)
            
            with lock:
                try:
                    # 강의계획서 창 전환
                    site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[4]/button').click()
                    
                    #TEST 
                    print(r)
                    site.switch_to.window(site.window_handles[1])

                    # 강의계획서 수강신청 유의사항 저장
                    try:
                        lecture['notice'] = site.find_element(By.XPATH, '/html/body/div/div/div[1]/table/tbody/tr[5]/td').text
                    except NoSuchElementException:
                        print(f"알림     : {u} {m} {r} 수강신청 유의사항 없음      ")
                        lecture['notice'] = ''
                        pass
                    
                    # 원래 창으로 전환
                    site.close()
                    site.switch_to.window(site.window_handles[0])
                except NoSuchElementException:
                    print(f"알림     : {u} {m} {r} 팝업창 없음      ")
                    lecture['notice'] = ''
                    pass

                # # 강의계획서 창 전환
                # site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[4]/button').click()
                # site.switch_to.window(site.window_handles[1])

                # # 강의계획서 수강신청 유의사항 저장
                # lecture['notice'] = site.find_element(By.XPATH, '/html/body/div/div/div[1]/table/tbody/tr[5]/td').text
    
                # # 원래 창으로 전환
                # site.close()
                # site.switch_to.window(site.window_handles[0])

                if lecnum in lectures and 'course_num' in lectures[lecnum]:
                    isExist = True
                    break
                
                # 중복 확인
                lecture['term'] = term
                
                continue
    
        lecture[id_dict[c]] = i

    with lock:
        if not isExist:
            lectures[lecnum] = lecture.copy()
        
# 멀티스레드 클래스
class ProcessRowThread(threading.Thread):
    def __init__(self, site, lectures, year, term, u='', m='', r_start=2, r_end=None):
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
        moreRow = True
        while moreRow and (self.r_end is None or r <= self.r_end):
            print(self.u, self.m, str(r), '                            ', end='\r')
            moreRow = process_row(self.site, r, self.lectures, self.year, self.term, self.u, self.m)
            r += 1


#전선,전필,지교,지필
def major_or_designated(idx, site, lectures, select_class, select_univ, select_major, year, term, mt):
    #이수구분 선택
    select_class.select_by_index(idx)
    time.sleep(1)

    #대학 필수 알림 뜰 시 확인 클릭
    try:
        site.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]').click()
    except:
        pass
    
    #대학들 순회
    univ = 0
    
    while True:
        #대학 선택
        try: select_univ.select_by_index(univ)
        except: break

        #대학 이름 확인
        univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{univ+1}]')
        time.sleep(0.5)

        #학과 순회
        major = 0
        isVisited = set()

        while True:
            #학과 선택
            try: select_major.select_by_index(major)
            except: break

            #학과 이름 확인
            major_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{major+1}]')

            #학과 이미 방문 했는지 확인
            if major_element in isVisited:
                major+=1
                continue
            else:
                isVisited.add(major_element)
            
            #진행 사항 출력
            print(univ_element.text,major_element.text,'0                 ',end='\r')

            #검색 버튼 클릭
            site.find_element(By.ID, 'btnSearch').click()
            time.sleep(10)

            #검색 결과 테이블 순회
            
            thread1 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=2, r_end=50)
            thread2 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=51, r_end=100)
            thread3 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=101, r_end=150)
            thread4 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=151, r_end=200)
            thread5 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=201, r_end=300)
            thread6 = ProcessRowThread(site, lectures, year, term, u=univ_element.text, m=major_element.text, r_start=301, r_end=350)

            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()
            thread5.start()
            thread6.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            thread5.join()
            thread6.join()

            # iterTable(site, lectures, log, year, term, univ_element.text, major_element.text)

            major+=1
        univ+=1
    

#일선, 교직, 기교, 심교, 융필, 융선
def other_subjects(idx, site, lectures, select_class, year, term, mt):
    #이수 구분 선택
    select_class.select_by_index(idx)
    time.sleep(1)

    #검색 버튼 클릭
    site.find_element(By.ID, 'btnSearch').click()
    time.sleep(1)

    #검색 결과 테이블 순회
    iterTable(site, lectures, year, term)