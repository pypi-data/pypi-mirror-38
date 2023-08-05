superconf18-midibadge
=====================


Generate Basic code for the Hackaday Superconf 2018 Badge from a MIDI file


## Quickstart

Install:

```
pip install superconf18_midibadge
```

See what tracks are in a MIDI file:

```
midiinfo --help
usage: midiinfo [-h] inpath

Prints a table of tracks in the given MIDI file.

positional arguments:
  inpath      Input MIDI file

optional arguments:
  -h, --help  show this help message and exit
```

```
midiinfo example.mid
These tracks in MIDI file example.mid contain sound:

  #  Tones   Track Name
---  ------  ------------------------------
  1     143  Lead Vox
  2     139  Lead Vox 2
  3    1921  Piano
  4     481  Bass
  5     780  Strings
  6     263  Choir
  7     155  Brass
  8     138  Horn
  9     274  Lead Guitr
 10     274  Lead GtEko
 11      76  Orc Hit
 12    1115  Drums
 13     179  Timpani
```

Split a MIDI file to listen to individual tracks:

```
midisplit --help
usage: midisplit [-h] [--out OUTPATH] inpath

Split a single MIDI file into multiple MIDI files, one for each track.

positional arguments:
  inpath         Input MIDI file

optional arguments:
  -h, --help     show this help message and exit
  --out OUTPATH  Output folder for single-track MIDI files (defaults to
                 current directory)
```

Create a BASIC file from three tracks in a MIDI file:

```
midi2basic --help
usage: midi2basic [-h] inpath outpath

Creates BASIC file form three tracks of a MIDI file.

positional arguments:
  inpath      Input MIDI file
  outpath     Output BASIC file

optional arguments:
  -h, --help  show this help message and exit
```
