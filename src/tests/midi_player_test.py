import unittest
from services.midi_player import MidiSongPlayer
from unittest.mock import patch, MagicMock
import mido
import time

class TestMidiSongPlayer(unittest.TestCase):
    @patch('pygame.midi.Output')
    @patch('mido.MidiFile')
    def setUp(self, mock_midi_file, mock_output):
        self.player = MidiSongPlayer("test.mid")
        self.player.midi_file = MagicMock()
        self.player.midi_file.play.return_value = iter([
            mido.Message('note_on', note=60, velocity=100),
            mido.Message('note_off', note=60, velocity=100)
        ])
        self.mock_output = mock_output.return_value
    
   
    @patch('pygame.midi.Output')
    @patch('pygame.midi.init')
    @patch('pygame.midi.quit')
    @patch("mido.MidiFile")
    def test_play_method(self, mock_midi_file_class,mock_quit, mock_init, mock_output):
        test_file_path = 'test.mid'
        mock_midi_file = MagicMock()
        mock_midi_file.play.return_value = [
            mido.Message('note_on', note=60, velocity=100),
            mido.Message('note_off', note=60, velocity=100)
        ]
        
        mock_midi_file_class.return_value = mock_midi_file
        player = MidiSongPlayer(test_file_path)
        player.play()

        mock_init.assert_called_once()
        mock_output.assert_called_once()

        mock_output.return_value.note_on.assert_called_with(60, 100)
        mock_output.return_value.note_off.assert_called_with(60, 100)

        mock_quit.assert_called_once()

       

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
    

        


        

        
    