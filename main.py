from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
# Important Arguments won't eun without them in Gitpod
options.add_argument("--disable-dev-shm-usage") 
options.add_argument("--headless")  
#예제
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



url = "https://www.naver.com/"

driver.get(url)

print(driver.page_source)

# driver.get("https://www.example.com")
# print(driver.title)

# driver.quit()
