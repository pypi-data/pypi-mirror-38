def print_trackinfo(trackinfo):
    print("  #  Tones   Track Name")
    print("---  ------  ------------------------------")
    for idx, track in trackinfo.items():
        print(f"{str(idx).rjust(3)}  {str(track['tones']).rjust(6)}  {track['name'][:30]}")


def input_tracklist(validate_length=None, default=None):
    default_info = " [press enter for all]" if default else ""
    tracklist = input(
        f"Select tracks as comma separated list, e.g. 2,6,7{default_info} ")

    tracklist = tracklist.strip().strip(',')
    if default and tracklist == "":
        tracklist = default
    else:
        tracklist = [int(el.strip()) for el in tracklist.split(',')]

    if validate_length:
        assert len(tracklist) == validate_length, f"Expected {validate_length} tracks, got {len(tracklist)}"

    return tracklist
