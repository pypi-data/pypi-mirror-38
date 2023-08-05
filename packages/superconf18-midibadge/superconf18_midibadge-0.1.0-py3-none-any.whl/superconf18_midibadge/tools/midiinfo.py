#!/usr/bin/env python3

import argparse 
from pathlib import Path

from ..midistuff import get_track_info_from_file
from ..uistuff import print_trackinfo


def main():
    parser = argparse.ArgumentParser(
        description="Prints a table of tracks in the given MIDI file.")
    parser.add_argument("inpath", help="Input MIDI file")
    args = parser.parse_args()

    infile = Path(args.inpath)
    trackinfo = get_track_info_from_file(str(infile))

    print(f"These tracks in MIDI file {infile} contain sound:")
    print("")
    print_trackinfo(trackinfo)
    
    
if __name__ == "__main__":
    main()
