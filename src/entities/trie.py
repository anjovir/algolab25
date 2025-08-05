import random


class TrieNode:
    """
    Class for Trie-node
    """
    def __init__(self):
        self.children = {}

    def __str__(self):
        return f"self.children: {self.children} "


class Trie:
    """
    Class for methods using TrieNode
    """
    def __init__(self, root_node):
        self.root = root_node

    def insert(self, score, max_order=100):
        """
        Inserts data to Trie Node

        Args:
            score (list)
            max_order (int), maximum Markov chain order used in saving notes to Trie
        """
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
        """
        Method for handling _collect_sequences

        Args:
            order (int)

        Returns:
            seqs (list)
                All sequences saved in the Trie-entity
        """
        seqs = []
        self._collect_sequences(self.root, seqs, order, seq=[])
        return seqs

    def _collect_sequences(self, node, seqs, order, seq):
        """
        Collects all sequences from the trie recursively and saves them to seqs

        Args:
            node (TrieNode)
            seqs (list)
            order (int)
            seq (list)
        """
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
        """
        Checks the TrieNode for the next to based on input sequence

        Args:
            sequence(list)
        
        Returns:
            next_element, output varies based on used trie-node
                can be tuple, list or int
        """
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
