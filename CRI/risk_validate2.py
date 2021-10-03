# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:12:16 2020

@author: rmileng
"""
import pandas as pd
import numpy as np
import h5py
import re
import os
import sys
import scipy.io
import pyodbc
sys.path.append(r'\\unicorn6\TeamData\VT\Yueshuang\my_tools\python') 
from rowSetdiff import rowSetdiff
from ismember import ismember

def risk_validate2(histMonth,tillDate=0,caliDate=0,econList):
    dataEnv = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\\'
    for econ in econList:
        Offi_path = dataEnv+'ProductionData\Historical\%d\Daily\Processing\P2_Pd\FinalDataForPdCalculation\\' % (histMonth)
        Incre_path = dataEnv+'ProductionData\Recent\Daily\\'
        PMT_path = r'\\unicorn6\teamdata\VT_PMT\Risk_Factors_for_criat\\'
        stock_histPath = dataEnv+'ProductionData\ModelCalibration\%d\IDMTData\CleanData\EconomicInformation\StockIndex\StockIndex_%d.mat'% (histMonth,econ)
        # load all data first
        stock_data = scipy.io.loadmat(stock_histPath)  
        stock_data = stock_data['stockIndex']
        stock_date = stock_data[:,0]
        # incre data
        incre_Data = np.empty((0,19))
        if tillDate != 0:
            dateMonth = np.floor(tillDate/100)
            # stock
            till_stock = [f for f in os.listdir(Incre_path) if re.match(str(tillDate),f)][0]
            stock_incre = scipy.io.loadmat(Incre_path+till_stock+r'\IDMTData\Clean\EconomicInformation\StockIndex\StockIndex_%d.mat' % econ)
            stock_incre = stock_incre['stockIndex']
            idx = stock_incre[:,0]>=dateMonth*100+1
            stock_date = np.concatenate((stock_date,stock_incre[idx,0]),axis=0)
            # incre data
            incre_files = [f for f in os.listdir(Incre_path) if re.match(str(int(dateMonth))+'.*', f)]
            for iFile in range(len(incre_files)):
                increFilename = incre_files[iFile]
                date = int(increFilename[:8])
                if date <= tillDate:
                    idata = scipy.io.loadmat(Incre_path+increFilename+r'\Processing\P2_Pd\covariates\final\Data_%d.mat' % econ)
                    idata = idata['firmspecific']
#                    idata = idata.transpose((2,0,1))[:,-1,:]
                    idata = idata.transpose(2,0,1).reshape((-1,20)) ##如果某一个维度长度不确定，也可以用-1代替。
                    idata[:,1] = idata[:,1]*100 + idata[:,2]
                    idata = idata[idata[:,1]==202003,:]
                    idata[:,1] = date
                    idata = np.delete(idata,2,axis=1)
                    incre_Data = np.concatenate((incre_Data,idata),axis=0)
        incre_Data[:,0] = incre_Data[:,0]*1000
        # hist data
        EconData = np.empty((0,19))
        files = [f for f in os.listdir(Offi_path+str(econ)) if re.match('fsFinal_.*',f)]        
        for iFile in range(len(files)):
            filename = files[iFile]
       #     u3_id = np.floor(int(filename[8:-4])/1000)
            iData = h5py.File(Offi_path+r'%d\%s'%(econ, filename),'r')
            iData = iData['thisFirmFsFinal'][:].transpose()
            iData = iData[iData[:,1].argsort()]
            EconData = np.concatenate((EconData,iData),axis=0)
        # revision data
        rev_comps = []
        if caliDate != 0:
            revi_path = dataEnv+'ProductionData\Historical\%d\Daily\Processing\P2_Pd\FinalDataForPdCalculation\%d\\'%(caliDate, econ)
            rev_files = [f for f in os.listdir(revi_path) if re.match(r'fsFinal_.*',f)]
            if len(rev_files) != 0:
                rev_data = np.empty((0,19))
                for iRev in range(len(rev_files)):
                    filename = rev_files[iRev]
                    revData = scipy.io.loadmat(revi_path+filename)
                    revData = revData['thisFirmFsFinal']
                    rev_data = np.concatenate((rev_data,revData),axis=0)
                    rev_comps.append(revData[0,0]) 
        # concat
        VTdata = np.concatenate((EconData,incre_Data),axis=0)
        if len(rev_comps) != 0:
            for icomp in rev_comps:
                idx = np.where((VTdata[:,0]==icomp) & (VTdata[:,1]<=caliDate))[0]
                VTdata = np.delete(VTdata, idx, axis=0)
            VTdata = np.concatenate((VTdata,rev_data),axis=0)
        
        ## data treatment
        VTdata = VTdata[VTdata[:,1].argsort()]    
        VTdata = pd.DataFrame(VTdata)                
        t1 = pd.to_datetime(str(int(VTdata.iloc[0,1])),format='%Y%m%d')
        t2 = pd.to_datetime(str(int(VTdata.iloc[-1,1])),format='%Y%m%d')
        DataDate = pd.date_range(start=t1, end=t2)    
        DataDate = pd.Series(DataDate.strftime('%Y%m%d').astype(int))   
        comps = pd.unique(VTdata.iloc[:,0])       
        rawComps = len(comps)
        # create new mat here
        vtmat = np.ones((rawComps*len(DataDate),2))
        vtmat[:] = np.nan
        vtmat[:,0] = comps.repeat(len(DataDate))
        vtmat[:,1] = np.tile(DataDate,rawComps)
        colname = [1,'datadate']
        vtmat = pd.DataFrame(vtmat)
        vtmat.columns = colname
        VTdata.columns = np.arange(1,20)
        vtmat = vtmat.sort_values(by=[1,'datadate'])    
        VTdata = VTdata.sort_values(by=[1,2])    
        vtmat = pd.merge(vtmat,VTdata,how='outer',left_on=[1,'datadate'],right_on=[1,2])
        ## fill data
        vtmat['idx'] = np.sum(np.isnan(vtmat.iloc[:,3:]),axis=1)
        vtmat['idx'][vtmat['idx']==17] = np.nan
        # id_bb
        conn = pyodbc.connect('Driver={SQL Server}; Server=dirac\dirac2012; Database=%s;'\
                          ' Trusted_Connection=yes;' %database)
        sql = 'select map.U3_COMPANY_NUMBER as u3_num, MAP.U4_COMPANY_ID as U4_ID,'\
            ' ci.ID_BB_COMPANY from tier3.ref.company_number_mapping_Temp map left join'\
            ' tier3.ref.company_information ci on map.u4_company_id = ci.company_id where U3_COMPANY_NUMBER = '
        ID_BB = []
        for icomp in pd.unique(vtmat.iloc[:,0]):
            u3_id = int(np.floor(icomp/1000))
            query = sql+str(u3_id)
            out = pd.read_sql(query,conn)
            ID_BB_comp = str(out.iloc[0,2])
            ID_BB.append(ID_BB_comp)
        vtmat['id_bb'] = np.repeat(ID_BB,len(DataDate))

 #       data, idx1 = np.unique(vtmat.iloc[:,0],return_index=True)
        idx2 = vtmat.groupby(1).idx.apply(lambda x: x.first_valid_index())
        idx3 = vtmat.groupby(1).idx.apply(lambda x: x.last_valid_index())
        # if Friday or holiday
        for iInd in range(len(idx3)):
            date = vtmat.iloc[idx3.iloc[iInd],1]
            stock_idx = np.argmax(stock_date==date)
            if stock_idx < len(stock_date)-1:
                t1 = pd.to_datetime(stock_date[stock_idx+1],format='%Y%m%d', errors='ignore')
                t2 = pd.to_datetime(stock_date[stock_idx],format='%Y%m%d', errors='ignore')
                delta = t1-t2
                if delta.days > 1:
                    idx3.iloc[iInd] = idx3.iloc[iInd] + delta.days - 1
        idx= []
        [idx.extend(np.arange(idx2.iloc[i],idx3.iloc[i]+1)) for i in range(len(idx2))];
        vtmat = vtmat.iloc[idx,:]
#        idx4 = len(DataDate)*np.arange(1,len(comps)+1) - 1
#        for iDel in range(len(idx1)):
#            vtmat.iloc[idx1[iDel]:(idx2.iloc[iDel]-1),:] = np.nan
#            vtmat.iloc[(idx3.iloc[iDel]+1):idx4[iDel],:] = np.nan
#        vtmat = vtmat.dropna(axis=0,how='all')
        vtmat.iloc[:,0] = vtmat.iloc[:,-1]        
        vtmat = vtmat.drop(['idx','id_bb'],axis=1)        
        vtmat = vtmat.sort_values(by=[1,'datadate'])
        # fill data
        idx = np.where(np.isnan(vtmat.iloc[:,2]))[0]
        result,idxT,idxF = ismember(idx,stock_date)
        vtmat = vtmat2.fillna(method='ffill')               
        vtmat.iloc[idxT,2:] = np.nan # not overfill
#        vtmat2 = vtmat.copy()
        # revision for incre data
        vtmat = vtmat[~np.isnan(vtmat.iloc[:,2])]
        vtmat.iloc[:,4] = vtmat.iloc[:,4].apply(lambda x: x/100) 
        vtmat = vtmat.sort_values(by='datadate')
        vtmat2 = vtmat.to_numpy()
        vtmat2 = vtmat2[:]
        scipy.io.savemat(r'D:\LYS\temp files\pythondata3.mat',mdict={'pmtData':vtmat})
        
        real = scipy.io.loadmat(r'D:\LYS\temp files\vtmat.mat')
        real = real['vtmat']
