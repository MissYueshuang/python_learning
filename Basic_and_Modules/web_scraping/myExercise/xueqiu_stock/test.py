# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:52:00 2020

@author: rmileng
"""
import requests   
import json # It's common to transmit and receive data between a server and web application in JSON format.
import pymysql   
import time
import multiprocessing as mp
import re

headers = {'Cookie':'s=bp1z9wdwyo; xq_a_token=b2f87b997a1558e1023f18af36cab23af8d202ea; xq_r_token=823123c3118be244b35589176a5974c844687d5e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU4MzE0MzIwMCwiY3RtIjoxNTgxMzAwMzc4NzA0LCJjaWQiOiJkOWQwbjRBWnVwIn0.YBpkA2xVxqGJU0SLHx2N8LJt-WYgFv6yND3J8ybO8hjaBkJK3Vn6F7kB-BXS3beZeFLoFF8-hS14QNoVOF_9MJ3oEwu8A2ORpzazhZewk637ZHl_ctZ7_wvEOWxCT7HUY-3FdaoOQJuHJIRIDeysZqhzHQSP2_tV00cudkqTtCGiM0rx2V16RXAQFbH6Ttb2XDtmGyaZ516EPiEsx42BcPT4IXaZSGXU0CB_IoCls3rDQfwpKtGFhjiTH3vFH6xM_Najg4eLASeQgiz-W-AFFk7g2RVb63YCFVpHIu5lOIAbPqItXte2Ir1sCM8bEDiWHEQgI84CyzEtSsgZ3k3fnQ; __utmc=1; __utmz=1.1581300379.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); u=171581300379555; device_id=c6e2843b6b4a1bb755f9883389edd391; Hm_lvt_1db88642e346389874251b5a1eded6e3=1581300380; __utma=1.216423986.1581300379.1581300379.1581316758.2; __utmb=1.1.10.1581316758; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1581317514',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        'Referer':'https://xueqiu.com/hq'}

class mysql_conn(object):
      # 魔术方法, 初始化, 构造函数  
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1',user='root',password='abc123',database='py101')
        self.cursor = self.db.cursor()
    # 执行modify(修改)相关的操作
    def execute_modify_mysql(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
    # 魔术方法, 析构化 ,析构函数
    def __del__(self):
        self.cursor.close()
        self.db.close()
        

def eachpage(url,headers):
    response = requests.get(url,headers=headers)
    json_str = response.text
    unicodestr = json.loads(json_str)
    list_lsit = unicodestr['data']['list']
    db = {}
    for list_item_dict in list_lsit:
        db['symbol'] = list_item_dict['symbol']
        db['name'] = list_item_dict['name']
        db['current'] = list_item_dict['current']
        db['market_capital'] = list_item_dict['market_capital']
        db['total_shares'] = list_item_dict['total_shares']
        db['turnover_rate'] = list_item_dict['turnover_rate']
        
        try:
            sql = 'insert into xueqiu (symbol,name,current,market_capital,total_shares,turnover_rate) values ("{symbol}","{name}","{current}","{market_capital}","{total_shares}","{turnover_rate}")'.format(**db)
            mc = mysql_conn()
            mc.execute_modify_mysql(sql)
        except:
            pass
    
    
    
def get_urls():
    url_list = []
    for i in range(1,131):
        url='https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1581319605192'.format(i)
        url_list.append(url)
    return url_list

# for i in range(1,131):
def mainfunc(headers):
    pool = mp.Pool(6)
    urls = get_urls() 
    # unicodestrs = [pool.apply_async(get_unicodestr,args=(url,headers)) for url in urls]
    for url in urls:
        res = re.findall(r'page=\d+',url)
        print(res[0])
        pool.apply_async(eachpage,args=(url,headers))
    pool.close()
    pool.join()
    
    
if __name__ == '__main__':
    time1 = time.time()    
    mainfunc(headers)    
    time2 = time.time()
    print('multiprocessing time is: ', time2-time1) # 28s
