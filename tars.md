
lectures : {
  [과목번호] : lecture
}
lecture : {
  course_num:string, //학수번호
  class:string, //이수구분
  name:string, //강의이름
  credit:int[0~21], //학점
  hour:int, //시간
  type_name:string, //강의종류,[미지정녹화, e-러닝(뭐시기), B-러닝(뭐시기), 일반]
  lang:string,  //원어 종류
  note:string, //비고
  class_elective:string, //교양영역
  grade:int, //학년
  basic_major:string, //개설학과
  instructor:string, //교강사
  num:int,
  days:[],        //오류시 9999
  starts:[],
  ends:[],
  buildings:[int[0~100]], //건물번호
  rooms:[string] //호실


  required_subject_set:set(),
  not_subject_set:set(),
  pmajors:[우선학과 리스트], //우선학
  exam:[],
}