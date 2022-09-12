import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Detecting Genres from Features",
    page_icon="🕵️"
)

st.markdown(
"""
## Detecting Genres from Features

The first goal of my analysis was to use machine learning to see what features were important in assigning a song to a specific genre. To do this, I needed to first prepare my data for modeling. I first began by determining which variables were categorical and continuous and converted the relevant categorical variables, here key, mode and time signature, using one hot encoding. 

I then checked to see if there was any significant collinearity in my dataset using a correlation heatmap as shown below.
"""
)
st.image('./graphs/corr_heatmap.png')

st.markdown(
"""
Since there is little correlation, I proceeded with my dataset. An issue I encountered with my data was that some genres were not represented enough in the data, causing issues with my model. As a result, I chose to remove genres that appeared less than 10 times and also used stratified k fold to split my data so that all genres were present in both the training and test data. 

I then trained multiple models using my training set and evaluated them using the test set. I used multinomial regression, knn, decision trees, random forest, and gradient boosting and my metrics were accuracy, top 5 accuracy, log loss, and F1 score. After performing hyperparameter tuning on the two best models (RF and GB), I found random forest to be the best based on these 4 metrics. 
"""
)


st.sidebar.success("Sections")
