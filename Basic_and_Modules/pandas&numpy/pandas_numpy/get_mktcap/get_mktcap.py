# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:46:28 2020

@author: -
"""
import pandas as pd
import numpy as np
import h5py
import os
import re
import sys
sys.path.append(r'D:\LYS\python_learning\my_tools\python')
from rowSetdiff_df import rowSetdiff_df
# U3ID,Data_month,Mktcap,Data_date,fx_rate
# I only consider econ 1 and econ 10

## initialize
main_path = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\Recent\Daily\\'
mktcap_path = r'\IDMTData\Clean\EquityWithStalePrice\\'
fx_path = r'\IDMTData\Clean\GlobalInformation\\'
mkt_list = ['Marketcap_1.mat', 'Marketcap_10.mat']
    
#datelist = glob.glob(main_path)
datelist = [f for f in os.listdir(main_path) if re.match(r'202003.*',f)]
#mkt_list = ['Marketcap_1.mat', 'Marketcap_10.mat']

# for 202003
idate = datelist[5] ## the last day info is enough
mktpath = main_path+idate+mktcap_path
fxpath = main_path+idate+fx_path
#mkt_list = os.listdir(mktpath)
for iecon in mkt_list:
    locals()['Data_'+iecon[10:-4]] = np.empty([0,3])
    mktdata = h5py.File(mktpath+iecon,'r')
    mktcap = mktdata['marketcap'][:].transpose()
    for icomp in range(1,np.size(mktcap,1)):
        u3_id = mktcap[0,icomp]
        row = -1
        while np.isnan(mktcap[row,icomp]):
            row += -1
        Data_month = np.floor(mktcap[row,0]/100)
        Mktcap = mktcap[row,icomp]
        data = np.array([u3_id,Data_month,Mktcap])
        data = data.reshape(1,3)
        locals()['Data_'+iecon[10:-4]] = np.vstack((locals()['Data_'+iecon[10:-4]],data))

# until 202002
old_path = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\ModelCalibration\202002\IDMTData\CleanData\EquityWithStalePrice\\'
for iecon in mkt_list:
    locals()['OldData4_'+iecon[10:-4]] = pd.DataFrame()
    mktdata = h5py.File(old_path+iecon,'r')
#    print(list(mktdata.keys()))
    mktcap = mktdata['marketcap'][:].transpose()
    for icomp in range(1,np.size(mktcap,1)):
        print(icomp)
        row = 1
        rrow = -1
        if np.isnan(mktcap[1:,icomp]).all():
            continue
        while np.isnan(mktcap[row,icomp]):
            row += 1 # find the fisrt nan mktcap  
        temp = mktcap[row:rrow,[0,icomp]] # first: locals()['OldData4_'+iecon[10:-4]]find the nan mktcap
        date_range = np.unique(np.floor(temp[:,0]/100))
        vtdata = date_range[:,np.newaxis]
        
        idx = ~np.isnan(mktcap[1:,icomp])
        nan_mktcap = mktcap[1:,[0,icomp]][idx] # find the nan mktcap 
        nan_mktcap[:,0] = np.floor(nan_mktcap[:,0]/100)
        data,idx2 = np.unique(nan_mktcap[::-1][:,0],return_index=True) # reverse the data to find the last day data
        nan_mktcap = nan_mktcap[::-1][idx2]
        
        df1 = pd.DataFrame(vtdata,columns=['date'])
        df2 = pd.DataFrame(nan_mktcap,columns=['date','mkt'])        
        VTdata = pd.merge(df1,df2,on='date',how='outer',indicator=False)
        VTdata.insert(loc=0, column='u3_id', value=mktcap[0,icomp])        
        
        locals()['OldData4_'+iecon[10:-4]] = locals()['OldData4_'+iecon[10:-4]].append(VTdata)
        VTdata = []
        
## pmtdata
with open (r"\\unicorn6\TeamData\IDMT_VT\CriAt_monthly_mktcap\Mktcap_1.txt", "r") as myfile:
    pmtdata=myfile.readlines()
header=pmtdata[0]
del pmtdata[0]
pmtdata = [p.replace('\n','') for p in pmtdata]
pmtdata = [p.split(',') for p in pmtdata]
PMTdata = np.array(pmtdata,dtype=float)     
# PMTdata = np.delete(PMTdata,[3,4],1)

# combine econ data 
econ1 = np.vstack((OldData4_1,Data_1))
econ1 = pd.DataFrame(econ1,columns=['u3_id','date','mkt'])
econ1 = econ1.sort_values(['u3_id','date'])
print(econ1.shape)
pmtdata = pd.DataFrame(PMTdata,columns=['u3_id','date','mkt'])
print(pmtdata.shape)
dif, diffrownum = rowSetdiff_df(econ1.iloc[:,[0,1]],pmtdata.iloc[:,[0,1]])
dif2, diffrownum2 = rowSetdiff_df(pmtdata.iloc[:,[0,1]],econ1.iloc[:,[0,1]])

data,idx3 = np.unique(test.iloc[:,0],return_index=True) 
sd = test.iloc[idx3,:]



