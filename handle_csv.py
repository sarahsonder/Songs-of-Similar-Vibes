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
import csv
from typing import Optional
from track import Track


def filter_csv(song_file: str) -> dict:
    """Returns a dictionary based on song_file. The key is the name and the artist of the song all lowercased,
    concatenated, with all spaces removed. Then, the associated value is the track id.

    Preconditions:
        - song_file refers to a valid csv file
    """
    with open(song_file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        song_dict = {}
        for row in reader:
            song_name = row[1].replace(' ', '')
            song_name = song_name.replace(',', '')
            artist_name = row[2].replace(' ', '')
            song_dict[song_name.lower() + artist_name.lower()] = row[0]

    return song_dict


def find_single_song(song_file: str, song: str) -> Optional[str]:
    """Returns a Track if the song the user inputs is found in the song_file, and returns None otherwise."""
    song_dict = filter_csv(song_file)
    song = song.replace(' ', '')
    song = song.replace(',', '')
    if song in song_dict:
        return song.lower()
    else:
        return None


def find_song(song_dict: dict, song: str) -> Optional[Track]:
    """Returns a Track if the song the user inputs is found in the song_file, and returns None otherwise."""
    song = song.replace(' ', '')
    song = song.replace(',', '')
    song = song.lower()
    if song in song_dict:
        return Track(song_dict[song])
    else:
        return None


def find_target_song(song_file: str, song: str) -> str:
    """Returns Sptofy URI."""
    song_dict = filter_csv(song_file)
    song = song.replace(' ', '')
    song = song.replace(',', '')
    song = song.lower()
    if song in song_dict:
        track = Track(song_dict[song])
        track_id = track.track_id
        uri = 'spotify:track:' + track_id
        return uri


def most_similar_songs(song_file: str, song: str, user_preferences: list[float]) -> dict:
    """Returns a dictionary of the top 10 most similar songs from a csv file.

    Preconditions:
        - song_file refers to a valid csv file
        - song != ''
        - len(user_preferences) == 11
    """
    song_dict = filter_csv(song_file)
    target = find_song(song_dict, song)
    track_lst = []
    returned_lst = {}
    track_song_and_artist = {}

    if target is not None:
        song_dict.pop(song)
        for song in song_dict:
            song = Track(song_dict[song])
            track_lst.append(song)
            track_song_and_artist[song.features['track_name']] = song.features['track_artist']

        similarity_score = target.calc_similarity_score(track_lst, user_preferences)
        sorted_similarity_scores = sorted(similarity_score.items(), key=lambda item: item[1], reverse=True)

        if len(sorted_similarity_scores) > 10:
            sorted_similarity_scores = sorted_similarity_scores[:11]

        for song in sorted_similarity_scores:
            if similarity_score[song[0]] >= 85:
                similar_ids = {track.track_id for track in track_lst if track.features['track_name'] == song[0]}

                artist = {track_song_and_artist[track] for track in track_song_and_artist if song[0] == track}
                returned_lst[similar_ids.pop()] = song[0] + ' by ' + artist.pop()

    return returned_lst
