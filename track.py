"""Hi"""
from typing import Any
from spotify_to_csv import get_songs_from_playlists, get_tracks_features


class Track:
    """Track/song class

    Instance Attributes:
        - track_id: Spotify URI
        - features: danceability, energy, loudness, mode, speechiness, acousticness, instrumentalness, valence, tempo,
                    duration, time signature, track_name, track_artist, track_id
    """
    track_id: str
    features: dict[str, Any]

    def __init__(self, track_id: str) -> None:
        """Initialize the Track object with its track_id and track features"""
        self.track_id = track_id
        self.features = get_tracks_features([track_id])[0]

    def calc_similarity_score(self, other_tracklst: list[Track]) -> dict[str, float]:
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
        target = get_tracks_features([self.track_id])[0]
        similar_variables = ['danceability', 'speechiness', 'energy', 'acousticness', 'instrumentalness', 'valence']
        mode, duration, time_signature = 0.0, 0.0, 0.0

        other_tracks = []

        for track in other_tracklst:
            other_tracks.append(track.track_id)

        all_song_similarities = {}

        for song in other_tracks:
            score_so_far = 0
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
            all_song_similarities[song['track_name']] = (score_so_far / 9) * 100

        return all_song_similarities


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
