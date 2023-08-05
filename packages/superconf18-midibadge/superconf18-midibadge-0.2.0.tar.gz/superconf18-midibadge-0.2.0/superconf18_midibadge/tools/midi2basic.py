#!/usr/bin/env python3

import argparse 
from pathlib import Path

from ..midistuff import get_track_info_from_file
from ..midistuff import read_midifile
from ..midistuff import get_three_tracks_from_file
from ..midistuff import get_timeline_from_track
from ..midistuff import get_notes_from_timelines
from ..uistuff import print_trackinfo
from ..uistuff import input_tracklist


def main():
    parser = argparse.ArgumentParser(
        description="Creates BASIC file form three tracks of a MIDI file.")
    parser.add_argument("inpath", help="Input MIDI file")
    parser.add_argument("outpath", help="Output BASIC file")
    args = parser.parse_args()

    infile = Path(args.inpath)
    outfile = Path(args.outpath)
    trackinfo = get_track_info_from_file(str(infile))

    print(f"These tracks in MIDI file {infile} contain sound:")
    print("")
    print_trackinfo(trackinfo)

    print("")
    print("")
    print("Select *exactly* three tracks to export into BASIC file!")
    tracklist = input_tracklist(validate_length=3)

    mf = read_midifile(str(infile))
    tracks_from_file = get_three_tracks_from_file(str(infile), *tracklist)
    t1 = get_timeline_from_track(tracks_from_file[0])
    t2 = get_timeline_from_track(tracks_from_file[1])
    t3 = get_timeline_from_track(tracks_from_file[2])
    notes = get_notes_from_timelines([t1, t2, t3])
    with open(outfile, 'w') as out:
        for line, note in enumerate(notes):
            out.write(f"{(line+1)} tune {note[1]},{note[2]},{note[3]},{note[0]}\n")

    print(f"Wrote {len(notes)} notes to file {outfile}")


if __name__ == "__main__":
    main()
