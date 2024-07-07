lectures : {
  [과목번호] : lecture
}
lecture : {
  class:int, //이수구분
  name:string, //강의이름
  credit:int[0~21], //학점
  lang:int[0~2^9] <1:한국어, 2:영어, 4:중국어, ..., 3:한국어+영어, ..., 7:한국어+영어+중국어, ...>, //언어유형
  pmajors:[우선학과 리스트], //우선학과
  instructor:string, //교강사
  building:int[0~100], //건물번호
  room:string //호실
  num:int,
  type_name:string, //강의종류
  hour:int, //시간
  type:[],
  days:[],
  starts:[],
  ends:[],
  exam:[],
}

id_dict = {
        2: 'course_num', 3: 'class', 4: 'lecnum', 5: 'name', 6: 'credit', 7: 'hour', 8: 'type_name',
        9: 'lang', 10: '해설', 11: 'note', 12: 'class_elective', 13: 'grade', 14: 'basic_major', 15: 'instructor', 16: 'info'
        }

        elif c == 10:
                continue
                #TODO 10: 해설[TODO 영어 한국어 해설도 조사] -> 현재는 비활성
            elif c == 16:
                if i == '(e-러닝)':
                    continue
                #TODO 16: info 변경 -> days, starts, ends