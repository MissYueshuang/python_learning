# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:56:57 2021

@author: ys.leng
"""
import os
from pymongo import MongoClient

parent_dir = r"\\Unicorn7\TeamData\RT1\ToMeng-jou\ToShenbiao\NLP_seminar\0301"
os.chdir(parent_dir)

client = MongoClient('gpu8',27017)
db = client.admin
db.authenticate("crinlp","123")
db = client.crinlp
# col_names = db.list_collection_names(session=None)
col_names = ["reuters_market"]

def get_text(collection, key_word, check_set):
    # title_filter={'Title':{'$regex':title_kw,'$options':'i'}}
    c = collection.find()
    original_text=[]
    for i in c:
        try:
            curr_content = i["Content"].replace("\n","").replace("\t","").replace("--//--","")
            if i['Title'] in check_set:
                print("REPEAT")
            else:
                original_text.append(i['Title']+'\n'+i['Date']+'\n'+ curr_content)
                check_set.add(i["Title"])
        except:
            continue
    return original_text


# for target_company in companies_ini:
article_dir = os.path.join(parent_dir, "all")
if not os.path.exists(article_dir):
    os.makedirs(article_dir)

os.chdir(article_dir)
idx = 1
check_set = set()
for curr_col_name in col_names:
    if 'sina' not in curr_col_name and 'Sina' not in curr_col_name:
        curr_col = db[curr_col_name]
        curr_ori_test = get_text(curr_col, '', check_set)
        if curr_ori_test:
            for article in curr_ori_test:
                with open("{}.txt".format(idx), "w", encoding="utf-8") as f:
                    f.write(article)
                idx += 1
                if idx == 20001:
                    break
                print("Article Found: {}. {}".format(idx, article[:50]))
                print('-' * 20)


