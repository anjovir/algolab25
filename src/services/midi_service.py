import mido
from entities.trie import Trie

midi_song_number = 0

class MidiService:
    def __init__(self):
        self._midi_file = None
        pass

    def _read_midi_file(self, file_path):
        all_notes = []
        self._midi_file = mido.MidiFile(file_path)
        for track in self._midi_file.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    note_value = msg.note
                    all_notes.append(note_value)
        
        return all_notes

    def save_generated_song(self, notes, tempo):
        # Create new file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        ticks_per_beat = 240

        # Add tempo message
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

        for note in notes:
            track.append(mido.Message('note_on', note=note, velocity=64, time=0))  # Note start
            track.append(mido.Message('note_off', note=note, velocity=64, time=ticks_per_beat))  # Note end

        global midi_song_number
        fp = f"src/data/midi_song{midi_song_number}.mid"
        midi_song_number += 1

        midi_file.save(fp)