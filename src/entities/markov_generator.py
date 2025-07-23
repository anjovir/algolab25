import random

class Markov_generator():
    def generate_next_note(trie, current_sequence, order):
    
        if len(current_sequence) < order:
            return None
        transitions = trie.get_next_notes(current_sequence[-4:])
        if not transitions:
            return None
        
        # Valitse seuraava nuotti siirtymien perusteella
        total = sum(transitions.values())
        rand = random.randint(1, total)
        cumulative = 0
        for note, freq in transitions.items():
            cumulative += freq
            if cumulative >= rand:
                return note
        return None

    def generate_sequence(trie, start_sequence, length, order):
        sequence = start_sequence.copy()
    
        for _ in range(length - len(start_sequence)):
            next_note = Markov_generator.generate_next_note(trie, sequence, order)
            if next_note is None:
                break
            sequence.append(next_note)
    
        return sequence
    
    
    def dfs(self, node=None, sequence=[]):
        if node is None:
            node = self.root

        if node.last_node:
            print(sequence)

        # Käydään läpi kaikki lapset
        for i in range(128):
            if node.children[i][0] is not None:
                sequence.append(i)
                # Kutsutaan rekursiivisesti seuraavaa solmua
                self.dfs(node.children[i][0], sequence)
