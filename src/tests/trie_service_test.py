import unittest
from entities.trie import Trie, TrieNode
from services.trie_service import TrieService
from services.midi_service import MidiService

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie_service = TrieService()
        self._file_path = "src/data/super_mario_play_test.mid"
        self.trie_service._read_file(self._file_path, 4)

    def test_constructor_root_node(self):
        self.assertIsInstance(self.trie_service.root, TrieNode)
    
    def test_constructor_trie(self):
        self.assertIsInstance(self.trie_service.trie, Trie)
    
    def test_constructor_midi_service(self):
        self.assertIsInstance(self.trie_service._midi_service, MidiService)

    def test_read_file(self):
        self.trie_service._trie_read_succesfully
        self.assertTrue(self.trie_service._trie_read_succesfully)
    
    def test_generate_random_sequence(self):
        seq = self.trie_service.generate_random_sequence_from_data(2)
        notes = [(76,120), (76,120), (200,120), (76,120),(200,120),(72,120),(76,120),(200,120),(79,120)]
        self.assertTrue(any(note in notes for note in seq))

    def test_generate_song(self):
        seq = self.trie_service.generate_random_sequence_from_data(1)
        song = self.trie_service.generate_song(seq, 10)
        notes = [(76,120), (76,120), (200,120), (76,120),(200,120),(72,120),(76,120),(200,120),(79,120)]
        self.assertTrue(note in notes for note in song)
    

        