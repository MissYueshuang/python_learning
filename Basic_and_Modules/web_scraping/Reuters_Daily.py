# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:03:50 2019

@author: rmidj
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 04 18:13:59 2019

@author: rmidj -- Duan Junxu
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
import uuid
import datetime

client = MongoClient('gpu8svr',27017)
db = client.admin
db.authenticate("crinlp","123")
db = client.crinlp
collection = db.reuters
#reuters - table name!!!
checktitle = []
CurrentDate = datetime.datetime.now()-datetime.timedelta(1)
CurrentDate = CurrentDate.strftime("%Y-%m-%d")

for i in range(1,1000,1):
    print ("Page " + str(i))
    dic = {}
    url = "https://www.reuters.com/news/archive/banks?view=page&page={}&pageSize=10".format(i)
    html =urlopen(url)
    bsObj = BeautifulSoup(html,"html.parser")
    links =  bsObj.find("div",{"class":"column1 col col-10"}).findAll("div",{"class":"story-content"})
    if links:
        for i in links:
            link = i.find("a").get('href')
            link = "https://www.reuters.com" + link
            #print(link)
            link = urlopen(link)
            bsObj =BeautifulSoup(link, "html.parser")
            title = bsObj.find("h1",{"class":"ArticleHeader_headline"}).get_text()
            if title in checktitle:
                continue
            else:
                checktitle.append(title)
                date = bsObj.find("div",{"class":"ArticleHeader_date"}).get_text().split("/")[0].strip()
                date = datetime.datetime.strptime(date,"%B %d, %Y")
                date = datetime.datetime.strftime(date,"%Y-%m-%d")
                if date == CurrentDate:                    
                    author = bsObj.find("a",{"target":"_blank"}).get_text()
                    content = bsObj.findAll("p")
                    p = []
                    for i in content:
                        p.append(i.get_text())
                    index = [0,-3,-2,-1]
                    for i in index:
                        p.remove(p[i])
                    para = "".join(p)
                    _id = uuid.uuid3(uuid.NAMESPACE_DNS,title+" "+datetime.datetime.now().strftime('%Y-%m-%d'))
                    dic["_id"] = _id
                    dic["Date"] = date
                    dic["Title"] = title
                    dic["Author"] = author
                    dic["Content"] = para
                    dic["Category"] = "Finance"
                    print(title)
                    result = collection.insert(dic)
                else:
                    print("Reuters_Daily Compelted")
                    sys.exit("No More Articles")
    else:
        sys.exit("No More Articles")
    



 





