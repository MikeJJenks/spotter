import spotipy
import spotipy.util as util
import numpy as np
import os.path
import datetime
import json
from pandas.io.json import json_normalize
import globs
import pandas as pd

def getFullPlaylist(un,playlistname,cr):
    
    sp = globs.sp
    # un = globs.un

    # Check whether the playlist exists and get its id
    pl = pd.DataFrame(sp.user_playlists(un)['items'])
    playlistid= pl[pl['name']==playlistname]['id']

    if( playlistid.shape[0]==0 ):
        if( cr == 0 ):
            print("Playlist \'" + playlistname + "\' does not exist. Exiting. \n") 
            return 0
        else:
            print("Creating playlist \'" + playlistname + "\' \n")
            playlistid = sp.user_playlist_create(un, playlistname, public=False)
            playlistid = [playlistid['id']]

    print(playlistid)
    playlistid='spotify:playlist:'+str(playlistid[0])

    results = sp.user_playlist_tracks(un, playlistid)
    tracks = results['items']

    # Spotify API limits to 100 tracks of playlist per query; must use pagination to get all
    while results['next']:
               results = sp.next(results)
               tracks.extend(results['items'])

    trnames = []
    tracksNew = []
    for tr in tracks:
        trnames.append(tr['track']['name'])
        tracksNew.append(tr['track'])
    # trnames.sort()

    print("Retrieved playlist \'" + playlistname + "\' which has the following tracks:")

    for tr in trnames:
        print(tr)

    tracksNew = pd.DataFrame(tracksNew)

    return tracksNew, playlistid 

#

def addToPlayList(un,playlistname,tracks,cr):

    sp = globs.sp
    # un = globs.un

    # Check whether the playlist exists and get its id
    pl = pd.DataFrame(sp.user_playlists(un)['items'])
    playlistid=pl[pl['name']==playlistname]['id']

    if( playlistid.shape[0]==0 ):
        if( cr == 0 ):
            print("Playlist \'" + playlistname + "\' does not exist. Exiting. \n")
            return 0
        else:
            print("Creating playlist \'" + playlistname + "\' \n")
            playlistid = sp.user_playlist_create(un, playlistname, public=False)
            playlistid = [playlistid['id']]

    playlistid='spotify:playlist:'+str(playlistid[0])


    # Add new tracks to the top of the playlist
    print("Adding " + str(tracks.shape[0]) + " new tracks to playlist \'" + playlistname + "\'\n")
    print(tracks)
    tr = list(tracks['trackid'])
    sp.user_playlist_add_tracks(un, playlistid, tr, position=0)

    return playlistid 

#

# No API functionality for deleting whole playlist at once
def removeAllPlaylist(un,playlistname,cr):

    sp = globs.sp

    # Check whether the playlist exists and get it 
    tracks, playlistid = getFullPlaylist(un,playlistname,cr)

    # Add new tracks to the top of the playlist

    if( tracks.shape[0]==0 ):
        print("No tracks to remove.")
    else:
        print("Removing all tracks from playlist \'" + playlistname + "\': \n")
        print(tracks['name'])
        tr = list(tracks['uri'])
        sp.user_playlist_remove_all_occurrences_of_tracks(un, playlistid, tr)

    return 0
