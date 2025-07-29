from entities.trie import Trie, TrieNode
import random
from services.midi_service import MidiService

class TrieService:
    def __init__(self, order=10):
        self.root = TrieNode()
        self.trie = Trie(self.root)
        self._mc_order = order
        self._trie_read_succesfully = False
        self._midi_service = MidiService()

    def _read_file(self, file_path, mc_order):
        all_notes = self._midi_service._read_midi_file(file_path)
        self._trie_read_succesfully = self._insert_to_trie(all_notes, mc_order)

    def _insert_to_trie(self, notes, mc_order):
        self.trie.insert(notes, mc_order)
        for node in self.root.children.values():
            if isinstance(node[0], TrieNode):
                return True
        return False

    def generate_random_sequence_from_data(self, order=3):
        seqs = self.trie._get_unique_sequences(order)
        return seqs[random.randint(0, (len(seqs) - 1))]

    def generate_song(self, sequence, length):
        length = length - len(sequence)
        markov_chain_song = []
        [markov_chain_song.append(s) for s in sequence]
        while_counter = 0
        for i in range(length):
            generated_note = self.trie.get_next_note(sequence)
            # Sometimes there is no next element (note) for the sequence, this is a workaround
            while not generated_note:
                while_counter += 1
                sequence = self.generate_random_sequence_from_data(
                    len(sequence))
                generated_note = self.trie.get_next_note(sequence)
                if while_counter > 100:
                    return False
            markov_chain_song.append(generated_note)
            sequence.pop(0)
            sequence.append(generated_note)

        return markov_chain_song
