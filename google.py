# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 00:03:32 2021

@author: Bill
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

driver=webdriver.Chrome("./chromedriver")
#直接指定chromedirver的路徑位置，例如把要執行的.py檔和chromedirver放在同一個folder，並在起始browser時指定chromedirver的路徑：webdriver.Chrome("./chromedriver")
driver.get("https://www.google.com")

#關鍵字輸入
q=driver.find_element_by_name("q")
print("關鍵字輸入")
a=input()
q.send_keys(a)
from selenium.webdriver.common.keys import Keys
q.send_keys(Keys.RETURN)

from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')
url=soup.select("div.hdtb-mitem a")       # 圖片 影片 新聞 地圖
imgurl=url[0].get("href")                 #picture 網址
print('https://www.google.com/'+imgurl)


import time
pgn=3
def googletitle(page):
    title1 = soup.find_all('h3',class_='LC20lb DKV0Md')
    for t in title1:
        print(t.text)
#     for p in range(page):
#         driver.find_element_by_link_text('下一頁').click()
#         soupnext = BeautifulSoup(driver.page_source, 'lxml')
#         for ele in soupnext.select('h3.LC20lb DKV0Md'):
#             print(ele.text)
#         time.sleep(1)

def goodlepic(url):
    r = requests.get('https://www.google.com/'+url) #picture網址
    soup = BeautifulSoup(r.text, 'lxml')
    picCount=0
    
    for ele in soup.select('img'): #class可能改
        if 'https://encrypted-tbn0.gstatic.com/images?q=tbn:'  in ele.get('src'):
            print(ele.get('src'))
            with open(str(picCount)+'.jpg','wb') as file:
                res = requests.get(ele.get('src'))
                for r in res:
                    file.write(r)
                picCount = picCount + 1

googletitle(pgn)
goodlepic(imgurl)