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
df['year'] = pd.DatetimeIndex(df['EST_time']).year
df['month'] = pd.DatetimeIndex(df['EST_time']).month
df['day'] = pd.DatetimeIndex(df['EST_time']).day
df['time'] = pd.DatetimeIndex(df['EST_time']).time
df['date'] = pd.DatetimeIndex(df['EST_time']).date
df['week'] = pd.DatetimeIndex(df['EST_time']).isocalendar()['week'].values

# options for various calendar visualizations
option = st.radio('Time Span', ('Year Calendar', 'Week/Day Schedules'))

if option == 'Year Calendar':
    cal = st.radio('Frequency or Cluster?', ('Frequency', 'Cluster'))
    
    if cal == 'Frequency':
        st.image('graphs/12m_heatmap.jpeg')
    if cal == 'Cluster':
        st.image('graphs/12m_cluster.jpeg')

if option == 'Week/Day Schedules':
    months = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    temp = st.selectbox('Month',
     ('May \'21','Jun \'21','Jul \'21','Aug \'21','Sep \'21','Oct \'21','Nov \'21','Dec \'21',
      'Jan \'22', 'Feb \'22', 'Mar \'22','Apr \'22','May \'22'))
    tri_month = temp[0:3]
    y = int('20' + temp[len(temp)-2:])
    m = months.index(tri_month) + 1
            
    dated = df.copy()
    dated = dated[(dated['month']==m) & (dated['year']==y)]
        
    level, selection = st.columns(2)
    
    with level:
        l = st.radio('Week or Day Schedule?', ('Week','Day'))
    
    if l == 'Week':
        weeks = dated['week'].unique().tolist()
        boxes = []
        
        with selection:
            st.write('Pick a week to visualize or compare the patterns of two weeks')

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
        
        try:
            if len(selected)==1:
                fig = week_pattern(selected[0],dated)
                st.pyplot(fig)
            elif len(selected)==2:
                col1, col2 = st.columns(2)
                with col1:
                    fig = week_pattern(selected[0],dated)
                    st.pyplot(fig)
                with col2:
                    fig = week_pattern(selected[1],dated)
                    st.pyplot(fig)
        except:
            st.markdown("**Please select a week to visualize**")
        
        
    if l == 'Day':
        start = dated['date'].iloc[0]
        end = dated['date'].iloc[len(dated['date'])-1]
        
        with selection:
            spec_date = st.date_input(label = 'Select a date', value = start, min_value=start, max_value=end)
        
        all_dates = pd.date_range(start=start,end=end)
        all_dates = pd.DatetimeIndex(all_dates).date.tolist()
        
        invalid=[]
        
        for date in all_dates:
            try: 
                fig = day_pattern(date,dated)
            except:
                invalid.append(date)
                
        if (spec_date in invalid):
            st.write("This date is not valid, please try again.")
            show = st.checkbox(label = 'Check this box to see a list of the invalid dates for {}'.format(temp))
            if show:
                for i in invalid:
                    st.write('-{} {}'.format(months[i.month-1],i.day))
        else:           
            fig = day_pattern(spec_date,dated)
            st.pyplot(fig)
        
