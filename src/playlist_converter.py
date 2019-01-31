from spotify_searcher import search_helper, get_tracks
from playlist_tools import search_list_by_keyword, playlists_insert, playlist_items_insert, get_authenticated_service

client = get_authenticated_service()

def search_tracks(tracks):
	video_ids = list()

	for track in tracks:
		video_id = search_video(track)
		print(video_id)
		print(f'https://www.youtube.com/watch?v={video_id}')
		video_ids.append(search_video(track))

	add_videos(video_ids)

def search_video(q):
  result = search_list_by_keyword(client,
    part='snippet',
    maxResults=1,
    q=q,
    type='')
  return result['items'][0]['id']['videoId']

def create_playlist(client, title='Untitled playlist', description=''):
  playlists_insert(client, 
    {'snippet.title': title,
     'snippet.description': description,
     'snippet.tags[]': '',
     'snippet.defaultLanguage': '',
     'status.privacyStatus': ''},
    part='snippet,status',
    onBehalfOfContentOwner='')

def add_videos(ids):
  for video_id in ids:
    playlist_items_insert(client, 
    {'snippet.playlistId': 'PLzGPWqCF_JAn3f44E-zOsExn4INffD3BG', #placeholder
     'snippet.resourceId.kind': 'youtube#video',
     'snippet.resourceId.videoId': video_id,
     'snippet.position': ''},
    part='snippet',
    onBehalfOfContentOwner='')

#print(get_tracks(search_helper('yeehaw')[0]['id']))
#search_tracks(get_tracks('7LBp7eofa3RjniCKhVZooF'))

