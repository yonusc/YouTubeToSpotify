import os
import spotipy
from spotipy import SpotifyOAuth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
import requests
import json

spotify_token = 'BQBdV0g9vfP_PM1BHOZy7VDzoxKFtg2ikGUcLenze3Dojfo-iTNcF6BU9QHRS8h95xZcRfuHBc_645h6TPZdF5mo3hbxyuUuezgFXvUCBCbjUJ-p6EQ'
spotify_user_id = 'c809b977677b45bcb6eb07936cd699be'
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

scope = "playlist-modify-public playlist-modify-private"
sp_oauth = SpotifyOAuth(client_id='c809b977677b45bcb6eb07936cd699be',
                        client_secret='616baaf2d66b430f95564bc3e08fc746',
                        redirect_uri='http://localhost:3000',
                        scope=scope)

def get_play():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only during development!
 
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "C:/Users/yonus/Documents/GitHub/YouTubeToSpotify/clientSecretYT.json"
 
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
 
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="PL61tGsgg52oXJuGWW-11eZ2DIXF059A0-"
    )
    response = request.execute()
 
    return response

def extract_song_from_yt(dic):
    """Fetch song name from Youtube"""
 
    url = "https://www.youtube.com/watch?v="
    info = []
    song = ""
    for i in range(len(dic["items"])):
 
        video_url = url+str(dic["items"][i]["snippet"]
                            ['resourceId']['videoId'])
        details = youtube_dl.YoutubeDL(
            {}).extract_info(video_url, download=False)
        track, artist = details['track'], details['artist']
 
        info.append((track,artist))
    return info

def get_spotify_uri(track, artist):
    """Search For the Song"""
 
    query = "https://api.spotify.com/v1/search?\
    query=track%3A{}+artist%3A{}&type=track".format(
        track,
        artist
    )
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response = response.json()
    songs = response["tracks"]["items"]
 
    url = songs[0]["uri"]
 
    return url
 
def create_playlist():
    """Create A New Playlist"""
    request_body = json.dumps(
        {
            "name": "Test Playlist",
            "description": "Songs",
            "public": True,
        }
    )
 
    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        spotify_user_id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token),
        },
    )
    response_json = response.json()
    print(response_json)  # Print the whole response
    return response_json.get("id") 

def add_song(playlist_id, urls):
    """Add all liked songs into a new Spotify playlist"""
 
    request_data = json.dumps(urls)
 
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
 
    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
 
    return "songs added successfully"
 
# fetching data from youtube
response = get_play()
 
# creating spotify playlist
play_id = create_playlist()
 
# getting track name and  artist name form yt
song_info = extract_song_from_yt(response)
 
# getting url for spotify songs
 
urls = []
for i in range(len(response['items'])):
    urls.append(get_spotify_uri(song_info[i][0], song_info[i][1]))
 
# adding song to new playlist
add_song(play_id, urls)