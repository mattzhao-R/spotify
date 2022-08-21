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
## Overview 


## Sections
* Summary
* Data Generation Process & Exploration
* Detecting Genres from Features
* Creating New Genre Clusters
* Visualizing Listening Patterns
"""
)