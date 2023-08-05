#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from ..midistuff import get_track_info_from_file
from ..midistuff import read_midifile
from ..midistuff import single_track_midi
from ..uistuff import print_trackinfo
from ..uistuff import input_tracklist


def main():
    parser = argparse.ArgumentParser(
        description="Split a single MIDI file into multiple MIDI files, one for each track.")
    parser.add_argument(
        "inpath", help="Input MIDI file")
    parser.add_argument(
        "--out", dest="outpath", default=".", required=False, 
        help="Output folder for single-track MIDI files (defaults to current directory)")
    args = parser.parse_args()

    infile = Path(args.inpath)
    inname = Path(args.inpath).stem  # stem = file name without extension
    outfolder = Path(args.outpath)
    trackinfo = get_track_info_from_file(str(infile))

    print(f"These tracks in MIDI file {infile} contain sound:")
    print("")
    print_trackinfo(trackinfo)

    print("")
    print("")
    tracklist = input_tracklist(default=list(trackinfo.keys()))

    os.makedirs(str(outfolder), exist_ok=True)

    mf = read_midifile(str(infile))
    for track in tracklist:
        destfile = f"{outfolder}/{inname}-{track}-{trackinfo[track]['name'][:10]}.mid"
        single_track_midi(mf, destfile, track)
        print(f"Wrote file {destfile}")


if __name__ == "__main__":
    main()
