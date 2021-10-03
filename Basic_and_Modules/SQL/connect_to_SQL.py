# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:02:43 2020

lesson 8: read from microsoft database

@author: rmileng
"""
import pandas as pd
import sys

# Parameters
# Create the connection

# version 2: pyodbc--Miscrosoft SQL
import pyodbc 
conn = pyodbc.connect('Driver={SQL Server}; Server=dirac\dirac2012; Database=Tier2; Trusted_Connection=yes;') # 若字符串内有空格一定要用{}
# MARS_Connection=Yes;' if Connection is busy with results for another hstmt

## method 1 
cursor = conn.cursor()
cursor.execute('SELECT TOP (3) [ID],[ISO_Code],[ISO_Name],[multiplier],[EUR_RATE] FROM [Tier2].[REF].[currency_information]')
for row in cursor:
    print(row)
## method 2 better
out = pd.read_sql('SELECT TOP (3) * FROM [Tier2].[REF].[currency_information]', conn) # Read SQL query or database table into a DataFrame.

## export to csv/excel/txt
df = out
df.to_csv('D:/LYS/python learning/sql.csv',index=False)


## pymysql--MySQL
import pymysql
conn = pymysql.connect(host='127.0.0.1',user='root',password='abc123',database='py101')
cursor = conn.cursor()
query = 'SELECT * from xueqiu limit 5;'
cursor.execute(query)
for row in cursor:
    print(row)
## conn.commit() # if input to a database



