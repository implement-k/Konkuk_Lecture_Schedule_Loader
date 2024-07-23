import time
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


#결과 테이블 순회
def iterTable(site, lectures, log, year, term, u='', m=''):
    r = 2
    moreRow = True
    
    #결과 테이블 행 순회
    while True:
        #진행 결과(현재 행) 출력
        print(u,m,str(r),'                            ',end='\r')

        lecnum = 0
        lecture = {}
        isExist = False

        #강의계획서 창 전환
        try:
            site.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[4]/button').click()
            site.switch_to.window(site.window_handles[1])

            #강의계획서 수강신청 유의사항 저장
            try:
                lecture['notice'] = site.find_element(By.XPATH, '/html/body/div/div/div[1]/table/tbody/tr[5]/td').text
            except:
                print(f"알림     : {u} {m} {r} 수강신청 유의사항 없음      ")
                lecture['notice'] = ''
                pass
            
            #원래 창으로 전환
            site.close()
            site.switch_to.window(site.window_handles[0])
        except:
            print(f"알림     : {u} {m} {r} 팝업창 없음      ")
            lecture['notice'] = ''
            pass

        for c in order:
            #해당 요소 불러오기
            try:
                i = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]').text
            except:
                moreRow = False
                break
            
            if c == 10:
                continue
            
            if c == 4:
                lecnum = int(site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[4]/button').text)
                
                #중복 확인
                if lecnum in lectures and 'course_num' in lectures[lecnum]:
                    log.append((u,m,str(r),str(lecnum)))
                    isExist = True
                    break
                
                lecture['term'] = term
                
                continue
        
            lecture[id_dict[c]] = i
        
        if not moreRow:
            break
        
        r += 1

        if isExist:
            continue
        
        lectures[lecnum] = lecture.copy()
        

#전선,전필,지교,지필
def major_or_designated(idx, site, lectures, select_class, select_univ, select_major, year, term, log):
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
            time.sleep(3)

            #검색 결과 테이블 순회
            iterTable(site, lectures, log, year, term, univ_element.text, major_element.text)

            major+=1
        univ+=1
    

#일선, 교직, 기교, 심교, 융필, 융선
def other_subjects(idx, site, lectures, select_class, year, term, log):
    #이수 구분 선택
    select_class.select_by_index(idx)
    time.sleep(1)

    #검색 버튼 클릭
    site.find_element(By.ID, 'btnSearch').click()
    time.sleep(1)

    #검색 결과 테이블 순회
    iterTable(site, lectures, log, year, term)