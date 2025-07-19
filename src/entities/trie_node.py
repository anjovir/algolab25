from graphviz import Digraph

class TrieNode:
    def __init__(self):
        self.children = {}
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, value):
        node = self.root
        for char in str(value):
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.frequency += 1

    def get_all_notes(self):
        notes = []
        self._collect_notes(self.root, "", notes)
        return notes

    def _collect_notes(self, node, prefix, notes):
        if node.frequency > 0:
            notes.append((int(prefix), node.frequency))
        for char, child in node.children.items():
            self._collect_notes(child, prefix + char, notes)
    
    def visualize(self):
        dot = Digraph()
        self._add_nodes(dot, self.root, "")
        dot.render('trie_structure', format='png', cleanup=True)  # Tallenna kuva tiedostoon
        dot.view()  # Avaa kuva oletuskuvankatseluohjelmassa
    
    def _add_nodes(self, dot, node, prefix):
        if node.frequency > 0:
            dot.node(prefix, f"{prefix}\nFreq: {node.frequency}")
        for note, child in node.children.items():
            child_prefix = prefix + str(note)
            dot.edge(prefix, child_prefix)
            self._add_nodes(dot, child, child_prefix)