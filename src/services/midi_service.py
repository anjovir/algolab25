import mido
from entities.trie import Trie

midi_song_number = 0


class MidiService:
    def __init__(self):
        self._midi_file = None

    def _read_midi_file(self, file_path):
        # This method reads the midi-file and returns the score (notes and their durations)
        self._midi_file = mido.MidiFile(file_path)
        tpb = self._midi_file.ticks_per_beat
        time_signatures = []
        bpms = []
        score = []
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
                        bar_lenght = tpb * \
                            time_signatures[ts_counter - 1][0] * \
                            (4 // time_signatures[ts_counter - 1][1])
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
                        bar_lenght = tpb * \
                            time_signatures[ts_counter - 1][0] * \
                            (4 // time_signatures[ts_counter - 1][1])
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
                # Last bar problems solution
                elif msg.type == "end_of_track" and skip_first_track == False:
                    if duration + bar_counter < bar_lenght:  # last note and bar not complete
                        score.append((200, bar_lenght-bar_counter))

                if ts_note_flag:
                    ts_note_flag = False
                    bar_lenght = tpb * \
                        time_signatures[ts_counter][0] * \
                        (4 // time_signatures[ts_counter][1])
        return score

    def save_generated_song(self, score, tempo, file_name="midi_song"):
        # Create new file
        midi_file = mido.MidiFile()
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        # Add tempo message
        track.append(mido.MetaMessage(
            "set_tempo", tempo=mido.bpm2tempo(tempo)))
        
        # Go through the score, 200 = rest
        rest_length = 0
        for n in range(len(score)):
            if  n < len(score) - 1 and score[n][0] == 200:
                rest_length += score[n][1]
                if score[n + 1][0] == 200:
                    continue
                else:
                    # Rest duration has to be applied to a next note_on message
                    track.append(mido.Message(
                        'note_on', note=score[n + 1][0], velocity=80, time=rest_length))
                    track.append(mido.Message(
                    'note_off', note=score[n + 1][0], velocity=64, time=score[n + 1][1]))  # Note end
                    rest_length = 0
            elif n > 0 and score[n-1][0] == 200:
                continue
            # Last note (rest) in the score
            elif n == len(score) - 1 and score[n][0] == 200:
                continue
            else:
                #print(n, score[n])
                track.append(mido.Message(
                    'note_on', note=score[n][0], velocity=80, time=0))  # Note start
                track.append(mido.Message(
                    'note_off', note=score[n][0], velocity=64, time=score[n][1]))  # Note end

        global midi_song_number
        fp = f"src/data/{file_name}.mid"
        midi_song_number += 1

        midi_file.save(fp)