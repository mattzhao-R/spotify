import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from collections import Counter
from tqdm.notebook import tqdm

import json
import os
import time
import csv

from dev_creds import alt_creds
from objects import song_artist

import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import matplotlib.pyplot as plt
plt.rc('font', size=14)
import seaborn as sns
sns.set(style='whitegrid', color_codes=True, rc={'figure.figsize':(11,8)}, font_scale=2)

# creates spotipy api object using alt cred (function used with parallelization to create multiple spotipy workers)
def sp_worker(alt):
    cid, secret = alt_creds(alt)
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

# takes in track_id and returns list of relevant audio features
def get_features(worker, track_id):
    ft = worker.audio_features(track_id)
    feats = list(ft[0].values())
    del feats[-7:-2]
    
    return(feats)

# general function for writing a list to a row of a csv
def row_writer(row, path):
    file = open(path, 'a')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()
    return


# create row of link table matching song_artist to track_id and audio feats (function used with parallelization to construct link table)
def id_feats(worker, song_artist, file_name = 'id_feats', write = True):
    try:
        track_id = search_getid(worker, song_artist)
        feats = get_features(worker, track_id)
    except:
        feats = [np.nan for i in range(0,14)]
    
    path = './modified/' + file_name + '.csv'
    
    if(write):
        row = [song_artist,track_id] + feats
        row_writer(row,path)
        return
    else:
        return track_id, feats

# get genre from last.fm
def get_genre(song_artist, file_name = 'genres', write = True):
    song = song_artist.song
    artist = song_artist.artist
    
    artist_query = "+".join(artist.split(" "))
    song_query = "+".join(song.split(" "))
    
    query = 'https://www.last.fm/music/' + artist_query + '/_/' + song_query
    
    try:
        req = requests.get(query, allow_redirects=False)
    except:
        genre = 'redirect error'
    
    try:
        sample = BeautifulSoup(req.content, 'html.parser')
    except:
        pass
    
    try:
        section = sample.find(name='section', class_ = 'catalogue-tags')
        genre = section.find(name='li').string
    except:
        genre = np.nan
    
    path = './modified/' + file_name + '.csv'
    
    if(write):
        row = [song_artist,genre]
        row_writer(row,path)
        return
    else:
        return genre

# combines row_writer, id_feats, and last_fm to create a table of track_id, audio feats, and genre using parallelization
def create_table(worker, song_artist, fname = 'full_table'):
    track_id, feats = id_feats(worker, song_artist, write = False)
    genre = get_genre(song_artist, write = False)
    
    path = './modified/' + fname + '.csv'
    row = [track_id,feats,genre]
    row_writer(row,path)
    return