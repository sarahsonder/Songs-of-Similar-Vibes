"""CSC111 Winter 2023 Project: Songs of Similar Vibez

This Python module contains the complete implementation of the Track class, with a
Track object representing a single song on Spotify.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Vivian White, Sarah Wang, and Rebecca Kong.
"""
from __future__ import annotations
from typing import Any
from spotify_to_csv import get_tracks_features


class Track:
    """A class representing a song on Spotify.

    Instance Attributes:
        - track_id: The spotify URI of the song
        - features: A mapping between the names of attributes of a given song and its values for said
        attributes. These attributes include danceability, energy, loudness, mode, speechiness, acousticness,
        instrumentalness, valence, tempo, duration, time signature, track_name, track_artist, and track_id.
        - is_connected: A mapping from the name of an attribute of a song (as listed above) and whether
        the similarity score for that attribute is above a certain value (0.85). This is used in the
        Playlist graph to determine where to place edges.

    Representation Invariants:
        - track_id is a valid Spotify URI
        - self.is_connected == {} if and only if self is the target song
    """
    track_id: str
    features: dict[str, Any]
    is_connected: dict[str, bool]

    def __init__(self, track_id: str) -> None:
        """Initialize a new Track object using its track_id and track features.

        Preconditions:
            - track_id is a valid Spotify URI
        """
        self.track_id = track_id
        self.features = get_tracks_features([track_id])[0]
        self.is_connected = {}

    def calc_similarity_score(self, other_tracklst: list[Track], user_preferences: list[float]) -> dict[str, float]:
        """Updates the attribute is_connected for a list of tracks. For each, is_connected is
        updated such that every audible "characteristic" in features is present and has a corresponding
        value in is_connected.

        user_preferences is in order: danceability, speechiness, energy, acousticness, instrumentalness,
        valence, loudness, tempo, mode, duration, time_signature

        This method will also return a dictionary mapping from the name of a song, to its cumulatively calculated
        general similarity score between itself and the central song.

        After running this method, the Track has all the necessary information to generate a Playlist.

        Preconditions:
            - all(0.0 <= preference <= 1.1 for preference in user_preferences)
            - self.is_connected == {}
            - len(user_preferences) == 11
        """
        target = get_tracks_features([self.track_id])[0]
        similar_variables = ['danceability', 'speechiness', 'energy', 'acousticness', 'instrumentalness', 'valence']

        all_song_similarities = {}

        for song in other_tracklst:
            song_info = get_tracks_features([song.track_id])[0]
            score_so_far = 0
            mode, duration, time_signature = 0.0, 0.0, 0.0
            song.is_connected['mode'], song.is_connected['duration_ms'], song.is_connected['time_signature'] = \
                False, False, False
            var_num = 0
            for variable in similar_variables:
                score = (1 - abs(target[variable] - song_info[variable])) * user_preferences[var_num]
                score_so_far += score
                song.is_connected[variable] = score >= 0.85 * user_preferences[var_num]
                var_num += 1

            loudness = (1 - abs(target['loudness'] - song_info['loudness']) / 60) * user_preferences[6]
            song.is_connected['loudness'] = loudness >= 0.85 * user_preferences[6]
            tempo = (1 - abs(target['tempo'] - song_info['tempo']) / 218) * user_preferences[7]
            song.is_connected['tempo'] = tempo >= 0.85 * user_preferences[7]

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
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['spotify_to_csv', 'track'],
        'max-line-length': 120,
        'disable': ['R0914']

    })
