import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import os
import time
import csv
import datetime

import matplotlib.pyplot as plt
#import seaborn as sns
#from plotly_calplot import calplot

'''
def heat_12m(df):
    temp = df.groupby('date').agg({'msPlayed':'sum'})
    heat_12m = temp.reset_index()
    heat_12m['date'] = pd.to_datetime(heat_12m['date'], format='%Y-%m-%d')
    
    fig = calplot(
         heat_12m,
         x="date",
         y="msPlayed"
    )
    fig.write_image("./graphs/12m_heatmap.jpeg")
    
def cluster_12m(df):
    temp = pd.DataFrame(df.groupby('date')['clusters'].value_counts())
    temp.rename(columns={"clusters": "counts"},inplace=True)
    temp.reset_index(inplace=True)
    cluster_12m = temp.groupby(['date'], as_index = False).agg({'counts':'max','clusters':'first'})
    
    cluster_12m.drop('counts',axis=1,inplace=True)
    cluster_12m['date'] = pd.to_datetime(cluster_12m['date'], format='%Y-%m-%d')
    
    fig = calplot(
         cluster_12m,
         x="date",
         y="clusters"
    )
    
    fig.write_image("./graphs/12m_cluster.jpeg")
'''
def hour_display(h):
    h = int(h)
    if h>12:
        temp = str(h-12)
        return temp + " PM"
    elif h==0:
        return "12 AM"
    else:
        return str(h) + " AM"
    
def date_display(date):
    months = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    mdy = "{} {}, {}".format(months[date.month-1],date.day,date.year)
    return mdy

def week_pattern(week,df):
    temp = df[df['week'] == week]
    temp['date'] = temp['date'].apply(lambda x: date_display(x))
    
    graph = temp.groupby(['date','new_gen']).agg({'msPlayed':'sum'})
    
    temp = graph.reset_index()
    c_num = len(pd.unique(temp['new_gen']))
    
    colors = ['#f2ac5b','#91a4bd','#ab5b34','#f0de58','#3373b4',
              '#383948','#949597','#ede1ce','#d9b58c','#988a55',
              '#abd9ab','#cb7f75','#419e71','#8f6ea6','#c4406c']
    c = colors[:c_num]
    
    graph['msPlayed'] = round(graph['msPlayed']/60000,2)
    
    months = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    DoW = pd.DatetimeIndex(df[df['week']==week]['EST_time']).isocalendar()['day'][0]
    date_DoW = pd.DatetimeIndex(df[df['week']==week]['EST_time']).isocalendar().index[0]
    first = date_DoW.date() - datetime.timedelta(days = int(DoW))

    week_name = "Week of {} {}, {}".format(months[first.month-1],first.day,first.year)
    
    fig = graph['msPlayed'].unstack().plot.bar(stacked=True,figsize=(10,8), color = c, rot = 30, 
                                           xlabel = "Day of Week", ylabel = "Minutes Listened", title = week_name).figure
    return fig
    
def day_pattern(date,df):
    y = date.day
    m = date.month
    d = date.day
    
    df['hour'] = pd.to_datetime(df['time'].astype(str)).dt.hour 
    
    temp = df[df['date'].isin([date,datetime.date(year=y,month=m,day=d+1)])]
    temp = temp[((temp['day'] == d) & (temp['hour']>=7))|((temp['day'] == d+1) & (temp['hour']<7))]
    temp['hour'] = temp['hour'].apply(lambda x: hour_display(x))
    
    graph = temp.groupby(['hour','new_gen']).agg({'msPlayed':'sum'})
    
    temp = graph.reset_index()
    c_num = len(pd.unique(temp['new_gen']))
    
    colors = ['#f2ac5b','#91a4bd','#ab5b34','#f0de58','#3373b4',
              '#383948','#949597','#ede1ce','#d9b58c','#988a55',
              '#abd9ab','#cb7f75','#419e71','#8f6ea6','#c4406c']
    c = colors[:c_num]
    
    graph['msPlayed'] = round(graph['msPlayed']/60000,2)
    
    day_name = date_display(date)
    
    fig = graph['msPlayed'].unstack().plot.bar(stacked=True,figsize=(10,8), color = c, rot = 30, 
                                           xlabel = "Time of Day", ylabel = "Minutes Listened", title=day_name).figure
    return fig