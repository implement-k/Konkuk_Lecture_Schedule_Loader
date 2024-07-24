#v2
from crawling_v2 import makeLectures
#v1.1
# from crawling import makeLectures
import json, datetime
NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#################################################
######## 건국대학교 종강시 강의 정보 수집기 ########
############### V.1.1(2024.7.22) ################
#################################################


################### 공통 옵션 ####################
URL = "https://sugang.konkuk.ac.kr/sugang/jsp/search/searchMainOuter.jsp" 	#종강시 사이트 링크
YEAR = 2024     #연도
SEMESTER = 1    #학기   여름학기, 겨울학기 미구현
MULTITHREADING = 0		#0: 자동 설정, 1: 멀티쓰레딩 끄기, 5, 7, 9 가능

################### 선택 옵션 ####################
#중간에 중단됐다면, 마지막으로 생성된 checkpoint파일 경로
#처음이라면, 공백
CHECKPOINT = ''

##################### 실행 ######################
#v1.1
# lectures = makeLectures(YEAR, SEMESTER, CHECKPOINT, URL)
#v2
lectures = makeLectures(YEAR, SEMESTER, CHECKPOINT, URL, MULTITHREADING)

##################### 출력 ######################
#checkpoint_[이수과정]_[날짜].json : 이수과정까지의 체크포인트
#lectures_[날짜].json 			  : 완료된 파일
with open(f'lectures_{NOW}.json', 'w', encoding='UTF-8') as f : 
	json.dump(lectures, f, indent=4, ensure_ascii=False)