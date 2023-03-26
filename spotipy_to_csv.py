"""Hi"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from typing import Any

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="d77034c7981d435a82a71f3f515f9a3a",
                                                           client_secret="5808c66cc4e04c0789dee00cb2e7b3d5"))


def get_songs_from_pl(pl_id: str) -> list[str]:
    """Takes in a playlist URI (pl_id), returns a list containing the song IDs from a given playlist.

    >>> song_list = get_songs_from_pl('spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5')
    >>> len(song_list)
    11
    """
    response = sp.playlist_items(pl_id, offset=0, fields='items.track.id,total', additional_types=['track'])
    song_lst = []

    for track_dict in response['items']:
        track_id = track_dict['track']
        song_id = track_id['id']
        song_lst.append(song_id)

    return song_lst


def get_songs_from_playlists(pl_ids: list[str]) -> list[str]:
    """Does the same thing as get_songs_from_pl except with several playlists"""
    all_songs = []

    for playlist in pl_ids:
        one_playlist = get_songs_from_pl(playlist)
        all_songs.extend(one_playlist)

    return all_songs

# TO CREATE A CSV FILE, YOU ONLY NEED TO USE THE TWO FUNCTIONS BELOW


def song_features(pl_ids: list[str]) -> list[dict[str, Any]]:
    """Returns the list of dictionaries that will be used to write the CSV file"""
    song_lst = get_songs_from_playlists(pl_ids)
    all_song_features = []

    for song in song_lst:  # Song is a Spotify URI
        track_info = sp.track(song, market=None)
        song_feature = sp.audio_features([song])[0]  # returns list[dict[str, Any]
        song_feature['track_name'] = track_info['name']
        song_feature['track_artist'] = track_info['artists'][0]['name']

        song_feature['track_id'] = song_feature.pop('id')
        for feature in ['uri', 'track_href', 'analysis_url', 'liveness', 'type', 'key']:
            song_feature.pop(feature)

        all_song_features.append(song_feature)

    return all_song_features


def write_csv(features: list[dict[str, Any]]) -> None:
    """Creat a new csv with the all song features"""
    with open('hi_songs.csv', mode='w') as csvfile:
        fieldnames = features[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(features)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
