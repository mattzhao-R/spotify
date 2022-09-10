import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(
    page_title="Introduction"
)

st.write("# Spotify Wrapped ver.2 - Listening Calendar & Genre Detection")

st.sidebar.success("Sections")

st.markdown(
"""
### Introduction

Hello! My name is Matthew Zhao and I am a junior at the University of Chicago studying Economics and Data Science. This website showcases my project on Spotify song classification and listening patterns. 

The inspiration for the various analyses in this project comes from my own interest in making cohesive Spotify playlists for my own and my friends' enjoyment, and looks to more closely examine the relationship between songs' assigned genres and its actual audio features. It then attempts to 're-classify' these songs into new genre groupings based on these features and finally visualizes the listening patterns of these new genre clusters using an interactive calendar-like format. 


### Sections
* Summary
* Data Generation Process & Exploration
* Detecting Genres from Features
* Creating New Genre Clusters
* Visualizing Listening Patterns
"""
)