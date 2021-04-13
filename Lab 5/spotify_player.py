import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import model

def getCreds():
    filename = input("creds filename: ")
    filename = filename + ".txt"
    
    with open(filename) as f:
        lines = f.readlines()
    
    return lines[0].rstrip(), lines[1].rstrip(), lines[2].rstrip()

def without(clientID, secret):
    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
        client_id=clientID, 
        client_secret=secret
        ))
    

def withAuth(clientID, secret, redi):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID, 
    client_secret=secret, 
    redirect_uri=redi,
    scope="user-read-playback-state user-modify-playback-state"
    ))
    
def isCurrentlyPlaying():
    return sp.current_user_playing_track()["is_playing"]

if __name__ == "__main__":
    clientID, secret, redi = getCreds()
    sp = withAuth(clientID, secret,redi)
    threshold = 60
    
    while True:
        
        try:
            print(sp.current_user_playing_track()["is_playing"])
        except:
            pass
            
        time.sleep(1)
        cmd, highP = model.get_action(threshold)
        
        if not highP:
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
        
     
