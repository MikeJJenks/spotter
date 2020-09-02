# Global variables and settings for use in spotter.py and other libs/modules:
# - spot.py
# - playHistory.py

import pandas as pd
import os.path 
import secsets

# Some global variables for Spotipy tracker (Spotify object and current username)
sp = 0
un = secsets.un
# Plays to pull from the Spotipy API call (max 50)
numPlays = 50

# Turns off setwithcopywarning for chained assignment
pd.options.mode.chained_assignment = None
# Options for terminal and .txt printout
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 120)
pd.options.display.max_colwidth = 20

# File paths and names
dirp  = secsets.dirp 
logp  = os.path.join(dirp,'logs')
logf  = 'log.csv'
datp  = os.path.join(dirp,'data')
csvf  = 'plays.csv'
jsonf = 'plays.json'

