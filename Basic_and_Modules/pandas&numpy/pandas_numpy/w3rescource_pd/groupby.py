# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 16:22:34 2020

@author: rmileng
"""
import numpy as np
import pandas as pd

student_data = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s004'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'height': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

grouped = student_data.groupby('school_code')

# data to list
list(grouped)

# call a specific group with the name of the group.
grouped.get_group('s001')

df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['2012-10-05','2012-09-10','2012-10-05','2012-08-17','2012-09-10','2012-07-27','2012-09-10','2012-10-10','2012-10-10','2012-06-27','2012-08-17','2012-04-25'],
'customer_id':[3001,3001,3005,3001,3005,3001,3005,3001,3005,3001,3005,3005],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001]})

# sort value in each group
df_agg = df.groupby(['customer_id','salesman_id']).purch_amt.sum()
result = df_agg.groupby(level=0,group_keys=False)
result.nlargest()

# create a list of order date for each group
df.groupby('customer_id').ord_date.apply(list)

## group by one column based on month of the order date and find the total purchase amount of that month.
df['date'] = pd.to_datetime(df['ord_date'])
df.set_index('date').groupby(pd.Grouper(freq='M')).agg({'purch_amt':'sum'}) 

## group by month and year based on order date and find the total purchase amount year wise, month wise.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['05-10-2012','09-10-2012','05-10-2013','08-17-2013','10-09-2013','07-27-2014','10-09-2012','10-10-2012','10-10-2012','06-17-2014','07-08-2012','04-25-2012'],
'customer_id':[3001,3001,3005,3001,3005,3001,3005,3001,3005,3001,3005,3005],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001]})
df['date'] = pd.to_datetime(df['ord_date'])
df['month'] = df.date.apply(lambda x: x.month)
df['year'] = df.date.apply(lambda x: x.year)
df.groupby(['year','month']).purch_amt.sum()


df = pd.DataFrame( {'X' : [10, 10, 10, 20, 30, 30, 10], 
                    'Y' : [10, 15, 11, 20, 21, 12, 14], 
                    'Z' : [22, 20, 18, 20, 13, 10, 0]})

df.groupby('X').agg({'Y': lambda x: list(x),'Z': lambda x: list(x)})
df.groupby('X').agg(lambda x: x.unique().tolist()) # answer

# based on all columns and calculate Groupby value counts on the dataframe.
df = pd.DataFrame( {'id' : [1, 2, 1, 1, 2, 1, 2], 
                    'type' : [10, 15, 11, 20, 21, 12, 14], 
                    'book' : ['Math','English','Physics','Math','English','Physics','English']})

df.groupby(['id','type','book']).size().unstack(fill_value=0)
# or
pd.pivot_table(data=df,index=['id','type'],columns='book',aggfunc='size',fill_value=0)

## count unique values of 'value' column.
df = pd.DataFrame({
    'id': [1, 1, 2, 3, 3, 4, 4, 4],
    'value': ['a', 'a', 'b', None, 'a', 'a', None, 'b']
})
df.groupby('value').id.nunique()

## list all the keys from the GroupBy object.
df = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s004'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'height': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

df.groupby('school_code').groups.keys()


## create a new column with count from GroupBy.
df = pd.DataFrame({
'book_name':['Book1','Book2','Book3','Book4','Book1','Book2','Book3','Book5'],
'book_type':['Math','Physics','Computer','Science','Math','Physics','Computer','English'],
'book_id':[1,2,3,4,1,2,3,5]})

df.groupby(['book_name','book_type'])['book_type'].count().reset_index(name='count')

# split a given dataframe into groups with bin counts.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'customer_id':[3005,3001,3002,3009,3005,3007,3002,3004,3009,3008,3003,3002],
'sales_id':[5002,5003,5004,5003,5002,5001,5005,5007,5008,5004,5005,5001]})

df.groupby(['customer_id',pd.cut(df['sales_id'],3)]).ord_no.count().unstack()

# by school code, class and get mean, min, and max value of height and age for each value of the school.
df = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s001'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'height': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

df.groupby(['school_code','class'])['height','weight'].agg(['mean','min','max'])

# display target column as a list of unique values.
df = pd.DataFrame( {'id' : ['A','A','A','A','A','A','B','B','B','B','B'], 
                    'type' : [1,1,1,1,2,2,1,1,1,2,2], 
                    'book' : ['Math','Math','English','Physics','Math','English','Physics','English','Physics','English','English']})

df.groupby(['id','type']).book.apply(list).reset_index(name='book')

## calculate quarterly purchase amount.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['05-10-2012','09-10-2012','05-10-2012','08-17-2012','10-09-2012','07-27-2012','10-09-2012','10-10-2012','10-10-2012','06-17-2012','07-08-2012','04-25-2012'],
'customer_id':[3001,3001,3005,3001,3005,3001,3005,3001,3005,3001,3005,3005],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001]})

df['ord_date']= pd.to_datetime(df['ord_date'])
result = df.set_index('ord_date').groupby(pd.Grouper(freq='Q')).agg({'purch_amt':sum})

## with customized column name
student_data = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s004'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    ' height ': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

student_data.groupby('school_code').age.agg([('Age_Mean','mean'),('Age_Maz','max'),('Age_Min','min')])

##  into groups on customer id and calculate the number of customers starting with 'C', the list of all products and the difference of maximum purchase amount and minimum purchase amount.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5, 270.65, 65.26, 110.5, 948.5, 2400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'ord_date': ['05-10-2012','09-10-2012','05-10-2012','08-17-2012','10-09-2012','07-27-2012','10-09-2012','10-10-2012','10-10-2012','06-17-2012','07-08-2012','04-25-2012'],
'customer_id':['C3001','C3001','D3005','D3001','C3005','D3001','C3005','D3001','D3005','C3001','D3005','D3005'],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001]})

df.groupby('salesman_id').agg({'customer_id':{'customer_id_start_C':lambda x: (x.str[0] == 'C').sum(),
                               'customer_id_list':lambda x: x.tolist()},
                              'purch_amt':{'purchase_amt_gap':lambda x: x.max()-x.min()}})


## groups on customer_id to summarize purch_amt and calculate percentage of purch_amt in each group.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['05-10-2012','09-10-2012','05-10-2012','08-17-2012','10-09-2012','07-27-2012','10-09-2012','10-10-2012','10-10-2012','06-17-2012','07-08-2012','04-25-2012'],
'customer_id':[3001,3001,3005,3001,3005,3001,3005,3001,3005,3001,3005,3005],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001]})


gr_data = df.groupby(['customer_id','salesman_id']).agg({'purch_amt':'sum'})
gr_data["% (Purch Amt.)"] = gr_data.apply(lambda x:  100*x / x.sum())

## group by two columns and convert other columns of the dataframe into a dictionary with column header as key.
df = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s004'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'height': [173, 192, 186, 167, 151, 159],
    'weight': [35, 32, 33, 30, 31, 32],
    'address': ['street1', 'street2', 'street3', 'street1', 'street2', 'street4']},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

dict_data_list = []
for gg, dd in df.groupby(['school_code','class']):
    group = dict(zip(['school_code','class'],gg))
    ocolumns_list = []
    for _, data in dd.iterrows():
        data = data.drop(columns=['school_code','class'])
        ocolumns_list.append(data.to_dict())
    group['other_column'] = ocolumns_list
    dict_data_list.append(group)

## apply an aggregate function to few columns and another aggregate function to the rest of the columns of the dataframe.
df = pd.DataFrame({
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5006,5003,5002,5007,5001],
'sale_jan':[150.5, 270.65, 65.26, 110.5, 948.5, 2400.6, 1760, 2983.43, 480.4,  1250.45, 75.29,1045.6],
'sale_feb':[250.5, 170.65, 15.26, 110.5, 598.5, 1400.6, 2760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_mar':[150.5, 270.65, 65.26, 110.5, 948.5, 2400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_apr':[150.5, 270.65, 95.26, 210.5, 948.5, 2400.6, 760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_may':[130.5, 270.65, 65.26, 310.5, 948.5, 2400.6, 760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_jun':[150.5, 270.65, 45.26, 110.5, 948.5, 3400.6, 5760, 983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_jul':[950.5, 270.65, 65.26, 210.5, 948.5, 2400.6, 5760, 983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_aug':[150.5, 70.65,  65.26, 110.5, 948.5, 400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_sep':[150.5, 270.65, 65.26, 110.5, 948.5, 200.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_oct':[150.5, 270.65, 65.26, 110.5, 948.5, 2400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6],
'sale_nov':[150.5, 270.65, 95.26, 110.5, 948.5, 2400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6], 
'sale_dec':[150.5, 70.65, 65.26, 110.5, 948.5, 2400.6, 5760, 1983.43, 2480.4, 250.45, 75.29, 3045.6]
})
df.groupby('salesman_id').agg(lambda x : x.sum() if x.name in ['sale_jan','sale_feb','sale_mar'] else x.mean())

## group by one column and remove those groups if all the values of a specific columns are not available.
df = pd.DataFrame({
    'school_code': ['s001','s002','s003','s001','s002','s004'],
    'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David Parkes'],
    'date_Of_Birth ': ['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'age': [12, 12, 13, 13, 14, 12],
    'weight': [173, 192, 186, 167, 151, 159],
    'height': [35, None, 33, 30, 32, None]},
    index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'])

df[(~df['height'].isna()).groupby(df['school_code']).transform('any')]

## split a given dataset using group by on specified column into two labels and ranges.
'''
Split the group on 'salesman_id',
Ranges:
1) (5001...5006)
2) (5007..5012)
'''
df = pd.DataFrame({
'salesman_id': [5001,5002,5003,5004,5005,5006,5007,5008,5009,5010,5011,5012],
'sale_jan':[150.5, 270.65, 65.26, 110.5, 948.5, 2400.6, 1760, 2983.43, 480.4,  1250.45, 75.29,1045.6]})

groups = pd.cut(df.salesman_id,[5000,5006,5012],labels = ['S1','S2'])
df.groupby(groups).sale_jan.agg('sum').reset_index(name='sale_jan')

## group by on first column and aggregate over multiple lists on second column.
df = pd.DataFrame({
    'student_id': ['S001','S001','S002','S002','S003','S003'],
    'marks': [[88,89,90],[78,81,60],[84,83,91],[84,88,91],[90,89,92],[88,59,90]]})

df.groupby('student_id')['marks'].apply(list).apply(lambda x: np.mean(x,axis=0))

## group by on 'salesman_id' and find the first order date for each group.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['2012-10-05','2012-09-10','2012-10-05','2012-08-17','2012-09-10','2012-07-27','2012-09-10','2012-10-10','2012-10-10','2012-06-27','2012-08-17','2012-04-25'],
'customer_id':[3005,3001,3002,3009,3005,3007,3002,3004,3009,3008,3003,3002],
'salesman_id': [5002,5005,5001,5003,5002,5001,5001,5004,5003,5002,5004,5001]})

df.ord_date = pd.to_datetime(df.ord_date)
df.groupby('salesman_id')['ord_date'].min()
    
## group by on multiple columns and drop last n rows of from each group.
df = pd.DataFrame({
'ord_no':[70001,70009,70002,70004,70007,70005,70008,70010,70003,70012,70011,70013],
'purch_amt':[150.5,270.65,65.26,110.5,948.5,2400.6,5760,1983.43,2480.4,250.45, 75.29,3045.6],
'ord_date': ['2012-10-05','2012-09-10','2012-10-05','2012-08-17','2012-09-10','2012-07-27','2012-09-10','2012-10-10','2012-10-10','2012-06-27','2012-08-17','2012-04-25'],
'customer_id':[3002,3001,3001,3003,3002,3002,3001,3004,3003,3002,3003,3001],
'salesman_id':[5002,5003,5001,5003,5002,5001,5001,5003,5003,5002,5003,5001]})

result = df.groupby(['salesman_id', 'customer_id'])
for name,group in result:
    print("\nGroup:")
    print(name)
    print(group)
    
n = 2
result1 = df.drop(df.groupby(['salesman_id', 'customer_id']).tail(n).index, axis=0)
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    





