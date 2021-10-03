# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:13:58 2020

lesson11: combine data from various sources

@author: rmileng
"""
import pandas as pd
import matplotlib
import os
import sys

# Create DataFrame
d = {'Channel':[1], 'Number':[255]}
df = pd.DataFrame(d)
df

# Export to Excel
df.to_excel('test1.xlsx', sheet_name = 'test1', index = False)
df.to_excel('test2.xlsx', sheet_name = 'test2', index = False)
df.to_excel('test3.xlsx', sheet_name = 'test3', index = False)
print('Done')

# List to hold file names
FileNames = []


# Find any file that ends with ".xlsx"
for files in os.listdir("."):
    if files.endswith(".xlsx"):
        FileNames.append(files)
        
FileNames

def GetFile(fnombre):

    # Path to excel file
    # Your path will be different, please modify the path below.
    location = r'D:\LYS\python learning' + '/'+ fnombre
    
    # Parse the excel file
    # 0 = first sheet
    df = pd.read_excel(location, 0)
    
    # Tag record to file name
    df['File'] = fnombre
    
    # Make the "File" column the index of the df
    return df.set_index(['File'])

# Create a list of dataframes
df_list = [GetFile(fname) for fname in FileNames]
df_list
# Combine all of the dataframes into one
big_df = pd.concat(df_list)
big_df

# Plot it!
big_df['Channel'].plot.bar();

# On the inside, the type of a column is pd.Series
pd.Series([1,2,3])
np.array([1,2,3])
pd.Series([1,2,3]).values #  If you add .values to the end of any Series, you'll get its internal numpy array


arr = np.array([1,2,3])
arr != 2
arr[arr != 2] # index
