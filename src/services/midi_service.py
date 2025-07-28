import mido
from entities.trie import Trie

midi_song_number = 0

class MidiService:
    def __init__(self):
        self._midi_file = None
    
    def _read_midi_file(self, file_path):
        # This method reads the midi-file and packets the rhythms to a bar based rhythms
        self._midi_file = mido.MidiFile(file_path)
        tpb = self._midi_file.ticks_per_beat
        
        time_signatures = []
        bpms = []
        score = []
        bar = []
        skip_first_track = True
        ts_note_flag = False
        messages = {}
        msg_counter = 0
        ts_counter = -1
        bar_counter = 0
        
        for track in self._midi_file.tracks:
            for msg in track:              
                msg_counter += 1
                messages[msg_counter] = msg
                note_or_rest = False
                if msg.type == "note_on":
                    if messages[msg_counter-1].type == "time_signature" and messages[msg_counter-1].time != 0:
                        duration = messages[msg_counter-1].time
                        bar_lenght = tpb * time_signatures[ts_counter - 1][0] * (4 // time_signatures[ts_counter - 1][1])
                        note_or_rest = True
                        ts_note_flag = True
                        note = 200
                    if msg.time > 0:
                        duration = msg.time
                        note_or_rest = True
                        note = 200

                    pitchwheel_duration = 0
                                      
                elif msg.type == "note_off":
                    if messages[msg_counter-1].type == "time_signature":
                        duration = messages[msg_counter-1].time
                        bar_lenght = tpb * time_signatures[ts_counter - 1][0] * (4 // time_signatures[ts_counter - 1][1])
                        ts_note_flag = True
                    else:
                        duration = msg.time + pitchwheel_duration
                    note = msg.note
                    note_or_rest = True
                
                elif msg.type == "pitchwheel":
                    pitchwheel_duration += msg.time    
                elif msg.type == "time_signature":
                    time_signatures.append((msg.numerator, msg.denominator))
                    ts_counter += 1
                    bar_lenght = tpb * msg.numerator * (4 // msg.denominator)
                elif msg.type == "set_tempo":
                    bpms.append(mido.tempo2bpm(msg.tempo))
                
                if note_or_rest:
                    score.append((note, duration))
                
                # In the first track there is no note-data
                if msg.type == "end_of_track" and skip_first_track:
                    skip_first_track = False
                elif msg.type == "end_of_track" and skip_first_track == False:
                    if duration + bar_counter < bar_lenght: # last note and bar not complete
                        score.append((200, bar_lenght-bar_counter))

                if ts_note_flag:
                        ts_note_flag = False
                        bar_lenght = tpb * time_signatures[ts_counter][0] * (4 // time_signatures[ts_counter][1])
        return score

    def save_generated_song(self, score, tempo):
        # Create new file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        # Add tempo message
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

        counter = 1
        for n in range(len(score)):
            #print("LOOPPI",len(score), n, score[n])
            if score[n][0] == 200 and n < len(score) - 1:
                if score[n + 1] == 200:
                    continue
                else:
                    track.append(mido.Message('note_on', note=score[n + 1][0], velocity=80, time=score[n][1]))  # Rest
            elif score[n-1][0] == 200 and n < len(score) - 1:
                continue
            elif score[n][0] == 200 and n == len(score) - 1:
                continue
            else:
                track.append(mido.Message('note_on', note=score[n][0], velocity=80, time=0))  # Note start
                track.append(mido.Message('note_off', note=score[n][0], velocity=64, time=score[n][1]))  # Note end

        global midi_song_number
        fp = f"src/data/midi_song{midi_song_number}.mid"
        midi_song_number += 1

        midi_file.save(fp)

    def save_generated_song_copy(self, notes, tempo):
        # Create new file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        # Add tempo message
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

        for n in notes:
            track.append(mido.Message('note_on', note=n[0], velocity=64, time=0))  # Note start
            track.append(mido.Message('note_off', note=n[0], velocity=64, time=n[1]))  # Note end

        global midi_song_number
        fp = f"src/data/midi_song{midi_song_number}.mid"
        midi_song_number += 1

        midi_file.save(fp)

    def _read_midi_file_copy(self, file_path):
        # This method reads the midi-file and packets the rhythms to a bar based rhythms
        self._midi_file = mido.MidiFile(file_path)
        tpb = self._midi_file.ticks_per_beat
        
        time_signatures = []
        bpms = []
        score = []
        bar = []
        skip_first_track = True
        ts_note_flag = False
        messages = {}
        msg_counter = 0
        ts_counter = -1
        bar_counter = 0
        
        for track in self._midi_file.tracks:
            for msg in track:              
                msg_counter += 1
                messages[msg_counter] = msg
                note_or_rest = False
                if msg.type == "note_on":
                    if messages[msg_counter-1].type == "time_signature" and messages[msg_counter-1].time != 0:
                        duration = messages[msg_counter-1].time
                        bar_lenght = tpb * time_signatures[ts_counter - 1][0] * (4 // time_signatures[ts_counter - 1][1])
                        note_or_rest = True
                        ts_note_flag = True
                        note = "rest" 
                    if msg.time > 0:
                        duration = msg.time
                        note_or_rest = True
                        note = "rest"

                    pitchwheel_duration = 0
                                      
                elif msg.type == "note_off":
                    if messages[msg_counter-1].type == "time_signature":
                        duration = messages[msg_counter-1].time
                        bar_lenght = tpb * time_signatures[ts_counter - 1][0] * (4 // time_signatures[ts_counter - 1][1])
                        ts_note_flag = True
                    else:
                        duration = msg.time + pitchwheel_duration
                    note = msg.note
                    note_or_rest = True
                
                elif msg.type == "pitchwheel":
                    pitchwheel_duration += msg.time    
                elif msg.type == "time_signature":
                    time_signatures.append((msg.numerator, msg.denominator))
                    ts_counter += 1
                    bar_lenght = tpb * msg.numerator * (4 // msg.denominator)
                elif msg.type == "set_tempo":
                    bpms.append(mido.tempo2bpm(msg.tempo))
                
                if note_or_rest:
                    if duration + bar_counter < bar_lenght:
                        bar.append((note,duration))
                        bar_counter += duration
                    elif duration + bar_counter == bar_lenght:
                        bar.append((note,duration))
                        score.append(bar)
                        bar = []
                        bar_counter = 0
                    elif duration + bar_counter > bar_lenght:
                        left_over = bar_lenght-bar_counter
                        bar.append((note,left_over))
                        score.append(bar)
                        bar = []
                        duration_to_next_bar = duration-left_over
                        bar.append((note, duration_to_next_bar))
                        bar_counter = duration_to_next_bar
                
                # In the first track there is no note-data
                if msg.type == "end_of_track" and skip_first_track:
                    skip_first_track = False
                elif msg.type == "end_of_track" and skip_first_track == False:
                    if duration + bar_counter < bar_lenght: # last note and bar not complete
                        bar.append(("rest", bar_lenght-bar_counter))
                        score.append(bar)

                if ts_note_flag:
                        ts_note_flag = False
                        bar_lenght = tpb * time_signatures[ts_counter][0] * (4 // time_signatures[ts_counter][1])