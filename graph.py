"""Graphs yay"""
from __future__ import annotations

from typing import Any

import networkx as nx
from pyvis.network import Network


from spotify_to_csv import get_songs_from_playlists, get_tracks_features
from track import Track, SIMILARITY_VALUE

FEATURES = {'danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence',
            'tempo', 'duration', 'time_signature'}


class Playlist:
    """Description"""
    _song: str | Track
    _neighbours: dict[str, Playlist]

    def __init__(self, song: str, is_target: bool = False) -> None:
        """Description"""
        self._neighbours = {}
        if song in FEATURES:
            self._song = song
        else:
            self._song = Track(song)
        if is_target:
            for feature in FEATURES:
                feature_playlist = Playlist(feature)
                self._neighbours[feature] = feature_playlist
                feature_playlist._neighbours[song] = self
        else:
            self._neighbours = {}

    def add_neighbour(self, song: Track) -> None:
        """Connects a new neighbour to a feature node."""
        new_playlist = Playlist(song.track_id)
        self._neighbours[song.track_id] = new_playlist
        new_playlist._neighbours[self._song] = self

    def generate_playlist(self, songs: list[str], user_preferences: list[float]) -> dict[str, float]:
        """Updates the playlist graph to reflect the similarity scores of the songs."""
        songs_list = [Track(song) for song in songs]
        similarity_score = self._song.calc_similarity_score(songs_list, user_preferences)
        for song in songs_list:
            for feature in FEATURES:
                if song.is_connected[feature]:
                    self._neighbours[feature].add_neighbour(song)

        return similarity_score

    def generating_graph(self) -> None:
        """Generates a graph presented as a static HTML file."""
        graph = Network(
            notebook=True,
            cdn_resources='remote',
            height='750px',
            width='100%',
            select_menu=True,
            filter_menu=True,
        )
        graph.add_node(self._song.features['track_name'])

        for feature in FEATURES:
            graph.add_node(feature, size=len(self._neighbours[feature]._neighbours), title=feature)
            graph.add_edge(self._song.features['track_name'], feature)

            for neighbour in self._neighbours[feature]._neighbours:
                track_feature = get_tracks_features([neighbour])
                track_name = track_feature[0]['track_name']
                graph.add_node(track_name)
                graph.add_edge(feature, track_name)

        graph.show('graph.html')
