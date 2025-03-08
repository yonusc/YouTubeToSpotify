import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp as youtube_dl
import youtube_dl
import requests
import json

spotify_token = 'BQDDeZ8OdeIH3UuwiWnHMLY-KRgaxHpyOk8jAfbheaotm641xGElWDKlD_sAAgpW9PAS2sfMHvcpw__hof3w2Dm25v50OgOrIyuKycQs4UpiGesL3k8vmfcyJKnIWCuLb8lziKdeLDM'
spotify_user_id = 'c809b977677b45bcb6eb07936cd699be'
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Set up Spotify client with automatic token management
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='c809b977677b45bcb6eb07936cd699be',
    client_secret='616baaf2d66b430f95564bc3e08fc746',
    redirect_uri='http://localhost:3000',
    scope="playlist-modify-public playlist-modify-private"
))

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
 
        info.append((track, artist))
    return info

def get_spotify_uri(track, artist):
    """Search For the Song"""

    query = "https://api.spotify.com/v1/search?query=track%3A{}_artist%4A{}&type=track".format(
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

    print("Status Code:", response.status_code)
    print("Headers Sent:", response.request.headers)
    print("API Response:", response.json())
    
    songs = response["tracks"]["items"]

    url = songs[0]["uri"]

    return url


def create_playlist(spotify_user_id):
    """Create A New Playlist using user's Spotify ID"""
    playlist = sp.user_playlist_create(user=sp.me()['id'], name="Test Playlist", public=True, description="Songs")
    return playlist['id']

# Use this function to create a playlist and catch any exceptions if failed
try:
    playlist_id = create_playlist(spotify_user_id)
    print("Created playlist with ID:", playlist_id)
except Exception as e:
    print("Failed to create playlist:", e)

def add_song(playlist_id, urls):
    """Add all songs into the new Spotify playlist"""

    request_data = json.dumps(urls)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
    
    response = requests.post(
        query,
        data = request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )

    print("Status Code:", response.status_code)
    print("Headers Sent:", response.request.headers)
    print("API Response:", response.json())
    
    return "Songs were added successfully"

# Fetch data from YouTube
response = get_play()

# Create Spotify playlist
play_id = create_playlist(spotify_user_id)

# Get track name and artist name form yt
song_info = extract_song_from_yt(response)

# Get URLs for Spotify songs
urls = []
for i in range(len(response['items'])):
    urls.append(get_spotify_uri(song_info[i][0], song_info[i][1]))

# Add songs to new playlist
add_song(play_id, urls)