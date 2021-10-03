# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:25:26 2020

@author: rmileng
"""

import re
from bs4 import BeautifulSoup
import requests
import time

base_url = 'https://mp.weixin.qq.com/s/KBPhJmA3taZG0YkzoeuJsQ'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}

def crawl(url):
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'
    return response.text # return html

def parse(html):
    soup = BeautifulSoup(html,'lxml')
    all_href = soup.find_all('a',{'href':re.compile(r'https://.+?')})
    page_urls = set([l['href'] for l in all_href]) # 网页的所有url
    title = soup.find('h2').get_text().strip()
    url = soup.find('meta', {'property': "og:url"})['content']  # 爬的该网页的url
    return title,page_urls,url

import multiprocessing as mp

if __name__=='__main__':
    unseen = set([base_url,])
    seen = set()
    
    count, t1 = 1, time.time()
    
    all_links = []
    all_titles = []
    
    pool = mp.Pool(6)
    
    while len(unseen) != 0: 
        crawl_jobs = [pool.apply_async(crawl,args=(url,)) for url in unseen]
        htmls = [j.get() for j in crawl_jobs]
        
        parse_jobs = [pool.apply_async(parse,args=(html,)) for html in htmls]
        results = [j.get() for j in parse_jobs]
        
        seen.update(unseen)         # seen the crawled
        unseen.clear() 
        
        for title,page_urls,url in results:
            print(count,title, url)
            all_links.append(url)
            all_titles.append(title)
            count += 1
            unseen.update(page_urls - seen) 
        # get new url to crawl
    print('Total time: %.1f s' % (time.time()-t1, )) # 31.3s       