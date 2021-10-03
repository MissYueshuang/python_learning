# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:46:04 2020

@author: rmileng
"""
import numpy as np
import pandas as pd

exam_data = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}

labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

df = pd.DataFrame(exam_data,index=labels)
df = df[['attempts','name','qualify','score']]
df.info()
df.dtypes
df[['name','score']].iloc[[1,3,5,6],:]

df[df.score.isnull()]
df.loc['k'] = [1,'Suresh','yes', 15.5]
df = df.drop('k')
df.sort_values(by=['name','score'],ascending=[True,False])

match = {'yes':True,'no':False}
df.qualify = df.qualify.apply(lambda x: match.get(x))
df['qualify'] = df['qualify'].map({'yes': True, 'no': False})

df['name'][df.name == 'James'] = 'Suresh'
df.name = df.name.replace('James','Suresh')

del df['attempts']

exam_data = [{'name':'Anastasia', 'score':12.5}, {'name':'Dima','score':9}, {'name':'Katherine','score':16.5}]
data2 = pd.DataFrame(exam_data)
for index,row in data2.iterrows():
    print(row['name'],row['score'])
df.columns.values
df.values
df = df.rename(columns={'score':'Score'})
df.rename(index={'a':'aa'})

df1 = pd.DataFrame({'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
'city': ['California', 'Los Angeles', 'California', 'California', 'California', 'Los Angeles', 'Los Angeles', 'Georgia', 'Georgia', 'Los Angeles']})
df1.groupby('city').name.size().reset_index(name='Number')

d = {'col1': [1, 4, 3, 4, 5], 'col2': [4, 5, 6, 7, 8], 'col3': [7, 8, 9, 0, 1]}
df = pd.DataFrame(data=d)
df = df[df.col2 != 5]

pd.options.display.max_columns = 10
pd.set_option('display.max_columns',10)
pd.reset_option("^display")
df.iloc[[2]]

df.score = df.score.fillna(0)
df = df.reset_index()
print(df.to_string(index=False))

df.isnull().values.sum()
df.reset_index()

df = pd.DataFrame(np.random.randn(10,2))
drop70 = df.sample(frac=0.7)
drop30 = df.drop(drop70.index)
df.sample(frac=1)

data = pd.DataFrame(np.random.randn(2,2),index=['index1','index2'],columns=['col1','col2'])
data.col2.argmax()
df = df.mask(df.isnull(),np.inf)
df = df.replace(np.inf,np.nan)
data.insert(1,value=np.random.randn(2),column='col1.5')

li = [[2, 4], [1, 3]]
data = pd.DataFrame(li,columns=['col1','col2'])

data = pd.DataFrame( {'col1':['C1','C1','C2','C2','C2','C3','C2'], 'col2':[1,2,3,3,4,6,5]})
data.groupby('col1')['col2'].apply(list)

[i for i in range(len(df.columns)) if df.columns[i] == 'name'][0]

df.loc[:,df.columns!='name']
temp = df[::-1].reset_index(drop=True) # reverse row order
temp = df.loc[:,::-1]
df.select_dtypes(include='object')


data = pd.DataFrame({
    'Name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Syed Wharton'],
    'Date_Of_Birth ': ['17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'Age': [18.5, 21.2, 22.5, 22, 23]
})
names = data.columns
names = names.str.lower()    
names = names.str.rstrip()
data.columns = names

df1 = data.copy()
df1 = df1.loc[[2,3,4],:]
df2 = data.copy().loc[[0,1,3,4],:]
df_121 = pd.merge(df1,df2,validate='one_to_one')

data = { 'Name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Syed Wharton', 'Kierra Gentry'], 'Age': [18, 22, 40, 50, 80, 5] }
data = pd.DataFrame(data)
data['age_groups'] = pd.cut(data.Age,[0,18,66,99],labels=['kids','adult','elderly'])
data.memory_usage(deep=True)

sr1 = pd.Series(['php', 'python', 'java', 'c#', 'c++'])
sr2 = pd.Series([1, 2, 3, 4, 5])
ser_df = pd.concat([sr1,sr2],axis=1)
ser_df = ser_df.rename(columns={0:'col1',1:'col2'})
df.loc['c','score'] = np.nan
temp = df.interpolate()

data = pd.DataFrame(np.random.randint(50,100,(5,4)),columns=['W','X','Y','Z'])
# method one
data.loc[data.W<data.W.max(),:]
# method 2
maxx = data.W.max()
data.query('W < @maxx')

d = {"agent": ["a001", "a002", "a003", "a003", "a004"], "purchase":[4500.00, 7500.00, "$3000.25", "$1250.35", "9000.00"]}
df = pd.DataFrame(d)
import re
regex = re.compile(r'^$.*')
df.purchase.apply()

df.purchase.apply(type)
df.purchase = df.purchase.replace('[$,]','',regex=True).astype('float')

df = pd.DataFrame({
    'Name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill'],
    'Date_Of_Birth ': ['17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'Age': [18.5, 21.2, 22.5, 22, 23]
})
label1,unique1 = pd.factorize(df.Name)     

data = {
"year": [2002, 2003, 2015, 2018],
"day_of_the_year": [250, 365, 1, 140]
}
df = pd.DataFrame(data)
df['combined'] = df.year*1000+df.day_of_the_year
df['date'] = pd.to_datetime(df.combined,format='%Y%j')

df = pd.read_clipboard()
df1 = pd.DataFrame(np.random.randint(50,100,(5,4)),columns=['W','X','Y','Z'])
df2 = pd.DataFrame(np.random.randint(50,100,(5,4)),columns=['W','X','Y','Z'])
df1.iloc[4,0] = df2.iloc[4,0] = np.nan
result = df1.values == df2.values
df1.ne(df2)

df = pd.DataFrame(np.random.randint(0,10,(6,3)),columns=['col1','col2','col3'])
df.nsmallest(3,'col1')

















































