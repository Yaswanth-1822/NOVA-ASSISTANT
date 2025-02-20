import os
import shutil
import subprocess

# Mapping common app names to correct executables
APP_ALIASES = {
    "vs code": "code",  # VS Code CLI
    "notepad++": "notepad++.exe",
    "word": "winword.exe",
    "excel": "excel.exe"
}

def open_directory(path):
    """
    Open the given path in File Explorer.
    Handles keywords like "file explorer" and system folders.
    """
    try:
        if "file explorer" in path.lower():
            subprocess.Popen("explorer.exe")
            return "Opened File Explorer."
        
        system_folders = {
            "documents": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads"),
            "desktop": os.path.expanduser("~/Desktop"),
        }
        if path.lower() in system_folders:
            os.startfile(system_folders[path.lower()])
            return f"Opened {path} folder."
        
        if os.path.exists(path):
            os.startfile(path)
            return f"Opened: {path}"
        else:
            return f"Error: Path '{path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"

def create_directory(path):
    """Create a new directory."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created directory: {path}"
    except Exception as e:
        return f"Error: {str(e)}"

def rename_file(old_path, new_path):
    """Rename a file or directory."""
    try:
        os.rename(old_path, new_path)
        return f"Renamed '{old_path}' to '{new_path}'"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(path):
    """Delete a file or directory."""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"Deleted directory: {path}"
        else:
            os.remove(path)
            return f"Deleted file: {path}"
    except Exception as e:
        return f"Error: {str(e)}"

def list_files(path="."):
    """List files in a directory."""
    try:
        files = os.listdir(path)
        return f"Files in {path}: {', '.join(files)}"
    except Exception as e:
        return f"Error: {str(e)}"

def navigate_to_path(path, current_directory):
    """
    Determine a new directory based on the given path string.
    
    Recognizes:
      - Drive commands like "D drive"
      - Relative folder names
      - The "go out" command to move one level up.
    
    Returns either an absolute path (if found) or an error message.
    """
    try:
        if path.lower() in ["go out", "go out of"]:
            if current_directory.endswith(":\\"):
                if not current_directory.upper().startswith("C:"):
                    return os.path.expanduser("~")
                return current_directory
            else:
                new_path = os.path.dirname(current_directory.rstrip("\\"))
                return new_path if new_path else os.path.expanduser("~")
        
        parts = path.split()
        if len(parts) >= 2 and parts[1] == "drive":
            drive_letter = parts[0].upper()
            new_path = f"{drive_letter}:\\"
            if os.path.exists(new_path):
                return new_path
            else:
                return f"Error: Drive '{drive_letter}:' not found."
        
        if not os.path.isabs(path):
            new_path = os.path.join(current_directory, path)
        else:
            new_path = path
        
        if os.path.exists(new_path) and os.path.isdir(new_path):
            return new_path
        else:
            return f"Error: Path '{new_path}' not found or is not a directory."
    except Exception as e:
        return f"Error: {str(e)}"

def open_file(file_path, application=None):
    """Open a file with the default application or a specified application."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."

        if application is None:
            try:
                os.startfile(file_path)
                return f"Opened '{file_path}' with the default application."
            except OSError:
                subprocess.run(["cmd", "/c", "start", "", file_path], check=False, shell=True)
                return f"Opened '{file_path}' with the default application."
        
        application = APP_ALIASES.get(application.lower(), application)
        try:
            subprocess.run([application, file_path], check=False, shell=True)
            return f"Opened '{file_path}' with {application}."
        except FileNotFoundError:
            return f"Error: Application '{application}' not found. Try specifying the full path."
    
    except Exception as e:
        return f"Error: {str(e)}"

def open_application(app_name):
    """Open an application by name."""
    try:
        if app_name.lower() == "notepad":
            subprocess.Popen("notepad.exe")
            return "Opened Notepad."
        return f"Error: Application '{app_name}' not supported yet."
    except Exception as e:
        return f"Error: {str(e)}"

def copy_file(source, destination):
    """Copy a file or directory from source to destination."""
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        return f"Copied '{source}' to '{destination}'"
    except Exception as e:
        return f"Error: {str(e)}"

def move_file(source, destination):
    """Move a file or directory from source to destination."""
    try:
        shutil.move(source, destination)
        return f"Moved '{source}' to '{destination}'"
    except Exception as e:
        return f"Error: {str(e)}"