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