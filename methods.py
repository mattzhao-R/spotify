import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from collections import Counter
from tqdm.notebook import tqdm
import json
import os
import time

import dev_creds

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import matplotlib.pyplot as plt
plt.rc('font', size=14)
import seaborn as sns
sns.set(style='whitegrid', color_codes=True, rc={'figure.figsize':(11,8)}, font_scale=2)

# creates spotipy api object using alt cred (function used with parallelization to create multiple spotipy workers)
def sp_worker(alt):
    cid, secret = dev_creds.alt_creds(alt)
    client_credentials_manager = SpotifyClientCredentials(client_id=cid,client_secret=secret)
    worker = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return worker


# takes in song_artist object and returns track ID based on song-artist matching from searching Spotify API
def search_getid(worker,song_artist):
    pair = song_artist.song + ' ' + song_artist.artist
    temp = worker.search(pair)
    end = len(temp['tracks']['items'])
    for x in range(0,end):
        out_track = temp['tracks']['items'][x]['name']
        out_artist = temp['tracks']['items'][x]['artists'][0]['name']
        track_id = temp['tracks']['items'][x]['id']
        if ((song_artist.song == out_track) and (song_artist.artist == out_artist)):
            return(track_id)

# create row matching track_id to song_artist combination (function used with parallelization to construct link table)
def table_ids(worker, song_artist):
    track_id = search_getid(worker,song_artist)
    
    file = open('./modified/table_ids.csv', 'a')
    writer = csv.writer(file)
    row = [song_artist,track_id]
    writer.writerow(row)
    file.close()