import json
import re

with open ("lecture_info.json", "r") as f:
    lectures = json.load(f)

# building_num_dic = {
#     '경영':2, '상허관':3, '사':4, '예':5, '언어원':6, '법':8, '종강':8, '의':10, 
#     '생':11, '산학':14, '수':15, '새':16, '건':17, '부':18, '문':19, '공':21, 
#     '신공':22, '이':23, '창':24, '중장비':100, '체육관':101, '공별':211
#     }

def check_kor(text):
    p = re.compile('[ㄱ-힣]')
    r = p.search(text)
    if r is None:
        return False
    else:
        return True

for lecnum, lecture in lectures.items():
    lecture['credit'] = int(lecture['credit'])
    lecture['hour'] = int(lecture['hour'])
    del lecture['해설']
    lecture['grade'] = int(lecture['grade'])

    days = []
    starts = []
    ends = []
    buildings = []
    rooms = []
    times = lecture['info'].replace(' ', '').split(',')
    for time in times:
        if len(time) == 0:
            continue

        if time == '(e-러닝)':
            lecture['type_name'] = '미지정녹화'
            continue

        days.append(time[0])
        s = 0
        try:
            start, end = map(int, time[1:6].split('-'))
            s = 7
        except:
            start, end = int(time[1:3]), int(time[1:3])
            s = 4
        starts.append(start)
        ends.append(end)

        building = ''
        room = ''

        if '온라인(실시간)' in time[s:]:
            buildings.append('실시간')
            rooms.append('실시간')
            continue
        
        if '온라인(녹화)' in time[s:]:
            buildings.append('녹화')
            rooms.append('녹화')
            continue
            
        for t in time[s:]:
            if t == ')': break

            if check_kor(t): building += t
            else: room += t
        
        buildings.append(building)
        rooms.append(room)
    
    del lecture['info']
    lecture['num'] = len(days)
    lecture['days'] = days
    lecture['starts'] = starts
    lecture['ends'] = ends
    lecture['buildings'] = buildings
    lecture['rooms'] = rooms

with open('tars_type_lectures.json', 'w', encoding='UTF-8') as f : 
	json.dump(lectures, f, indent=4, ensure_ascii=False)
