# spotter

## Overview

The goal of this project is to create an application to track my full Spotify listening history over time. The Spotify application only shows a limited number of plays and the Spotify Web API only allows users to access up to their fifty most recent plays. To view the output of a version of the application in deployment, [visit](http://www.mikejjenkinson.com/listening) my personal page.

The main Python application, when run once, works as follows:

1. Pull the user's most recent (up to fifty) plays from Spotify.   
2. Reference the database of user track plays and add the new track plays from the pull which aren't already in the database to avoid duplicates (or create a new database if it doesn't exist; a smaller CSV file and a larger JSON file are used).
3. Update the user's playlist "History" (or create it doesn't exist) with the new track plays. 

Since only the most recent fifty plays may be pulled at a time, the app must be run periodically before the user has listened to more tracks than the app is able to pull (up to fifty) since it was last run. Options to automate this are found below. 
 
This application relies on the following libraries:

1. The *[Spotipy](https://spotipy.readthedocs.io/en/2.14.0/)* package for interacting with the Spotify Web API. 
2. The *[Pandas](https://pandas.pydata.org/)* and *[NumPy](https://numpy.org/)* packages for data manipulation. 

## Setup instructions

Follow these instructions to set up and run the application in `spotipy/spot.py`

1. Download the contents of this repository to a new folder `<folder>` which should contain the `spotipy` folder and the `requirements.txt` and `README.md` files. The `data` and `logs` folders are generated automatically in this location and were included here as examples.

2. Install the Python packages in `requirements.txt` to your distribution. E.g.
       pip install -r requirements.txt

3. [Register your application](https://developer.spotify.com/documentation/general/guides/app-settings/) with Spotify to obtain a Client ID and Client Secret. For the redirect URI, you can use `http://localhost/`.

4. Change the following variables in `<folder>/spotipy/globs.py`. 
  - Change `un` to be your Spotipy user ID, which is a ten digit integer found on your [account overview](https://www.spotify.com/us/account/overview/).	
  - Change `clientid` to be your application's Client ID.
  - Change `clientsec` to be your application's Client Secret.
  - Change `dirp` to be the file path to the folder contaning the `spotter` application, `<folder>`. 

5. Run the application `<folder>/spotipy/spot.py` to pull and add your latest (up to fifty) track plays to your data files in your `<folder>/data` directory, as well as add them to your `History` playlist in Spotify. The first time you run the application, a browser window will open and you will be asked to log in to Spotify and  paste the resulting URL into the command line to authorize your Spotipy instance.   
       python <folder>/spotipy/spot.py


## Automation 

I opted to use *cron* in UNIX as a lightweight way to schedule runs of `<folder>/spotipy/spot.py` at periodic intervals. While I currently do not know the rate limit for requests to the Spotify API through the authorized Spotipy instance, my current deployment tracked [here](http://www.mikejjenkinson.com/listening) updates at intervals of fifteen minutes since it is unlikely that I will listen to more than fifty tracks in that interval.  

Create a file `cronscript.sh` in your `<folder>` directory containing the line

       python <folder>/spotipy/spot.py

Then activate the permissions

       chmod a+x cronscript.sh 

Finally, activate your Cron Job by entering `crontab -e` and adding the command

       */15 * * * * cd <folder>/spotipy && <folder>/spotipy/cronscript.sh 2>&1 >> <folder>/spotipy/cronlog.txt

which will run the application every fifteen minutes. Because your machine must be active to run the script at regular intervals, I opted to deploy my application on my virtual machine at [Digital Ocean](https://www.digitalocean.com/products/droplets/).

## Useful links and documentation
Spotipy Python library (wrapper for Spotify API):
- [Spotipy Documentation](https://spotipy.readthedocs.io/en/latest/)

Spotify developer guides and documentation:
- [Register Your Spotify Application](https://developer.spotify.com/documentation/general/guides/app-settings/)
- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/)

Download Spotify and register an account:
- [Spotify Website](https://www.spotify.com/us/)
