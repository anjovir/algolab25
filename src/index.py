import mido
from music21 import *
from entities.trie import Trie
from entities.pygame_midi_player import MidiPlayer


if __name__ == "__main__":
    trie = Trie()
    midi_file = mido.MidiFile('src\data\Super Mario Bross (Theme Song) - melody.mid')
    all_notes = []
    mc_order = 10

    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_value = msg.note
                all_notes.append(note_value)
    
    trie.insert(all_notes, mc_order)

    sequence = trie.generate_random_sequence_from_data(2)
    print(sequence)
    
    song = trie.generate_song(sequence, 20)
    print(song)
    
    midi_player = MidiPlayer()
    # Play the song in tempo 60 and note lenght 1/4
    midi_player.play_notes(song, 0.25)

