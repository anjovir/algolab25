import unittest
import os
from services.midi_service import MidiService


class TestMidiService(unittest.TestCase):
    def setUp(self):
        self.midi_service = MidiService()
        self._test_file_path = "src\\data\\midi_test_data/Super Mario Bross (Theme Song) - melody.mid"
        self.test_dir = "src/data/tests"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_directory = "src/data/midi_test_data"
        self.test_files = []
        for filename in os.listdir(self.test_directory):
            if filename.endswith(".mid"):
                self.test_files.append(os.path.join(self.test_directory, filename))

    def tearDown(self):
        for file in os.listdir(self.test_dir):
            if file.endswith(".mid"):
                os.remove(os.path.join(self.test_dir, file))
        return super().tearDown()

    def test_constructor(self):
        self.assertIsNone(self.midi_service._midi_file)

    def test_read_midi_file_path(self):
        file_path = "src\\data\\midi_test_data/Super Mario Bross (Theme Song) - melody.mid"
        score = self.midi_service.read_midi_file(file_path)
        self.assertEqual(score[2][1], (76, 120))
    
    def test_read_midi_file_rhythm_bars(self):
        score = self.midi_service.read_midi_file(self._test_file_path)
        for bar in score[1]:
            self.assertEqual(sum(bar), 1920)

    def test_save_last_note(self):
        midi_service1 = MidiService()
        original_score = [[(80, 120), (82, 120), (200, 120),
                          (200, 120), (80, 120), (90, 120), (83, 120), (200, 120)], [(1920)]]
        file_name = "tests/last_note"
        midi_service1.save_generated_song(original_score, 120, file_name)
        file_path = f"src\\data\\{file_name}{0}.mid"
        score = midi_service1.read_midi_file(file_path)
        test_score = [(80, 120), (82, 120), (200, 240),
                      (80, 120), (90, 120), (83, 120), (200, 1080)]
        self.assertEqual(test_score, score[2])

    def test_save_two_rest_notes_after_another(self):
        midi_service2 = MidiService()
        original_score = [[(80, 120), (82, 120), (200, 120),
                          (200, 120), (80, 120), (90, 120), (200, 120), (83, 120)], [(1920)]]
        file_name = "tests/two_rests"
        midi_service2.save_generated_song(original_score, 120, file_name)
        file_path = f"src\\data\\{file_name}{0}.mid"
        score = midi_service2.read_midi_file(file_path)
        test_score = [(80, 120), (82, 120), (200, 240),
                      (80, 120), (90, 120), (200, 120), (83, 120), (200,960)]
        self.assertEqual(test_score, score[2])
    
    def test_read_file_quantification_works(self):
         for file in self.test_files:
            midi_file = self.midi_service.read_midi_file(file)
            self.assertEqual(0, midi_file[1][0][0] % 40)
            self.assertEqual(0, self.midi_service.read_midi_file(self._test_file_path)[1][0][0] % 40)
    
    def test_read_file_no_negatives(self):
         for file in self.test_files:
            midi_file = self.midi_service.read_midi_file(file)
            for bar in midi_file[1]:
                for note in bar:        
                    self.assertLess(-1, note)
    
    def test_read_file_no_zero_rhythms(self):
        for file in self.test_files:
            midi_file = self.midi_service.read_midi_file(file)
            for bar in midi_file[1]:
                for note in bar:        
                    self.assertIsNot(0, note)

        
