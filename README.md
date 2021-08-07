# Ufrj Analytica Training

Implementations and analysis that contributes for the Ufrj Analytica Training Project 

## Spotify API Function Summary

- get_track_artist_id(track, artist): recieves 2 strings the track name and the artist name, then returns a dictionary with "track_id" and "artist_id" as keys.
- get_genres(): returns a list of spotify's genres.
- get_audio_description(id): recieves the track id and returns a dictionary with audio descriptions.
- get_tracks_by_year(year): recieves the year as an int and returns a dictionary with  "track_id",  "artist_id", "track_name" and "artist" as keys. Each key contains a list of 1000 values corresponding to the specific year.

## Note

You should learn how to get the api's authorization before using this class. For instancing this class you need: an username, a client_id, a client_secret, a redirect_uri, a scope. To do so, I recommend this medium article:  https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3
