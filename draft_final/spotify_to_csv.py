"""Extracts data from Spotify API, cleans the data, and converts the data into a CSV file."""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from typing import Any

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="d77034c7981d435a82a71f3f515f9a3a",
                                                           client_secret="5808c66cc4e04c0789dee00cb2e7b3d5"))


def get_songs_from_playlists(playlists: list[str]) -> list[str]:
    """Takes a list of playlist URIs. Returns a list containing all the song URIs in the playlists.

    >>> playlst = ['spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5', 'spotify:playlist:3mfVIXTsVA0O0yfHrPD4yE']
    >>> track_ids = get_songs_from_playlists(playlst)
    >>> track_ids[0]
    '7qjF1j0sMTLcmiTKXwVh09'
    """
    all_songs = []

    for playlist in playlists:
        response = sp.playlist_items(playlist, offset=0, fields='items.track.id,total', additional_types=['track'])

        for track_dict in response['items']:
            track_tag = track_dict['track']
            song_id = track_tag['id']
            all_songs.append(song_id)

    return all_songs


def get_tracks_features(track_ids: list[str]) -> list[dict[str, Any]]:
    """Takes in a list of song URIs, return the track features for each songs.

    >>> playlst = ['spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5']
    >>> songlst = get_songs_from_playlists(playlst)
    >>> features = get_tracks_features(songlst)
    >>> features[0]
    {'danceability': 0.276, 'energy': 0.154, 'loudness': -18.451, 'mode': 0, 'speechiness': 0.0327, 'acousticness':
    0.968, 'instrumentalness': 0.363, 'valence': 0.144, 'tempo': 80.763, 'duration_ms': 209815, 'time_signature': 3,
    'track_name': 'Doppelgänger', 'track_artist': 'Lissom', 'track_id': '7qjF1j0sMTLcmiTKXwVh09'}
    """
    all_track_features = []

    for track in track_ids:
        track_info = sp.track(track, market=None)
        track_features = sp.audio_features([track])[0]  # returns list[dict[str, Any]

        track_features['track_name'] = track_info['name']
        track_features['track_artist'] = track_info['artists'][0]['name']
        track_features['track_id'] = track_features.pop('id')

        title_and_artist = track_info['name'] + track_info['artists'][0]['name']
        no_space = title_and_artist.replace(' ', '')
        no_comma = no_space
        track_features['title_and_artist'] = no_comma.lower()
        for feature in ['uri', 'track_href', 'analysis_url', 'liveness', 'type', 'key']:
            track_features.pop(feature)

        all_track_features.append(track_features)

    return all_track_features


def write_csv(playlists: list[str]) -> None:
    """Creat a new csv with the all song features"""
    track_lst = get_songs_from_playlists(playlists)
    features = get_tracks_features(track_lst)

    with open('small_dataset.csv', mode='w') as csvfile:
        fieldnames = features[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(features)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
