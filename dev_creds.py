import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

def get_creds():
    cid = 'c210de964165497b851bdb12688c548b'
    c_secr = 'd7bbca6aaa334d71bed52eac97516495'
    return cid,c_secr