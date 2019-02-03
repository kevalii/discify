# Ensures absolute import from root
import os, sys
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = CURRENT_DIR + "/logs/"
sys.path.append(os.path.dirname(CURRENT_DIR))

import src
import logging
from pathlib import Path
from time import localtime, strftime

Path(f'{CURRENT_DIR}/logs').mkdir(exist_ok=True)

# Generate latest.log file and replace previous
latest_path = Path(f'{LOGS_DIR}latest.log')
if latest_path.exists():
   latest_path.rename(f"{LOGS_DIR}{strftime('%Y-%m-%d-%H-%M-%S', localtime(latest_path.stat().st_mtime))}")

logging.basicConfig(filename=f'{CURRENT_DIR}/logs/latest.log', level=logging.DEBUG)

# Spotify
def spotify_api():
   if src.spotify_searcher.search_helper('koalas') is None:
      logging.warning('Failed to obtain Spotify playlists!\n')

   if src.spotify_searcher.get_tracks('4ERqwnEWy7WDuoPgGlOPaE') is None:
      logging.warning('Failed to obtain tracks\n')

def youtube_api():
   if src.youtube_searcher.search_video('koalas') is None:
      logging.warning('Failed to obtain Youtube video!')

if __name__ == "__main__":
   logging.info(f"{'#' * 20} Begin tests {'#' * 20}\n")
   spotify_api()
   youtube_api()
   logging.info(f"{'#' * 20} End tests {'#' * 20}\n")

