# Module for obtaining/updating user play history objects 

# Grab new plays:
    # - add/update csv/json history files in 'globs.datp' and update log file in 'globs.logp'
    # - add/update user Spotify playlist 'History'

# Custom libs/modules
import playlist
import globs

# Other libs/modules
import spotipy
import spotipy.util as util
import pandas as pd
import numpy as np
import os.path
import datetime
import json
from pandas.io.json import json_normalize

# Options for terminal and .txt printout
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 120)
pd.options.display.max_colwidth = 20

def updatePlayHistory():
    
    # Get global Spotify object, username, and plays to get
    sp = globs.sp
    un = globs.un
    numPlays = globs.numPlays
    
    # Get most recent n = numPlays tracks in history, max = 50
    results = sp.current_user_recently_played(limit=numPlays) 

    # Flatten all results interpreted as json into dataframe
    histDFjson = pd.json_normalize(results['items']) 
    
    # Column names for simple play history csv 
    colNames = ["Track_Name", "Artist", "Album", "Time_Played", "Mult_Arts", "trackid", "artistid"]
    histDF = pd.DataFrame(columns = colNames) 
    tracks = []
    
    # Counting plays
    j = 1

    # Construct new simple dataframe of new play history by unnesting json. 
    for its in results['items']:

        allArtists = ''
        artists = its['track']['artists']
        allArtistids = ''
        for artist in artists:
            allArtists= allArtists + artist['name'] + '; '
            allArtistids = allArtistids + artist['id'] + '; ' 

        multArts = 0
        if len(artists) > 1:
            multArts = 1

        allArtists = allArtists[:-2]
        allArtistids = allArtistids[:-2]

        track=its['track']['name']
        album=its['track']['album']['name']
        timePlayed=its['played_at']
        trackid=its['track']['id']  

        newRow = [track,allArtists,album,timePlayed,multArts,trackid, allArtistids]
        histDF.loc[j-1] = newRow
        j+=1

    # Check if data directory exists and create if not 
    datp = globs.datp
    if not os.path.exists(datp):
        f = os.mkdir(datp)

    # Update history csv file or create new one
    csvf = os.path.join(datp,globs.csvf)
    if os.path.isfile(csvf):
        histOLD = pd.read_csv(csvf, sep=',', index_col=0) 
    else:
        histOLD = pd.DataFrame(columns = colNames)

    # Update full history json or create new one
    jsonf = os.path.join(datp,globs.jsonf) 
    if os.path.isfile(jsonf):
        histOLDjson = pd.read_json(jsonf)
    else:
        histOLDjson = pd.DataFrame()

    # Add new plays to history if they are new, and sort by time they occurred
    histNew = pd.concat([histDF,histOLD], sort=False).drop_duplicates()
    histNew = histNew.sort_values('Time_Played', ascending=False)

    # Count the number of plays added
    newPlays = pd.concat([histDF, histOLD, histOLD], sort=False).drop_duplicates(keep=False)
    
    # Convert to date-time so comparison of duplicates works with histOLD; issue with loading json from file
    htemp = histDFjson['played_at']

    # Combine new and old json format plays.
    histDFjson  = histDFjson.head(len(newPlays))
    histNewjson = histDFjson.append(histOLDjson)

    # Save new history with correct ordered indices
    indNew  = pd.Series(range(0,len(histNew)))
    histNew = histNew.set_index(indNew)
    histNew.to_csv(csvf, sep=',', encoding='utf-8',index_label='id')
    histNewjson.to_json(jsonf, orient='records')    

    # Update play history playlist on my account
    if len(newPlays) > 0:
        pl = playlist.addToPlayList(un,'History',newPlays,1)
    else:
        pl = playlist.getFullPlaylist(un,'History',1)[1]



    # Check if log folder exists and create if not 
    logp = globs.logp
    logf = os.path.join(logp,globs.logf)
    if not os.path.exists(globs.logp):
        f = os.mkdir(logp)
    
    logNames = ["Time_Updated", "Plays_Added", "Playlist_id"]
    # Update history csv file or create new one
    if os.path.isfile(logf):
        log = pd.read_csv(logf, sep=',', index_col=0)
    else:
        log = pd.DataFrame(columns = logNames)

    # Save update history to log and print to display
    log['Time_Updated']= pd.to_datetime(log['Time_Updated'])
    log.loc[len(log)] = [ pd.to_datetime('now'), len(newPlays), pl] 
    log = log.sort_values('Time_Updated', ascending=False)
    log.to_csv(logf, sep=',', encoding='utf-8',index_label='id')

    print("\n")
    print("*" * 34)
    print("Latest Update  %s" % datetime.datetime.now().replace(microsecond=0))
    print("*" * 34)
   
    if len(newPlays) > 0:
        if len(newPlays) == 1:
            print("Added 1 new track:\n")
        else:
            print("Added %i new tracks:\n" % len(newPlays))

        print(newPlays.to_string())
        print("\n")
    else:
        print("No new plays\n")


    return histNew


