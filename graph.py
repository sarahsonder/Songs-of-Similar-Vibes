"""CSC111 Winter 2023 Project: Songs of Similar Vibez

This Python module contains the complete implementation of the Graph class,
representing a graph of Tracks and their similarity to the target Track.
It contains the methods to generate and to visualize the graph.

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

from typing import Optional

import networkx as nx
from pyvis.network import Network

from python_ta.contracts import check_contracts

from spotify_to_csv import get_tracks_features
from track import Track


class Playlist:
    """A tree structure representing how a list of songs are related to a "central" target song.
    Each node stores either a Track representing a song on Spotify, or a string representing
    an attribute of the central song.

    Instance Attributes:
        - _song: the value stored at this node: a string if this node connects directly to
        the central song, and a Track otherwise.
        - _neighbours: a mapping consisting of every node connected to this node. It maps
        from the name of a song or attribute to the Playlist which is connected to self and
        contains that name.

    Representation Invariants:
        - all(self._neighbours[neighbour]._song == neighbour or self._neighbours[neighbour]._song.track_id /
        == neighbour for neighbour in self._neighbours)
        - all(self in neighbour._neighbours for neighbour in self._neighbours.values())
        - all(self._song.isinstance(str) != neighbour._song.isinstance(str for neighbour in self._neighbours.values())
    """
    _song: str | Track
    _neighbours: dict[str, Playlist]

    def __init__(self, song: str, features_list: Optional[list[Playlist]] = None) -> None:
        """Initialize a new Playlist.

        Preconditions:
            - all(playlist._song.isinstance(str) for playlist in features_list)
            - song is a valid Spotify URI
        """
        features = {'danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                    'valence', 'tempo', 'duration_ms', 'time_signature'}
        self._neighbours = {}
        if song in features:
            self._song = song
        else:
            self._song = Track(song)
        if features_list is not None:
            for feature in features_list:
                self._neighbours[feature._song] = feature
                feature._neighbours[song] = self
        else:
            self._neighbours = {}

    def add_neighbour(self, song: Playlist) -> None:
        """Connects a new neighbour to a feature node.

        Preconditions:
            - self._song.isinstance(str)
            - song.is_connected[self._song]
        """
        self._neighbours[song._song.track_id] = song
        song._neighbours[self._song] = self

    def generate_playlist(self, songs: list[str], user_preferences: list[float]) -> dict[str, float]:
        """Updates the playlist graph to reflect the similarity scores of the songs.

        Preconditions:
            - all(0.0 <= preference <= 1.0 for preference in user_preferences)
            - all strings in songs are valid Spotify URIs
            - self._song.isinstance(Track)
            - all(feature in self._song.features for feature in self._neighbours)
            - self._song.is_connected == {}
        """
        songs_list = [Track(s) for s in songs]
        similarity_score = self._song.calc_similarity_score(songs_list, user_preferences)
        for song in songs_list:
            features = song.features
            features.pop('track_name')
            features.pop('track_artist')
            features.pop('track_id')
            for feature in song.features:
                if song.is_connected[feature]:
                    playlist = Playlist(song.track_id)
                    self._neighbours[feature].add_neighbour(playlist)

        return similarity_score

    def generating_graph(self) -> None:
        """Generates a graph presented as a static HTML file.
        """
        features = {'danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                    'valence', 'tempo', 'duration_ms', 'time_signature'}
        graph = Network(
            notebook=True,
            cdn_resources='remote',
            height='750px',
            width='100%',
            select_menu=True,
            filter_menu=True,
        )
        graph.add_node(self._song.features['track_name'])

        for feature in features:
            graph.add_node(feature, size=len(self._neighbours[feature]._neighbours), title=feature)
            graph.add_edge(self._song.features['track_name'], feature)

            for neighbour in self._neighbours[feature]._neighbours:
                track_feature = get_tracks_features([neighbour])
                track_name = track_feature[0]['track_name']
                graph.add_node(track_name)
                graph.add_edge(feature, track_name)

        graph.show('graph.html')


if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
