#-*- coding: utf-8 -*
import requests
import random
from bs4 import BeautifulSoup
import re

def beauty_crawler(name):
    image_urls = []
    re_img = re.compile("http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png)") #圖片網站 imgur的 regex pattern
    #由request.session傳送PTT年齡驗證
    sess = requests.session()
    sess.post("https://www.ptt.cc/ask/over18", data={"from":"bbs/Beauty/index.html", "yes":"yes"})

    search_url = f"https://www.ptt.cc/bbs/Beauty/search?q={name}"
    search_result = sess.get(search_url)

    web = BeautifulSoup(search_result.text, "html.parser")
    titles = web.select("div.title a")

    for title in titles:
        title_url = sess.get(f"https://www.ptt.cc/{title['href']}") #取得每篇文章網址
        content = BeautifulSoup(title_url.text, "html.parser")
        images = re_img.findall(content.text)
        image_urls += [x for x in images if x.startswith('https')] #僅保留https開頭之網址
        if len(image_urls) > 10:
            break
    return random.choice(image_urls)