import mido
from entities.trie import Trie, TrieNode
import random
from services.midi_service import MidiService

midi_song_number = 1

class TrieService:
    def __init__(self, order=10):
        self.root = TrieNode()
        self.root_rhythm = TrieNode()
        self.trie = Trie(self.root)
        self.trie_rhythm = Trie(self.root_rhythm)
        self._mc_order = order
        self._trie_read_succesfully = False
        self._midi_service = MidiService()
    
    def _read_file(self, file_path, mc_order):
        all_notes = self._midi_service._read_midi_file(file_path)
        self._trie_read_succesfully = self._insert_to_trie(all_notes, mc_order)
    
    def _insert_to_trie(self, notes, mc_order):
        self.trie.insert(notes, mc_order)
        for node in self.root.children.values():
            print(node)
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
        length = length - len(sequence)
        markov_chain_song = []
        [markov_chain_song.append(s) for s in sequence]
        while_counter = 0
        for i in range(length):
            generated_note = self.trie.get_next_note(sequence)
            while not generated_note: # Sometimes there is no next element (note) for the sequence, this is a workaround
                while_counter += 1
                sequence = self.generate_random_sequence_from_data(len(sequence))
                generated_note = self.trie.get_next_note(sequence)
                if while_counter > 100:
                    return False
            markov_chain_song.append(generated_note)
            sequence.pop(0)
            sequence.append(generated_note)

        return markov_chain_song