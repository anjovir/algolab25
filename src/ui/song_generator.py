import tkinter as tk
from tkinter import font, ttk, constants, filedialog, messagebox
from services.midi_player import MidiSongPlayer
from services.trie_service import TrieService
from services.midi_service import MidiService


class SongGenerator:
    def __init__(self, root):
        self._root = root
        self._player = MidiSongPlayer(None)
        self._trie_service = TrieService()
        self._midi_service = MidiService()
        self._file_path = None
        self.option_var = tk.IntVar()
        self.first_bar_length = 1920

        self._frame1 = None
        self._frame2 = None
        self._frame3 = None
        self._frame4 = None
        self._frame5 = None

        self._font = font.Font(family='Helvetica', size=12, weight="bold")
        self._initialize()
        self._root.protocol("WM_DELETE_WINDOW", self.window_exit)

    def pack(self):
        self._frame1.pack(fill=constants.X)
        self._frame4.pack(fill=constants.X)
        self._frame2.pack(fill=constants.X)
        self._frame5.pack(fill=constants.X)
        self._frame3.pack(fill=constants.X)

    def destroy(self):
        self._frame1.destroy()
        self._frame2.destroy()
        self._frame3.destroy()
        self._frame4.destroy()
        self._frame5.destroy()

    def _initialize_header(self):
        title = ttk.Label(master=self._frame1, text="Markov chain music generator",
                          font=self._font, padding=5)
        title.grid(row=0, column=0, columnspan=2)

        self.open_file_button = tk.Button(
            master=self._frame1, text="Open midi file", command=self._open_midi_file)
        self.open_file_button.grid(row=1, column=0, padx=5, pady=5)

        self.open_directory_button = tk.Button(
            master=self._frame1, text="Open directory", command=self._process_directory_midi_files)
        self.open_directory_button.grid(row=1, column=1, padx=5, pady=5)

        self.read_to_trie_button = tk.Button(
            master=self._frame1, text="Read file", command=self.read_file_to_trie)
        self.read_to_trie_button.grid(row=1, column=2, padx=5, pady=5)
        

        self.reset_trie_button = tk.Button(
            master=self._frame1, text="Reset trie", command=self.reset_trie)
        self.reset_trie_button.grid(row=1, column=3, padx=5, pady=5)

        self.generator_option1_button = tk.Radiobutton(master=self._frame1,
                                                       text="Notes and rhythm considered as an unit",
                                                       variable=self.option_var,
                                                       value=1
                                                       )

        self.generator_option1_button.grid(row=2, column=0, padx=0, pady=2)

        self.generator_option2_button = tk.Radiobutton(master=self._frame1,
                                                       text="Notes and rhythm generated separately",
                                                       variable=self.option_var,
                                                       value=2
                                                       )

        self.generator_option2_button.grid(row=2, column=2, padx=0, pady=2)

    def _initialize_footer(self):
        self.status = tk.Label(master=self._frame3, text="",
                               bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _initialize_main_parameters(self):
        self.trie_slider_label = tk.Label(master=self._frame2,
                                          text="Choose markovian chain order used when loading the data to trie",
                                          wraplength="100")
        self.trie_slider_label.grid(row=1, column=0)

        self.mc_order_trie_slider = tk.Scale(
            master=self._frame2,
            from_=1, to=20,
            orient=tk.HORIZONTAL,
            label="Order (trie)",
            command=lambda x: self.update_max_value()
        )
        self.mc_order_trie_slider.set(10)
        self.mc_order_trie_slider.grid(row=1, column=1)

        self.mc_order_label = tk.Label(master=self._frame2,
                                       text="Choose markovian chain order used in generating the song",
                                       wraplength="100")
        self.mc_order_label.grid(row=2, column=0)

        self.mc_order_song_slider = tk.Scale(master=self._frame2, from_=1, to=self.mc_order_trie_slider.get(
        )-1, orient=tk.HORIZONTAL, label="Order (song)")
        self.mc_order_song_slider.set(9)
        self.mc_order_song_slider.grid(row=2, column=1)

        self.set_tempo_slider = tk.Scale(
            master=self._frame2, from_=1, to=250, orient=tk.HORIZONTAL, label="Set tempo")
        self.set_tempo_slider.set(120)
        self.set_tempo_slider.grid(row=3, column=0)

        self.choose_song_lenght_slider = tk.Scale(
            master=self._frame2, from_=1, to=50, orient=tk.HORIZONTAL, label="Song length")
        self.choose_song_lenght_slider.set(10)
        self.choose_song_lenght_slider.grid(row=3, column=1)

        self.starting_sequence_button = tk.Button(
            master=self._frame2, text="Generate starting sequence", command=self.generate_and_print_starting_sequence)
        self.starting_sequence_button.grid(row=4, column=0, padx=5, pady=5)

        self.generate_song_button = tk.Button(
            master=self._frame2, text="Generate song notes", command=self.generate_and_print_song_notes)
        self.generate_song_button.grid(row=4, column=1, padx=5, pady=5)

        self.play_button = tk.Button(
            master=self._frame2, text="Play", command=self.play)
        self.play_button.grid(row=5, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(
            master=self._frame2, text="Stop", command=self._player.stop_playing)
        self.stop_button.grid(row=5, column=1, padx=5, pady=5)

    def _initialize_print_window(self):
        self.starting_seq = tk.Label(master=self._frame5, text="")
        self.starting_seq.grid(row=0, column=0)

        self.song_notes = tk.Label(master=self._frame5, text="")
        self.song_notes.grid(row=1, column=0)

    def reset_trie(self):
        self._trie_service = TrieService()
        self.play_button.config(command=self._player.start_playing)
        self.stop_button.config(command=self._player.stop_playing)
        self.read_to_trie_button.config(command=self.read_file_to_trie)
        self.starting_sequence_button.config(
            command=self.generate_and_print_starting_sequence)
        self.generate_song_button.config(
            command=self.generate_and_print_song_notes)
        self.status.config(text="Trie reset")
        self.starting_seq.config(text="")
        self.song_notes.config(text="")

    def play(self):
        self._player.start_playing()

    def update_max_value(self):
        value = self.mc_order_trie_slider.get()
        self.mc_order_song_slider.config(to=(value - 1))

    def generate_and_print_starting_sequence(self):
        self.generate_starting_sequence()
        self.print_starting_sequence()

    def generate_starting_sequence(self):
        self._starting_sequence = self._trie_service.generate_random_sequence_from_data(
            self.mc_order_song_slider.get(), self.option_var.get())
        if self.option_var.get() == 2:
            self.first_bar_length = self._starting_sequence[2]

    def print_starting_sequence(self):
        if self.option_var.get() == 2:
            notes = f"NOTES: {self._starting_sequence[0]}"
            rhythm = f"RHYTHM: {self._starting_sequence[1]}"
            sequence = f"STARTING SEQUENCE\n{notes}\n{rhythm}"
        else:
            sequence = f"STARTING SEQUENCE\n{self._starting_sequence}"

        self.starting_seq.config(text=str(sequence), wraplength=500)

    def generate_and_print_song_notes(self):
        self.generate_song_notes()
        self.print_song_notes()

    def generate_song_notes(self):
        self._song_score = self._trie_service.generate_score(
            self._starting_sequence, self.choose_song_lenght_slider.get(), self.option_var.get())
        self._midi_service.save_generated_song(
            self._song_score, tempo=self.set_tempo_slider.get(), first_bar_lenght=self.first_bar_length)

    def print_song_notes(self):
        sequence = f"FULL SCORE:\n{str(self._song_score)}"
        self.song_notes.config(text=sequence, wraplength=700)

    def read_file_to_trie(self):
        success = self._trie_service._read_file(
            self._file_path, self.mc_order_trie_slider.get())
        if success:
            self.status.config(
                text="File loaded successfully to trie")
        else:
            self.status.config(text="Loading failed")

    def _open_midi_file(self):
        file = filedialog.askopenfilename(filetypes=[("Midi files", "*.mid")])
        if file:
            self._player = MidiSongPlayer(file)
            self._file_path = file

            self.play_button.config(command=self._player.start_playing)
            self.stop_button.config(command=self._player.stop_playing)
            self.read_to_trie_button.config(command=self.read_file_to_trie)
            self.starting_sequence_button.config(
                command=self.generate_and_print_starting_sequence)
            self.generate_song_button.config(
                command=self.generate_and_print_song_notes)
    
    def _process_directory_midi_files(self):
        directory = filedialog.askdirectory(title="Choose a directory which midi-files you want to load")
        if directory:
            success = self._trie_service.process_midi_files(directory, self.mc_order_trie_slider.get())
            print(success)
            if success:
                self.status.config(
                    text="File loaded successfully to trie")
            else:
                self.status.config(text="Loading failed")
        
    def window_exit(self):
        close = messagebox.askyesno("Exit?", "Are you sure you want to exit?")
        if close:
            self._player.stop_playing()
            self._root.destroy()

    def _initialize(self):
        self._frame1 = tk.Frame(master=self._root)
        self._frame2 = tk.Frame(master=self._root, bd=2, relief="sunken")
        self._frame3 = tk.Frame(master=self._root)
        self._frame4 = tk.Frame(master=self._root, bd=2, relief="ridge")
        self._frame5 = tk.Frame(master=self._root, bd=2, relief="solid")

        self._initialize_header()
        self._initialize_main_parameters()
        self._initialize_footer()
        self._initialize_print_window()
