import random


class TrieNode:
    def __init__(self):
        self.children = {}

    def __str__(self):
        return f"self.children: {self.children} "


class Trie:
    def __init__(self, root_node):
        self.root = root_node

    def insert(self, score, max_order=100):
        curr_node = self.root

        for n in range(len(score)):
            curr_node = self.root
            for i in range(max_order):
                if n + i >= len(score):
                    break
                index = score[n+i]
                if index not in curr_node.children or curr_node.children[index] is None:
                    curr_node.children[index] = [TrieNode(), 1]

                curr_node.children[index][1] += 1
                curr_node = curr_node.children[index][0]

    def get_unique_sequences(self, order=3):
        seqs = []
        self._collect_sequences(self.root, seqs, order, seq=[])
        return seqs

    def _collect_sequences(self, node, seqs, order, seq):
        for n in node.children:
            if node.children[n][1] > 0:
                if len(seq) < order:
                    seq.append(n)
                    self._collect_sequences(
                        node.children[n][0], seqs, order, seq)
                elif seq not in seqs and len(seq) == order:
                    seqs.append(seq)
                seq = []

    def get_next_note(self, sequence):
        curr_node = self.root
        for element in sequence:
            if curr_node.children[element][0] is None:
                return False

            curr_node = curr_node.children[element][0]

        elements = []
        for n in curr_node.children:
            if curr_node.children[n][1] > 0:
                elements.extend([n]*curr_node.children[n][1])

        if len(elements) < 1:
            return False
        next_element = elements[random.randint(0, len(elements)-1)]
        return next_element
