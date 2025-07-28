import unittest
from services.midi_service import MidiService


class TestMidiService(unittest.TestCase):
    def setUp(self):
        self.midi_service = MidiService()

    def test_constructor(self):
        self.assertIsNone(self.midi_service._midi_file)

    def test_read_midi_file_path(self):
        file_path = "src\data\Super Mario Bross (Theme Song) - melody.mid"
        score = self.midi_service._read_midi_file(file_path)
        self.assertEqual(score[0], (76, 120))
