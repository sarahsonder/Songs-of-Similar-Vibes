"""CSC111 Winter 2023 Project: Songs of Similar Vibez

This Python module contains the complete implementation of  functions filter_csv,
find_song, and most_similar_songs.

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


def filter_csv(csv_file: str) -> dict[str, list[str]]:
    """Returns a dictionary based on song_file. The key is the name and the artist of the
    song all lowercased,concatenated, with all spaces removed. Then, the associated value
    is the track id.

    Preconditions:
        - song_file refers to a valid csv file
    """
    with open(csv_file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        song_dict = {}
        for row in reader:
            song_dict[row[3]] = [row[0], row[1], row[2]]

    return song_dict


def find_song(song_dict: dict[str, list[str]], user_entry: str) -> Optional[Track]:
    """Returns a Track if the song the user inputs is found in the song_file, and returns
    None otherwise.

    song_dict is the dictionary obtained from the function filter_csv, where the key value is the
    concatenated string of the song title and artist, and the value is a list containing the track id,
    the track title, and the artist.

    Preconditions:
        - user_entry != ''
    """
    if user_entry in song_dict:
        track_id = song_dict[user_entry][0]
        return Track(track_id)
    else:
        return None


def most_similar_songs(song_dict: dict[str, list[str]], target: Track, user_preferences: list[float]) -> dict[str, str]:
    """Returns a dictionary of the top 10 most similar songs from a csv file where the key is the track id, and the
    associated value is in the form: track_name + ' by ' + track_artist.
    If there are less than 10 songs that meet the minimum threshold of having a similarity score of above or equal
    to 85 %, then only those songs that meet the 85% are returned.

    Preconditions:
        - song != ''
        - len(user_preferences) == 11
    """
    track_lst = []
    returned_lst = {}

    song_dict.pop(target.features['title_and_artist'])

    for song in song_dict:
        song = Track(song_dict[song][0])
        track_lst.append(song)

    similarity_score = target.calc_similarity_score(track_lst, user_preferences)
    sorted_similarity_scores = sorted(similarity_score.items(), key=lambda item: item[1], reverse=True)

    if len(sorted_similarity_scores) > 10:
        sorted_similarity_scores = sorted_similarity_scores[:11]

    for song in sorted_similarity_scores:
        if similarity_score[song[0]] >= 85:
            similar_ids = {track.track_id for track in track_lst if track.features['track_name'] == song[0]}

            artist = {song_dict[track][2] for track in song_dict if song[0] == song_dict[track][1]}
            returned_lst[similar_ids.pop()] = song[0] + ' by ' + artist.pop()

    return returned_lst


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['spotify_to_csv', 'track', 'csv'],
        'allowed-io': ['filter_csv'],
        'max-line-length': 120,
        'disable': ['R1704']
    })
