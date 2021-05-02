import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import model
from time import sleep
from os import system as sys

def getCreds():
    #filename = input("creds filename: ")
    #sys("clear")
    filename = "c" + ".txt"
    
    with open(filename) as f:
        lines = f.readlines()
    
    return lines[0].rstrip(), lines[1].rstrip(), lines[2].rstrip()

# login without user authentication
def without(clientID, secret):
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
        client_id=clientID, 
        client_secret=secret
        ))
    
# login with user authentication (needed for playback ops)
def withAuth(clientID, secret, redi):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID, 
    client_secret=secret, 
    redirect_uri=redi,
    scope="user-read-playback-state user-modify-playback-state"
    ))

# ask Spotify is user is currently playing a song, pause/play will
# crash if this API request is done without considering this
def isCurrentlyPlaying():
    return sp.current_user_playing_track()["is_playing"]

if __name__ == "__main__":
    sys("clear")
    clientID, secret, redi = getCreds()
    sp = withAuth(clientID, secret,redi)
    threshold = 60
    
    start = "n"
    while start != "y":
        start = input("Enter \"y\" to start: ")
    
    while True:
        
        # ask for action every second (getting action takes ~5s)
        sleep(1)
        
        # take picture and determine what action needs to be taken
        # and probability of action requested
        cmd, highP = model.get_action(threshold)
        print(cmd, highP)
        
        # low probability of what user is doing, no action taken
        # or user not making any request
        if not highP or cmd == "Neutral":
            continue
            
        try:
            if cmd == "Next":
                sp.next_track()
            elif cmd == "Previous":
                sp.previous_track()
            elif cmd == "Pause/Play":
                if isCurrentlyPlaying():
                    sp.pause_playback()
                else:
                    sp.start_playback()
        except:
            pass
        
     
