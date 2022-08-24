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

def week_pattern(week,df):
    temp = df[df['week'] == week]
    graph = temp.groupby(['date','new_gen']).agg({'msPlayed':'sum'})
    
    temp = graph.reset_index()
    c_num = len(pd.unique(temp['new_gen']))
    
    colors = ['#B05BDB','#16a4d8','#60dbe8','#71DB5B','#efdf48','#f9a52c','#F97171']
    c = colors[:c_num]
    
    return graph['msPlayed'].unstack().plot.bar(stacked=True,figsize=(10,8), color = c)
    
def day_pattern(date,df):
    y = date.day
    m = date.month
    d = date.day
    
    df['hour'] = pd.to_datetime(df['time'].astype(str)).dt.hour 
    
    temp = df[df['date'].isin([spec_date,datetime.date(year=y,month=m,day=d+1)])]
    temp = temp[((temp['day'] == d) & (temp['hour']>=7))|((temp['day'] == d+1) & (temp['hour']<7))]
    graph = temp.groupby(['hour','new_gen']).agg({'msPlayed':'sum'})
    
    temp = graph.reset_index()
    c_num = len(pd.unique(temp['new_gen']))
    
    colors = ['#B05BDB','#16a4d8','#60dbe8','#71DB5B','#efdf48','#f9a52c','#F97171']
    c = colors[:c_num]
    
    return graph['msPlayed'].unstack().plot.bar(stacked=True,figsize=(10,8), color = c)