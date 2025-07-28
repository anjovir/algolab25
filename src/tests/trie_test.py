import unittest
from entities.trie import Trie, TrieNode


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.test_trie = TrieNode()

    def test_constructor_works(self):
        self.assertIsInstance(self.test_trie.children, dict)
