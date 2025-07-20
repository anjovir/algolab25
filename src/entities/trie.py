import random

class TrieNode:
    def __init__(self):
        self.children = [[None, 0] for _ in range(128)]
        self.last_node = False
    
    def __str__(self):
        return f"self.children: {self.children}"

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, notes, max_order=100):
        curr_node = self.root
   
        for n in range(len(notes)):
            curr_node = self.root
            for i in range(max_order):
                if n + i >= len(notes):
                    break
                if curr_node.children[notes[n + i]][0] == None:
                    curr_node.children[notes[n + i]][0] = TrieNode()
            
                curr_node.children[notes[n + i]][1] += 1
                curr_node = curr_node.children[notes[n + i]][0]

    def get_all_notes(self):
        notes = {}
        self._collect_notes(self.root, notes)
        return notes

    def _collect_notes(self, node, notes):      
        for i in range(128):
            if node.children[i][1] > 0:
                notes[i] = node.children[i][1]
                self._collect_notes(node.children[i][0], notes)
    
    def sequence_exist(self, sequence):
        curr_node = self.root

        for note in sequence:
            if curr_node.children[note][0] is None:
                return False
            
            curr_node = curr_node.children[note][0]
        return True
    
    def get_next_note(self, sequence):
        curr_node = self.root
        for note in sequence:            
            if curr_node.children[note][0] is None:
                return False
            
            curr_node = curr_node.children[note][0]

        notes = []
        for i in range(128):
            if curr_node.children[i][1] > 0:
                for j in range(curr_node.children[i][1]):
                    notes.append(i)           
                
        if len(notes) < 1:
            return False
        next_note = notes[random.randint(0,len(notes)-1)]
        return next_note
    
    def generate_song(self, sequence, length):
        markov_chain_song = []
        markov_chain_song.extend(sequence)
        for i in range(length):
            generated_note = self.get_next_note(sequence)
            markov_chain_song.append(generated_note)
            sequence.pop(0)
            sequence.append(generated_note)

        return markov_chain_song
