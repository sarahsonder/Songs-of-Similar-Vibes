"""Interactive visualization"""

import tkinter as tk
from tkinter import ttk


def create_gui() -> None:
    """Creates the visualization"""
    root = tk.Tk()
    root.title('Songs of Similar Vibes')
    root.geometry('900x600')

    background_img = tk.PhotoImage(file='background_pic1.png')
    background_label = tk.Label(root, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    upper_frame(root)
    mid_frame = middle_frame(root)
    bottom_frame(root)
    combo_boxes(mid_frame)

    root.mainloop()


def upper_frame(root: tk) -> tk.Button:
    """Upper frame of the visualization"""
    frame = tk.Frame(root, bg='#306844', bd=5)
    frame.place(relx=0.1, rely=0.07, relwidth=0.8, relheight=0.15)

    instructions1 = tk.Text(frame, wrap=tk.WORD, font=('Calibri', 12))
    instructions1.configure(state='normal')
    instructions1.insert(tk.INSERT, 'Enter the song as: (song name, artist name)')
    instructions1.configure(state='disabled')
    instructions1.place(relwidth=1, relheight=0.28)

    entry = tk.Entry(frame, font=40)
    entry.place(rely=0.37, relwidth=0.65, relheight=0.6)

    find_song_button = tk.Button(frame, text='Find Song', font=('Calibri', 17, 'bold'), command=search)
    find_song_button.place(relx=0.7, rely=0.37, relwidth=0.3, relheight=0.6)

    return find_song_button


def middle_frame(root: tk) -> tk.Frame:
    """Middle Frame"""
    frame = tk.Frame(root, bg='#306844', bd=5)
    frame.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.55)

    instructions2 = tk.Text(frame, wrap=tk.WORD, font=('Calibri', 12))
    instructions2.configure(state='normal')
    instructions2.insert(tk.INSERT,
                         ' Customization: on a scale of 0 - 10, rank the importance of a feature when generating '
                         'recommendations.' + '\n' + ' You may leave any or all fields blank.' + '\n\n' +
                         ' 0-4: less important, 5: default value, 6-10: more important.')
    instructions2.configure(state='disabled')
    instructions2.place(relwidth=1, relheight=0.275)

    return frame


def bottom_frame(root: tk) -> None:
    """Bottom frame of the visualization"""
    # BOTTOM FRAME
    frame = tk.Frame(root, bg='#306844', bd=5)
    frame.place(relx=0.34375, rely=0.85, relwidth=0.3125, relheight=0.08)

    # GENERATE BUTTON
    button = tk.Button(frame, text='Generate!', font=('Calibri', 17, 'bold'))
    button.place(relwidth=1, relheight=1)


def combo_boxes(frame: tk.Frame) -> list[ttk.Combobox]:
    """Creates all combo boxes and stores them in a list"""
    all_combo_boxes = []
    values = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    # DANCEABILITY
    dance_lbl = tk.Label(frame, text='Danceability')
    dance_cb = ttk.Combobox(frame, values=values, state='readonly')
    dance_lbl.place(relx=0.095, rely=0.32, relwidth=0.12, relheight=0.08)
    dance_cb.place(relx=0.08, rely=0.401, relwidth=0.15, relheight=0.08)
    dance_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    # ENERGY
    energy_lbl = tk.Label(frame, text='Energy')
    energy_cb = ttk.Combobox(frame, values=values, state='readonly')
    energy_lbl.place(relx=0.325, rely=0.32, relwidth=0.12, relheight=0.08)
    energy_cb.place(relx=0.31, rely=0.401, relwidth=0.15, relheight=0.08)
    energy_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    # LOUDNESS
    loud_lbl = tk.Label(frame, text='Loudness')
    loud_cb = ttk.Combobox(frame, values=values, state='readonly')
    loud_lbl.place(relx=0.555, rely=0.32, relwidth=0.12, relheight=0.08)
    loud_cb.place(relx=0.54, rely=0.401, relwidth=0.15, relheight=0.08)
    loud_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    # MODE
    mode_lbl = tk.Label(frame, text='Mode (major/minor)')
    mode_cb = ttk.Combobox(frame, values=values, state='readonly')
    mode_lbl.place(relx=0.76, rely=0.32, relwidth=0.17, relheight=0.08)
    mode_cb.place(relx=0.77, rely=0.401, relwidth=0.15, relheight=0.08)
    mode_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    speech_lbl = tk.Label(frame, text='Speechiness')
    speech_cb = ttk.Combobox(frame, values=values, state='readonly')
    speech_lbl.place(relx=0.095, rely=0.57, relwidth=0.12, relheight=0.08)
    speech_cb.place(relx=0.08, rely=0.65, relwidth=0.15, relheight=0.08)
    speech_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    acoustic_lbl = tk.Label(frame, text='Acousticness')
    acoustic_cb = ttk.Combobox(frame, values=values, state='readonly')
    acoustic_lbl.place(relx=0.325, rely=0.57, relwidth=0.12, relheight=0.08)
    acoustic_cb.place(relx=0.31, rely=0.65, relwidth=0.15, relheight=0.08)
    acoustic_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    instru_lbl = tk.Label(frame, text='Instrumentalness')
    instru_cb = ttk.Combobox(frame, values=values, state='readonly')
    instru_lbl.place(relx=0.54, rely=0.57, relwidth=0.15, relheight=0.08)
    instru_cb.place(relx=0.54, rely=0.65, relwidth=0.15, relheight=0.08)
    instru_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    valence_lbl = tk.Label(frame, text='Valence')
    valence_cb = ttk.Combobox(frame, values=values, state='readonly')
    valence_lbl.place(relx=0.785, rely=0.57, relwidth=0.12, relheight=0.08)
    valence_cb.place(relx=0.77, rely=0.65, relwidth=0.15, relheight=0.08)
    valence_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    tempo_lbl = tk.Label(frame, text='Tempo')
    tempo_cb = ttk.Combobox(frame, values=values, state='readonly')
    tempo_lbl.place(relx=0.21, rely=0.82, relwidth=0.12, relheight=0.08)
    tempo_cb.place(relx=0.195, rely=0.901, relwidth=0.15, relheight=0.08)
    tempo_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    duration_lbl = tk.Label(frame, text='Duration')
    duration_cb = ttk.Combobox(frame, values=values, state='readonly')
    duration_lbl.place(relx=0.435, rely=0.82, relwidth=0.12, relheight=0.08)
    duration_cb.place(relx=0.42, rely=0.901, relwidth=0.15, relheight=0.08)
    duration_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())

    timesig_lbl = tk.Label(frame, text='Time Signature')
    timesig_cb = ttk.Combobox(frame, values=values, state='readonly')
    timesig_cb.bind("<<ComboboxSelected>>", lambda e: frame.focus())
    timesig_lbl.place(relx=0.67, rely=0.82, relwidth=0.12, relheight=0.08)
    timesig_cb.place(relx=0.655, rely=0.901, relwidth=0.15, relheight=0.08)

    return all_combo_boxes


if __name__ == '__main__':
    create_gui()
    import doctest

    doctest.testmod(verbose=True)
