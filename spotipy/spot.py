# Tracker  for Spotify listening history using Spotipy (Python library).
# Custom libs/modules
import playhistory
import playlist
import secsets
import globs
import time

# Other libs/modules
import spotipy
import spotipy.util as util
import numpy as np
import os.path
from datetime import datetime
import json
from pandas.io.json import json_normalize
import pandas as pd


# token = util.prompt_for_user_token(
#        username=secsets.un,
#        scope=secsets.scopeCur,
#        client_id=secsets.clientid,
#        client_secret=secsets.clientsec,
#        redirect_uri=secsets.reduri)

def main():
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(username=secsets.un,
         scope=secsets.scopeCur,
         client_id=secsets.clientid,
         client_secret=secsets.clientsec,
         redirect_uri=secsets.reduri))
    me = sp.me()

    # Get spotify object, username, and filepath
    globs.sp = sp

    # Grab new plays: 
    # - add/update files 'playHistory.csv', 'playHistoryLong.json', 'updateLog.txt' 
    # - add/update user Spotify playlist 'History'
    hist = playhistory.updatePlayHistory()

    print(me)
    
    print("spot.py run at time  =", datetime.now())

if __name__ == "__main__":
    main()
