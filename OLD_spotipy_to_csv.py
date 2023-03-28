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


def get_single_track_features(track_id: str) -> dict[str, Any]:
    """Return the track features for ONE song."""
    track_info = sp.track(track_id, market=None)
    track_features = sp.audio_features([track_id])[0]  # returns list[dict[str, Any]

    track_features['track_name'] = track_info['name']
    track_features['track_artist'] = track_info['artists'][0]['name']
    track_features['track_id'] = track_features.pop('id')
    for feature in ['uri', 'track_href', 'analysis_url', 'liveness', 'type', 'key']:
        track_features.pop(feature)

    return track_features


def get_many_track_features(track_ids: list[str]) -> list[dict[str, Any]]:
    """Return the track features for SEVERAL songs."""
    all_track_features = []

    for track in track_ids:
        single_track_feature = get_single_track_features(track)
        all_track_features.append(single_track_feature)

    return all_track_features


def song_features(pl_ids: list[str]) -> list[dict[str, Any]]:
    """Returns the list of dictionaries that will be used to write the CSV file"""
    track_ids = get_songs_from_playlists(pl_ids)
    return get_many_track_features(track_ids)
    # song_lst = get_songs_from_playlists(pl_ids)
    # all_song_features = []
    #
    # for song in song_lst:  # Song is a Spotify URI
    #     track_info = sp.track(song, market=None)
    #     song_feature = sp.audio_features([song])[0]  # returns list[dict[str, Any]
    #     song_feature['track_name'] = track_info['name']
    #     song_feature['track_artist'] = track_info['artists'][0]['name']
    #
    #     song_feature['track_id'] = song_feature.pop('id')
    #     for feature in ['uri', 'track_href', 'analysis_url', 'liveness', 'type', 'key']:
    #         song_feature.pop(feature)
    #
    #     all_song_features.append(song_feature)
    #
    # return all_song_features


def write_csv(features: list[dict[str, Any]]) -> None:
    """Create a new csv with the all song features"""
    with open('hi_songs.csv', mode='w') as csvfile:
        fieldnames = features[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(features)


def similarity_score(track_id: str, other_song_id: list[str], playlist: bool = True) -> str:  # dict[str, float]:
    """Calculates the similarity score between songs"""
    string = ''
    target = get_single_track_features(track_id)
    if playlist:
        other_songs = song_features(other_song_id)
    else:
        other_songs = get_many_track_features(other_song_id)

    all_song_similarities = {}
    for song in other_songs:
        danceability = 1 - abs(target['danceability'] - song['danceability'])
        energy = 1 - abs(target['energy'] - song['energy'])
        loudness = 1 - (abs(target['loudness'] - song['loudness']) / 60)
        if target['mode'] == song['mode']:
            mode = 0.5
        else:
            mode = 0.0
        speechiness = (1 - abs(target['speechiness'] - song['speechiness']))
        accousticness = 1 - abs(target['acousticness'] - song['acousticness'])
        instramentalness = 1 - abs(target['instrumentalness'] - song['instrumentalness'])
        valence = 1 - abs(target['valence'] - song['valence'])
        tempo = 1 - (abs(target['tempo'] - song['tempo']) / 218)
        if target['duration_ms'] - 60000 <= song['duration_ms'] <= target['duration_ms'] + 60000:
            duration = 0.3
        else:
            duration = 0.0
        if target['time_signature'] == song['time_signature']:
            time_signature = 0.2
        else:
            time_signature = 0.0

        score = ((danceability + energy + loudness + mode + speechiness + accousticness +
                 instramentalness + valence + tempo + duration + time_signature) / 9) * 100
        string = f' Score: {score}, Danceability: {danceability}, Energy: {energy}, Loudness: {loudness}, Mode: {mode}' \
                 f' Speechiness: {speechiness}, acousticness: {accousticness}, Instramentalness: {instramentalness}' \
                 f' Valence: {valence}, Tempo: {tempo}, Duration: {duration}, Time Signature: {time_signature}'

        all_song_similarities[song['track_name']] = score
    return string
    # return all_song_similarities


def similarity_score1(track_id: str, other_song_id: list[str], playlist: bool = True) -> dict[str, float]:
    """i can't think rn"""
    target = get_single_track_features(track_id)
    similar_variables = ['danceability', 'speechiness', 'energy', 'acousticness', 'instrumentalness', 'valence']
    mode, duration, time_signature = 0.0, 0.0, 0.0

    if playlist:
        other_songs = song_features(other_song_id)
    else:
        other_songs = get_many_track_features(other_song_id)

    all_song_similarities = {}
    score_so_far = 0

    for song in other_songs:
        for variable in similar_variables:
            score_so_far += 1 - abs(target[variable] - song[variable])

        loudness = 1 - (abs(target['loudness'] - song['loudness']) / 60)
        tempo = 1 - (abs(target['tempo'] - song['tempo']) / 218)

        if target['mode'] == song['mode']:
            mode = 0.5
        if target['duration_ms'] - 60000 <= song['duration_ms'] <= target['duration_ms'] + 60000:
            duration = 0.3
        if target['time_signature'] == song['time_signature']:
            time_signature = 0.2

        score_so_far += (loudness + mode + tempo + duration + time_signature)
        all_song_similarities[song['track_name']] = (score_so_far/9) * 100

    return all_song_similarities


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
