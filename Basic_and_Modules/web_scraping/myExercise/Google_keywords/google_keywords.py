# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import urllib.request
import requests
from bs4 import BeautifulSoup
import pickle
import multiprocessing as mp
import time 


''' Tips:
之前没有得到完整的list的原因是header!!!!所以header以后一定用上述模板
Q： 解析最后得到的tag/list/...不完整
步骤： 
1. 首先分析是response的问题还是soup的问题（可以打印下来寻找代码是否完整）
2. 如果是第一步(response)的问题，可能是header的问题，加/改cookie； 
   a. 'User-Agent也可能有问题，可以换成IE的Agent或者直接删掉User-Agent
   b. Cookie要找ALL下面request url和Input url相同的
3. 如果是第二部（soup)的问题，可能是解析器的问题，在3个解析器中轮番替换: html5lib（import html5lib）, lxml, html.parser
 '''
 
 
def scrape_google(result,ikey):
#    print(ikey)
    url = r'https://www.google.com/search?q=%s&rlz=1C1GCEU_zh-CNSG879SG879&oq=%s&aqs=chrome..69i57j69i59.26344j0j8&sourceid=chrome&ie=UTF-8'% (ikey,ikey)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
               'Cookie':'CGIC=EhcxQzFHQ0VVX3poLUNOU0c4NzlTRzg3OSJ8dGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOQ; HSID=AKDP2F9to5O0O18pN; SSID=A4lnI5GRoYiSTaN73; APISID=rvkvB3xk-ame6mIB/AlpTMppVTtUrqV7Cg; SAPISID=-SRrEoXmOwd3Oc39/AZNhFcL9CdLT5E7bL; __Secure-HSID=AKDP2F9to5O0O18pN; __Secure-SSID=A4lnI5GRoYiSTaN73; __Secure-APISID=rvkvB3xk-ame6mIB/AlpTMppVTtUrqV7Cg; __Secure-3PAPISID=-SRrEoXmOwd3Oc39/AZNhFcL9CdLT5E7bL; CONSENT=YES+CN.zh-CN+20161204-19-0; SEARCH_SAMESITE=CgQIgI8B; SID=uwf4_pRqxZHRVduLXRzSsqTgDuIjgCRaM6deZa0D4ch3HFRK2r5zxlJeoag3mRzPnSq53A.; __Secure-3PSID=uwf4_pRqxZHRVduLXRzSsqTgDuIjgCRaM6deZa0D4ch3HFRKKOABMsfzY7ZXBCkfUl69Ag.; ANID=AHWqTUk_PGSmaq1mwAbjXIgiB3vm6ABTPHCyQxEkobbjG-X2OtNCC1OQWhyooJjF; NID=200=OX5vgIHH8JRB6T_ue6b-_TxC6hEzFPraYkHlDkOQwsUzUENMRAKvJcCged8Vj5pO9Pwxmhm6lbSfdP-Exh9vDC5LB8oLsxCgrEmuW63NleJZrg6iKe10PC9XPgT38aVI-sMjVFsDUTIllt6uqYsUs5YOBsIPrwtLRWTqOjMv125oSvMdknkOE0H0CDFxw2glLZp8xuD0-6ScWnfVUwKEUark1VW6SXzwn2_ir4cp; 1P_JAR=2020-3-23-3; DV=Y1M2HrVpVbtK4NvUndzzyhlNKIpYEBcvSfGgakoo6QAAAGCqGssnH9E8XQAAAFQ5Rwsg6qLjQgAAAA; SIDCC=AJi4QfEHTc0pflnG1tZ5_eZ6suQ-wQ8m7XIgRE10QLz4Fg6KMAIAugDj_CKPJriK-l9xsBSyWA',
               'Referer':url}    
# even though you change the link, the old cookie is still available
   
    response = requests.get(url,headers=headers) 
    soup = BeautifulSoup(response.text, 'html.parser') # html5lib, lxml, html.parser
    all_infos = soup.find_all('div',class_='srg')
    allhref = []
    for all_info in all_infos:
        all_g = all_info.find_all('div',class_='g')
   #     print(len(all_g))
        p_allhref = [r.find('a')['href'] for r in all_g]
  #      print(p_allhref)
        allhref.extend(p_allhref)
    
    if len(allhref) == 10:  
        result[ikey] = allhref        
    else:
        result['!!!'+ikey] = allhref
        print('the list length for %s is shorter than 10' % ikey)    
        
    return result   
    
def multicore(): 
    keyword_list = ['covid 2019','American market crisis','oil price strike','music','love','a stock market']
    pool = mp.Pool(processes=6)
    mg = mp.Manager()
    result = mg.dict()

    [pool.apply_async(scrape_google,(result,ikey)) for ikey in keyword_list]
    pool.close()
    pool.join()    
    
    output = dict(result) # have to return it to normal dict so to save it
#    print(type(result))
    
    with open(r'D:\LYS\python_learning\exercise\web_scraping\Google_keywords\google_result3.pickle','wb') as file:
       pickle.dump(output,file)


if __name__ == '__main__':
    s1_time = time.time()
    multicore()
    s2_time = time.time()
    print(s2_time-s1_time)
    
    
#with open(r'D:\LYS\python_learning\exercise\web_scraping\Google_keywords\google_result3.pickle','rb') as file:
#    load_dict = pickle.load(file)

#with open('soup.txt','w') as file:
#    file.write(soup.prettify())  








