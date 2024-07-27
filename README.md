<div align="center" style="margin-top: 0;">
  <h1>✨ Konkuk Univ. lecture schedule(종강시) crawler 🤖</h1>
</div>
<em>
  <h5 align="center">(Programming Language - Python 3)</h5>
</em>
  
---

This Docker environment is designed to facilitate web scraping using Python with Selenium and Google Chrome. It comes preinstalled with all the necessary tools and configurations to run Selenium web scraping scripts.


## Usage

1️⃣ main.py의 옵션 수정

2️⃣ 실행

 * 로컬에서 사용시 Dockerfile, .gitpod.yml 삭제 후 사용하여도 문제 없음.

## v.2 변경 사항

<div>
  id_dict = {<br/>
    2: 'course_num',<br/>
    3: 'class',<br/>
    4: 'lecnum',<br/>
    5: 'name',<br/>
    6: 'credit',<br/>
    7: 'hour',<br/>
    8: 'type_name',<br/>
    9: 'lang',<br/>
    10: '해설', -> 제거<br/>
    11: 'note',<br/>
    12: 'class_elective',<br/>
    13: 'grade',<br/>
    14: 'basic_major',<br/>
    15: 'instructor',<br/>
    16: 'info' -> 'time'<br/>
    + : 'notice'<br/>
  }

</div>


## 추가될 기능

- 해설 및 영문명 불러오기

## About Image

The Docker image `Chetan11/gitpod-selenium` contains:

- Google Chrome: A web browser required for Selenium to interact with web pages.
- Python 3: The programming language in which the web scraping script is written.
- Selenium: A web testing library for Python to automate web browser interaction.
- `webdriver-manager`: A tool to manage the browser driver for Chrome.
