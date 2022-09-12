import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Generation Process & Exploration",
    page_icon="💾"
)

st.markdown(
"""
## Data Generation Process (DGP)

In this section I will describe how I generated my dataset. 

*Spotify Streaming History*

First, I requested my past year's Spotify streaming history from Spotify. You can find the link describing how to do so [here](https://support.spotify.com/us/article/data-rights-and-privacy-settings/?ref=related). This data included the time when I started playing the song down to the minute in UTC, the song and artist names, and the duration I listened to the song for in milliseconds. 

*Getting Audio Features from Spotify API*

From here, I wrote a series of functions which would allow me to get the audio features for each song using parallel processing via the Spotify API. This process mimics how parallelization works for Selenium workers in webscraping, with each Spotify 'worker' being fed into the queue for parallelization. 

*Webscraping Genres*

I then needed to get the genre for each song since there was an issue with the Spotify API where 90% of artists did not have genres assigned to them. As a result, I turned to webscraping to get the genre for each song from a website called [last.fm](https://www.last.fm/). Scraping the genre for each song resulted in high variance and inconsistent genre assignments so I instead scraped the genre for each artist and assigned those to each song. This was done using BeautifulSoup and multiprocessing pool. 

The resulting dataframe from the DGP can be seen below.
"""
)

df = pd.read_csv('./final/final_table.csv')
st.dataframe(df)

st.markdown(
"""
## Exploration

With this data, we can replicate some of the fun statistics from Spotify Wrapped
"""
)

artists, songs, genres = st.columns([3,5,3])

def min_hour(minutes):
    t = int(minutes)
    h = int(t/60)
    m = t % 60
    return('{}h {}m'.format(h,m))

with artists:
    temp = df.groupby('artistName',as_index=False).agg({'msPlayed':'sum'}).sort_values(by='msPlayed', axis=0,ascending=False).iloc[:5,:]
    temp['msPlayed'] = (temp['msPlayed']/60000).apply(lambda x: min_hour(x))
    temp.rename(columns={'artistName':'Artist','msPlayed':'Duration'},inplace=True)
    temp.set_index(pd.Index([1, 2, 3, 4,5]),inplace=True)
    st.write('Top 5 Artists')
    st.table(temp)
    
with songs:
    temp = df.groupby(['trackName','artistName'],as_index=False).agg({'msPlayed':'sum'}).sort_values(by='msPlayed',axis=0,ascending=False).iloc[:5,:]
    temp['msPlayed'] = (temp['msPlayed']/60000).apply(lambda x: min_hour(x))
    temp.rename(columns={'trackName':'Song','artistName':'Artist','msPlayed':'Duration'},inplace=True)
    temp.set_index(pd.Index([1, 2, 3, 4,5]),inplace=True)    
    st.write('Top 5 Songs')
    st.table(temp)

with genres:
    temp = df.groupby('genre',as_index=False).agg({'msPlayed':'sum'}).sort_values(by='msPlayed', axis=0,ascending=False).iloc[:5,:]
    temp['msPlayed'] = (temp['msPlayed']/60000).apply(lambda x: min_hour(x))
    temp.rename(columns={'trackName':'Song','msPlayed':'Duration'},inplace=True)
    temp.set_index(pd.Index([1, 2, 3, 4,5]),inplace=True)
    st.write('Top 5 Genres')
    st.table(temp)

st.markdown(
"""
Additionally, there are a lot of genres in the initial dataset, over 250 among the nearly 20,000 songs I've listened to the past year. However, many of them only appear a handful of times, with only around 20 appearing more than 250 times. 
"""
)
st.image('./graphs/genre_histogram.png')


st.sidebar.success("Sections")
