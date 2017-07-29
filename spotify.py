import sys
import spotipy
import spotipy.util as util
import json
import random
from contextlib import contextmanager
import os
import time

# Stop html output to console
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
	old_stdout = sys.stdout
	sys.stdout = devnull
	try:  
		yield
	finally:
		sys.stdout = old_stdout

def getSong(username, query):

	scope = 'user-library-read'

	token = util.prompt_for_user_token(username, scope)
	sp = spotipy.Spotify(auth=token)

	sp.trace = True # turn on tracing
	sp.trace_out = True # turn on trace out
	
	# Pick the most popular playlist
	moodList = None 
	maxFollows = 0
	f ='followers,name,owner(!href,external_urls),tracks.items(added_by.id,track(name,href,artists(name),album(name,href)))'

	# Searches for the most popular playlist in groups of 10 playlists
	for x in range(0,2):
		try:
			with suppress_stdout():
				playlists = sp.search(q=query,limit=10,offset=(x*10),type='playlist')
			
			for playlist in playlists['playlists']['items']:
				with suppress_stdout():
					currList = sp.user_playlist(playlist['owner']['id'],playlist_id=playlist['id'],fields=f)
				if currList['followers']['total'] > maxFollows:
					maxFollows = currList['followers']['total']
					moodList = currList
		except Exception as e:
			print str(e)
			break

        # Of the popular playlist, choose a random song and output it
	if moodList is not None:
		i = random.randint(0,len(moodList['tracks']['items']) - 1)
		
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		print 'Playlist Name: ', moodList['name']
		print 'Playlist Owner: ', moodList['owner']['id']
		print 'Playlist Followers: ', maxFollows
		print moodList['tracks']['items'][i]['track']['name'], ' - ',

		for artist in moodList['tracks']['items'][i]['track']['artists']:
			if moodList['tracks']['items'][i]['track']['artists'].index(artist) == 0:
				print artist['name'],
			else:
				print ', ', artist['name'],
		print 
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	else:
		print('Unable to find an appropiate playlist!')

	return


    
