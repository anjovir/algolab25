import os
import unittest
from entities.trie import Trie, TrieNode
from services.trie_service import TrieService
from services.midi_service import MidiService


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie_service = TrieService()
        self._file_path = "src/data/midi_test_data/super_mario_play_test.mid"
        self.order = 4
        self.file = self.trie_service._read_file(self._file_path, self.order)
        self._notes = [(76, 120), (76, 120), (200, 120), (76, 120),
                 (200, 120), (72, 120), (76, 120), (200, 120), (79, 120)]

    def test_constructor_root_node(self):
        self.assertIsInstance(self.trie_service.root, TrieNode)

    def test_constructor_trie(self):
        self.assertIsInstance(self.trie_service.trie, Trie)

    def test_constructor_midi_service(self):
        self.assertIsInstance(self.trie_service._midi_service, MidiService)

    def test_read_file(self):
        self.assertTrue(self.file)

    def test_generate_random_sequence1(self):
        seq = self.trie_service.generate_random_sequence_from_data(1)
        self.assertTrue(any(note in self._notes for note in seq))
    
    def test_generate_random_sequence2(self):
        seq = self.trie_service.generate_random_sequence_from_data(2)
        self.assertTrue(any(note in self._notes for note in seq))

    def test_generate_song(self):
        seq = self.trie_service.generate_random_sequence_from_data(1)
        song = self.trie_service.generate_song(seq, 10, 1)
        self.assertTrue(note in self._notes for note in song)
    
    def test_generate_score_notes1(self):
        file_path = "src\\data\\midi_test_data/Super Mario Bross (Theme Song) - melody.mid"
        self.trie_service._read_file(file_path, self.order)
        notes = self.trie_service.trie_notes.get_unique_sequences(1)        
        seq = self.trie_service.generate_random_sequence_from_data(1,1)
        length = 5
        option = 1
        song = self.trie_service.generate_score(seq, length, option)
        self.assertTrue(note in notes for note in song)

    def test_generate_score_notes2(self):
        file_path = "src\\data\\midi_test_data/Super Mario Bross (Theme Song) - melody.mid"
        self.trie_service._read_file(file_path, self.order)
        rhythms = self.trie_service.trie_rhythm.get_unique_sequences(1)
        seq = self.trie_service.generate_random_sequence_from_data(1,2)
        length = 5
        option = 2
        song = self.trie_service.generate_score(seq, length, option)
        self.assertTrue(rhythm in rhythms for rhythm in song)

    def test_process_midi_files(self):
        directory = "src/data/midi_test_data"
        result = self.trie_service.process_midi_files(directory, 3)
        self.assertTrue(result)
        



    
        

