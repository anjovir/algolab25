import unittest
import os
from services.midi_service import MidiService


class TestMidiService(unittest.TestCase):
    def setUp(self):
        self.midi_service = MidiService()
        self.test_dir = "src/data/tests"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
    
    def tearDown(self):
        for file in os.listdir(self.test_dir):
            if file.endswith(".mid"):
                os.remove(os.path.join(self.test_dir, file))
        return super().tearDown()

    def test_constructor(self):
        self.assertIsNone(self.midi_service._midi_file)

    def test_read_midi_file_path(self):
        file_path = "src\\data\\Super Mario Bross (Theme Song) - melody.mid"
        score = self.midi_service._read_midi_file(file_path)
        self.assertEqual(score[0], (76, 120))

    def test_save_last_note(self):
        midi_service1 = MidiService()
        original_score = [(80, 120),(82, 120),(200, 120),(200, 120),(80, 120),(90, 120),(83, 120),(200, 120)]
        file_name = "tests/last_note"
        midi_service1.save_generated_song(original_score, 120, file_name)
        file_path = f"src\\data\\{file_name}.mid"
        score = midi_service1._read_midi_file(file_path)
        test_score = [(80, 120),(82, 120),(200, 240),(80, 120),(90, 120),(83, 120)]
        self.assertEqual(test_score, score)
    
    def test_save_two_rest_notes_after_another(self):
        midi_service2 = MidiService()
        original_score = [(80, 120),(82, 120),(200, 120),(200, 120),(80, 120),(90, 120),(200, 120),(83, 120)]
        file_name = "tests/two_rests"
        midi_service2.save_generated_song(original_score, 120, file_name)
        file_path = f"src\\data\\{file_name}.mid"
        score = midi_service2._read_midi_file(file_path)
        test_score = [(80, 120),(82, 120),(200, 240),(80, 120),(90, 120),(200, 120),(83, 120)]
        self.assertEqual(test_score, score)


