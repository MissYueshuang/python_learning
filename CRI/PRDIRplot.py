# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:16:38 2020

@author: rmileng
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def makeplot(stats_Rating,stats_Change,path):
        df=pd.DataFrame(stats_Rating)
        df2=pd.DataFrame(stats_Change)
        titles = ["Asia","Namr","Euro","Lamr","Global","PDiR Change"]
        labels = ["AAA","AA","A","BBB","BB","B","CCC"]
        labels6 = ["Only In Pre","Only In Cur","No Change","Upgrade","Downgrade"]
        colors = ['xkcd:periwinkle blue','xkcd:powder blue','xkcd:light cyan','xkcd:light seafoam','xkcd:pastel yellow','xkcd:goldenrod','xkcd:bright red']
        colors6 = ['xkcd:periwinkle blue','xkcd:powder blue','xkcd:light seafoam','xkcd:goldenrod','xkcd:bright red']
        fig2, axes = plt.subplots(nrows=2,ncols=3,figsize=(30,15))
        for i, ax in enumerate(axes.flatten()):
            ax.set_facecolor('xkcd:salmon')
            if(i<=4):
                ax.pie(np.array(df.loc[i]),colors=colors,startangle=90, wedgeprops ={'linewidth': 1,'edgecolor':'black'},
                autopct='%1.0f%%', textprops={'fontsize': 14}, pctdistance=1.2, )
                ax.legend(labels,#loc = 'lower right',
                  bbox_to_anchor=(0.3, 0.5, 1, 0.1),prop={'size':18},frameon=False)

            else:
                  ax.pie(np.array(df2),colors=colors6,startangle=90, wedgeprops ={'linewidth': 1,'edgecolor':'black'},
                    autopct='%1.0f%%', textprops={'fontsize': 14}, pctdistance=1.2, )
                  ax.legend(labels6,#loc = 'lower right',
                    bbox_to_anchor=(0.4, 0.4, 1, 0.1),prop={'size':18},frameon=False)
            ax.set_title(titles[i],fontsize=20)
        fig2.set_facecolor('xkcd:white')
        plt.savefig(path,format='png')
        
stats_Rating = pd.read_csv(r'D:\LYS\temp files\stats_Rating.csv')
stats_Change = pd.read_csv(r'D:\LYS\temp files\stats_Change.csv')
path = r'D:\LYS\temp files\plot.png'
makeplot(stats_Rating,stats_Change,path)
