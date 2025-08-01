import unittest
from services.midi_player import MidiSongPlayer
from unittest.mock import patch, MagicMock
import time

class TestMidiSongPlayer(unittest.TestCase):
    @patch('pygame.midi.Output')
    @patch('mido.MidiFile')
    def setUp(self, mock_midi_file, mock_output):
        self.player = MidiSongPlayer("test.mid")
        self.player.midi_file = MagicMock() 
        self.player.midi_file.play.return_value = iter([]) 

    def test_start_playing_starts_thread(self):
        self.player.start_playing()
        self.assertTrue(self.player.thread is not None)

    def test_start_playing_when_already_playing(self):
        self.player.is_playing = True
        self.player.start_playing()
        self.assertIsNone(self.player.thread)

    def test_start_playing_with_no_file(self):
        self.player.file_path = None
        with patch('builtins.print') as mocked_print:
            self.player.start_playing()
            mocked_print.assert_called_with("Choose a file")

    def test_stop_playing(self):
        "Starting a thread takes some time, so we need to wait a bit before stopping it"
        self.player.start_playing()
        time.sleep(0.1)
        self.player.stop_playing()
        self.assertFalse(self.player.is_playing)
    

        


        

        
    