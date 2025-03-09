import os
import re
import urllib.parse
import yt_dlp as youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json

# Stores the Spotify API token and user ID for making authorized API requests
spotify_token = 'BQBedx-SyaPrIziLjdDpNLbhdrGGeg_5LhUfo_GFFT9LCDGVcrOu4ewbclnPKYbtI_X6IdxyRf_LFI8f4AkFh7lgJkQ6WJG1USCiNUfg7DILjYnovRF2PXNem-Cb3JYlg5WscAgLC6U'
spotify_user_id = 'c809b977677b45bcb6eb07936cd699be'

# Define the scopes for the YouTube API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Set up Spotify client with automatic token management
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='c809b977677b45bcb6eb07936cd699be',
    client_secret='616baaf2d66b430f95564bc3e08fc746',
    redirect_uri='http://localhost:3000',
    scope="playlist-modify-public playlist-modify-private"
))

def get_play():

    # Fetches playlist data from YouTube using the YouTube Data API v3
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only during development!
 
    api_service_name = "youtube"
    api_version = "v3"

    # Get the path to the client secrets file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    client_secrets_file = os.path.join(dir_path, "clientSecretYT.json")
 
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
 
    # Make API request to get playlist items
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="PL61tGsgg52oXJuGWW-11eZ2DIXF059A0-"
    )
    response = request.execute()
 
    return response

def extract_song_from_yt(dic):

    # Extracts song and artist information from YouTube playlist data
    url = "https://www.youtube.com/watch?v="
    info = []
    ydl_opts = {
        'quiet': True,  # Suppresses most console output
        'no_warnings': True,  # Suppresses warnings
        'ignoreerrors': True  # Continue on download errors
    }

    for item in dic["items"]:
        video_url = url + item["snippet"]['resourceId']['videoId']
        title = item["snippet"]['title']
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                details = ydl.extract_info(video_url, download=False)
            # Attempt to parse title in the format "Artist - Track"
            match = re.match(r"(.+?)\s*-\s*(.+)", title)
            if match:
                artist, track = match.groups()
                info.append((track, artist))
            else:
                print(f"Could not parse title: {title}")
        except Exception as e:
            print(f"Error extracting video {video_url}: {str(e)}")

    return info

def clean_title(title):

    # Remove common suffixes and other non-essential parts of titles
    title = re.sub(r"\(official.*?\)", "", title, flags=re.I)
    title = re.sub(r"\[official.*?\]", "", title, flags=re.I)
    title = re.sub(r"\(lyric.*?\)", "", title, flags=re.I)
    title = re.sub(r"\[lyric.*?\]", "", title, flags=re.I)
    title = title.strip()
    return title

def get_spotify_uri(track, artist):

    # Search Spotify for a track and artist and return the track URI if found
    track = urllib.parse.quote(clean_title(track))  # URL encode the track
    artist = urllib.parse.quote(clean_title(artist))  # URL encode the artist
    query = f"https://api.spotify.com/v1/search?query=track%3A{track}+artist%3A{artist}&type=track"
    response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": f"Bearer {spotify_token}"})
    
    print("Spotify Query:", query)  # Print the query to debug
    if response.status_code == 200:
        songs = response.json()["tracks"]["items"]
        if songs:
            return songs[0]["uri"]
        else:
            print(f"No results found for {track} by {artist}")
            return None
    else:
        print(f"Failed to search Spotify for {track} by {artist}: {response.status_code} - {response.text}")
        return None

def create_playlist(spotify_user_id):
    # Create A New Playlist using user's Spotify ID
    playlist = sp.user_playlist_create(user=sp.me()['id'], name="Test Playlist", public=True, description="Songs")
    return playlist['id']

def add_song(spotipy_client, playlist_id, urls):

    # Add songs to Spotify playlist
    if not urls:
        print("No URLs provided to add to the playlist.")
        return "No songs to add."
    
    try:
        results = spotipy_client.playlist_add_items(playlist_id, urls)
        print("Songs added successfully to the playlist:", results)
        return "Songs were added successfully"
    except spotipy.SpotifyException as e:
        print(f"Failed to add songs: {e}")
        return f"Failed to add songs, error: {str(e)}"

# Fetch data from YouTube
response = get_play()
print("YouTube Response:", response)

# Get track name and artist name form yt
song_info = extract_song_from_yt(response)
print("Extracted Song Info:", song_info)

if song_info:
    # Create Spotify playlist
    play_id = create_playlist(spotify_user_id)
    print("Created Spotify Playlist ID:", play_id)

    # Get URLs for Spotify songs
    urls = [get_spotify_uri(track, artist) for track, artist in song_info if track and artist]
    print("Spotify URLs:", urls)

    # Add songs to the new playlist
    if urls:
        add_song(sp, play_id, urls)
else:
    print("No valid song data extracted from YouTube.")