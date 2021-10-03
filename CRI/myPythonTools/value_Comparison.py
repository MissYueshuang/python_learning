# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 14:46:51 2020

@author: rmileng
"""
import pandas as pd
import numpy as np
# from myPythonTools.rowSetdiff import rowSetdiff
import sys
sys.path.append(r'\\unicorn7\TeamData\VT\Yueshuang\Python\myPythonTools\rowSetdiff.py')

# pmtmat and vtmat are dataframes
def value_Comparison(pmtmat,vtmat,keyCols=0,threshold=1e-8,option='absolute'):
    out = {};
    
    if keyCols == 0:
        keyCols = np.arange(np.size(vtmat,1))
        
    if vtmat.shape != pmtmat.shape:
        onlyinVT, pos_vt = rowSetdiff(vtmat.iloc[:,keyCols], pmtmat.iloc[:,keyCols]);
        onlyinPMT, pos_pmt = rowSetdiff(pmtmat.iloc[:,keyCols], vtmat.iloc[:,keyCols]);
        
        if onlyinVT.empty == False:
            out['onlyinVT'] = onlyinVT
            vtmat = vtmat.merge(onlyinVT,how='outer',indicator=True).loc[lambda x: x['_merge']=='left_only']
            vtmat = vtmat.drop(['_merge'],axis=1)
        if onlyinPMT.empty == False:
            out['onlyinPMT'] = onlyinPMT
            pmtmat = pmtmat.merge(onlyinPMT,how='outer',indicator=True).loc[lambda x: x['_merge']=='left_only']
            pmtmat = pmtmat.drop(['_merge'],axis=1)
    
    vtmat = vtmat.fillna(value=-9999)
    pmtmat = pmtmat.fillna(value=-9999)
    
    if option == "absolute":
        dif = vtmat - pmtmat 
        finaldiff = dif.abs()
    elif option == "relative":
        dif = vtmat - pmtmat 
        finaldiff = dif/vtmat.abs()
    else:
        errmsg = "Please give the correct option: absolute or relative ..."
        raise ValueError(errmsg)
     
    if finaldiff.values.max() > threshold:
        rows = []
        cols = []
        idx = finaldiff.apply(lambda x: x >= threshold).reset_index(drop=True)
        for iRow in range(len(idx.iloc[:,0])):
            for jCol in range(len(idx.iloc[0,:])):
                if idx.iloc[iRow,jCol] == True:
                    rows.append(iRow)
                    cols.append(jCol)
        cols = pd.DataFrame(cols)
        out["pmtdata"] = pd.concat([pmtmat.iloc[rows,:],cols],axis=1)
        out["vtdata"] = pd.concat([vtmat.iloc[rows,:],cols],axis=1)
        out["Cols"] = {}
        out["Cols"]["raw_data"] = 1
        out["Cols"]["error_col"] = 2
        
    return out    
        
        
        