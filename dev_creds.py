import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials

def get_creds():
    cid = 'client_id main'
    c_secr = 'client_secret main'
    return cid,c_secr

def alt_creds(cred_num=0): # unique pairs of cid and c_secret from spotify apps
    if (cred_num==0):
        cid = 'client_id 0' 
        c_secr = 'client_secret 0'
        return cid,c_secr
    if (cred_num==1):
        cid = 'client_id 1' 
        c_secr = 'client_secret 1'
        return cid,c_secr
    if (cred_num==2):
        cid = 'client_secret 2' 
        c_secr = 'client_secret 2'
        return cid,c_secr
    if (cred_num==3):
        cid = 'client_secret 3' 
        c_secr = 'client_secret 3'
        return cid,c_secr
    if (cred_num==4):
        cid = 'client_secret 4' 
        c_secr = 'client_secret 4'
        return cid,c_secr