# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:52:15 2020

@author: rmileng
"""

import multiprocessing as mp
import time
import json
from jsonpath import jsonpath
import requests

headers = {'Cookie':'yfx_c_g_u_id_10000042=_ck20021010264813547241018717773; VISITED_MENU=%5B%228451%22%2C%228528%22%2C%229055%22%5D; VISITED_COMPANY_CODE=%5B%22600000%22%2C%22600010%22%2C%22600004%22%5D; VISITED_STOCK_CODE=%5B%22600000%22%2C%22600010%22%2C%22600004%22%5D; seecookie=%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C%2C%5B600010%5D%3A%u5305%u94A2%u80A1%u4EFD%2C%5B600004%5D%3A%u767D%u4E91%u673A%u573A; yfx_f_l_v_t_10000042=f_t_1581301608356__r_t_1581301608356__v_t_1581302307081__r_c_0',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
           'Referer':'http://www.sse.com.cn/assortment/stock/list/share/'}

def find_pageA(c): #根据传递参数c（提取的页数）来选择目标url地址
        return 'http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback58056&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage='+str(c)+'&pageHelp.pageSize=25&pageHelp.pageNo='+str(c)+'&pageHelp.endPage='+str(c)+'1&_=1581305654651'+str(c-1)

def datascreenA(unicodestr):#封装解析输出的部分
    COMPANY_CODE=jsonpath(unicodestr,'$..pageHelp..COMPANY_CODE')#公司/A股代码
    COMPANY_ABBR=jsonpath(unicodestr,'$..pageHelp..COMPANY_ABBR')#公司/A股简称
    list_date=jsonpath(unicodestr,"$..pageHelp..LISTING_DATE") #A股总资本
    
    L1=list()
    L2=list()
    L3=list()
    for x in COMPANY_CODE:
        L1.append(x)
    for x in COMPANY_ABBR:
        L2.append(x)
    for x in list_date:
        L3.append(x)
    
    #由于同时解四个包太过复杂，python不干，故拆分开来
    x=0
    print('公司/A股代码','\t','公司/A股简称','\t','上市日期')
    while(x<len(L1)):
        print(L1[x],'\t','\t',L2[x],'\t','\t',L3[x])
        x+=1
        
def get_unicodestr(c):
    response = requests.get(find_pageA(c),headers=headers)
    json_str ='{"content":'+response.text[19:-1]+'}'
    unicodestr=json.loads(json_str)
    return unicodestr
    
def collect_30_pagesA2():#调取30页，相当于主函数
    pool = mp.Pool(4)
    c=1
    st = time.time()
    while(c<31):
        print('第', c, '页:')
        response=pool.apply_async(get_unicodestr,(c,))
        datascreenA(response.get())
        c+=1
    str1 = time.time()
    print('multiprocessing time:', str1 - st)

if __name__=='__main__':
    collect_30_pagesA2() # 14秒