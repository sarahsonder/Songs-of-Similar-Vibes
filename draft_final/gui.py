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
import tkinter as tk
from tkinter import ttk, messagebox
from handle_csv import filter_csv, find_song, most_similar_songs
from graph import Playlist


def create_gui(csv_file: str) -> None:
    """Creates the visualization"""
    root = tk.Tk()
    root.title('Songs of Similar Vibes')
    root.geometry('900x600')

    background_img = tk.PhotoImage(file='background_pic.png')
    background_label = tk.Label(root, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    all_tracks = filter_csv(csv_file)

    def search() -> None:
        """Hello"""
        user_entry = track_entry.get()
        no_space = user_entry.replace(' ', '')
        no_comma = no_space.replace(',', '')
        lowercase = no_comma.lower()
        track_input = find_song(all_tracks, lowercase)

        if track_input is not None:
            messagebox.showinfo(title='Yay!', message='Song found! (✿◠‿◠)')
        else:
            messagebox.showwarning(title='Error', message='Song not found (╯°□°)╯︵ ┻━┻')

    def convert_preferences() -> list[float]:
        """Blop"""
        converted_preferences = []
        preferences = [dance_cb.get(), speech_cb.get(), energy_cb.get(), acoustic_cb.get(), instru_cb.get(),
                       valence_cb.get(), loud_cb.get(), tempo_cb.get(), mode_cb.get(), duration_cb.get(),
                       timesig_cb.get()]

        for i in range(0, len(preferences)):
            if preferences[i] == '' or preferences[i] == '5':
                converted_preferences.append(0.2)
            else:
                float_val = float(preferences[i])
                converted_value = (2 * (1.38 ** (float_val - 5))) / 10
                converted_preferences.append(converted_value)

        return converted_preferences

    def tab2() -> None:
        """Hola"""
        user_entry = track_entry.get()
        no_space = user_entry.replace(' ', '')
        no_comma = no_space.replace(',', '')
        lowercase = no_comma.lower()
        track_input = find_song(all_tracks, lowercase)

        if track_input is None:
            messagebox.showwarning(title='Error', message='Please insert a valid song (╯°□°)╯︵ ┻━┻')
        else:
            official_preferences = convert_preferences()
            chosen_tracks = most_similar_songs(all_tracks, track_input, official_preferences)

            #####################################################################
            upper_frame.destroy()
            mid_frame.destroy()
            bottom_frame.destroy()

            def run_analysis() -> None:
                """Adios"""
                features = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
                            'instrumentalness',
                            'valence', 'tempo', 'duration_ms', 'time_signature']
                lst = []

                for feature in features:
                    lst.append(Playlist(feature))

                songlst = []
                for track_concat in all_tracks:
                    songlst.append(all_tracks[track_concat][0])

                target_track = 'spotify:track:' + track_input.track_id
                p = Playlist(target_track, lst)
                p.generate_playlist(songlst, official_preferences)
                p.generating_graph()

            def end() -> None:
                """Nihao"""
                root.destroy()

            tab2_frame = tk.Frame(root, bg='#306844', bd=5)
            tab2_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

            results = tk.Text(tab2_frame, font=('Calibri', 13))
            results.tag_configure('tag_name', justify='center')
            results.configure(state='normal')

            if not chosen_tracks:
                results.insert(tk.INSERT, 'No similar songs')
                results.pack()
            else:
                for track_id in chosen_tracks:
                    results.insert(tk.INSERT, chosen_tracks[track_id] + '\n\n')
                    results.pack()

            results.tag_add('tag_name', '1.0', 'end')
            results.configure(state='disabled')

            analysis_frame = tk.Frame(root, bg='#306844', bd=5)
            analysis_frame.place(relx=0.2, rely=0.85, relwidth=0.2, relheight=0.08)
            analysis_button = tk.Button(analysis_frame, text='See Analysis', font=('Calibri', 17, 'bold'),
                                        command=run_analysis)
            analysis_button.place(relwidth=1, relheight=1)

            finish_frame = tk.Frame(root, bg='#306844', bd=5)
            finish_frame.place(relx=0.6, rely=0.85, relwidth=0.2, relheight=0.08)
            finish_button = tk.Button(finish_frame, text='Finish', font=('Calibri', 17, 'bold'), command=end)
            finish_button.place(relwidth=1, relheight=1)

    # UPPER FRAME
    upper_frame = tk.Frame(root, bg='#306844', bd=5)
    upper_frame.place(relx=0.1, rely=0.07, relwidth=0.8, relheight=0.15)

    instructions1 = tk.Text(upper_frame, wrap=tk.WORD, font=('Calibri', 12))
    instructions1.configure(state='normal')
    instructions1.insert(tk.INSERT, 'Enter the song as: song name, artist name')
    instructions1.configure(state='disabled')
    instructions1.place(relwidth=1, relheight=0.28)

    track_entry = tk.Entry(upper_frame, font=('Calibri', 17))
    track_entry.place(rely=0.37, relwidth=0.65, relheight=0.6)

    find_song_button = tk.Button(upper_frame, text='Find Song', font=('Calibri', 17, 'bold'), command=search)
    find_song_button.place(relx=0.7, rely=0.37, relwidth=0.3, relheight=0.6)

    # MIDDLE FRAME
    mid_frame = tk.Frame(root, bg='#306844', bd=5)
    mid_frame.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.55)

    instructions2 = tk.Text(mid_frame, wrap=tk.WORD, font=('Calibri', 12))
    instructions2.configure(state='normal')
    instructions2.insert(tk.INSERT,
                         ' Customization: on a scale of 0 - 10, rank the importance of a feature when generating '
                         'recommendations.' + '\n' + ' You may leave any or all fields blank, '
                                                     'in which the default value will be used.' + '\n\n' +
                         ' 0-4: less important, 5: default value, 6-10: more important.')
    instructions2.configure(state='disabled')
    instructions2.place(relwidth=1, relheight=0.275)

    # COMBOBOXES
    values = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    dance_lbl = tk.Label(mid_frame, text='Danceability')
    dance_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    dance_lbl.place(relx=0.095, rely=0.32, relwidth=0.12, relheight=0.08)
    dance_cb.place(relx=0.08, rely=0.401, relwidth=0.15, relheight=0.08)

    speech_lbl = tk.Label(mid_frame, text='Speechiness')
    speech_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    speech_lbl.place(relx=0.325, rely=0.32, relwidth=0.12, relheight=0.08)
    speech_cb.place(relx=0.31, rely=0.401, relwidth=0.15, relheight=0.08)

    energy_lbl = tk.Label(mid_frame, text='Energy')
    energy_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    energy_lbl.place(relx=0.555, rely=0.32, relwidth=0.12, relheight=0.08)
    energy_cb.place(relx=0.54, rely=0.401, relwidth=0.15, relheight=0.08)

    acoustic_lbl = tk.Label(mid_frame, text='Acousticness')
    acoustic_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    acoustic_lbl.place(relx=0.77, rely=0.32, relwidth=0.15, relheight=0.08)
    acoustic_cb.place(relx=0.77, rely=0.401, relwidth=0.15, relheight=0.08)

    instru_lbl = tk.Label(mid_frame, text='Instrumentalness')
    instru_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    instru_lbl.place(relx=0.08, rely=0.57, relwidth=0.15, relheight=0.08)
    instru_cb.place(relx=0.08, rely=0.65, relwidth=0.15, relheight=0.08)

    valence_lbl = tk.Label(mid_frame, text='Valence')
    valence_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    valence_lbl.place(relx=0.325, rely=0.57, relwidth=0.12, relheight=0.08)
    valence_cb.place(relx=0.31, rely=0.65, relwidth=0.15, relheight=0.08)

    loud_lbl = tk.Label(mid_frame, text='Loudness')
    loud_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    loud_lbl.place(relx=0.54, rely=0.57, relwidth=0.15, relheight=0.08)
    loud_cb.place(relx=0.54, rely=0.65, relwidth=0.15, relheight=0.08)

    tempo_lbl = tk.Label(mid_frame, text='Tempo')
    tempo_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    tempo_lbl.place(relx=0.785, rely=0.57, relwidth=0.12, relheight=0.08)
    tempo_cb.place(relx=0.77, rely=0.65, relwidth=0.15, relheight=0.08)

    mode_lbl = tk.Label(mid_frame, text='Mode (major/minor)')
    mode_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    mode_lbl.place(relx=0.185, rely=0.82, relwidth=0.17, relheight=0.08)
    mode_cb.place(relx=0.195, rely=0.901, relwidth=0.15, relheight=0.08)

    duration_lbl = tk.Label(mid_frame, text='Duration')
    duration_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    duration_lbl.place(relx=0.435, rely=0.82, relwidth=0.12, relheight=0.08)
    duration_cb.place(relx=0.42, rely=0.901, relwidth=0.15, relheight=0.08)

    timesig_lbl = tk.Label(mid_frame, text='Time Signature')
    timesig_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    timesig_lbl.place(relx=0.67, rely=0.82, relwidth=0.12, relheight=0.08)
    timesig_cb.place(relx=0.655, rely=0.901, relwidth=0.15, relheight=0.08)

    # BOTTOM FRAME
    bottom_frame = tk.Frame(root, bg='#306844', bd=5)
    bottom_frame.place(relx=0.34375, rely=0.85, relwidth=0.3125, relheight=0.08)

    button = tk.Button(bottom_frame, text='Generate!', font=('Calibri', 17, 'bold'), command=tab2)
    button.place(relwidth=1, relheight=1)

    root.mainloop()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'allowed-io': ['write_csv'],
        'extra-imports': ['__future__', 'tkinter', 'handle_csv', 'graph']
    })
