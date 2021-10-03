# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:51:27 2020

@author: rmileng
"""
import numpy as np
import datetime
import matplotlib.pyplot as plt

def plotSingleTS(report_path,Array_date,Array_data,graph_name='plot',xlabel='Date',ylabel='data',color='pink',interval=6):
    plt.figure(figsize=(12,8))

    date = [datetime.datetime.strptime(str(int(d)),'%Y%m%d').date().strftime('%Y%m%d') for d in Array_date]
    plt.plot(date,Array_data,color=color)
    
    tick_idx = np.round(np.linspace(0,len(date)-1,interval)).astype(int)
    new_label = [date[i] for i in tick_idx]
    
    plt.xticks(new_label)

    plt.title(graph_name,fontsize=20)
    plt.xlabel(xlabel,fontsize=15)
    plt.ylabel(ylabel,fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    plt.savefig(report_path+graph_name)
    plt.show()
    plt.close()