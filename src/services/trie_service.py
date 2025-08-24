import os
import random
from entities.trie import Trie, TrieNode
from services.midi_service import MidiService



class TrieService:
    """
    Service for the trie-entity and generating score
    """
    def __init__(self, order=10):
        """
        Class constructor
            creates unique tries for saving only notes or rhythm or both
            creates midi-service
        
        Args:
            order (int), Markov chain order
        """
        self.root = TrieNode()
        self.trie = Trie(self.root)
        self.root_notes = TrieNode()
        self.trie_notes = Trie(self.root_notes)
        self.root_rhythm = TrieNode()
        self.trie_rhythm = Trie(self.root_rhythm)
        self._trie_read_succesfully = False
        self._midi_service = MidiService()

    def _read_file(self, file_path, mc_order):
        """
        Reads the midi-file to score (list) and inserts it to trie
        Updates the self._trie_read_succesfully, if insert successfull
        
        Args:
            file_path (str)
            mc_order (int) Markov chain order
        """
        score = self._midi_service.read_midi_file(file_path)
        return self._insert_to_trie(score, mc_order)

    def process_midi_files(self, directory: str, mc_order: int):
        """
        Processes all the midi-files in a directory

        Args:
            directory (string)
            mc_order (int) Markov chain order
        """
        for filename in os.listdir(directory):
            if filename.endswith(".mid"):
                file_path = os.path.join(directory, filename)
                success = self._read_file(file_path, mc_order)
                if not success:
                    return False
        return True


    def _insert_to_trie(self, score, mc_order):
        """
        Inserts the midi-files score to different trie-entities

        Args:
            score (list) with tuples
            mc_order (int) Markov chain order
        
        Returns:
            True or false if inserting notes to trie was successfull
        """
        full_score_ok = False
        score_notes_ok = False
        self.trie.insert(score[2], mc_order)
        for node in self.root.children.values():
            if isinstance(node[0], TrieNode):
                full_score_ok = True

        self.trie_notes.insert(score[0])
        for node in self.root_notes.children.values():
            if isinstance(node[0], TrieNode):
                score_notes_ok = True

        self.trie_rhythm.insert(score[1])
        if full_score_ok and score_notes_ok:
            for node in self.root_rhythm.children.values():
                if isinstance(node[0], TrieNode):
                    return True
        return False

    def generate_random_sequence_from_data(self, order=3, option=1):
        """
        Generates random sequence with parameters chosen by the user

        Args:
            order (int) Markov chain order
            option (int) 
                1: note and rhythm are one unit
                2: note and rhythm are generated separately
        
        Returns:
            option 1:
                sequence (list) of notes with rhythms
            option 2:
                sequence (tuple) 
                    of lists with notes, rhythm
        """
        if option == 1:
            seqs = self.trie.get_unique_sequences(order)
            return seqs[random.randint(0, (len(seqs) - 1))]
        if option in [2,3]:
            rhythm_seqs = self.trie_rhythm.get_unique_sequences(1)
            rhythm_seq = rhythm_seqs[random.randint(0, (len(rhythm_seqs) - 1))]
            note_seqs = self.trie_notes.get_unique_sequences(order)
            note_seq = note_seqs[random.randint(0, (len(note_seqs) - 1))]
            return (note_seq, rhythm_seq)

    def generate_score(self, sequence, lenght, option=1):
        """
        Handles the generate_song-method for generating the song
        based on paratemeters chosen by the user

        Args:
            sequence (list), output from generate random sequence
            lenght (int), song lenght either in notes or bars
            option (int)
        
        Returns:
            Score (list)        
        """
        if option == 1:
            return (self.generate_song(sequence, lenght, 1), ((1920,1920)))
        if option == 2:
            rhythm_score = self.generate_song(sequence[1], lenght, 2)
            rhythm_score_bar_lengths = [sum(measure) for measure in rhythm_score]
            rhythm_score = [note for measure in rhythm_score for note in measure]
            quantum_of_notes = len(rhythm_score)
            note_score = self.generate_song(sequence[0], quantum_of_notes, 3)
        return (list(zip(note_score, rhythm_score)), rhythm_score_bar_lengths)

    def _generate_next_note(self, sequence, option):
        """
        Generates next note based on used parameters

        Args:
            sequence (list)
            option (int)
        
        Returns:
            option 1: tuple (note, rhythm)
            option 2: int (rhythm)
            option 3: int (pitch)
        """
        if option == 1:
            generated_note = self.trie.get_next_note(sequence)
        elif option == 2:
            generated_note = self.trie_rhythm.get_next_note(sequence)
        elif option == 3:
            generated_note = self.trie_notes.get_next_note(sequence)
        return generated_note

    def _generate_next_note_again(self, sequence, option):
        """
        Generates new sequence if markov chain get starved of next notes

        Args:
            sequence (list)
            option (int)

        Returns:
            generated note tuple (option 1), int (options 2 and 3)
        """
        sequence = self.generate_random_sequence_from_data(len(sequence), option)
        if option == 1:
            generated_note = self.trie.get_next_note(sequence)
        elif option == 2:
            sequence = sequence[1]
            generated_note = self.trie_rhythm.get_next_note(sequence)
        elif option == 3:
            sequence = sequence[0]
            generated_note = self.trie_notes.get_next_note(sequence)

        return generated_note

    def generate_song(self, sequence, length, option):
        """
        Generates the song based on args

        Args:
            sequence (list)
            lenght (int)
            option (int)
        
        Returns:
            markov_chain_song (list), song notes and rhythms as a tuple
        """
        length = length - len(sequence)
        markov_chain_song = []
        for s in sequence:
            markov_chain_song.append(s)
        while_counter = 0
        while length > 0:
            generated_note = self._generate_next_note(sequence, option)

            # Sometimes there is no next element (note) for the sequence, this is a workaround
            while not generated_note:
                while_counter += 1
                generated_note = self._generate_next_note_again(sequence, option)
                if while_counter > 100:
                    return False

            markov_chain_song.append(generated_note)
            sequence.pop(0)
            sequence.append(generated_note)
            length -= 1

        return markov_chain_song
