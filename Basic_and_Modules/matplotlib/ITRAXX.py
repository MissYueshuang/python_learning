# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:09:47 2020

@author: rmileng
"""
import pandas as pd
import matplotlib.pyplot as plt
import sys
import h5py
import os
import glob
import re
import fnmatch
sys.path.append(r'\\unicorn6\TeamData\VT\Yueshuang\Python\myPythonTools')
from ismember import ismember 
from findMonthendTradingDay import findMonthendTradingDay
from plotSingleTS import plotSingleTS
import numpy as np
import datetime

dailypath = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\Recent\Daily\\'
# method 1 (best)
file2020 = [f for f in os.listdir(dailypath) if re.match(r'2020*',f)]
# method 2
file2 = fnmatch.filter(os.listdir(dailypath), r'2020*')
# method 3
os.chdir(dailypath)
file3 = glob.glob(r'2020*')

# 2020 data
VTdata = pd.DataFrame()
for ifile in file2[:-1]:
    foldername = ifile[:8]+'_Europe_caliDate'+ifile[14:]
    path1 = r'\Products\P101_WebDisplay\\'    
    path2 = r'\pd\pd_%s.csv' % ifile[:8]
    filepath = dailypath+ifile+path1+foldername+path2
    data = pd.read_csv(filepath)
    VTdata = VTdata.append(data)
complist = VTdata['CompanyID'].unique()
VTdata['date'] = VTdata[' year']*10000+VTdata[' month']*100+VTdata[' day'] # exist space
vtdata = VTdata[['CompanyID',' 60M','date']]

report_path = r'\\unicorn6\TeamData\VT\Yueshuang\Matlab\ITRAXX'

## hist data
histpath = r'\\dirac\CRI3\OfficialTest_AggDTD_SBChinaNA\ProductionData\Historical\201912\Monthly\Products\P101_WebDisplay\Pd'
filename = r'\outputFinal_20110101To20191231.mat'
histdata = h5py.File(histpath+filename,'r')
histdata = histdata['outputFinal'][:].transpose()
histdata = pd.DataFrame(histdata)
histdata['date'] = histdata.iloc[:,2]*10000+histdata.iloc[:,3]*100+histdata.iloc[:,4]
histdata = histdata[histdata.date>=20151231]

result,idxT,idxF = ismember(histdata.iloc[:,1],complist)
eurodata = histdata.iloc[idxT,:]
# find bad comps
badcomp = eurodata[eurodata.iloc[:,14]>10].iloc[:,1].unique()
result,idxT,idxF = ismember(eurodata.iloc[:,1],badcomp)
baddata = eurodata.iloc[idxT,:]
baddata = baddata.iloc[:,[1,12,15]]

result,idxT,idxF = ismember(vtdata.iloc[:,0],badcomp)
vtdata2 = vtdata[result]
colnames = ['id','pd','date']
vtdata2.columns = baddata.columns = colnames
data = baddata.append(vtdata2)
data = data.sort_values(['id','date'])

# get median
outputArray = data.groupby(data.date,as_index=False)[['pd']].median()
idx = [findMonthendTradingDay(x) for x in outputArray.date]
idx = list(set(idx))
idx.sort()
result,idxT,idxF = ismember(outputArray.iloc[:,0],idx)
outputArray2 = outputArray[result]
outputArray2 = outputArray2.append(outputArray.iloc[-1,:])

############### plot 
plt.figure(figsize=(12,8))

date = [datetime.datetime.strptime(str(int(d)),'%Y%m%d').date().strftime('%Y%m%d') for d in outputArray2.date]
plt.plot(date,outputArray2.pd)

#ax.xticks(np.linspace)
tick_idx = np.round(np.linspace(0,51,6)).astype(int)
new_label = [date[i] for i in tick_idx]

plt.xticks(new_label)
# x_label
# ax = plt.gca()
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
#ax.xaxis.set_major_locator(mdates.DayLocator())
#plt.gcf().autofmt_xdate()
plt.title('median pd for BBB Euro Comp',fontsize=20)
plt.xlabel('Date',fontsize=15)
plt.ylabel('5 year pd',fontsize=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig(r'\\unicorn6\TeamData\VT\Yueshuang\Matlab\ITRAXX\pyplot1.png')
plt.show()
plt.close()

## combine with itraxx
itraxx = pd.read_csv(r'\\unicorn6\TeamData\VT\Yueshuang\Matlab\ITRAXX\ITRAXX_5y.csv',header=None)
result,idxT,idxF = ismember(itraxx.iloc[:,0],outputArray2.date.astype(int))
itraxx_temp = itraxx[result]
itraxx_temp = itraxx_temp[::-1]
itraxx_temp.columns = outputArray2.columns
itraxx_temp = itraxx_temp.append(itraxx.iloc[0,:])
itraxx_temp = itraxx_temp.append(itraxx[itraxx.iloc[:,0]==20180329])
itraxx_temp = itraxx_temp.sort_values(['date'])

# plot single itraxx
report_path = r'\\unicorn6\TeamData\VT\Yueshuang\Matlab\ITRAXX\\'
graph_name = 'ITRAXX'
xlabel = 'Date'
ylabel = 'ITRAXX index'
Array_date = itraxx_temp.date
Array_data = itraxx_temp.pd
c = 'red'
plotSingleTS(report_path,graph_name,xlabel,ylabel,Array_date,Array_data,c)

## plot together
# method : subplots
f, ((ax11, ax12)) = plt.subplots(1, 2, sharex=False, sharey=False) #共享x轴或y轴
f.set_size_inches(20,8)
f.subplots_adjust(top=0.85) # change the distance between subplots to top of the fig

# subplot 1
ax11.plot(date,outputArray2.pd,color='lightsalmon')
tick_idx = np.round(np.linspace(0,len(date)-1,6)).astype(int)
new_label = [date[i] for i in tick_idx]
ax11.set_xticks(new_label)
ax11.tick_params(axis="both", labelsize=12)
ax11.tick_params(axis="y", labelsize=12)
ax11.set_title('median pd for BBB Euro Comp',fontsize=20,pad=15)
ax11.set_xlabel('Date',fontsize=15,labelpad=10) # labelpad change the distance between ticks and label
ax11.set_ylabel('5 year pd',fontsize=15,labelpad=10)

# subplot 2
ax12.plot(date,itraxx_temp.pd,color='pink')
tick_idx = np.round(np.linspace(0,len(date)-1,6)).astype(int)
new_label = [date[i] for i in tick_idx]
ax12.set_xticks(new_label)
ax12.tick_params(axis="x", labelsize=12)
ax12.tick_params(axis="y", labelsize=12)
ax12.set_title('ITRAXX index',fontsize=20,pad=15)
ax12.set_xlabel('Date',fontsize=15,labelpad=10)
ax12.set_ylabel('5 year pd',fontsize=15,labelpad=10)

f.suptitle('vs plot',fontsize=30, y=0.98) # y: change the distane between suptitle and top of the fig. In the end, you change the distance bewteen subplots and suptitle
plt.savefig(r'\\unicorn6\TeamData\VT\Yueshuang\Matlab\ITRAXX\vs_plot.png')
# plt.show()
plt.close()
















