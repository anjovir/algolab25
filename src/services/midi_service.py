import mido


class MidiService:
    def __init__(self):
        self._midi_file = None
        self._midi_song_number = 0
        self.time_signatures = None
    
    def round_mod_four(self, value):
        return round(value / 4) * 4

    def read_midi_file(self, file_path):
        """
        Method reads the midi-file and returns tuple with lists with notes, rhythm and both

        Args:
            file_path (str)
        
        Returns:
            Score (tuple)
                inside the tuple there are three lists
                1: only notes and their midi-values
                2: only full bar rhythm-patterns
                3: notes and their durations in one tuple in a list
        """

        self._midi_file = mido.MidiFile(file_path)
        tpb = self._midi_file.ticks_per_beat

        time_signatures = []
        bpms = []
        note_score = []
        rhythm_score = []
        full_score = []
        measure = []
        ts_note_flag = False
        messages = {}
        msg_counter = 0
        ts_counter = -1
        bar_counter = 0
        duration = 0
        pitchwheel_duration = 0
        control_change_duration = 0

        for track in self._midi_file.tracks:
            for msg in track:
                msg_counter += 1
                messages[msg_counter] = msg
                note_or_rest = False
                if msg.type == "note_on":
                    if (messages[msg_counter-1].type == "time_signature" and 
                        self.round_mod_four(messages[msg_counter-1].time) > 0):
                        duration = messages[msg_counter-1].time
                        bar_lenght = tpb * \
                            time_signatures[ts_counter - 1][0] * \
                            (4 // time_signatures[ts_counter - 1][1])
                        note_or_rest = True
                        ts_note_flag = True
                        note = 200  # rest
                    if self.round_mod_four(msg.time) > 0 and msg.velocity > 0:
                        duration = self.round_mod_four(msg.time + pitchwheel_duration + control_change_duration)
                        note_or_rest = True
                        note = 200  # rest
                    if msg.time > 0 and msg.velocity == 0:
                        note = msg.note
                        duration = self.round_mod_four((msg.time + pitchwheel_duration + control_change_duration))
                        note_or_rest = True

                    pitchwheel_duration = 0
                    control_change_duration = 0

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
                elif msg.type == "control_change":
                    control_change_duration +=  msg.time

                elif msg.type == "time_signature":
                    time_signatures.append((msg.numerator, msg.denominator))
                    ts_counter += 1
                    bar_lenght = tpb * msg.numerator * (4 // msg.denominator)
                elif msg.type == "set_tempo":
                    bpms.append(mido.tempo2bpm(msg.tempo))

                if note_or_rest:
                    note_score.append(note)
                    full_score.append((note, duration))

                    if duration + bar_counter < bar_lenght:
                        measure.append(duration)
                        bar_counter += duration
                    elif duration + bar_counter == bar_lenght:
                        measure.append(duration)
                        rhythm_score.append(tuple(measure))
                        measure = []
                        bar_counter = 0
                    elif duration + bar_counter > bar_lenght:
                        left_over = bar_lenght-bar_counter
                        measure.append(left_over)
                        rhythm_score.append(tuple(measure))
                        measure = []
                        duration_to_next_bar = duration-left_over
                        measure.append(duration_to_next_bar)
                        bar_counter = duration_to_next_bar

                # In the first track there might not be no note-data
                if msg.type == "end_of_track" and len(time_signatures) == 0:
                    continue
                elif msg.type == "end_of_track" and len(time_signatures) > 0:
                    if duration + bar_counter < bar_lenght:  # last note and bar not complete
                        note_score.append(200)
                        full_score.append((200, bar_lenght-bar_counter))
                        measure.append(bar_lenght-bar_counter)
                        rhythm_score.append(tuple(measure))

                if ts_note_flag:
                    ts_note_flag = False
                    bar_lenght = tpb * \
                        time_signatures[ts_counter][0] * \
                        (4 // time_signatures[ts_counter][1])
        self.time_signatures = time_signatures
        return (note_score, rhythm_score, full_score)

    def save_generated_song(self, score, tempo, file_name="midi_song", first_bar_lenght=1920):
        """
        Saves the generated score as a midi-file

        Args:
            score (list)
            tempo (int)
            file_name (str) option for future development in UI
            first_bar_lenght (int), for time signature
        """
        bar_lengths = score[1]
        score = score[0]
        tpb = 480 # default ticks per beat
        ts_numerator = bar_lengths[0] // tpb
        ts_denominator = 4

        # Create new file
        midi_file = mido.MidiFile(ticks_per_beat=tpb)
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        # Add tempo message
        track.append(mido.MetaMessage(
            "set_tempo", tempo=mido.bpm2tempo(tempo)))
        track.append(mido.MetaMessage("time_signature",
                     numerator=ts_numerator, denominator=ts_denominator))

        # Go through the score, 200 = rest
        rest_length = 0
        duration_counter = 0
        bar_counter = 0
        for n in range(len(score)):
            if n < len(score) - 1 and score[n][0] == 200:
                rest_length += score[n][1]
                if score[n + 1][0] == 200:
                    continue
                # Rest duration has to be applied to a next note_on message
                track.append(mido.Message(
                    'note_on', note=score[n + 1][0], velocity=80, time=rest_length))
                track.append(mido.Message(
                    'note_off', note=score[n + 1][0], velocity=64, time=score[n + 1][1]))
                duration_counter += rest_length
                # Case where measure is full when rest is added
                if duration_counter == bar_lengths[bar_counter]:
                    if bar_counter > 0 and bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                        ts_numerator = bar_lengths[bar_counter]
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    bar_counter += 1
                    duration_counter = score[n + 1][1]

                    # Special case with time signature changing with next added note duration
                    if duration_counter == bar_lengths[bar_counter]:
                        if bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                            ts_numerator = bar_lengths[bar_counter]
                            track.append(mido.MetaMessage("time_signature",
                                numerator=ts_numerator, denominator=ts_denominator))
                        bar_counter += 1
                        duration_counter = 0
                # Case where rest + next note duration = full measure
                elif duration_counter + score[n + 1][1] == bar_lengths[bar_counter]:
                    if bar_counter > 0 and bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                        ts_numerator = bar_lengths[bar_counter]
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    bar_counter += 1
                    duration_counter = 0
                else:
                    duration_counter += score[n + 1][1]
                rest_length = 0
            elif n > 0 and score[n-1][0] == 200:
                continue
            # Last note (rest) in the score
            elif n == len(score) - 1 and score[n][0] == 200:
                continue
            else:
                track.append(mido.Message(
                    'note_on', note=score[n][0], velocity=80, time=0))  # Note start
                track.append(mido.Message(
                    'note_off', note=score[n][0], velocity=64, time=score[n][1]))  # Note end
                duration_counter += score[n][1]
                if duration_counter == bar_lengths[bar_counter]:
                    if bar_counter > 0 and bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                        ts_numerator = bar_lengths[bar_counter]
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    bar_counter += 1
                    duration_counter = 0

        fp = f"src/data/{file_name}{self._midi_song_number}.mid"
        self._midi_song_number += 1

        midi_file.save(fp)
