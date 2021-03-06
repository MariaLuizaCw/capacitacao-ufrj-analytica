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
    def get_tracks_by_year(self, year):
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
    def search_track(self, track_name, artist):
        self.geneate_token()
        track_name = track_name.replace("#", "")
        url = f'https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist}&type=track'
        response = requests.get(url ,headers = self.headers, timeout = 5)
        tracks = response.json()["tracks"]["items"]
        keyList = ["id", "popularity", "explicit", "artist_id"]
        if len(tracks) > 0 and response.status_code == 200:
            track_data = {key: tracks[0][key] for key in keyList[:-1]}
            track_data[keyList[-1]] = tracks[0]["artists"][0]["id"]
            return track_data
        return {key: None for key in keyList}
    def get_genres(self):
        self.geneate_token()
        url  = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        response = requests.get(url,headers = self.headers, timeout = 5)
        return response.json()["genres"]
    def get_audio_description(self, id):
        if id:
            self.geneate_token()
            url = f"https://api.spotify.com/v1/audio-features/{id}"
            response = requests.get(url,headers = self.headers, timeout = 5)
            return response.json()
        else:
            return {}
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
    def get_artist_albums_description(self, id):
        self.geneate_token()
        url =  f"https://api.spotify.com/v1/artists/{id}/albums"
        response = requests.get(url, headers = self.headers, timeout = 5)
        albumsJson = response.json()
        albums = albumsJson["items"]
        albums_description = []
        for album in albums:
            albums_description.append({"id": album["id"], "name": album["name"]})
        return albums_description
    def get_album_tracks(self, id):
        self.geneate_token()
        url = f"https://api.spotify.com/v1/albums/{id}/tracks"
        response = requests.get(url, headers = self.headers, timeout = 5)
        tracksJson = response.json()
        tracks = tracksJson["items"]
        tracks_description = []
        for track in tracks:
            tracks_description.append({"id": track["id"], "name": track["name"], "duration": track["duration_ms"]})
        return tracks_description
    def get_artist_tracks(self, id):
        self.geneate_token()
        tracks_description = []
        albums_description = self.get_artist_albums_description(id)
        for album in albums_description:
            tracks = self.get_album_tracks(album["id"])
            tracks_description = tracks_description + tracks
        return tracks_description
    # def get_tracks_by_date(self, date):
    #     self.geneate_token()
    #     keys = ['id', "name", "popularity", "explicit", "release_date", "artist", "artist_id"]
    #     tracks_artists = {key: [] for key in keys}
    #     params={'q': f"day:{date}", 'type':'track', 'limit': 1, 'offset': 0}   
    #     url = "https://api.spotify.com/v1/search"
    #     response = requests.get(url, params= params, headers = self.headers, timeout = 5)
    #     total = response.json()["tracks"]["total"]
    #     num_requests = total//50
    #     left_requests = total % 50
    #     while num_requests+1:
    #         num_requests -= 1
    #         params["limit"] = 50 if num_requests > 0 else left_requests 
    #         response = requests.get(url, params= params, headers = self.headers, timeout = 5)
    #         json_response = response.json()
    #         for track in json_response["tracks"]["items"]:
    #             for key in keys[:-3]:
    #                 tracks_artists[key].append(track[key])
    #             tracks_artists["release_date"].append(track["album"]["release_date"])
    #             tracks_artists["artist_id"].append(track["artists"][0]["id"])
    #             tracks_artists["artist"].append(track["artists"][0]["name"])
    #         params["offset"] += 50
    #     return response.json()
