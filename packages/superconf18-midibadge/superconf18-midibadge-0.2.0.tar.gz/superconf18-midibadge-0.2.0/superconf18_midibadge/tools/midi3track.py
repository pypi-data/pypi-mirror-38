#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from ..midistuff import get_track_info_from_file
from ..midistuff import read_midifile
from ..midistuff import three_track_midi
from ..uistuff import print_trackinfo
from ..uistuff import input_tracklist


def main():
    parser = argparse.ArgumentParser(
        description="Extracts three tracks from a MIDI and creates a new MIDI file from it..")
    parser.add_argument("inpath", help="Input MIDI file")
    parser.add_argument("outpath", help="Output MIDI file")
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
    three_track_midi(mf, str(outfile), *tracklist)
    print(f"Wrote file {outfile}")


if __name__ == "__main__":
    main()
