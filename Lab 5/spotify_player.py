import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def getCreds():
    filename = input("creds filename: ")
    filename = filename + ".txt"
    
    with open(filename) as f:
        lines = f.readlines()
    
    return lines[0].rstrip(), lines[1].rstrip(), lines[2].rstrip()

def without(clientID, secret):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID, client_secret=secret))

def withAuth(clientID, secret, redi):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=secret, redirect_uri=redi))

if __name__ == "__main__":
    clientID, secret, redi = getCreds()
    sp = withAuth(clientID, secret,redi)
    print(sp.current_user_playing_track())
     
