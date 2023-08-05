import copy
import midi


def read_midifile(fname):
    return midi.read_midifile(str(fname))


def get_track_info_from_file(fname):
    mf = midi.read_midifile(fname)
    tracks = {}

    for idx, el in enumerate(mf):
        if not hasattr(el[0], 'text'):
            continue
        tracks[idx] = {
            "name": el[0].text,
            "tones": sum([1 for event in el[1:] if type(event) == midi.events.NoteOnEvent], 1)
        }

    return tracks


def single_track_midi(mf, dest, track):
    if isinstance(mf, str):
        mf = midi.read_midifile(mf)
    pat = midi.Pattern()
    pat.append(mf[track])
    midi.write_midifile(dest, pat)


def three_track_midi(source, dest, tr1, tr2, tr3):
    if isinstance(mf, str):
        mf = midi.read_midifile(mf)
    pat = midi.Pattern()
    pat.append(mf[tr1])
    pat.append(mf[tr2])
    pat.append(mf[tr3])
    midi.write_midifile(dest, pat)


def get_three_tracks_from_file(mf, t1, t2, t3):
    if isinstance(mf, str):
        mf = midi.read_midifile(mf)
    return [mf[t1], mf[t2], mf[t3]]


def get_timeline_from_track(track, tick_multiplier=2):
    timestamp = 0
    notes = []
    for ev in track:
        timestamp += ev.tick * tick_multiplier
        if type(ev) == midi.events.NoteOnEvent:
            if ev.data[1] == 0:
                # if the volume is set to zero we shouldn't play the tone,
                # setting the tone to 0 apparently achieves that
                notes.append((timestamp, 0))
            else:
                notes.append((timestamp, ev.data[0]))
    
    # insert noop first entry if the first entry isn't at t=0
    if notes[0][0] != 0:
        notes = [(0, 0), *notes]
    
    return notes
    

def get_notes_from_timelines(timelines: list):
    timelines = copy.copy(timelines)
    last_timestamp = 0
    notes = []
    
    while sum(len(t) for t in timelines) > 0:
        next_timestamp = min(t[0][0] for t in timelines if len(t) > 0)

        if len(notes) == 0:
            next_note = [0, 0, 0, 0]
        else:
            # sub in duration for last note
            notes[-1][0] = next_timestamp - last_timestamp
            next_note = [0, *notes[-1][1:]]

        for i in range(len(timelines)):
            if len(timelines[i]) > 0 and timelines[i][0][0] == next_timestamp:
                next_track_note = timelines[i].pop(0)
                next_note[i+1] = next_track_note[1]

        notes.append(next_note)
        last_timestamp = next_timestamp

    return notes 
    
    # MIDI notes are numbered from 0 to 127 assigned to C-1 to G9. This 
    # corresponds to a range of 8.175798916Hz to 12543.85395Hz (assuming equal 
    # temperament and 440Hz A4) and extends beyond the 88 note piano range from 
    # A0 to C8.
    
    # return [
    #     f"tune {ev.data[0]},{ev.data[0]},{ev.data[0]},1000"
    #     for ev in track
    #     if type(ev) == midi.events.NoteOnEvent
    # ]
