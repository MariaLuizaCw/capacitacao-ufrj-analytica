import requests
import spotipy.util as util


class SpotApi:
    def __init__(self, username, client_id, client_secret, redirect_uri, scope):
        self.username =  username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def geneate_token(self):
        self.token = util.prompt_for_user_token(
            username=self.username, 
            scope=self.scope, 
            client_id=self.client_id,   
            client_secret=self.client_secret,     
            redirect_uri=self.redirect_uri
        )
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer ' + self.token
        }  

    def get_tracks_by_year(self, year, number_of_tracks=1000):
        self.geneate_token()
        tracks_artists = {'track_id': [], "track_name": [], "artist": [], "artist_id": []}
        yearRange = f'year:{year}'
        params={
            'q': yearRange,
            'type':'track',
            'limit':50,
            'offset': 0
        }   
        url = "https://api.spotify.com/v1/search"
        for requets in range(20):
            response = requests.get(url, params= params ,headers = self.headers, timeout = 5)
            json_response = response.json()
            for track in json_response["tracks"]["items"]:
                tracks_artists["track_id"].append(track["id"])
                tracks_artists["track_name"].append(track["name"])
                tracks_artists["artist_id"].append(track["artists"][0]["id"])
                tracks_artists["artist"].append(track["artists"][0]["name"])
            params["offset"] += 50
        return tracks_artists

        
    def get_track_artist_id(self, track_name, artist):
        self.geneate_token()
        url = f'https://api.spotify.com/v1/search?q=track:"{track_name}"%20artist:"{artist}"&type=track'
        response = requests.get(url ,headers = self.headers, timeout = 5)
        track = response.json()["tracks"]["items"][0]
        return {"track_id": track["id"], "artist_id": track["artists"][0]["id"]}

    def get_genres(self):
        self.geneate_token()
        url  = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        response = requests.get(url,headers = self.headers, timeout = 5)
        return response.json()["genres"]

    def get_audio_description(self, id):
        self.geneate_token()
        url = f"https://api.spotify.com/v1/audio-features/{id}"
        response = requests.get(url,headers = self.headers, timeout = 5)
        return response.json()
    def get_artist_description(self, id):
        self.geneate_token()
        url = f"https://api.spotify.com/v1/artists/{id}"
        response = requests.get(url, headers = self.headers, timeout = 5)
        artist = response.json()
        artist_description = {
            "popularity": artist["popularity"],
            "genres": artist["genres"],
            "followers" :  artist["followers"]["total"]
        }
        return artist_description

