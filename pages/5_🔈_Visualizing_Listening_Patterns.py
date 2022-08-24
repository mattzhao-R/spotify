import streamlit as st
import pandas as pd
import numpy as np
import os

from viz_methods import *


st.set_page_config(
    page_title="Visualizing Listening Patterns",
    page_icon="🔈"
)

st.markdown("# Visualizing Listening Patterns")
st.sidebar.header("Visualizing Listening Patterns")

st.markdown("""

In this section, we get to see what our listening habits look like across time using the newly generated clusters. 

""")

# prep dataframe for calendar viz
df = pd.read_csv('./final/final_newGen.csv')
df['endTime'] = pd.to_datetime(df['endTime'], format='%Y-%m-%d %H:%M:%S')
df['EST_time'] = df['endTime'] - datetime.timedelta(hours=5)
df = df[['endTime','EST_time','artistName','trackName','msPlayed','genre','clusters','new_gen']]
df['EST_time'] = pd.DatetimeIndex(df['EST_time'])
df['month'] = pd.DatetimeIndex(df['EST_time']).month
df['day'] = pd.DatetimeIndex(df['EST_time']).day
df['time'] = pd.DatetimeIndex(df['EST_time']).time
df['date'] = pd.DatetimeIndex(df['EST_time']).date
df['week'] = pd.DatetimeIndex(df['EST_time']).isocalendar()['week'].values

# options for various calendar visualizations
option = st.radio('Time Span', ('Year', 'Month'))

if option == 'Year':
    cal = st.radio('Frequency or Cluster?', ('Frequency', 'Cluster'))
    
    if cal == 'Frequency':
        st.image('graphs/12m_heatmap.jpeg')
    if cal == 'Cluster':
        st.image('graphs/12m_cluster.jpeg')

if option == 'Month':
    temp = st.selectbox('Month',
     ('Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'))
    months = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    m = months.index(temp) + 1
    
    dated = df.copy()
    dated = dated[dated['month']==m]
        
    level, selection = st.columns(2)
    
    with level:
        l = st.radio('Week or Day Pattern?', ('Week','Day'))
    
    if l == 'Week':
        weeks = dated['week'].unique().tolist()
        boxes = []
        
        for w in weeks:
            if weeks.index(w) == 0:
                DoW = pd.DatetimeIndex(dated[dated['week']==w]['EST_time']).isocalendar()['day'][0]
                date_DoW = pd.DatetimeIndex(dated[dated['week']==w]['EST_time']).isocalendar().index[0]
                first = date_DoW.date() - datetime.timedelta(days = int(DoW))

                c = selection.checkbox("Week of {} {}, {}".format(months[first.month-1],first.day,first.year), value = True)
            else:
                DoW = pd.DatetimeIndex(dated[dated['week']==w]['EST_time']).isocalendar()['day'][0]
                date_DoW = pd.DatetimeIndex(dated[dated['week']==w]['EST_time']).isocalendar().index[0]
                first = date_DoW.date() - datetime.timedelta(days = int(DoW))

                c = selection.checkbox("Week of {} {}, {}".format(months[first.month-1],first.day,first.year))
            boxes.append(c)
        
        selected = [w for (w, b) in zip(weeks, boxes) if b]
        
        fig = week_pattern(selected[0],dated)
        st.pyplot(fig)
        
        
    if l == 'Day':
        start = dated['date'].iloc[0]
        end = dated['date'].iloc[len(dated['date'])-1]
        
        with selection:
            spec_date = st.date_input(label = 'Select a date', value = start, min_value=start, max_value=end)
        
        valid_dates = dated['date'].unique().tolist()
        
        if (spec_date in valid_dates):
            fig = day_pattern(spec_date,dated)
            st.pyplot(fig)
        else:
            st.write("There are 330 valid dates out of 365 available, please try again.")            