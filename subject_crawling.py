import time
from selenium.webdriver.common.by import By


id_dict = {
        2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
        9: 'lang', 10: '해설', 11: 'note', 12: 'class_elective', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'info'
        }
order = [i for i in range(2, 17)]
order = [order[2]] + order[:2] + order[3:]    #4->2->3->5->6->...


def iterTable(site, lectures, log, u='', m=''):
    r = 2
    moreRow = True
    
    while True:
        # #test용
        # if r == 5:
        #     break

        print(u,m,str(r),'                            ',end='\r')
        lecnum = 0
        lecture = {}
        isExist = False

        for c in order:
            try:
                i = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]').text
            except:
                moreRow = False
                break

            if c == 4:
                lecnum = int(site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[{r}]/td[{c}]/button').text)
                #TODO 강의 계획서 불러오기
                if lecnum in lectures and 'course_num' in lectures[lecnum]:
                    log.append((u,m,str(r),str(lecnum)))
                    isExist = True
                    break

                continue
        
            lecture[id_dict[c]] = i
        
        if not moreRow:
            break
        
        r += 1

        if isExist:
            continue
        
        lectures[lecnum] = lecture.copy()
        

#전선,전필,지교,지필
def major_or_designated(idx, site, lectures, select_class, select_univ, select_major, log):
    select_class.select_by_index(idx)
    time.sleep(1)

    try:
        site.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]').click()
    except:
        pass
    
    univ = 0
    
    while True:
        try: select_univ.select_by_index(univ)
        except: break

        univ_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[3]/select/option[{univ+1}]')
        time.sleep(0.5)

        major = 0
        isVisited = set()

        while True:
            try: select_major.select_by_index(major)
            except: break

            major_element = site.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[1]/form/table/tbody/tr[2]/td[4]/select/option[{major+1}]')
            if major_element in isVisited:
                major+=1
                continue
            else:
                isVisited.add(major_element)
            print(univ_element.text,major_element.text,'0                 ',end='\r')

            site.find_element(By.ID, 'btnSearch').click()
            time.sleep(1)
            iterTable(site, lectures, log, univ_element.text, major_element.text)
            major+=1
        univ+=1
    

#일선, 교직, 기교, 심교, 융필, 융선
def other_subjects(idx, site, lectures, select_class, log):
    select_class.select_by_index(idx)
    time.sleep(1)
    site.find_element(By.ID, 'btnSearch').click()
    time.sleep(1)
    iterTable(site, lectures, log)