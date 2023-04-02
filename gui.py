"""Interactive visualization"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from track import Track
from typing import Optional
import csv


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
    if song in song_dict:
        return Track(song_dict[song])
    else:
        return None


def most_similar_songs(song_file: str, song: str, user_preferences: list[float]) -> list[str]:
    """Returns a list of the top 10 most similar songs from a csv file.
    Preconditions:
        - song_file refers to a valid csv file
        - song != ''
        - len(user_preferences) == 11
    """
    song_dict = filter_csv(song_file)
    target = find_song(song_dict, song)
    track_lst = []
    returned_lst = []
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
                artist = {track_song_and_artist[track] for track in track_song_and_artist if song[0] == track}
                returned_lst.append(song[0] + ' by ' + artist.pop())

    return returned_lst


def create_gui(csv_file: str) -> None:
    """Creates the visualization"""
    root = tk.Tk()
    root.title('Songs of Similar Vibes')
    root.geometry('900x600')

    background_img = tk.PhotoImage(file='background_pic1.png')
    background_label = tk.Label(root, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def cleaned_song() -> Optional[str]:
        """Konichiwa"""
        track_name = track_entry.get()
        one = track_name.replace(',', '')
        two = one.replace(' ', '')
        three = two.lower()
        return find_single_song('small_dataset.csv', three)

    def search() -> None:
        """Hello"""
        track = cleaned_song()

        if track is not None:
            messagebox.showinfo(title='Yay!', message='Song found! (✿◠‿◠)')
        else:
            messagebox.showwarning(title='Error', message='Song not found (╯°□°)╯︵ ┻━┻')

    def tab2():
        """Hola"""
        track = cleaned_song()

        if track is None:
            messagebox.showwarning(title='Error', message='Please insert a valid song (╯°□°)╯︵ ┻━┻')
        else:
            preferences = [dance_cb.get(), speech_cb.get(), energy_cb.get(), acoustic_cb.get(), instru_cb.get(),
                           valence_cb.get(), loud_cb.get(), tempo_cb.get(), mode_cb.get(), duration_cb.get(),
                           timesig_cb.get()]

            converted_preferences = []

            for i in range(0, len(preferences)):

                if preferences[i] == '' or preferences[i] == '5':
                    converted_preferences.append(0.2)
                else:
                    float_val = float(preferences[i])
                    converted_value = (2 * (1.38 ** (float_val - 5))) / 10
                    converted_preferences.append(converted_value)

            chosen_tracks = most_similar_songs(csv_file, track, converted_preferences)
            print(preferences)
            print(converted_preferences)

            #####################################################################

            upper_frame.destroy()
            mid_frame.destroy()
            bottom_frame.destroy()

            def end() -> None:
                """Nihao"""
                root.destroy()

            # MIDDLE FRAME
            tab2_frame = tk.Frame(root, bg='#306844', bd=5)
            tab2_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

            results = tk.Text(tab2_frame, font=('Calibri', 13))
            results.tag_configure('tag_name', justify='center')
            results.configure(state='normal')

            for chosen_track in chosen_tracks:
                results.insert(tk.INSERT, chosen_track + '\n\n')
                results.pack()

            results.tag_add('tag_name', '1.0', 'end')
            results.configure(state='disabled')

            # FINISH FRAME
            finish_frame = tk.Frame(root, bg='#306844', bd=5)
            finish_frame.place(relx=0.34375, rely=0.85, relwidth=0.3125, relheight=0.08)
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

    track_entry = tk.Entry(upper_frame, font=40)
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
                         'recommendations.' + '\n' + ' You may leave any or all fields blank.' + '\n\n' +
                         ' 0-4: less important, 5: default value, 6-10: more important.')
    instructions2.configure(state='disabled')
    instructions2.place(relwidth=1, relheight=0.275)

    # COMBOBOXES
    values = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    # DANCEABILITY
    dance_lbl = tk.Label(mid_frame, text='Danceability')
    dance_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    dance_lbl.place(relx=0.095, rely=0.32, relwidth=0.12, relheight=0.08)
    dance_cb.place(relx=0.08, rely=0.401, relwidth=0.15, relheight=0.08)
    dance_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    # ENERGY
    energy_lbl = tk.Label(mid_frame, text='Energy')
    energy_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    energy_lbl.place(relx=0.325, rely=0.32, relwidth=0.12, relheight=0.08)
    energy_cb.place(relx=0.31, rely=0.401, relwidth=0.15, relheight=0.08)
    energy_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    # LOUDNESS
    loud_lbl = tk.Label(mid_frame, text='Loudness')
    loud_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    loud_lbl.place(relx=0.555, rely=0.32, relwidth=0.12, relheight=0.08)
    loud_cb.place(relx=0.54, rely=0.401, relwidth=0.15, relheight=0.08)
    loud_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    # MODE
    mode_lbl = tk.Label(mid_frame, text='Mode (major/minor)')
    mode_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    mode_lbl.place(relx=0.76, rely=0.32, relwidth=0.17, relheight=0.08)
    mode_cb.place(relx=0.77, rely=0.401, relwidth=0.15, relheight=0.08)
    mode_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    speech_lbl = tk.Label(mid_frame, text='Speechiness')
    speech_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    speech_lbl.place(relx=0.095, rely=0.57, relwidth=0.12, relheight=0.08)
    speech_cb.place(relx=0.08, rely=0.65, relwidth=0.15, relheight=0.08)
    speech_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    acoustic_lbl = tk.Label(mid_frame, text='Acousticness')
    acoustic_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    acoustic_lbl.place(relx=0.325, rely=0.57, relwidth=0.12, relheight=0.08)
    acoustic_cb.place(relx=0.31, rely=0.65, relwidth=0.15, relheight=0.08)
    acoustic_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    instru_lbl = tk.Label(mid_frame, text='Instrumentalness')
    instru_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    instru_lbl.place(relx=0.54, rely=0.57, relwidth=0.15, relheight=0.08)
    instru_cb.place(relx=0.54, rely=0.65, relwidth=0.15, relheight=0.08)
    instru_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    valence_lbl = tk.Label(mid_frame, text='Valence')
    valence_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    valence_lbl.place(relx=0.785, rely=0.57, relwidth=0.12, relheight=0.08)
    valence_cb.place(relx=0.77, rely=0.65, relwidth=0.15, relheight=0.08)
    valence_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    tempo_lbl = tk.Label(mid_frame, text='Tempo')
    tempo_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    tempo_lbl.place(relx=0.21, rely=0.82, relwidth=0.12, relheight=0.08)
    tempo_cb.place(relx=0.195, rely=0.901, relwidth=0.15, relheight=0.08)
    tempo_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    duration_lbl = tk.Label(mid_frame, text='Duration')
    duration_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    duration_lbl.place(relx=0.435, rely=0.82, relwidth=0.12, relheight=0.08)
    duration_cb.place(relx=0.42, rely=0.901, relwidth=0.15, relheight=0.08)
    duration_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())

    timesig_lbl = tk.Label(mid_frame, text='Time Signature')
    timesig_cb = ttk.Combobox(mid_frame, values=values, state='readonly')
    timesig_cb.bind("<<ComboboxSelected>>", lambda e: mid_frame.focus())
    timesig_lbl.place(relx=0.67, rely=0.82, relwidth=0.12, relheight=0.08)
    timesig_cb.place(relx=0.655, rely=0.901, relwidth=0.15, relheight=0.08)

    # BOTTOM FRAME
    bottom_frame = tk.Frame(root, bg='#306844', bd=5)
    bottom_frame.place(relx=0.34375, rely=0.85, relwidth=0.3125, relheight=0.08)

    button = tk.Button(bottom_frame, text='Generate!', font=('Calibri', 17, 'bold'), command=tab2)
    button.place(relwidth=1, relheight=1)

    root.mainloop()


if __name__ == '__main__':
    create_gui('small_dataset.csv')
