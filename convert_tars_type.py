import json

with open ("파일이름.json", "r") as f:
    lectures = json.load(f)

building_num_dic = {
    '경영':2, '상허관':3, '사':4, '예':5, '언어원':6, '법':8, '종강':8, '의':10, 
    '생':11, '산학':14, '수':15, '새':16, '건':17, '부':18, '문':19, '공':21, 
    '신공':22, '이':23, '창':24, '중장비':100, '체육관':101
    }

def check_kor(text):
    p = re.compile('[ㄱ-힣]')
    r = p.search(text)
    if r is None:
        return False
    else:
        return True

lectures : {
  [과목번호] : lecture
}
lecture : {
  course_num:string, //학수번호
  class:string, //이수구분
  name:string, //강의이름
  credit:int[0~21], //학점
  hour:int, //시간
  type_name:string, //강의종류
  lang:string,  //원어 종류
  note:string, //비고
  class_elective:string, //교양영역
  grade:int, //학년
  basic_major:string, //개설학과
  instructor:string, //교강사
  num:int,
  type:[],
  days:[],
  starts:[],
  ends:[],
  buildings:[int[0~100]], //건물번호
  rooms:[string] //호실


  required_subject_set:set(),
  not_subject_set:set(),
  pmajors:[우선학과 리스트], //우선학과
  
  
  
  

  exam:[],
}


e-러닝(녹화)      금05-12(온라인(녹화))(e-러닝)
e-러닝(녹화)    (e-러닝)


#TODO 
         16: 'info'

        elif c == 10:
                continue
                #TODO 10: 해설[TODO 영어 한국어 해설도 조사] -> 현재는 비활성
            elif c == 16:
                if i == '(e-러닝)':
                    continue
                #TODO 16: info 변경 -> days, starts, ends



for lecnum, lecture in lectures.items():
    lecture['credit'] = int(lecture['credit'])
    lecture['hour'] = int(lecture['hour'])
    del lecture['해설']
    lecture['grade'] = int(lecture['grade'])

    types = []
    days = []
    starts = []
    ends = []
    buildings = []
    rooms = []
    times = lecture['info'].split(',')

    for time in times:
        days.append(time[0])
        
        start, end = map(int, time[1:6].split('-'))
        starts.append(start)
        ends.append(end)

        building = ''
        room = ''

        for t in time[7:]:
            if t == ')': break

            if check_kor(t): building.append(t)
            else: room.append(t)
        

        buildings.append(building)
        rooms.append(room)
    
    del lecture['info']
    lecture['days'] = days
    lecture['starts'] = starts
    lecture['ends'] = ends
    lecture['buildings'] = buildings
    lecture['rooms'] = rooms




    

        
    월10-12(중장비306), 수04-06(중장비306)



    





with open('tars_type_lectures.json', 'w', encoding='UTF-8') as f : 
	json.dump(lectures, f, indent=4, ensure_ascii=False)
