from threading import Thread
import pygame.midi
import mido


class MidiSongPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.midi_file = mido.MidiFile(self.file_path)
        self.is_playing = False
        self.thread = None

    def __str__(self):
        default = "None-type object"
        if self.file_path is None:
            return default
        return self.file_path

    def play(self):
        pygame.midi.init()
        player = pygame.midi.Output(0)

        self.is_playing = True
        for msg in self.midi_file.play():
            if not self.is_playing:
                break
            if msg.type == 'note_on':
                player.note_on(msg.note, msg.velocity)
            elif msg.type == 'note_off':
                player.note_off(msg.note, msg.velocity)

        player.close()
        pygame.midi.quit()

    def start_playing(self):
        if not self.is_playing and self.file_path is not None:
            self.thread = Thread(target=self.play)
            self.thread.start()
        else:
            print("Choose a file")

    def stop_playing(self):
        self.is_playing = False
        if self.thread is not None:
            self.thread.join()
