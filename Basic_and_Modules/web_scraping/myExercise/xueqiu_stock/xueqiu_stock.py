# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:51:39 2020

动态网页：雪球网

@author: rmileng
"""

import requests   
import json # It's common to transmit and receive data between a server and web application in JSON format.
import pymysql   
from jsonpath import jsonpath
import time
import multiprocessing as mp
    
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

      
headers = {'Cookie':'s=bp1z9wdwyo; xq_a_token=b2f87b997a1558e1023f18af36cab23af8d202ea; xq_r_token=823123c3118be244b35589176a5974c844687d5e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU4MzE0MzIwMCwiY3RtIjoxNTgxMzAwMzc4NzA0LCJjaWQiOiJkOWQwbjRBWnVwIn0.YBpkA2xVxqGJU0SLHx2N8LJt-WYgFv6yND3J8ybO8hjaBkJK3Vn6F7kB-BXS3beZeFLoFF8-hS14QNoVOF_9MJ3oEwu8A2ORpzazhZewk637ZHl_ctZ7_wvEOWxCT7HUY-3FdaoOQJuHJIRIDeysZqhzHQSP2_tV00cudkqTtCGiM0rx2V16RXAQFbH6Ttb2XDtmGyaZ516EPiEsx42BcPT4IXaZSGXU0CB_IoCls3rDQfwpKtGFhjiTH3vFH6xM_Najg4eLASeQgiz-W-AFFk7g2RVb63YCFVpHIu5lOIAbPqItXte2Ir1sCM8bEDiWHEQgI84CyzEtSsgZ3k3fnQ; __utmc=1; __utmz=1.1581300379.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); u=171581300379555; device_id=c6e2843b6b4a1bb755f9883389edd391; Hm_lvt_1db88642e346389874251b5a1eded6e3=1581300380; __utma=1.216423986.1581300379.1581300379.1581316758.2; __utmb=1.1.10.1581316758; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1581317514',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        'Referer':'https://xueqiu.com/hq'}

url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1581317627074'
response = requests.get(url,headers=headers)
        
json_str = response.text    
unicodestr = json.loads(json_str)

### method1 (only one page)
comp_symbol = jsonpath(unicodestr,'$..list..symbol')    
comp_name = jsonpath(unicodestr,'$..list..name')
comp_current = jsonpath(unicodestr,'$..list..current')
comp_mc = jsonpath(unicodestr,'$..list..market_capital')
comp_shares = jsonpath(unicodestr,'$..list..total_shares')
comp_turnover = jsonpath(unicodestr,'$..list..turnover_rate')

# connect to database
sql = 'create table xueqiu (symbol char(50) NOT NULL, name char(50) NOT NULL, current float NULL, market_capital int(50) NULL, total_shares int NULL, turnover_rate float NULL, PRIMARY KEY (symbol)) Engine = InnoDB;'
sql = 'alter table xueqiu modify column market_capital decimal(20,1);'
sql = 'truncate table xueqiu;'
mc = mysql_conn()
mc.execute_modify_mysql(sql)

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
    
    
## all pages (method2)
time1 = time.time()
for i in range(1,131):
    print('Page: ', str(i))
    url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1581319605192'.format(i)        
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

time2 = time.time()
print('normal time is: ', time2-time1)  # 73.09397315979004 s

## all pages using multiprocessing (method3)
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


############### all pages using Asyncio (method4)
## 应用： 协程在解决 IO 密集型任务上有优势
## referebce: https://juejin.im/post/5b430456e51d45198a2ea433
import asyncio
import aiohttp


async def get_url(url,headers): 
    session = aiohttp.ClientSession()
    response = await session.get(url,headers=headers) # requests 返回的 Response 对象不能和 await 一起使用
    json_str = await response.text()
    session.close()
    return json_str
        
async def eachpage2(url,headers):
    json_str =  await get_url(url,headers) 
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
            sql = 'insert into xueqiu (symbol,name,current,market_capital,total_shares,turnover_rate) values ("{symbol}", \
            "{name}","{current}","{market_capital}","{total_shares}","{turnover_rate}")'.format(**db)
            mc = mysql_conn()
            mc.execute_modify_mysql(sql)
        except:
            pass    

urls = get_urls()

## 执行    
t1 = time.time()
tasks = [asyncio.ensure_future(eachpage2(url,headers)) for url in urls]
loop = asyncio.get_event_loop()             # 建立 loop
loop.run_until_complete(asyncio.wait(tasks))         # 执行 loop
#for task in tasks:
#    print('Task Result:', task.result())
    
#loop.close()                                # 关闭 loop
print("Async total time : ", time.time() - t1)    # 39s


## 如果遇到了 await，那么就会将当前协程挂起，转而去执行其他的协程，直到其他的协程也挂起或执行完毕，再进行下一个协程的执行。
# 我们可以使用 async 关键字来定义一个方法，这个方法在调用时不会立即被执行，而是返回一个协程对象。
# task：任务，它是对协程对象的进一步封装，包含了任务的各个状态。
#future：代表将来执行或没有执行的任务的结果，实际上和 task 没有本质区别。
#async 定义的方法就会变成一个无法直接执行的 coroutine 对象，必须将其注册到事件循环中才可以执行。
#task，它是对 coroutine 对象的进一步封装，它里面相比 coroutine 对象多了运行状态，比如 running、finished 等
#接下来我们再了解一下 await 的用法，使用 await 可以将耗时等待的操作挂起，让出控制权。当协程执行的时候遇到 await，时间循环就会将本协程挂起，转而去执行别的协程，直到其他的协程挂起或执行完毕。

