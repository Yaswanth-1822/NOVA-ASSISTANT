import pyautogui

def control_youtube(action):
    if action == "play" or action == "pause":
        pyautogui.press("space")  # ✅ Simulate pressing Spacebar for Play/Pause
        return f"YouTube {action} command executed."
    return f"❌ Unsupported YouTube action: {action}"
