# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:12:01 2020

@author: rmileng
"""
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}

######################### method 1 (mine)
total_rank = []
total_title = []
total_star = []
total_quote = []
total_comment = []

for i in range(0,226,25):
    print ("Page " + str(i))
    response = requests.get("https://movie.douban.com/top250?start={}&filter=".format(i),headers=headers)
    response.encoding = 'utf-8'    
    
    if response.status_code == 200:    
        soup = BeautifulSoup(response.text, 'lxml')     
    
    lis = soup.find_all('li')
    for movie in lis:
        if movie.find_all('span',{'class':'title'}) == []:
            continue
        rank =  movie.find_all('em')[0].get_text()
        title = movie.find_all('span',{'class':'title'})[0].get_text()
        star = movie.find_all('span',{'class':'rating_num','property':'v:average'})[0].get_text()
        quote = movie.find_all('span',{'class':'inq'})
        
        commentinfo = movie.find_all('div',{'class':'star'})
        num = re.findall(r'\d+',str(commentinfo))[-1]
        
        total_rank.append(rank)
        total_title.append(title)
        total_star.append(star)
        total_comment.append(num)
        # total_quote.append(quote)      
        if quote != []:
            total_quote.append(quote[0].get_text())
        else:
            total_quote.append('无')
            
# 用pandas输出为csv格式的文件
data = {'title':total_title,
    'rank':total_rank,
    'star':total_star,
    'quote':total_quote,
    'comment':total_comment}
df = pd.DataFrame(data)
df.to_csv('douban_movie2.csv',index=False,header=True,encoding='utf-8-sig')

## write txt
data2 = list(zip(total_title,total_rank,total_star,total_comment,total_quote)) # list-tuple
data3 = list(map(list,data2)) # list-list

with open('douban_movie3.txt','w',encoding='utf-8-sig') as f:
    for listitem in data2:
        f.writelines('%s\n' %listitem)

######################### method 2 (online)
def make_url_lists():
    url_list = []
    for i in range(0,226,25):
        url = "https://movie.douban.com/top250?start={}&filter=".format(i)
        url_list.append(url)
    return url_list

url_list =  make_url_lists()

total_rank_list = []  
total_movie_name = []
total_movie_score = []
total_comment_num = []
total_quote_list = []

for url in url_list:
    
    movie_name = []
    comment_num = []
    quote_list = []

    res = requests.get(url,headers=headers)
    res.raise_for_status()
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, "html.parser")
    
    rank = soup.select('em')
    rank_list = [i.getText() for i in rank]

    score = soup.select('.rating_num')
    movie_score = [j.getText() for j in score]
    
    ## big difference: find its upper tag which only includes the subtags you want 
    movie_list = soup.find('ol',attrs={'class':'grid_view'})
    
    for movie in movie_list.find_all('li'):
    
        name = movie.find('span',attrs={'class':'title'}).getText()
        movie_name.append(name)
    
        comment_info = movie.find('div',attrs = {'class':'star'})
        num = re.findall(r'\d+',str(comment_info))[-1]
        comment_num.append(num)
        
        quote = movie.find('span',attrs = {'class':'inq'})
        if quote is not None:
            quote_list.append(quote.getText())
        else:
            quote_list.append('无')
            
    total_rank_list.extend(rank_list)
    total_movie_name.extend(movie_name)
    total_movie_score.extend(movie_score)
    total_comment_num.extend(comment_num)
    total_quote_list.extend(quote_list)

# 用pandas输出为csv格式的文件
data = {'电影排名':total_rank_list,'电影名称':total_movie_name,\
        '电影评分':total_movie_score,'评论人数':total_comment_num,\
        '短评':total_quote_list}
df = pd.DataFrame(data)
df.to_csv('douban_movie.csv',index=False,header=True,encoding='utf-8-sig')





