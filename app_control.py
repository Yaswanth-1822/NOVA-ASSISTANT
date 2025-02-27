import os
import pyautogui
import time
import subprocess
import pygetwindow as gw
import webbrowser
from whatsapp_control import open_whatsapp
# from file_manager import FileManager
from gmail_control import open_gmail
# file_manager = FileManager()
from mediaplayer import close_media_app, open_media_app


def open_application(command):
        # Open Gmail command
    if "open gmail" in command:
        return open_gmail()
        # Command: "open whatsapp"
    if "open whatsapp" in command:
        return open_whatsapp()
    if "notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Notepad opened."
    elif "calculator" in command:
        os.system("calc")
        return "Calculator opened."
    elif "file explorer" in command or "open explorer" in command:
        os.system("start explorer")
        return "File Explorer opened."
    elif "open vs code" in command or "open visual studio code" in command:
        VS_CODE_FOLDER = "D:\Testing"
        os.system(f"code {VS_CODE_FOLDER}")
        print(f"Opened VS Code in {VS_CODE_FOLDER}")
    elif "open google" in command or "open browser" in command:
        try:
            webbrowser.get("chrome").open("https://www.google.com")
            return "Opened Google in Chrome."
        except webbrowser.Error:
            print("Chrome not found. Trying Edge...")
            os.system("start msedge https://www.google.com")
            return "Opened Google in Edge."
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opened YouTube."
    elif "open twitter" in command:
        webbrowser.open("https://www.twitter.com")
        return "Opened Twitter."
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opened Facebook."
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Opened Gmail."
    elif "open pictures" in command:
        os.startfile(os.path.expanduser("~/Pictures"))
        return "Opened Pictures folder."
    elif "open documents" in command:
        os.startfile(os.path.expanduser("~/Documents"))
        return "Opened Documents folder."
    elif "open downloads" in command:
        os.startfile(os.path.expanduser("~/Downloads"))
        return "Opened Downloads folder."
    elif "open music floder" in command:
        os.startfile(os.path.expanduser("~/Music"))
        return "Opened Music folder."
    elif "open music" in command or "open video" in command:
        open_media_app()
    else:
        return "Application or command not recognized."
    

def close_application(command):
    if "notepad" in command:
        os.system("taskkill /f /im notepad.exe")
    elif "calculator" in command:
        os.system("taskkill /f /im calc.exe")
    elif "file explorer" in command or "close explorer" in command:
        os.system("taskkill /f /im explorer.exe")
    elif "browser" in command or "close browser" in command:
        browsers = ["chrome.exe", "msedge.exe", "firefox.exe", "brave.exe"]
        for browser in browsers:
            os.system(f"taskkill /f /im {browser}")
        print("Closed all browsers.")
    elif "close pictures" in command or "close documents" in command or "close downloads" in command or "close music" in command:
        os.system("taskkill /f /im explorer.exe")
        print("Closed all opened folders.")
    elif "close vs code" in command or "close visual studio code" in command:
        os.system("taskkill /F /IM Code.exe")
    elif "close media player" in command or "close video" in command:
        close_media_app()
    elif "close instagram" in command or " close facebook" in command or "close youtube " in command :
        try:
        # ✅ Bring the browser to focus
            pyautogui.hotkey("alt", "tab")  
            time.sleep(1)

            # ✅ Select the address bar (Works for Chrome, Edge)
            pyautogui.hotkey("ctrl", "l")
            time.sleep(1)

            # ✅ Copy the URL (or tab title)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(1)

            # ✅ Paste the copied text into a temporary variable
            pyautogui.hotkey("ctrl", "v")  

            # ✅ Check if the tab is the one we want to close
            if command.lower() in pyautogui.hotkey("ctrl", "v").lower():
                pyautogui.hotkey("ctrl", "w")  # ✅ Close the tab
                return f"✅ Closed {command} tab."
            else:
                return f"❌ {command} tab not found."

        except Exception as e:
            return f"❌ Error closing {command} tab: {e}"

    else:
        print("Application not recognized.")


def type_in_notepad(command):
    try:
        text = command.replace("write", "").strip()
        time.sleep(0.5)
        pyautogui.write(text, interval=0)
        print(f"Typed in Notepad: {text}")
    except Exception as e:
        print(f"Error typing in Notepad: {e}")

def open_directory(command):
    try:
        path = command.replace("go to", "").strip()
        if os.path.exists(path):
            os.startfile(path)
        else:
            print("Directory not found.")
    except Exception as e:
        print(f"Error opening directory: {e}")


def close_directory():
    try:
        os.system("taskkill /f /im explorer.exe")
        print("Closed all File Explorer windows.")
    except Exception as e:
        print(f"Error closing directories: {e}")


def switch_drive(command):
    try:
        drive = command.replace("go to", "").replace("drive", "").strip().upper() + ":\\"
        if os.path.exists(drive):
            os.chdir(drive)
            print(f"Switched to {drive}")
        else:
            print("Drive not found.")
    except Exception as e:
        print(f"Error switching drive: {e}")


def save_notepad_file(command):
    try:
        filename = command.replace("save as", "").strip() + ".txt"
        file_path = os.path.join(os.getcwd(), filename)

        notepad_window = None
        for window in gw.getWindowsWithTitle("Untitled - Notepad"):
            notepad_window = window
            break

        if notepad_window:
            notepad_window.activate()
            time.sleep(1)
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1)
            pyautogui.write(filename, interval=0.1)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.press("enter")
            print(f"Notepad file saved as {filename}")
        else:
            print("Notepad window not found.")
    except Exception as e:
        print(f"Error saving Notepad file: {e}")