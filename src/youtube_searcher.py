import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Get YouTube service resource
def get_service():
  return build(API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY)

client = get_service()

def print_response(response):
  print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

''' Legacy functions
def playlists_list_mine(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlists().list(
    **kwargs
  ).execute()

  return print_response(response)

def playlists_insert(client, properties, **kwargs):
  # See full sample for function
  resource = build_resource(properties)

  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlists().insert(
    body=resource,
    **kwargs
  ).execute()

def playlist_items_insert(client, properties, **kwargs):
  resource = build_resource(properties)
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().insert(
    body=resource,
    **kwargs
  ).execute()

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
'''

def search_list_by_keyword(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  return response

# Returns the video id of the first video in the search result for q
def search_video(q):
    try:
        result = search_list_by_keyword(client,
            part='snippet',
            maxResults=1,
            q=q,
            type='')
        return f"https://www.youtube.com/watch?v={result['items'][0]['id']['videoId']}"
    except KeyError:
        return None




