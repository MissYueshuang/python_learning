# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:49:38 2020

@author: rmileng
"""

'''
link reference: https://blog.csdn.net/su377486/article/details/51175568
'''
## you can add chart into excel 
import pandas as pd
import numpy as np

df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=["a", "b", "c"])

report_name = r'D:\LYS\temp files\example_report2.xlsx'
sheet_name = 'Sheet1'

## you can add chart into excel 
with pd.ExcelWriter(report_name, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Add a new worksheet.
    ## newworksheet = workbook.add_worksheet('Graphs')
    chart = workbook.add_chart({'type':'line'})
    
    '''
    chart = workbook.add_chart({type,'column'})    #创建一个column图表
    更多图表类型说明:
    area:创建一个面积样式的图表;
    bar:创建一个条形样式的图表;
    column:创建一个柱形样式的图表;
    line:创建一个线条样式的图表
    pie:创建一个饼图样式的图表
    scatter:创建一个散点样式的图表
    stock:创建一个股票样式的图表;
    radar:创建一个雷达央视的图表
    '''
    for i in range(1,4):
        chart.add_series({
                'categories':[sheet_name,1,0,3,0], # categories作用是设置图表类别标签范围
                'values':[sheet_name,1,i,3,i], # values是设置图表数据范围
                # 'line':'red'
                })
    chart.set_x_axis({'name':'Index','position_axis':'on_tick'})
    chart.set_y_axis({'name':'Value','marjor_gridlines':{'visible':False}})
    chart.set_legend({'position':'best'})
    chart.set_title({'name':'example','font_size':12})
    chart.set_size({'width':520,'height':400})
    worksheet.insert_chart('E2', chart) # position
    # newworksheet.insert_chart('E2', chart) ## add to the new work sheet
    writer.save()
    
# compress (to save memory)
df.to_csv(r'D:\LYS\temp files\example_report.gz', compression='gzip', index=False)
df2 = pd.read_csv(r'D:\LYS\temp files\example_report.gz')