# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:48:33 2020

a further explore about transform

@author: rmileng
"""

# method one: merging
import pandas as pd
df = pd.read_excel('D:/LYS/python learning/sales_transactions.xlsx')
df.groupby('order')["ext price"].sum()

order_total = df.groupby('order')["ext price"].sum().rename("Order_Total").reset_index() #
df_1 = df.merge(order_total)
df_1["Percent_of_Order"] = df_1["ext price"] / df_1["Order_Total"]

# method two: transform
df["Order_Total"] = df.groupby('order')["ext price"].transform('sum') # return the same length
df["Percent_of_Order"] = df["ext price"] / df["Order_Total"]
# or just in one row
df["Percent_of_Order"] = df["ext price"] / df.groupby('order')["ext price"].transform('sum')






