import pygame
import numpy as np
import pygame.midi
import time
import mido
class MidiPlayer():
    def __init__(self):
        pass

    def play_notes(self, notes, duration):
        pygame.init()
        pygame.midi.init()
        midi_output=pygame.midi.Output(0)
        for note in notes:
            midi_output.note_on(note, 127)  # Soitetaan nuotti (127 on äänenvoimakkuus)
            time.sleep(duration)  # Odotetaan nuotin kesto
            midi_output.note_off(note, 127)  # Lopetetaan nuotti
        
        midi_output.close()
        pygame.midi.quit()
        pygame.quit()

#    def play_note2(note):
#        frequency = 440 * 2 ** ((note - 69) / 12)  # Change the note value to frequency
#        sample_rate = 22050
#        duration = 0.5  # Duration in seconds
#        t = np.linspace(0, duration, int(sample_rate * duration), False)
#        wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # waveform
#        audio = np.array(wave * 32767, dtype=np.int16)  # Change to 16 bit

        # Change to 2D
#        audio_stereo = np.column_stack((audio, audio))  # Copy the same sound to both channels

#        sound = pygame.sndarray.make_sound(audio_stereo)
#        sound.play()
#        pygame.time.delay(int(duration * 1000))