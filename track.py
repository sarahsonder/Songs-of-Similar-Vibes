"""Hi"""
from __future__ import annotations
from typing import Any
from spotify_to_csv import get_songs_from_playlists, get_tracks_features


SIMILARITY_VALUE = 0.85


class Track:
    """Track/song class

    Instance Attributes:
        - track_id: Spotify URI
        - features: danceability, energy, loudness, mode, speechiness, acousticness, instrumentalness, valence, tempo,
                    duration, time signature, track_name, track_artist, track_id
    """
    track_id: str
    features: dict[str, Any]
    is_connected: dict[str, bool]

    def __init__(self, track_id: str) -> None:
        """Initialize the Track object with its track_id and track features"""
        self.track_id = track_id
        self.features = get_tracks_features([track_id])[0]
        self.is_connected = {}

    def calc_similarity_score(self, other_tracklst: list[Track], user_preferences: list[float]) -> dict[str, float]:
        """Returns the similarities of songs compared to a target track

        DOCTEST CURRENTLY DOES NOT WORK
        >>> playlst = ['spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5']
        >>> songlst = get_songs_from_playlists(playlst)
        >>> target_track = Track('spotify:track:1KxwZYyzWNyZSRyErj2ojT')
        >>> scores = target_track.calc_similarity_score(songlst)
        >>> scores['Doppelgänger']
        71.03231566428813
        >>> scores['Better Days']
        69.30658341828067
        """
        # user preferences is in order: danceability, speechiness, energy, acousticness, instrumentalness \
        # valence, loudness, tempo, mode, duration, time_signature
        target = get_tracks_features([self.track_id])[0]
        similar_variables = ['danceability', 'speechiness', 'energy', 'acousticness', 'instrumentalness', 'valence']

        all_song_similarities = {}

        for song in other_tracklst:
            song_info = get_tracks_features([song.track_id])[0]
            score_so_far = 0
            mode, duration, time_signature = 0.0, 0.0, 0.0
            song.is_connected['mode'], song.is_connected['duration'], song.is_connected['time_signature'] = \
                False, False, False
            var_num = 0
            for variable in similar_variables:
                score = (1 - abs(target[variable] - song_info[variable])) * user_preferences[var_num]
                score_so_far += score
                song.is_connected[variable] = score >= SIMILARITY_VALUE * user_preferences[var_num]
                var_num += 1

            loudness = (1 - abs(target['loudness'] - song_info['loudness']) / 60) * user_preferences[6]
            song.is_connected['loudness'] = loudness >= SIMILARITY_VALUE * user_preferences[6]
            tempo = (1 - abs(target['tempo'] - song_info['tempo']) / 218) * user_preferences[7]
            song.is_connected['tempo'] = tempo >= SIMILARITY_VALUE * user_preferences[7]

            if target['mode'] == song_info['mode']:
                mode = user_preferences[8]
                song.is_connected['mode'] = True
            if target['duration_ms'] - 60000 <= song_info['duration_ms'] <= target['duration_ms'] + 60000:
                duration = user_preferences[9]
                song.is_connected['duration_ms'] = True
            if target['time_signature'] == song_info['time_signature']:
                time_signature = user_preferences[10]
                song.is_connected['time_signature'] = True

            score_so_far += (loudness + mode + tempo + duration + time_signature)
            all_song_similarities[song_info['track_name']] = (score_so_far / sum(user_preferences)) * 100

        return all_song_similarities


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
