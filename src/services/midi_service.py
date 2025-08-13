import mido


class MidiService:
    def __init__(self):
        self._midi_file = None
        self._midi_song_number = 0
        self.time_signatures = None

    def round_mod_four(self, value):
        return round(value / 4) * 4

    def rest_quantizer(self, numerator, denominator):
        result = denominator * ((numerator / denominator) - int(numerator / denominator))
        if result > 0:
            return result
        return denominator

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
        ts_counter = -1
        bar_counter = 0
        duration = 0
        pitchwheel_duration = 0
        control_change_duration = 0
        note_on_ts_flag = False
        note_q_flag = False

        for track in self._midi_file.tracks:
            msg_counter = 0
            for msg in track:
                msg_counter += 1
                note_or_rest = False
                if msg.type == "note_on":
                    if (track[msg_counter-2].type == "time_signature" and
                        self.round_mod_four(track[msg_counter-2].time) > 0 and
                        note_on_ts_flag is False):
                        duration = track[msg_counter-2].time
                        bar_lenght = tpb * \
                            time_signatures[ts_counter - 1][0] * \
                            (4 // time_signatures[ts_counter - 1][1])
                        note_or_rest = True
                        ts_note_flag = True
                        note = 200  # rest
                    elif self.round_mod_four(msg.time) > 0 and msg.velocity > 0:
                        if not note_q_flag:
                            if (msg.time +
                                pitchwheel_duration +
                                control_change_duration >
                                2 * bar_lenght):
                                duration = self.rest_quantizer(
                                    self.round_mod_four(msg.time +
                                                        pitchwheel_duration +
                                                        control_change_duration),
                                                        bar_lenght)
                            else:
                                duration = self.round_mod_four(msg.time +
                                                               pitchwheel_duration +
                                                               control_change_duration)
                            note_on_ts_flag = False
                            note_or_rest = True
                            note = 200  # rest
                        else:
                            note_q_flag = False
                    elif msg.time > 0 and msg.velocity == 0:
                        note = msg.note
                        duration = self.round_mod_four((msg.time +
                                                        pitchwheel_duration +
                                                        control_change_duration))

                        # Different next note_on midi-message cases
                        if (msg_counter < len(track) and
                            track[msg_counter].type == "time_signature" and
                            note_on_ts_flag is False and
                            track[msg_counter].time < bar_lenght):
                            duration += self.round_mod_four(track[msg_counter].time)
                            note_on_ts_flag = True
                        elif (msg_counter < len(track) and
                              track[msg_counter].type == "note_on" and
                              track[msg_counter].velocity > 0 and
                              track[msg_counter].time < 150 and
                              track[msg_counter].time > 4 and
                              track[msg_counter].time % 20 != 0):
                            duration += self.round_mod_four(track[msg_counter].time)
                            note_q_flag = True
                        elif (msg_counter < len(track) and
                              track[msg_counter].type == "note_on" and
                              track[msg_counter].velocity > 0 and
                              track[msg_counter].time + msg.time > bar_lenght and
                              track[msg_counter].time % 20 != 0 and
                              track[msg_counter].time < 2 * bar_lenght):
                            duration += self.round_mod_four(track[msg_counter].time)
                            note_q_flag = True

                        note_or_rest = True

                    if note_on_ts_flag and self.round_mod_four(msg.time) == 0:
                        note_on_ts_flag = False

                    pitchwheel_duration = 0
                    control_change_duration = 0

                elif msg.type == "note_off":
                    if track[msg_counter-2].type == "time_signature":
                        duration = track[msg_counter-2].time
                        bar_lenght = tpb * \
                            time_signatures[ts_counter - 1][0] * \
                            (4 // time_signatures[ts_counter - 1][1])
                        ts_note_flag = True
                    else:
                        duration = msg.time + pitchwheel_duration + control_change_duration
                        pitchwheel_duration = 0
                        control_change_duration = 0
                    note = msg.note
                    note_or_rest = True

                elif msg.type == "pitchwheel":
                    pitchwheel_duration += msg.time
                elif msg.type == "control_change":
                    control_change_duration +=  msg.time
                elif msg.type == "time_signature":
                    time_signatures.append((msg.numerator, msg.denominator))
                    ts_counter += 1
                    bar_lenght = tpb * msg.numerator * (4 / msg.denominator)
                elif msg.type == "set_tempo":
                    bpms.append(mido.tempo2bpm(msg.tempo))

                if note_or_rest:
                    note_score.append(note)
                    if duration > bar_lenght and note == 200:
                        remainder = duration % bar_lenght
                        if remainder > 0:
                            duration = int(remainder * bar_lenght + bar_lenght)
                        else:
                            duration = bar_lenght
                    duration = int(duration)
                    bar_lenght = int(bar_lenght)
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

                # In the first track there might not be note-data
                if msg.type == "end_of_track" and len(time_signatures) == 0:
                    continue
                if msg.type == "end_of_track" and len(time_signatures) > 0:
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
        print("NS\n",note_score, "RS\n",rhythm_score, "FS\n",full_score)
        return (note_score, rhythm_score, full_score)

    def save_generated_song(self, score, tempo, file_name="midi_song"):
        """
        Saves the generated score as a midi-file

        Args:
            score (list)
            tempo (int)
            file_name (str) option for future development in UI
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

        # Add tempo and time signature messages
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

                duration_counter += rest_length
                # Case where measure is full when rest is added
                if duration_counter == bar_lengths[bar_counter]:
                    if bar_counter > 0 and bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                        ts_numerator = bar_lengths[bar_counter] // tpb
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    if bar_counter + 1 < len(bar_lengths):
                        bar_counter += 1
                    duration_counter = score[n + 1][1]

                    # Special case with time signature changing with next added note duration
                    if duration_counter == bar_lengths[bar_counter]:
                        if bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                            ts_numerator = bar_lengths[bar_counter] // tpb
                            track.append(mido.MetaMessage("time_signature",
                                numerator=ts_numerator, denominator=ts_denominator))
                        if bar_counter + 1 < len(bar_lengths):
                            bar_counter += 1

                        duration_counter = 0
                # Case where rest + next note duration = full measure
                elif duration_counter + score[n + 1][1] == bar_lengths[bar_counter]:
                    if bar_counter > 0 and bar_lengths[bar_counter - 1] != bar_lengths[bar_counter]:
                        ts_numerator = bar_lengths[bar_counter] // tpb
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    if bar_counter + 1 < len(bar_lengths):
                        bar_counter += 1
                    duration_counter = 0
                else:
                    duration_counter += score[n + 1][1]

                track.append(mido.Message(
                    'note_off', note=score[n + 1][0], velocity=64, time=score[n + 1][1]))
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
                        ts_numerator = bar_lengths[bar_counter] // tpb
                        track.append(mido.MetaMessage("time_signature",
                            numerator=ts_numerator, denominator=ts_denominator))
                    if bar_counter + 1 < len(bar_lengths):
                        bar_counter += 1
                    duration_counter = 0

        fp = f"src/data/{file_name}{self._midi_song_number}.mid"
        self._midi_song_number += 1

        midi_file.save(fp)
