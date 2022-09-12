import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Creating New Genre Clusters",
    page_icon="🎙️"
)

st.markdown(
"""
## Creating New Genre Clusters

In this section I attempted to create new song groupings to see if there were better ways to group together songs than just their genres. To do this, I used unsupervised learning, specific k-means clustering, to identify new 'genres' in my songs. To find the optimal number of clusters k, I used the elbow method and found 15 to be the best as seen below.
"""
)
st.image('./graphs/kmeans_elbow.png')

st.markdown(
"""
Once I had added the new cluster assignments to each song, I wanted to see how these compared to the actual genres my songs had been assigned. To do this, I looked at the 5 most common genres for each cluster to see the type of music each cluster roughly corresponded to. You can see an example for some of the clusters below:
"""
)
final_df = pd.read_csv('./final/final_newGen.csv')

col1, col2, col3 = st.columns(3)
with col1:
    temp = final_df[final_df['clusters']==0]
    st.write('Cluster {}'.format(0))
    st.table(pd.DataFrame(temp['genre'].value_counts()).iloc[:5,:])

with col2:
    temp = final_df[final_df['clusters']==1]
    st.write('Cluster {}'.format(1))
    st.table(pd.DataFrame(temp['genre'].value_counts()).iloc[:5,:])

with col3:
    temp = final_df[final_df['clusters']==2]
    st.write('Cluster {}'.format(2))
    st.table(pd.DataFrame(temp['genre'].value_counts()).iloc[:5,:])

st.markdown(
"""
Since some clusters had the same top genre, I used the next most common genre for that cluster. There are significant limitations to my current method in regrouping these songs so I hope to revisit this project at a later time to perform more analyses. Specifically, I want to use a large sample of songs and attempt to get more accurate genres for my data and I want to examine the trends within each of my playlists to see if they are cohesive or could use some reorganizing. 
"""
)



st.sidebar.success("Sections")
