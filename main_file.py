"""Hi"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="d77034c7981d435a82a71f3f515f9a3a",
                                                           client_secret="5808c66cc4e04c0789dee00cb2e7b3d5"))

song_id = 'spotify:track:2QhURnm7mQDxBb5jWkbDug'
print(sp.audio_features([song_id]))
# results = sp.search(q='BTS', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])

# pl_id = 'spotify:playlist:5RIbzhG2QqdkaP24iXLnZX'
# pl_id = 'spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5'
# offset = 0
#
# while True:
#     response = sp.playlist_items(pl_id,
#                                  offset=offset,
#                                  fields='items.track.id,total',
#                                  additional_types=['track'])
#
#     if len(response['items']) == 0:
#         break
#
#     print(response['items'])
#     offset = offset + len(response['items'])
#     print(offset, "/", response['total'])
