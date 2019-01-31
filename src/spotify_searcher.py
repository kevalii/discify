import requests
import requests.auth
from dotenv import load_dotenv
import os

load_dotenv()
SPOT_CLIENT_ID=os.getenv('SPOT_CLIENT_ID')
SPOT_CLIENT_SECRET=os.getenv('SPOT_CLIENT_SECRET')
SPOTIFY_ENDPOINT = 'https://api.spotify.com/v1/'

# Client credentials auth
def auth():
	client_auth = requests.auth.HTTPBasicAuth(SPOT_CLIENT_ID, SPOT_CLIENT_SECRET)
	body = {'grant_type': 'client_credentials'}
	response = requests.post("https://accounts.spotify.com/api/token", auth=client_auth, data=body)
	return {'Authorization': 'Bearer ' + response.json()['access_token']}

## TODO It would be better to check status code of the response than to silence the exception this way.
# Searches for a specified playlist and displays the results
def search_helper(q):
   try:
      results = requests.get(f"{SPOTIFY_ENDPOINT}search/?q={q}&type=playlist&limit=25", headers=auth()).json()['playlists']['items']
      return [playlist for playlist in results]
   except KeyError:
      return

# Get all of a playlist's tracks
def get_tracks(playlist_id):
   try:
      tracks = requests.get(f"{SPOTIFY_ENDPOINT}playlists/{playlist_id}/tracks", headers=auth()).json()
      return [f"{track['track']['name']} by {track['track']['artists'][0]['name']}" for track in tracks['items']]
   except KeyError:
      return
