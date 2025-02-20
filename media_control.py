import os

def play_media(command):
    if "song" in command:
        os.system("start example.mp3")
    else:
        print("Media not recognized.")