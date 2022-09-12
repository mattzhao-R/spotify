import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Generation Process & Exploration",
    page_icon="💾"
)

st.markdown(
"""
## Data Generation Process & Exploration

In this section I will describe how I generated my dataset since it was a fairly intensive part of this project. First, I requested my past year's Spotify streaming history from Spotify. You can find the link describing how to do so [here](https://support.spotify.com/us/article/data-rights-and-privacy-settings/?ref=related). This data included the time when I started playing the song down to the minute in UTC, the song and artist names, and the duration I listened to the song for in milliseconds. 

From here, I wrote a series of functions which would allow me to get the audio features for each song using parallel processing via the Spotify API. This process mimics how parallelization works for Selenium workers in webscraping, with each Spotify 'worker' being fed into the queue for parallelization. 

I then needed to get the genre for each song since there was an issue with the Spotify API where 90% of artists did not have genres assigned to them. As a result, I turned to webscraping to get the genre for each song from a website called [last.fm](https://www.last.fm/). Scraping the genre for each song resulted in high variance and inconsistent genre assignments so I instead scraped the genre for each artist and assigned those to each song. This was done using BeautifulSoup and multiprocessing pool. 

The resulting dataframe from the DGP can be seen below.
"""
)

df = pd.read_csv('./final/final_table.csv')
st.dataframe(df)
st.sidebar.success("Sections")
