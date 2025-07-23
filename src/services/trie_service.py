import mido
from entities.trie import Trie, TrieNode
import random
import os

midi_song_number = 1

class TrieService:
    def __init__(self, order=10):
        self.root = TrieNode()
        self.trie = Trie(self.root)
        self._mc_order = order
        self._trie_read_succesfully = False    
    
    def _read_file(self, file_path, mc_order):
        all_notes = []
        midi_file = mido.MidiFile(file_path)
        for track in midi_file.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    note_value = msg.note
                    all_notes.append(note_value)

        self._trie_read_succesfully = self._insert_to_trie(all_notes, mc_order)
    
    def _insert_to_trie(self, notes, mc_order):
        self.trie.insert(notes, mc_order)
        for node in self.root.children:
            if isinstance(node[0], TrieNode):
                return True
        return False
    
    def generate_random_sequence_from_data(self, order=3):
        seqs = self.trie._get_unique_sequences(order)
        return seqs[random.randint(0, (len(seqs) - 1))]
    
    def get_next_note(self, sequence):
        curr_node = self.root
        for note in sequence:            
            if curr_node.children[note][0] is None:
                return False
            
            curr_node = curr_node.children[note][0]

        notes = []
        for i in range(128):
            if curr_node.children[i][1] > 0:
                for j in range(curr_node.children[i][1]):
                    notes.append(i)           
                
        if len(notes) < 1:
            return False
        next_note = notes[random.randint(0,len(notes)-1)]
        return next_note
    
    def generate_song(self, sequence, length):
        markov_chain_song = []
        markov_chain_song.extend(sequence)
        for i in range(length):
            generated_note = self.trie.get_next_note(sequence)
            markov_chain_song.append(generated_note)
            sequence.pop(0)
            sequence.append(generated_note)

        return markov_chain_song
    
    def save_generated_song(self, notes, tempo):
        # Create new file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        ticks_per_beat = 240

        # Add tempo message
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

        for note in notes:
            track.append(mido.Message('note_on', note=note, velocity=64, time=0))  # Note start
            track.append(mido.Message('note_off', note=note, velocity=64, time=ticks_per_beat))  # Note end

        global midi_song_number
        fp = f"src/data/midi_song{midi_song_number}.mid"
        midi_song_number += 1

        midi_file.save(fp)