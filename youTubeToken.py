import os
import google_auth_oauthlib.flow 
import googleapiclient.discovery
import googleapiclient.errors
 
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
 
 
def main():
   
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
 
    print(response)
 
if __name__ == "__main__":
    main()
