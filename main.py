from crawling import makeLectures
import json, datetime
NOW = datetime.datetime.now().strftime("%Y_%m_%d")


#################################################
#########건국대학교 종강시 강의 정보 수집기#########

######공통 옵션######
YEAR = 2024     #연도
SEMESTER = 1    #학기   여름학기, 겨울학기 미구현

######선택 옵션######
#만약 중간에 중단됐다면, 마지막으로 생성된 checkpoint파일 경로
#처음이라면 공백으로
CHECKPOINT = '' 

# lectures = makeLectures(YEAR, SEMESTER, CHECKPOINT)

########출력########
#checkpoint_[이수과정]_[날짜].json : 이수과정까지의 체크포인트
#lectures_[날짜].json 			  : 완료된 파일
#dub_log.json 					  : 로그파일
with open(f'lectures_{NOW}.json', 'w', encoding='UTF-8') as f : 
	json.dump(lectures, f, indent=4, ensure_ascii=False)