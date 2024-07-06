from crawling import makeLectures

#################################################
#########건국대학교 종강시 강의 정보 수집기#########

######공통 옵션######
YEAR = 2024     #연도
GRADE = 1       #학년
SEMESTER = 2    #학기   여름학기, 겨울학기 미구현

######학과 선택######
#[작성법]
#종강시에서 대학 + 학과 몇번째에 있는지를 기준으로 작성
#예시)
# 공과대학 컴퓨터공학부 : 대학 5번째, 학과 19번째 -> 0519
# KU융합과학기술원 미래에너지공학과 : 대학 1번째, 학과 1번째 -> 0101
limitMAJOR = True   #True: 한 학과만 불러오기, False: 모든 학과 불러오기
MAJOR = '0519'      #총 4글자

lectures = makeLectures(YEAR, GRADE, SEMESTER, limitMAJOR, MAJOR)

##아웃풋 형식##
