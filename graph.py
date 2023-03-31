"""Graphs yay"""
from __future__ import annotations

from typing import Any

import networkx as nx
import matplotlib.pyplot as plt
from spotipy_to_csv import similarity_score1, get_songs_from_playlists, get_single_track_features, song_features
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

    # def draw_graph(self, playlist_id: list[str]) -> None:
    #     """Description"""
    #     graph = self.generate_graph(playlist_id, set())
    #     subax1 = plt.subplot(221)
    #     nx.draw(graph, with_labels=True, font_weight='bold')
    #
    #     plt.show()


# def generate_graph(song: str, playlist_id: list[str], visited: set) -> nx:
#     """function to generate a graph"""
#     G = nx.Graph()
#     songs = get_single_track_features(song)
#     G.add_node(songs['track_name'])
#
#     playlist_features = song_features((playlist_id))
#
#     visited.add(songs['track_name'])
#
#     for song in playlist_features:
#         visited.add(song['track_name'])
#         similarity_scores = similarity_score1(song['track_id'], playlist_id)
#         for score in similarity_scores:
#             if similarity_scores[score] >= 85 and score not in visited:
#                 G.add_node(score)
#                 G.add_edge(song['track_name'], score)
#     return G
#
#
# def draw_graph(song: str, playlist_id: list[str]) -> None:
#     """Description"""
#     graph = generate_graph(song, playlist_id, set())
#     # subax1 = plt.subplot(221)
#     nx.draw(graph, with_labels=True, font_weight='bold')
#
#     plt.show()
