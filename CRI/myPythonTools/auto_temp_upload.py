# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 18:12:34 2020

@author: rmileng
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import numpy as np

driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
url = 'https://myaces.nus.edu.sg/htd/'
driver.get(url)
driver.find_element_by_id("userNameInput").click()
driver.find_element_by_id("userNameInput").send_keys("nusstf\\rmileng")
#driver.find_element_by_id("content").click()
#driver.find_element_by_id("loginForm").submit()
driver.find_element_by_id("passwordInput").send_keys("7993725Shuang")
driver.find_element_by_id("submitButton").click()

temp = str(round(np.random.uniform(36.0,37.0),1)) # randomly regerate my temp

if time.localtime().tm_hour == 9: ## in the morning
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("AM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_name("Save").click()
elif time.localtime().tm_hour == 14:
    driver.find_element_by_name("declFrequency").click()
    Select(driver.find_element_by_name("declFrequency")).select_by_visible_text("PM")
    driver.find_element_by_id("temperature").click()
    driver.find_element_by_id("temperature").clear()    
    driver.find_element_by_id("temperature").send_keys(temp)
    driver.find_element_by_name("Save").click()
driver.quit() # 关闭chrome