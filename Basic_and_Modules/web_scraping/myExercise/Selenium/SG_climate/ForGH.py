# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:07:15 2020

@author: -
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import datetime
import time

url = r'http://www.weather.gov.sg/climate-historical-daily//'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
info = soup.find('div',class_='btn-group')
states = [a.text for a in info.find_all('li')]
## cannot achieve this because button aria-expanded="false, should use json instead
Months = soup.find('div',{'class':'selectbox','id':'monthContainer'})
months = [m.text for m in Months.find_all('li')]
MONTH = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
Year = ["2019","2020"]
count = 1

driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get("http://www.weather.gov.sg/climate-historical-daily/")
for iciti in states:
    driver.find_element_by_id("cityname").click()
    time.sleep(1)
    driver.find_element_by_link_text(iciti).click()
    time.sleep(1)
    for iyear in Year:
        if iyear == str(datetime.datetime.now().year): # for 2020, part of months
            driver.find_element_by_id("year").click()
            time.sleep(1)
            driver.find_element_by_link_text(iyear).click()
            time.sleep(1)
            for imonth in months:
                driver.find_element_by_id("month").click()
                time.sleep(1)       
                driver.find_element_by_link_text(imonth).click()
                time.sleep(1)
                driver.find_element_by_id("display").click()
                time.sleep(3)
#                locals()['botton'+str(count)] = driver.find_element_by_link_text("CSV")
#                locals()['botton'+str(count)].click()
#                count += 1
                driver.find_element_by_link_text("CSV").click()
                time.sleep(1)
        else: # before 2020, all months
            driver.find_element_by_id("year").click()
            time.sleep(1)
            driver.find_element_by_link_text(iyear).click()
            time.sleep(1)
            for imonth in MONTH:
                driver.find_element_by_id("month").click()
                time.sleep(1)       
                driver.find_element_by_link_text(imonth).click()
                time.sleep(1)
                driver.find_element_by_id("display").click()
                time.sleep(3)
#                locals()['botton'+str(count)] = driver.find_element_by_link_text("CSV")
#                locals()['botton'+str(count)].click()
#                count += 1
                driver.find_element_by_link_text("CSV").click()
                time.sleep(1)
driver.quit() # 关闭chrome

#for i in range(4):
#    locals()['v'+str(i)]=i**2