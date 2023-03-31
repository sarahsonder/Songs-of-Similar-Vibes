def calc_similarity_score(target_id: str, other_track_ids: list[str]) -> dict[str, float]:
    """Returns the similarities of songs compared to a target track

    >>> playlst = ['spotify:playlist:3c3ORzOlXdL2pQPv7MtuS5']
    >>> songlst = get_songs_from_playlists(playlst)
    >>> scores = calc_similarity_score('spotify:track:1KxwZYyzWNyZSRyErj2ojT', songlst)
    >>> scores['Doppelgänger']
    71.03231566428813
    >>> scores['Better Days']
    69.30658341828067
    """
    target = get_tracks_features([target_id])[0]
    other_tracks = get_tracks_features(other_track_ids)
    similar_variables = ['danceability', 'speechiness', 'energy', 'acousticness', 'instrumentalness', 'valence']
    mode, duration, time_signature = 0.0, 0.0, 0.0

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
        all_song_similarities[song['track_name']] = (score_so_far/9) * 100

    return all_song_similarities
