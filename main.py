from crawling import makeLectures
import json

#################################################
#########건국대학교 종강시 강의 정보 수집기#########

######공통 옵션######
YEAR = 2024     #연도
SEMESTER = 1    #학기   여름학기, 겨울학기 미구현

GRADE = 1       #TODO 학년 제거, TODO 중단된 체크포인트부터 시작
lectures = makeLectures(YEAR, GRADE, SEMESTER)

########출력########
#checkpoint_[이수과정].json : 이수과정까지의 체크포인트
#lecture_info.json : 완료된 파일
#dub_log.json : 로그파일
with open('lecture_info.json', 'w', encoding='UTF-8') as f : 
	json.dump(lectures, f, indent=4, ensure_ascii=False)

