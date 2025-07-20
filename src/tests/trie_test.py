import unittest
from entities.trie_node import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")
    
    def test_constructor_works1(self):
        test_trie = TrieNode()
        test = test_trie.children
        self.assertIsNotNone(test)
    
    def test_constructor_works2(self):
        test_trie = TrieNode()
        test = test_trie.frequency
        self.assertEqual(test, 0)