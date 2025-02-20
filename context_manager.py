import os
import pyautogui
import keyboard
import time
from database_handler import get_conversation_history, update_conversation_history
from gemini_handler import generate_response
from file_manager import (
    open_directory, create_directory, rename_file, delete_file, list_files,
    navigate_to_path, open_file, open_application, copy_file, move_file
)

current_directory = os.path.expanduser("~")

def extract_after_keyword(user_input, keyword):
    if keyword in user_input:
        result = user_input.split(keyword, 1)[1].strip()
        if result.lower().startswith("the "):
            result = result[4:].strip()
        return result
    return None

def generate_contextual_response(user_input, user_id):
    global current_directory
    
    file_response = handle_file_commands(user_input)
    if file_response is not None:
        update_conversation_history(user_id, user_input, file_response)
        return file_response
    
    history = get_conversation_history(user_id)
    context = "\n".join([f"User: {item['user']}\nNova: {item['nova']}" for item in history])
    prompt = f"{context}\nUser: {user_input}\nNova: Respond concisely."
    
    nova_response = generate_response(prompt)
    update_conversation_history(user_id, user_input, nova_response)
    return nova_response

def handle_file_commands(user_input):
    global current_directory
    user_input_lower = user_input.lower()

    if "open notepad" in user_input_lower:
        return open_application("notepad")

    if "modify" in user_input_lower and "with notepad" in user_input_lower:
        file_name = user_input_lower.replace("modify", "").replace("with notepad", "").strip()
        if file_name:
            file_path = os.path.join(current_directory, file_name)
            return open_file(file_path, "notepad")
        return "Specify a file to modify."

    if "type" in user_input_lower:
        text = user_input_lower.replace("type", "").strip()
        pyautogui.write(text)
        return f"Typed: {text}"

    if "select all" in user_input_lower:
        send_keys(["ctrl", "a"])
        return "Selected all text."

    if "copy file" in user_input_lower:
        try:
            command_part = user_input_lower.split("copy file", 1)[1].strip()
            parts = command_part.split(" to ")
            if len(parts) == 2:
                source_file = parts[0].strip()
                dest_file = parts[1].strip()
                source_path = os.path.join(current_directory, source_file)
                dest_path = os.path.join(current_directory, dest_file)
                return copy_file(source_path, dest_path)
            else:
                return "Specify source and destination file names for copying."
        except Exception as e:
            return f"Error processing copy file command: {str(e)}"

    if "copy" in user_input_lower:
        send_keys(["ctrl", "c"])
        return "Copied selected text."

    if "paste" in user_input_lower:
        send_keys(["ctrl", "v"])
        return "Pasted clipboard content."

    if "cut" in user_input_lower:
        send_keys(["ctrl", "x"])
        return "Cut selected text."

    if "undo" in user_input_lower:
        send_keys(["ctrl", "z"])
        return "Undid last action."

    if "redo" in user_input_lower:
        send_keys(["ctrl", "y"])
        return "Redid last action."

    if "find" in user_input_lower:
        search_text = user_input_lower.replace("find", "").strip()
        send_keys(["ctrl", "f"])
        time.sleep(1)
        pyautogui.write(search_text)
        send_keys(["enter"])
        return f"Searched for '{search_text}'."

    if "replace" in user_input_lower and "with" in user_input_lower:
        parts = user_input_lower.replace("replace", "").split("with")
        old_text = parts[0].strip()
        new_text = parts[1].strip()
        send_keys(["ctrl", "h"])
        time.sleep(1)
        pyautogui.write(old_text)
        send_keys(["tab"])
        pyautogui.write(new_text)
        send_keys(["enter"])
        return f"Replaced '{old_text}' with '{new_text}'."

    if "save file as" in user_input_lower:
        file_name = user_input_lower.replace("save file as", "").strip()
        send_keys(["ctrl", "shift", "s"])
        time.sleep(1)
        pyautogui.write(file_name)
        send_keys(["enter"])
        return f"Saved file as '{file_name}'."

    if "save file" in user_input_lower:
        send_keys(["ctrl", "s"])
        return "Saved file."

    if "close notepad" in user_input_lower:
        send_keys(["alt", "f4"])
        return "Closed Notepad."

    if "open file explorer" in user_input_lower:
        response = open_directory(current_directory)
        return response

    if "go out" in user_input_lower:
        new_path = navigate_to_path("go out", current_directory)
        if not new_path.lower().startswith("error"):
            current_directory = new_path
            open_directory(current_directory)
            return f"Moved out to: {current_directory}"
        else:
            return new_path

    if "go to" in user_input_lower:
        path = extract_after_keyword(user_input_lower, "go to")
        if path:
            new_path = navigate_to_path(path, current_directory)
            if not new_path.lower().startswith("error"):
                current_directory = new_path
                open_directory(current_directory)
                return f"Navigated to: {current_directory}"
            else:
                return new_path
        return "Specify a path to navigate to."

    if "list files" in user_input_lower:
        return list_files(current_directory)
    
    if "create folder" in user_input_lower:
        folder_name = extract_after_keyword(user_input_lower, "create folder")
        if folder_name:
            response = create_directory(os.path.join(current_directory, folder_name))
            return response
        return "Specify a folder name."
    
    if "rename" in user_input_lower and " to " in user_input_lower:
        try:
            command_part = user_input_lower.split("rename", 1)[1]
            old_name, new_name = command_part.split(" to ", 1)
            old_name = old_name.strip()
            new_name = new_name.strip()
            if old_name and new_name:
                return rename_file(
                    os.path.join(current_directory, old_name),
                    os.path.join(current_directory, new_name)
                )
            return "Specify old and new names."
        except Exception as e:
            return f"Error processing rename command: {str(e)}"
    
    if "delete" in user_input_lower:
        file_name = extract_after_keyword(user_input_lower, "delete")
        if file_name:
            return delete_file(os.path.join(current_directory, file_name))
        return "Specify a file to delete."
    
    if "move file" in user_input_lower:
        try:
            command_part = user_input_lower.split("move file", 1)[1].strip()
            parts = command_part.split(" to ")
            if len(parts) == 2:
                source_file = parts[0].strip()
                dest_file = parts[1].strip()
                source_path = os.path.join(current_directory, source_file)
                dest_path = os.path.join(current_directory, dest_file)
                return move_file(source_path, dest_path)
            else:
                return "Specify source and destination for moving file."
        except Exception as e:
            return f"Error processing move file command: {str(e)}"
        
    if "open" in user_input_lower:
        if "youtube" in user_input_lower:
            return open_application("open youtube")
        elif "browser" in user_input_lower:
            return open_application("open browser")
        elif "vs code" in user_input_lower or "visual studio code" in user_input_lower:
            return open_application("open vs code")
        elif "notepad" in user_input_lower:
            return open_application("open notepad")
        elif "calculator" in user_input_lower:
            return open_application("open calculator")
        elif "file explorer" in user_input_lower:
            return open_application("open file explorer")
        elif "pictures" in user_input_lower:
            return open_application("open pictures")
        elif "documents" in user_input_lower:
            return open_application("open documents")
        elif "downloads" in user_input_lower:
            return open_application("open downloads")
        elif "music" in user_input_lower:
            return open_application("open music")
        else:
            return "Command not recognized."
    return None

def send_keys(keys):
    for key in keys:
        keyboard.press_and_release(key)
        time.sleep(0.1)