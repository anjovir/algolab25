import unittest
from services.midi_player import MidiSongPlayer
from unittest.mock import patch, MagicMock


class TestMidiSongPlayer(unittest.TestCase):

    def setUp(self):
        self._midi_file = "src\\data\\super_mario_play_test.mid"
        self._midi_player = MidiSongPlayer(self._midi_file)