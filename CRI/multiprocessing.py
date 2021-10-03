# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:43:27 2020

@author: rmileng
"""    
import pandas as pd
import sqlite3
import numpy as np
from datetime import timedelta
import datetime as dt
import pyodbc
import multiprocessing as mp

#class get_data_from_AIG():
#    
#    def __init__(self): 
#        self.conn_live =  sqlite3.connect(r'\\unicorn7\TeamData\VT\Team_Working\CE_website_check\CE_succeed.db')
#        self._save_save_path = r'D:\LYS\temp files\\'
#    def read_data(self,i):
#        print('%d start' %i)
#        '''
#        date = '2020-07-01'
#        date = pd.to_datetime(date)
#        end_date='2020-12-11'
#        end_date = pd.to_datetime(end_date)
#
#
#        while date < end_date:
#            x = str(date).strip(' 00:00:00')
#            date = date + timedelta(days=10)
#            y = str(date).strip(' 00:00:00')
#            query = f"select * from RiskFactor where DataDate >= '{​​​​​​​x}​​​​​​​' and DataDate< '{​​​​​​​y}​​​​​​​';"
#            rf = pd.read_sql(query,self.conn_live)
#            rf = pd.DataFrame(rf)
#            rf['DataDate'] = rf['DataDate'].astype(str)
#            rf.to_csv(self._save_save_path+'rf_{​​​​​​​0}​​​​​​​_{​​​​​​​1}​​​​​​​.xlsx'.format(x,y),index=False)
#          '''
#        limit = 100
#        if i == 1:
#            offset = 0
#        offset = limit*i
#        query = "select * from Meta.LOG.revision_registry order by ID offset​​​​​​​ %d rows​​​​​​​;" % offset
#        rf = pd.read_sql(query,self.conn_live)
#        rf = pd.DataFrame(rf)
#        rf.to_csv(self._save_save_path+'rf_{​​​​​​​0}​​​​​​​.csv'.format(offset),index=False)
#        print('%d finish' %i)
        
#    def multicore(self):
#        workers = 5
#        processes = []
#        for p_number in range(workers):
#	        p = mp.Process(target=self.read_data, args=(np.arange(1,1001),))
#	        p.start()
#	        processes.append(p)
#	
#        for p in processes:
#	        p.join()
class nn():
    def read_data(self,i):
        save_save_path = r'D:\LYS\temp files'
    #    conn_live =  sqlite3.connect(r'\\unicorn7\TeamData\VT\Team_Working\CE_website_check\CE_succeed.db')
        limit = 100
        offset = limit*i
        rf = np.random.randn(offset,2)
        rf = pd.DataFrame(rf)
        rf.to_csv(save_save_path+r'\rf_{0}.csv'.format(offset),index=False)
            
                
    def multicore(self):
        t1 = dt.datetime.today()
        with mp.Pool(processes=6) as p:
            p.map(self.read_data, np.arange(1,4))
        t2 = dt.datetime.today()
        print(t2-t1)

if __name__ == '__main__': 
 #   res = get_data_from_AIG()   
 #   res.multicore()
     res = nn()
     res.multicore()


