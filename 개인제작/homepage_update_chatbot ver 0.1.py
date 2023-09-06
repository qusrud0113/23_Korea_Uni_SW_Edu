from bs4 import BeautifulSoup
from datetime import date
import requests
import time
import telegram
from telegram.ext import Updater
# from telegram.ext import MessageHandler, Filters
import asyncio
import nest_asyncio 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# SQLite3로 DB를 만들어서
# 기존에 없는 데이터가 적재되면 새로운 것으로 인식(key를 보낸다던가)
# 내 텔레그렘에 쏴주는 방식
# 그리고 !과제, !공지를 넣어서
# 신호를 보낸 시간 전까지의 due가 있는 게시글을 보낸다.

# 크롬드라이버 실행
# 아래 웹드라이버를 통해 크롬 드라이버를 다운받는다.
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome() 
Login_url = 'https://lms.sunde41.net/auth/login'


# 로그인이 필요한 사이트이므로 계정 정보 저장
id = :ID
password = :PW

login_date = {
    'id': id,
    'password': password
}

#크롬 드라이버에 url 주소 넣고 실행
driver.get(Login_url)
time.sleep(3)

# 로그인 하기
driver.find_element(By.XPATH , '//*[@id="email"]').send_keys(login_date['id'])
driver.find_element(By.XPATH , '//*[@id="password"]').send_keys(login_date['password'])
driver.find_element(By.XPATH , '//*[@id="button"]').click()
time.sleep(2)


# 전체화면 하기
driver.maximize_window()
# 과제 게시판 클릭
driver.find_element(By.XPATH , '/html/body/div[1]/div/div[1]/div/ul/li[3]/div/ul/li[2]/a/span').click()

# 사이트 과제 텍스트 저장
# tbody > tr의 값 불러와서 dict에 저장
bodys = driver.find_elements(By.TAG_NAME, "tbody")
rows = bodys[0].find_elements(By.TAG_NAME, "tr")
data_set = {}

gb = []
text_data = []
due = []

for index, value in enumerate(rows):
    gb.append(value.find_elements(By.TAG_NAME, "td")[0].text)
    text_data.append(value.find_elements(By.TAG_NAME, "td")[1].text)
    due.append(value.find_elements(By.TAG_NAME, "td")[2].text)
    
data_set['gb'] = gb
data_set['text_data'] = text_data
data_set['due'] = due
data_set

driver.close()

nest_asyncio.apply()
async def main():
    TOKEN = :TOKEN
    # chat_id는 https://api.telegram.org/bot[TOKEN]/getUpdates 에서 채팅을 보낸 후 F5를 눌러 id 값을 가져옴
    chat_id = :CHAT_ID
    bot = telegram.Bot(token = TOKEN)
    today = date.today().isoformat().replace('-', '.')
    
    # 새로운 아이디어 > 기한이 오늘자보다 작거나 같은 등록글은 넣지않음
    # 시간은 9시, 오후 8시 2번 보내는 걸로 수정
    # + !출석이라는 커맨드가 들어오면 due가 당일보다 작거나 같은 과제를 제외한 나머지 과제를 보내는 것으로 수정
    if len(data_set['gb']) != 1:
        for i in range(1, len(data_set['gb'])):
            text = '- 신규 등록) {0} -\n\n구분: {1}\n\n제목: {2}\n\n기한: {3}'.format(today, data_set['gb'][i], data_set['text_data'][i], data_set['due'][i])
            await bot.send_message(chat_id, text)
        time.sleep(2)
        #bf_len += 3
    else:
        pass

    
asyncio.run(main())
driver.quit()