import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

def get_creds():
    cid = 'client_id' # your client id here
    c_secr = 'client_secret' # your client secret here
    return cid,c_secr