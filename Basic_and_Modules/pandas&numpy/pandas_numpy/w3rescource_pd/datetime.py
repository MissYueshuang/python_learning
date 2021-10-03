# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 14:36:43 2020

@author: rmileng
"""
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import matplotlib.cm as cm

data = pd.read_csv(r'D:\LYS\python_learning\exercise\pandas_numpy\w3rescource\ufo_sighting_data.csv')
data['Date_time'] = pd.to_datetime(data.Date_time.str.replace('24:','00:'))
data['Date_time'] = data['Date_time'].astype('datetime64[ns]')

now = pd.to_datetime(dt.date.today(),format='%Y-%m-%d')

#data.Date_time.astype('datetime64[ns]')
#data["sincethen"] = pd.to_datetime(dt.date.today())-data.Date_time.astype('datetime64[ns]')

# Write a Pandas program to get the current date, oldest date and number of days between Current date and oldest date of Ufo dataset. 
current = pd.to_datetime(dt.date.today(),format='%Y-%m-%d')
temp = data.Date_time.str.split(' ')
data['Date'] = [i[0] for i in temp]
data.Date = pd.to_datetime(data.Date)
oldest = data.Date.min()
delta = (current - oldest).days

# Write a Pandas program to get all the sighting days of the unidentified flying object (ufo) which are less than or equal to 40 years (365*40 days).
idx = [i for i in data.Date if (current - i).days < 40*365]

answer = data[now-data.Date<=dt.timedelta(40*365)]

# between 1950-10-10 and 1960-10-10.
my = data[(data.Date>pd.to_datetime('1950-10-10')) & (data.Date<pd.to_datetime('1960-10-10'))]

# get all the sighting years
data['year'] = data.Date_time.dt.year

# 7. create a plot to present the number of unidentified flying object (UFO) reports per year. 
data.groupby('year').agg({'UFO_shape':'count'}).plot(kind='bar')
# answer
data.year.value_counts().sort_index().plot(x="year")

# 8  extract year, month, day, hour, minute, second and weekday 
data['Date_time'] = pd.to_datetime(data.Date_time.str.replace('24:','00:'))
data['Date_time'] = data['Date_time'].astype('datetime64[ns]')
data.Date_time.dt.weekday_name

# 9 convert given datetime to timestamp (answer)
df = pd.DataFrame(index=pd.DatetimeIndex(start=dt.datetime(2019,1,1,0,0,1),
   end=dt.datetime(2019,1,1,10,0,1), freq='H'))\
   .reset_index().rename(columns={'index':'datetime'})
df.datetime.values.astype(np.int64) // 10 ** 9

# 10 count year-country wise frequency of reporting dates
data.groupby(['year','country']).size()
## the result would be different if you use data.groupby(['year','country']).UFO_shape.count()

# 11 extract unique reporting dates of unidentified flying object (UFO)
data.Date_time.dt.date.unique()

# 12, get the difference (in days) between documented date and reporting date
data.date_documented = data.date_documented.astype('datetime64[ns]')
data['diff'] = data.Date_time.dt.date-data.date_documented
# answer
data['Difference'] = (data['date_documented'] - data['Date_time']).dt.days

# 13 add 100 days with reporting date
report_100 = data['date_documented'] + dt.timedelta(days=100)

# 14 generate sequences of fixed-frequency dates and time spans.
ser = pd.date_range('2020-01-01',freq='3D',periods=12)

# 15. create a conversion between strings and datetime. 
print('convert datetime to string')
stamp=dt.datetime(2019,7,1)
string = stamp.strftime('%Y%m%d')
from dateutil.parser import parse
parse(string) # method 1
parse('1/11/2019', dayfirst=False)
parse('Sept 17th 2019')
dt.datetime.strptime(string,'%Y%m%d') # method 2

# 16. convert date times with timezone information
dtt = pd.date_range('2018-01-01', periods=3, freq='H')
dtt = dtt.tz_localize('UTC')
dtt = dtt.tz_convert('America/Los_Angeles')

# 17. get the average mean of the UFO
data.Date_time.mean() # wrongly understood the question

## answer
# Add a new column instance, this adds a value to each instance of ufo sighting
data['instance'] = 1
# set index to time, this makes df a time series df and then you can apply pandas time series functions.
data.set_index(data['date_documented'], drop=True, inplace=True)
# create another df by resampling the original df and counting the instance column by Month ('M' is resample by month)
ufo2 = pd.DataFrame(data['instance'].resample('M').count())
ufo2['date_documented'] = pd.to_datetime(ufo2.index.values)
ufo2['month'] = ufo2['date_documented'].apply(lambda x: x.month)
df = ufo2.groupby(by='month').mean()

# 18 graphical analysis of UFO Sightings year.
years_data = data.year.value_counts()
years_index = years_data.index
years_values = years_data.values
plt.figure(figsize=(15,8))
plt.xticks(rotation = 60)
plt.title('UFO Sightings by Year')
plt.xlabel("Year")
plt.ylabel("Number of reports")
sns.barplot(x=years_index[10:],y=years_values[10:],palette = "Reds")

# 19 check the empty values of UFO
data.isnull().sum()

# 20 create a plot of distribution of UFO observation time.'length_of_encounter_seconds'
data['length_of_encounter_seconds'] = data['length_of_encounter_seconds'].str.replace('`','')
data['duration_sec'] = (data['length_of_encounter_seconds'].astype(float))/60
s = data["duration_sec"].quantile(0.95)
temp = data['duration_sec']
temp = temp.sort_values()
temp = temp[temp < s]

plt.figure(figsize=(10,8))
sns.distplot(temp)
plt.xlabel('Duration(min)',fontsize=20)
plt.ylabel('Frequency',fontsize=15)
plt.title('-Distribution of UFO obervation time-',fontsize=20)
plt.xticks(fontsize=12)
plt.show()

# create a graphical analysis of UFO (unidentified flying object) sighted by month. 
data['month'] = data.Date_time.dt.month
month_data = data.month.value_counts()
month_data.sort_index(inplace=True)
plt.figure(figsize=(15,8))
plt.xticks(rotation = 60)
plt.title('UFO Sightings by Month')
plt.xlabel("Month")
plt.ylabel("Number of reports")
sns.barplot(x=month_data.index,y=month_data.values,palette = "Blues")

# 22 create a comparison of the top 10 years in which the UFO was sighted vs the hours of the day.
most_sightings_years = data.year.value_counts().head(10)
data['hour'] = data.Date_time.dt.hour
data['instance'] = 1
df = data[data.year.isin(most_sightings_years.index)]
pd.pivot_table(data=df,index='year',columns='hour',values='instance',aggfunc='sum')
# answer
most_sightings_years = df['Date_time'].dt.year.value_counts().head(10)
def is_top_years(year):
   if year in most_sightings_years.index:
       return year
hour_v_year = df.pivot_table(columns=df['Date_time'].dt.hour,index=df['Date_time'].dt.year.apply(is_top_years),aggfunc='count',values='city')
hour_v_year.columns = hour_v_year.columns.astype(int)
hour_v_year.columns = hour_v_year.columns.astype(str) + ":00"
hour_v_year.index = hour_v_year.index.astype(int)

# 24  create a heatmap (rectangular data as a color-encoded matrix) for comparison of the top 10 years in which the UFO was sighted vs each Month.
hour_v_month = df.pivot_table(columns=df['Date_time'].dt.month,index=df['Date_time'].dt.year.apply(is_top_years),aggfunc='count',values='city')
plt.figure(figsize=(15,8))
sns.heatmap(hour_v_month,vmin=0, vmax=4)
plt.xlabel('month')
plt.ylabel('year')
plt.title('heatmap')
plt.show()

# 25 create a Timewheel of Month Vs Year comparison of the top 10 years in which the UFO was sighted.
## answer
month_vs_year = df.pivot_table(columns=df['Date_time'].dt.month,index=df['Date_time'].dt.year.apply(is_top_years),aggfunc='count',values='city')
month_vs_year.index = month_vs_year.index.astype(int)
month_vs_year.columns = month_vs_year.columns.astype(int)
def pie_heatmap(table, cmap='coolwarm_r', vmin=None, vmax=None,inner_r=0.25, pie_args={}):
   n, m = table.shape
   vmin= table.min().min() if vmin is None else vmin
   vmax= table.max().max() if vmax is None else vmax

   centre_circle = plt.Circle((0,0),inner_r,edgecolor='black',facecolor='white',fill=True,linewidth=0.25)
   plt.gcf().gca().add_artist(centre_circle)
   norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
   cmapper = cm.ScalarMappable(norm=norm, cmap=cmap)

   for i, (row_name, row) in enumerate(table.iterrows()):
       labels = None if i > 0 else table.columns
       wedges = plt.pie([1] * m,radius=inner_r+float(n-i)/n, colors=[cmapper.to_rgba(x) for x in row.values],
           labels=labels, startangle=90, counterclock=False, wedgeprops={'linewidth':-1}, **pie_args)
       plt.setp(wedges[0], edgecolor='grey',linewidth=1.5)
       wedges = plt.pie([1], radius=inner_r+float(n-i-1)/n, colors=['w'], labels=[row_name], startangle=-90, wedgeprops={'linewidth':0})
       plt.setp(wedges[0], edgecolor='grey',linewidth=1.5)










