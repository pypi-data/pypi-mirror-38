# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['superconf18_midibadge', 'superconf18_midibadge.tools']

package_data = \
{'': ['*']}

install_requires = \
['midi', 'toml>=0.9,<0.10']

entry_points = \
{'console_scripts': ['midi2basic = superconf18_midibadge.tools.midi2basic:main',
                     'midi3track = superconf18_midibadge.tools.midi3track:main',
                     'midiinfo = superconf18_midibadge.tools.midiinfo:main',
                     'midisplit = superconf18_midibadge.tools.midisplit:main']}

setup_kwargs = {
    'name': 'superconf18-midibadge',
    'version': '0.2.0',
    'description': 'Generate Basic code for the Hackaday Superconf 2018 Badge from a MIDI file',
    'long_description': 'superconf18-midibadge\n=====================\n\n\nGenerate Basic code for the Hackaday Superconf 2018 Badge from a MIDI file\n\n\n## Quickstart\n\nInstall:\n\n```\npip install superconf18_midibadge\n```\n\nSee what tracks are in a MIDI file:\n\n```\nmidiinfo --help\nusage: midiinfo [-h] inpath\n\nPrints a table of tracks in the given MIDI file.\n\npositional arguments:\n  inpath      Input MIDI file\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\n```\nmidiinfo example.mid\nThese tracks in MIDI file example.mid contain sound:\n\n  #  Tones   Track Name\n---  ------  ------------------------------\n  1     143  Lead Vox\n  2     139  Lead Vox 2\n  3    1921  Piano\n  4     481  Bass\n  5     780  Strings\n  6     263  Choir\n  7     155  Brass\n  8     138  Horn\n  9     274  Lead Guitr\n 10     274  Lead GtEko\n 11      76  Orc Hit\n 12    1115  Drums\n 13     179  Timpani\n```\n\nSplit a MIDI file to listen to individual tracks:\n\n```\nmidisplit --help\nusage: midisplit [-h] [--out OUTPATH] inpath\n\nSplit a single MIDI file into multiple MIDI files, one for each track.\n\npositional arguments:\n  inpath         Input MIDI file\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --out OUTPATH  Output folder for single-track MIDI files (defaults to\n                 current directory)\n```\n\nCreate a BASIC file from three tracks in a MIDI file:\n\n```\nmidi2basic --help\nusage: midi2basic [-h] inpath outpath\n\nCreates BASIC file form three tracks of a MIDI file.\n\npositional arguments:\n  inpath      Input MIDI file\n  outpath     Output BASIC file\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n',
    'author': 'Jonas Neubert',
    'author_email': 'jn@jonasneubert.com',
    'url': 'https://github.com/jonemo/superconf18-midibadge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
