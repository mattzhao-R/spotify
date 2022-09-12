import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Summary",
    page_icon="📖"
)

st.markdown(
"""
## Summary

The two main goals of this project were to (1) examine the relationship between the audio features of a song and its assigned genre and (2) see how songs group together only based on their audio features to see if these groups are different than the song's assigned genre. Below I summarize the main results of each objective. 

**Relationship between Audio Features and Genre**

Since this is a multi-class classification task, I tested various machine learning models such as multinomial logistic regression, k-nearest neighbors, decision trees, random forest, and gradient boosting and compared their performances using metrics including accuracy, log loss, and F1. Random Forest and Gradient Boosting generally performed better than other models but RF performed better in F1 in out-of-sample (OOS) tests. Shown below is the feature importance chart for my model which indicates that the song's duration, as well as its danceability and loudness are some of the most important features in determining what a song's genre is.  
"""
)
st.image('./graphs/RF_featimp.png')

st.markdown(
"""
**Re-grouping Songs by Audio Features**

Here I wanted to see how songs cluster independently of their assigned genre to see if there were better ways of putting songs into cohesive groups. To do this, I used unsupervised learning via k-means clustering. I used the elbow method to determine the optimal number of clusters and found 15 to be the best. While there are over 100 genres represented in the training set, only around 20 appear more than 250 times which accounts for over a quarter of the total genres in the dataset, making this not entirely unexpected. 
"""
)

st.sidebar.success("Sections")
