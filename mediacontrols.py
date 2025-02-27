import pyautogui
import os
import subprocess

# ✅ Default music file (Leave empty if not set)
DEFAULT_MUSIC_FILE = ""  # Example: "C:\\Users\\Public\\Music\\Sample Music\\song.mp3"

def control_media(action):
    actions = {
        "pause": "playpause",  # Pause/Play toggle
        "play": "playpause",  # Try Play/Pause first
        "next": "nexttrack",  # Next song
        "previous": "prevtrack",  # Previous song
        "stop": "stop",  # Stop music
        "volume up": "volumeup",  # Increase volume
        "volume down": "volumedown",  # Decrease volume
    }

    if action == "play":
        # ✅ Try Play/Pause first
        pyautogui.press("playpause")
        print("✅ Sent Play/Pause command")

        # ✅ If nothing plays, check if default music exists
        if not is_music_playing():
            if DEFAULT_MUSIC_FILE and os.path.exists(DEFAULT_MUSIC_FILE):
                print("❌ No music detected, playing default song...")
                play_default_music()
                return "✅ Playing default music."
            else:
                print("❌ No default song found! Opening Windows Media Player...")
                open_media_player()
                return "❌ No default song found. Opened Windows Media Player."

        return "✅ Play command executed."

    if action in actions:
        pyautogui.press(actions[action])  # ✅ Send media key press
        print(f"✅ {action.capitalize()} command sent")
        return f"{action.capitalize()} command executed."

    print(f"❌ Unsupported media action: {action}")
    return f"Unsupported media action: {action}"

def is_music_playing():
    """Check if any media player is playing (Windows only)."""
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return "wmplayer.exe" in output or "vlc.exe" in output  # ✅ Adjust for your media player
    except Exception:
        return False

def play_default_music():
    """Play a default music file if nothing is playing."""
    try:
        os.startfile(DEFAULT_MUSIC_FILE)  # ✅ Open default song
    except Exception as e:
        print(f"❌ Error playing default music: {e}")

def open_media_player():
    """Open Windows Media Player if no default song is set."""
    try:
        os.system("start wmplayer")  # ✅ Open Windows Media Player
    except Exception as e:
        print(f"❌ Error opening media player: {e}")
