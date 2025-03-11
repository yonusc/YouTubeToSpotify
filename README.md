# YouTube to Spotify Playlist Automation

## About

This project automates the process of transferring music playlists from YouTube to Spotify. It leverages the YouTube Data API to fetch playlist details from YouTube and the Spotify Web API to create and manage playlists on Spotify. This tool is designed for users who enjoy curated YouTube music playlists and want to seamlessly integrate them into their Spotify account.

## Getting Started

## Prerequisites

To run this application, you'll need the following installed on your system:
- Python 3.13
- pip (Python package installer)

### Dependencies

This project depends on several Python libraries, which can be installed using pip. Below are the necessary libraries:
- `google-auth-oauthlib` for OAuth handling with Google APIs.
- `google-api-python-client` for accessing the YouTube Data API.
- `youtube-dl` for extracting video details (Note: `youtube-dl` often updates due to changes in YouTube's API, so use `yt-dlp` as an alternative if issues arise).
- `spotipy` for interacting with the Spotify Web API.
- `requests` for making HTTP requests.
- `json` for handling JSON data, included with Python.

To install these dependecies, run the following command:

- python -m pip install google-auth-oauthlib google-api-python-client yt-dlp spotipy requests

#### Configuration

- Spotify API: You need to register the application at Spotify Developer Dashboard (https://developer.spotify.com/dashboard) to get the client_id and client_secret. Set up the redirect URI as http://localhost:3000/ or another URI of your choice.

- YouTube API: Enable the YouTube Data API v3 via the Google Developers Console (https://console.cloud.google.com/) and download the client configuration. Save this file as clientSecretYT.json at the root of the project directory.

- Create a .env file at the root of the directory containing: 
    SPOTIFY_TOKEN=your_spotify_token_here
    SPOTIFY_USER_ID=your_spotify_user_id_here
    SPOTIFY_CLIENT_ID=your_spotify_client_id_here
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here


#### Usage

Navigate to the project directory and run the script:

- 'python ex.spotifyToken.py', copy and paste the result into "spotify_token" in main.py
- 'python main.py'

##### How It Works

The script performs several key steps:

- Authenticates the user using OAuth for both YouTube and Spotify.
- Fetches a list of videos from a specified YouTube playlist.
- Extracts the title and artist from each video and searches for the song on Spotify.
- If the song is found on Spotify, it adds it to a new Spotify playlist.

##### Limitations

- The accuracy of transferring songs depends on the availability of the songs on Spotify and the accuracy of the video titles on YouTube.
- YouTube videos without clear artist and song title information may not be correctly transferred.
