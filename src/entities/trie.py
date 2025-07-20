from graphviz import Digraph

class TrieNode:
    def __init__(self):
        self.children = [[None, 0] for _ in range(128)]
    
    def __str__(self):
        return f"self.children: {self.children}"

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, value):
        value = value
        node = self.root
        if value not in node.children:
            node.children[value][0] = TrieNode()
            node.children[value][1] += 1 
        node = node.children[value]       

    def get_all_notes(self):
        notes = []
        self._collect_notes(self.root, notes)
        return notes

    def _collect_notes(self, node, notes):      
        for i in range(128):
            if node.children[i][1] > 0:
                notes.append([i, node.children[i][1]])
                self._collect_notes(node.children[i][0], notes)