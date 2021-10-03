# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:49:47 2020

F9: 运行当前行 

@author: rmileng
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd

def shopping():
    ## search for beauty
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
    ## This is for viviscal
    url = 'https://www.lookfantastic.com.sg/brands/viviscal/all.list'
    # url = 'https://www.lookfantastic.com.sg/brands/shiseido/all-shiseido.list'
    response = requests.get(url,headers=headers)
    if response.status_code == 200:    
        soup = BeautifulSoup(response.text, 'lxml')
    allitem = soup.find('ul',{'class':'productListProducts_products'})
    lists = allitem.find_all('li',{'class':'productListProducts_product'})
    product = {}
    for li in lists:
        name = li.h3.text    
        price = li.find('span',class_='productBlock_priceValue').text
        product[name] = price
    result = pd.DataFrame.from_dict(product,orient='index',columns=['price'])
    # body3 = json.dumps(product,sort_keys=True, indent=4)
    

if __name__ == '__main__':
    shopping()
    