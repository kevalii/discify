import requests
import requests.auth
from dotenv import load_dotenv
import os

load_dotenv()
SPOT_CLIENT_ID=os.getenv('SPOT_CLIENT_ID')
SPOT_CLIENT_SECRET=os.getenv('SPOT_CLIENT_SECRET')

# Client credentials auth
def auth():
	client_auth = requests.auth.HTTPBasicAuth(SPOT_CLIENT_ID, SPOT_CLIENT_SECRET)
	body = {'grant_type': 'client_credentials'}
	response = requests.post("https://accounts.spotify.com/api/token", auth=client_auth, data=body)
	return {'Authorization': 'Bearer ' + response.json()['access_token']}

# Searches for a specified playlist and displays the results
def search_helper(q):
	token = auth()
	response = requests.get(f"https://api.spotify.com/v1/search/?q={q}&type=playlist&limit=2", headers=token).json()
	results = list()
	for playlist in response['playlists']['items']:
		results.append(playlist)
	return results

# Get all of a playlist's tracks
def get_tracks(playlist_id):
	token = auth()
	response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=token).json()
	tracks = list()
	for track in response['items']:
		tracks.append(f"{track['track']['name']} by {track['track']['artists'][0]['name']}")
	
	for track in tracks:
		print(track)
	return tracks