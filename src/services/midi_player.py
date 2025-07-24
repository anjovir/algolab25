import pygame
import pygame.midi
import mido
from threading import Thread

class MidiSongPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.is_playing = False
        self.thread = None
    
    def __str__(self):
        default = "None-type object"
        if self.file_path == None:
            return default
        return self.file_path

    def play(self):
        pygame.init()
        pygame.midi.init()
        player = pygame.midi.Output(0)

        mid = mido.MidiFile(self.file_path)
        
        self.is_playing = True
        for msg in mid.play():
            if not self.is_playing:
                break  # Stop playing
            if not msg.is_meta:
                if msg.type == 'note_on':
                    player.note_on(msg.note, msg.velocity)
                elif msg.type == 'note_off':
                    player.note_off(msg.note, msg.velocity)

        player.close()
        pygame.midi.quit()
        pygame.quit()

    def start_playing(self):
        if not self.is_playing and self.file_path is not None:
            self.thread = Thread(target=self.play)
            self.thread.start()
        else:
            print("Choose a file")

    def stop_playing(self):
        self.is_playing = False
        if self.thread is not None:
            self.thread.join()  # Wait for playing to stop
    