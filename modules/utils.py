
#remove from the list of all tracks the repeated ones 
def remove_repeated_tracks(tracks):
    repeated_tracks = tracks
    not_repeated_tracks_names = []
    filtered_tracks = []
    for track in repeated_tracks:
        if(track["name"].strip() not in not_repeated_tracks_names):
            not_repeated_tracks_names.append(track["name"].strip())
            filtered_tracks.append(track)
            
    return filtered_tracks