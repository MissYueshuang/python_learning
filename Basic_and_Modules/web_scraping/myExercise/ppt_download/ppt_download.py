# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:54:55 2020

@author: rmileng
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': r'D:\LYS\python_learning\exercise\web_scraping\ppt_download\download'}
options.add_experimental_option('prefs', prefs)

url = r'https://www.slideshare.net/nadeemakhter7374?utm_campaign=profiletracking&utm_medium=sssite&utm_source=ssslideview'
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=options)
driver.get(url)
driver.find_element_by_link_text("View all").click()
time.sleep(1)
driver.find_element_by_link_text("Microbial fuel cell ad...").click() ## randomly select a ppt
time.sleep(1)
#driver.find_element_by_xpath("//ul[@id='slideshow-actions']/li[3]/button").click()
#driver.find_element_by_xpath("//div[@id='ss-login-header']/p/a/span").click()
#driver.find_element_by_id("user_login").click()
#driver.find_element_by_id("user_login").clear()
        
driver.find_element_by_id("login").click()
time.sleep(1)
driver.find_element_by_id("user_login").click()
time.sleep(1)
driver.find_element_by_id("user_login").clear()
time.sleep(1)
driver.find_element_by_id("user_login").send_keys("YueshuangLeng")
time.sleep(1)
driver.find_element_by_id("user_password").clear()
time.sleep(1)
driver.find_element_by_id("user_password").send_keys("7993725shuang")
time.sleep(1)
driver.find_element_by_id("login_from_loginpage").click()
time.sleep(3)        
        
driver.find_element_by_xpath("//a[contains(text(),'Explore')]").click()

# get cookie
cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
cookiestr = ';'.join(item for item in cookie)  
url_new = driver.current_url
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
           'Cookie':cookiestr,
            'Referer':url_new}         
response = requests.get(url_new,headers=headers)
soup = BeautifulSoup(response.text,'lxml')
lists = soup.find('section',{'id':'topics-content','class':'ss-content'})
details = lists.find_all('div',class_='details')
topics = [t.find('a').text for t in details]

for itopic in topics[:2]: 
    driver.find_element_by_link_text(itopic).click()
    time.sleep(3) 
#    driver.find_element_by_xpath("//section[@id='list-page-content']/div/div/ul/li[100]/div/div/div[4]/a[2]/i").click()
    nli = 1
    while nli < 21: # 20 limit a day        
        try:
            driver.find_element_by_xpath("//section[@id='list-page-content']/div/div/ul/li[%d]/div/div/div[4]/a[2]/i"%nli).click()
            if EC.alert_is_present()(driver):
                driver.switch_to_alert().accept() #接受警告（等于点了个确定） 
                time.sleep(3)
            time.sleep(3)
            print('download %d successfully' % nli)
            nli += 1
            # 原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
                # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
                break     


#with open('soup.txt','w') as file:
#    file.write(soup.prettify())  

       
        