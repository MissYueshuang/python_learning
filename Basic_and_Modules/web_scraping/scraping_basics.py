# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:36:10 2020

@author: rmileng
"""
######################################################## 正则表达式
import re
from urllib.request import urlopen

html = urlopen("https://morvanzhou.github.io/static/scraping/basic-structure.html").read().decode('utf-8')
print(html) # 读出来的是源码

## select information using 正则表达式（选取文本信息），初级网页匹配

# 找到网页title
res = re.findall(r"<title>(.+?)</title>",html)
print("\nPage title is: ", res[0])

# 选择超链接
res = re.findall(r'href="(.*?)"',html)
print('\nAll links:', res)

# 中间段落
res = re.findall(r"<p>(.*?)</p>",html,flags=re.DOTALL) # 这个段落在 HTML 中还夹杂着 tab, new line, 所以我们给一个 flags=re.DOTALL 来对这些不敏感.
print("\nPage paragraph is: ", res[0])

########################################################  Beautiful Soup 简化匹配
## https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/ 中文参考文档
# pip install beautifulsoup4

from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://morvanzhou.github.io/static/scraping/basic-structure.html").read().decode('utf-8')
print(html) 
soup = BeautifulSoup(html,features='lxml') # 不过大家都推荐使用 lxml 的形式
print(soup.h1)
print(soup.title)


all_href = soup.find_all('a')
print(all_href)
allhref = [l['href'] for l in all_href] # 像字典一样找到属性，这里是href
print('\n',allhref)

######################################################## CSS解析网页
# 网页是由 HTML和 CSS组成
from bs4 import BeautifulSoup
from urllib.request import urlopen

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/list.html").read().decode('utf-8')
print(html)

soup = BeautifulSoup(html,features='lxml')

## use class to narrow search
month = soup.find_all('li',{'class': 'month'})
for m in month:
    print(m.get_text())
[print(m.get_text()) for m in month]


######################################################## BS+正则表达式
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

# if has Chinese, apply decode()
html = urlopen("https://morvanzhou.github.io/static/scraping/table.html").read().decode('utf-8')
print(html)


soup = BeautifulSoup(html, features='lxml')

img_links = soup.find_all("img", {"src": re.compile('.*?\.jpg')})
for link in img_links:
    print(link['src'])


course_links = soup.find_all('a', {'href': re.compile('https://morvan.*')})
for link in course_links:
    print(link['href'])

course_names = soup.find_all('tr', {'id': re.compile('course*')})
for name in course_names:
    print(name['id'])

######################################################## 爬百度百科
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random


base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"] #指向网页爬虫

url = base_url + his[-1]

html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
print(soup.find('h1').get_text(), '    url: ', his[-1])

# find valid urls
sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

if len(sub_urls) != 0:
    his.append(random.sample(sub_urls, 1)[0]['href'])
else:
    # no valid sub link found
    his.pop()
print(his)


his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

for i in range(20):
    url = base_url + his[-1]

    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("^/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()
        
# 原因：新拼接的url格式错误，无法打开url
        
######################################################## request
import requests
import webbrowser
# get
param = {"wd": "莫烦Python"}
r = requests.get('http://www.baidu.com/s', params=param)
print(r.url)
webbrowser.open(r.url) # 用默认浏览器打开

# post
data = {'firstname': 'mo', 'lastname': 'zhou'}
r = requests.post(
        'http://pythonscraping.com/pages/files/processing.php', 
        data=data)
print(r.text)

# upload fig
file = {'uploadFile': open(r'C:\Users\rmileng\downloads\H.png', 'rb')}
r = requests.post('http://pythonscraping.com/pages/files/processing2.php', files=file)
print(r.text)

# 登陆（用cookies保留登陆状态)
payload = {'username': 'Morvan', 'password': 'password'}
r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
print(r.cookies.get_dict())
r = requests.get('http://pythonscraping.com/pages/cookies/profile.php', cookies=r.cookies)
print(r.text)

# 用session替代cookies
session = requests.Session()
payload = {'username': 'Morvan', 'password': 'password'}
r = session.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
print(r.cookies.get_dict())
r = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(r.text)




