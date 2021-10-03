# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 16:06:14 2020

@author: rmileng
"""

import pandas as pd
import numpy as np

s = pd.Series(['X', 'Y', 'Z', 'Aaba', 'Baca', np.nan, 'CABA', None, 'bird', 'horse', 'dog'])
s.str.len()

s = pd.Series([10, 250, 3000, 40000, 500000])
s.map(lambda x: str(0)*(8-len(str(x)))+str(x))
s.apply(lambda x:'{0:0>8}'.format(x))

df = pd.DataFrame({
    'name_code': ['c001','c002','c022', 'c2002', 'c2222'],
    'date_of_birth': ['12/05/2002','16/02/1999','25/09/1998','12/02/2022','15/09/1997'],
    'age': [18.5, 21.2, 22.5, 22, 23]
})
print("\nCount occurrence of 22 in date_of_birth column:")
np.argwhere(df.date_of_birth.str.find('22')>0)

df = pd.DataFrame({
    'name': ['Alberto  Franco','Gino Ann Mcneill','Ryan  Parkes', 'Eesha Artur Hinton', 'Syed  Wharton'],
    'date_of_birth ': ['17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [18.5, 21.2, 22.5, 22, 23]
})
print("Original DataFrame:")
print(df)
df[["first", "middle", "last"]] = df["name"].str.split(" ", expand = True)
print("\nNew DataFrame:")
print(df)

import re
df = pd.DataFrame({
    'name_email': ['Alberto Franco af@gmail.com','Gino Mcneill gm@yahoo.com','Ryan Parkes rp@abc.io', 'Eesha Hinton', 'Gino Mcneill gm@github.com']
    })
def find_email(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+',str(text))
    return ','.join(email)

df['email'] = df['name_email'].map(lambda x: find_email(x))

df = pd.DataFrame({
    'tweets': ['#Obama says goodbye','Retweets for #cash','A political endorsement in #Indonesia', '1 dog = many #retweets', 'Just a simple #egg']
    })
    
df['hash_word'] = df.tweets.apply(lambda x: ','.join(re.findall(r'#\w+',str(x))))
    
df = pd.DataFrame({
    'company_code': ['c0001','c0002','c0003', 'c0003', 'c0004'],
    'address': ['7277 Surrey Ave.','920 N. Bishop Ave.','9910 Golden Star St.', '25 Dunbar St.', '17 West Livingston Court']
    })
s = '7277 Surrey Ave.'
re.findall(r'\d+',s)

# extract year between 1800 to 2200 
df = pd.DataFrame({
    'company_code': ['c0001#','c00@0^2','$c0003', 'c0003', '&c0004'],
    'year': ['year 1800','year 1700','year 2300', 'year 1900', 'year 2200']
    })
def find_year(text):
    result = re.findall(r'\b1[89][0-9]{2}|2[01][0-9]{2}|2200\b',text)
    return result
def find_nonalpha(text):
    result = re.findall(r'[^A-Za-z0-9 ]',text)
    return result

df.company_code.map(lambda x: find_nonalpha(x))

df = pd.DataFrame({
    'text_code': ['t0001.','t0002','t0003', 't0004'],
    'text_lang': ['She livedd a long life.', 'How oold is your father?', 'What is tthe problem?','TThhis desk is used by Tom.']
    })
    
df['text_text'] = df['text_lang'].apply(lambda s: ''.join([s[i] for i in range(len(s)-1) if s[i] != s[i+1]]) ) 

# extract number greater than 940
df = pd.DataFrame({
    'company_code': ['c0001','c0002','c0003', 'c0003', 'c0004'],
    'address': ['7277 Surrey Ave.1111','920 N. Bishop Ave.','9910 Golden Star St.', '1025 Dunbar St.', '1700 West Livingston Court']
    })

df.address.apply(lambda s: ' '.join(re.findall(r'\b94[1-9]|9[5-9][0-9]|[1-9][0-9]{3}\b',s)))

# key words = Ave, 9910
df = pd.DataFrame({
    'company_code': ['c0001','c0002','c0003', 'c0003', 'c0004'],
    'address': ['9910 Surrey Ave.','92 N. Bishop Ave.','9910 Golden Star Ave.', '102 Dunbar St.', '17 West Livingston Court']
    })
df.address.apply(lambda s: re.findall(r'.*9910.*|.*Ave.*',s))

# mm-dd-yyyy
df = pd.DataFrame({
    'company_code': ['Abcd','EFGF', 'zefsalf', 'sdfslew', 'zekfsdf'],
    'date_of_sale': ['12/05/2002','16/02/1999','05/09/1998','12/02/2022','15/09/1997'],
    'sale_amount': [12348.5, 233331.2, 22.5, 2566552.0, 23.0]
})
df.date_of_sale.apply(lambda s: re.findall(r'\b(0[1-9]|1[0-2])/(0[1-9]|12][0-9]|3[01])/([0-9]{4})\b',s))

# only words
df = pd.DataFrame({
    'company_code': ['Abcd','EFGF', 'zefsalf', 'sdfslew', 'zekfsdf'],
    'date_of_sale': ['12/05/2002','16/02/1999','05/09/1998','12/02/2022','15/09/1997'],
    'address': ['9910 Surrey Ave.','92 N. Bishop Ave.','9910 Golden Star Ave.', '102 Dunbar St.', '17 West Livingston Court']
})
df['only_words']=df.address.apply(lambda s: ''.join(re.findall(r'[a-zA-Z ]+',s)))
# extract specific word: Avenue
df = pd.DataFrame({
    'company_code': ['Abcd','EFGF', 'zefsalf', 'sdfslew', 'zekfsdf'],
    'date_of_sale': ['12/05/2002','16/02/1999','05/09/1998','12/02/2022','15/09/1997'],
    'address': ['9910 Surrey Avenue','92 N. Bishop Avenue','9910 Golden Star Avenue', '102 Dunbar St.', '17 West Livingston Court']
})
df['sentence']=df.address.apply(lambda s: re.findall(r'.*Avenue',s))
# extract words starting with capital words
df['Cap'] = df.address.apply(lambda s: re.findall(r'\b[A-Z]\w+',s))


df = pd.DataFrame({
    'company_code': ['Abcd','EFGF', 'zefsalf', 'sdfslew', 'zekfsdf'],
    'date_of_sale': ['12/05/2002','16/02/1999','05/09/1998','12/02/2022','15/09/1997'],
    'address': ['9910 Surrey Avenue\n9910 Surrey Avenue','92 N. Bishop Avenue','9910 Golden Star Avenue', '102 Dunbar St.\n102 Dunbar St.', '17 West Livingston Court']
})
df['new']=df.address.apply(lambda x: str(x).split('\n')[0])

















    
    