# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:14:54 2020

@author: rmileng
O"""
econList = [6,7,8,9]
curMonth = 201910
import h5py
import pandas as pd
import numpy as np
import sys
sys.path.append(r'\\unicorn6\TeamData\VT\Yueshuang\Python\myPythonTools\value_Comparison.py')
# import loadmat because matlab version issue

def vali_withStaleMarketCap(curMonth, econList):
    Official_path = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\ModelCalibration\\'
    specified_path = r'\IDMTData\CleanData\EquityWithStalePrice\\'
    current_path = Official_path+str(curMonth)+specified_path
    last_path = Official_path+str(curMonth-1)+specified_path
    # Official_path = rf'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\ModelCalibration\{curMonth}\IDMTData\CleanData\EquityWithStalePrice\\'
    validation_result = {}
    
    for iEcon in econList:
        mat = h5py.File(current_path+f'Marketcap_{iEcon}.mat','r')
        current_marketCap = mat['marketcap'][:].transpose()
        current_marketCap = pd.DataFrame(current_marketCap)
        current_noc = len(current_marketCap.iloc[0,:])-1
        
        mat2 = h5py.File(last_path+f'Marketcap_{iEcon}.mat','r')
        last_marketCap = mat2['marketcap'][:].transpose()
        last_marketCap = pd.DataFrame(last_marketCap)
        last_noc = len(last_marketCap.iloc[0,:])-1
        
        validation_result[str(iEcon)] = {}
        flag = 1
        
        # logic: number of companies not decrease
        if last_noc > current_noc:
            print(f"Number of companies decreased from {last_noc} to {current_noc} for Econ {iEcon} !!")
            flag = 0
        # marketcap > 0
        temp = current_marketCap < 0
        Temp = temp.astype(int).sum().sum()
        if Temp != 0:
             print(f"Marketcap for Econ {iEcon} has negative value. Please check the validation_result!!")
             flag = 0
        # % of datapoints that is NaN this month but not NaN last month.
        if last_noc <= current_noc:
            current_NaN = np.isnan(current_marketCap.iloc[1:len(last_marketCap.iloc[:,0]),1:len(last_marketCap.iloc[0,:])]).astype(int)
            last_NaN = np.isnan(last_marketCap).astype(int)
        else:
            onlyinLast = np.setdiff1d(last_marketCap.iloc[0,1:],current_marketCap.iloc[0,1:])
            current_NaN = np.isnan(current_marketCap.iloc[:len(last_marketCap.iloc[:,0]),:]).astype(int)
            idx = np.in1d(last_marketCap.iloc[0,:],onlyinLast)
            last_NaN = np.isnan(last_marketCap.iloc[:,~idx]).astype(int)
            last_NaN.columns = current_NaN.columns
            
        out2 = current_NaN - last_NaN
        idx2 = out2.apply(lambda x: x==1)
        if any(idx2) == True:
            dataPercent = out2.sum().sum() / last_NaN.sum().sum()
            if dataPercent > 1e-8:
                print(f"% of datapoints of NaN for Econ $iEcon is {dataPercent}. Please check the validation_result!!")
                validation_result[str(iEcon)]['NaN_idx'] = idx2
                flag = 0 
        if flag == 1:
            print(f'validation passed for econ {iEcon}....')
        
        
        
        