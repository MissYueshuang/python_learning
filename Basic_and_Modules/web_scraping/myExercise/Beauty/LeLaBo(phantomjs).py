# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:15:31 2020

selenium+PhantomJS 动态爬虫

@author: rmileng
"""
from selenium import webdriver
import time
from auto_send_email import sent_email_from_outlook
# from selenium.webdriver.common.by import By

def beauty():
    driver = webdriver.PhantomJS(r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(r'https://www.selfridges.com/SG/zh/cat/prod_141-77035800-448065DRW1T/')
    
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//div[@class='sorrymessage']")
        print('out of stock')
        sent_email_from_outlook('Gucci bag','still out of stock')
    except:
        print('in stock')
        sent_email_from_outlook('Gucci bag','in stock now, buy immediatly!!')
#    product = content.text.split('\n')
#    result = ['Body' in f for f in product]
    # driver.find_element_by_xpath("//a[contains(text(), 'Lys')]").text
    # find_element_by_xpath("//a[contains(text(), 'Pricing') and contains(text(), 'Catalogues')]")
#    if any(result):
#        body = 'LYS body lotion is in stock now!!!'
#        sent_email_from_outlook('网购啦',body)
if __name__ == '__main__':
    beauty()
'''
 This is for Le labo (json method, but you cannot repeatedly use this method because the link will be invalid)

headers2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
url2 = 'https://www.selfridges.com/api/cms/ecom/v1/SG/en/search/le+labo+41?pageNumber=1&pageSize=60&freeText=le+labo+41'
response2 = requests.get(url2,headers=headers2)
unicodestr = json.loads(response2.text)
product_names2 = [f['name'] for f in unicodestr['catalogEntryNavView']]
result2 = ['body' in f for f in product_names2]
if any(result2):
    body2 = 'LYS body lotion is in stock now!!!'
else:
    body2 = 'LYS body lotion has not be in stock yet!!!'   

# sent_email_from_outlook('网购啦',body2, df=result)
'''
    
#with open(r'D:\LYS\python_learning\exercise\web_scraping\Beauty\test.txt','w') as f:
#    f.write(driver.page_source)