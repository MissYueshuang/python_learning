# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:27:51 2020

@author: rmileng
"""

def rowSetdiff(vtmat,pmtmat):
    vtmat = vtmat.reset_index(drop=True)
    pmtmat = pmtmat.reset_index(drop=True)
    diffrownum = vtmat.merge(pmtmat,how='outer',indicator=True).loc[lambda x: x['_merge']=='left_only'].index.values # int64 array. Index num = row num
    dif = vtmat.iloc[diffrownum,:] # dataframe of the vtmat
    return dif, diffrownum

# When we reset the index, the old index is added as a column, and a new sequential index is used

