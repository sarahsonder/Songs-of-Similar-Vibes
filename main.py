"""CSC111 Winter 2023 Project: Songs of Similar Vibez

This Python module is the main module of the song recommender program and will
create a playlist as well as generate a graph given a Spotify playlist, a
desired "target" song, and weighting preferences for attributes.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Vivian White, Sarah Wang, and Rebecca Kong.
"""

if __name__ == '__main__':
    custom_options = {'danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'valence', 'tempo', 'duration', 'time signature'}

    preferences = []

    song = input('Please input the name of your song: ')

    customize = input('Do you want to customize the weightings of the song attributes during comparison? ')

    if customize == 'yes':

        for option in custom_options:
            user_preference = int(input('Please list on a scale of 1 to 10 how important ' + option + ' is to you.'))
            preferences.append(2 * (1.38 ** (user_preference - 5)))

    # ...run functions whatever etc...

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
