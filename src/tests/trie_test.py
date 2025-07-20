import unittest
from entities.trie import Trie, TrieNode

class TestTrie(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")
    
    def test_constructor_works1(self):
        test_trie = TrieNode()
        self.assertIsNotNone(test_trie.children[0])
    
    def test_constructor_works2(self):
        test_trie = TrieNode()
        self.assertEqual(test_trie.children[0][1], 0)