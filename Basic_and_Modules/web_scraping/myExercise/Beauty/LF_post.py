# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:42:45 2020

post+session

@author: rmileng
"""
import requests
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}

url = r'https://www.lookfantastic.com.sg/login.jsp?returnTo=https%3A%2F%2Fwww.lookfantastic.com.sg%2FaccountHome.account'
payloads = {
        'username':'Lengyueshuang.Luna@gmail.com',
        'password':'7993725shuang'}
response = requests.post(url,headers=headers,data=payloads)
## then it will return the first page source after login
cookies = response.cookies.get_dict()

'''
cookies中存储着session的编码信息，session中又存储了cookies的信息
'''

session=requests.session()
url='https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-login.php'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
data={
    'log':input('请输入账号：'),
    'pwd':input('请输入密码：'),
    'wp-submit':'登录',
    'redirect_to':'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-admin/',
    'testcookie':'1'
}
session.post(url,headers=headers,data=data)
print(type(session.cookies)) # RequestsCookieJar是cookies对象的类
print(session.cookies)
'''
json模块能把字典转成字符串。我们或许可以先把cookies转成字典，然后再通过json模块转成字符串。这样，就能用open函数把cookies存储成txt文件。
'''
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
#把cookies转化成字典。
print(cookies_dict)
#打印cookies_dict
cookies_str = json.dumps(cookies_dict)
#调用json模块的dumps函数，把cookies从字典再转成字符串。
print(cookies_str)
#打印cookies_str
f = open('cookies.txt', 'w')
#创建名为cookies.txt的文件，以写入模式写入内容。
f.write(cookies_str)
#把已经转成字符串的cookies写入文件。
f.close()
#关闭文件。
'''
读取cookies则刚好相反，要先把字符串转成字典，再把字典转成cookies本来的格式。
'''
cookies_txt = open('cookies.txt', 'r')
#以reader读取模式，打开名为cookies.txt的文件。
cookies_dict = json.loads(cookies_txt.read())
#调用json模块的loads函数，把字符串转成字典。
cookies = requests.utils.cookiejar_from_dict(cookies_dict)
#把转成字典的cookies再转成cookies本来的格式。
session.cookies = cookies
#获取cookies：就是调用requests对象（session）的cookies属性。







