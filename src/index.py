import mido
from music21 import *
from entities.trie_node import Trie



if __name__ == "__main__":
    trie = Trie()
    midi_file = mido.MidiFile('src\data\Super Mario Bross (Theme Song) - melody.mid')
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_value = msg.note  # Nuotin arvo
                trie.insert(note_value)  # Lisää trie-rakenteeseen
    
    all_notes = trie.get_all_notes()
    print(all_notes)

