import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow



# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtubepartner']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# When running locally, disable OAuthlib's HTTPs verification. When
# running in production *do not* leave this option enabled.
  
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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


def search_list_by_keyword(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  print(response)
  return response

'''playlist_items_insert(client, 
    {'snippet.playlistId': '',
     'snippet.resourceId.kind': 'youtube#video',
     'snippet.resourceId.videoId': 'M7FIvfx5J10',
     'snippet.position': ''},
    part='snippet',
    onBehalfOfContentOwner='')
  return print_response(response)'''

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

  

