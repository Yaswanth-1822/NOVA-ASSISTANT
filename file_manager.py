import os
import shutil
import subprocess

# Global clipboard for storing file content
CLIPBOARD = None

# Mapping common app names to correct executables
APP_ALIASES = {
    "vs code": "code",  # VS Code CLI
    "notepad++": "notepad++.exe",
    "word": "winword.exe",
    "excel": "excel.exe"
}

def open_directory(path):
    # ... (unchanged code)
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
    # ... (unchanged)
    try:
        os.makedirs(path, exist_ok=True)
        return f"Created directory: {path}"
    except Exception as e:
        return f"Error: {str(e)}"

def rename_file(old_path, new_path):
    # ... (unchanged)
    try:
        os.rename(old_path, new_path)
        return f"Renamed '{old_path}' to '{new_path}'"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(path):
    # ... (unchanged)
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
    """List directories and files in a given directory."""
    try:
        items = os.listdir(path)
        if not items:
            return f"The directory '{path}' is empty."
        # Separate directories and files
        dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        result = f"Directories: {', '.join(dirs)}" if dirs else "No directories."
        result += "\n"
        result += f"Files: {', '.join(files)}" if files else "No files."
        return result
    except Exception as e:
        return f"Error: {str(e)}"
def navigate_to_path(path, current_directory):
    # ... (unchanged)
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
    # ... (unchanged)
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

def open_file_with(file_path, app_name):
    """Open a file with a specified application (distinct from opening the application itself)."""
    try:
        if not os.path.exists(file_path):
            return f"Error: Path '{file_path}' not found."
        if os.path.isdir(file_path):
            return f"Error: '{file_path}' is a directory. Please specify a file."
        executable = APP_ALIASES.get(app_name.lower(), app_name)
        # For VS Code, use os.system so that it opens the file as expected.
        if executable.lower() == "code":
            os.system(f'{executable} "{file_path}"')
        else:
            subprocess.Popen([executable, file_path], shell=False)
        return f"Opened '{file_path}' with {executable}."
    except Exception as e:
        return f"Error: {str(e)}"


def copy_file(source, destination):
    """
    Copy a file or directory from source to destination.
    If destination is an empty string, copy the file's content to an internal clipboard.
    """
    global CLIPBOARD
    try:
        if destination == "":
            if os.path.isdir(source):
                return f"Error: Cannot copy content of a directory."
            with open(source, "r") as f:
                CLIPBOARD = f.read()
            return f"Copied content of '{source}' to clipboard."
        else:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            return f"Copied '{source}' to '{destination}'"
    except Exception as e:
        return f"Error: {str(e)}"

def paste_file(destination):
    """
    Paste the copied clipboard content into a new file at the destination.
    """
    global CLIPBOARD
    try:
        if CLIPBOARD is None:
            return "Clipboard is empty."
        with open(destination, "w") as f:
            f.write(CLIPBOARD)
        return f"Pasted clipboard content to '{destination}'."
    except Exception as e:
        return f"Error: {str(e)}"

def move_file(source, destination):
    """
    Move a file or directory from source to destination.
    If destination is an existing directory, move the source inside that directory.
    """
    try:
        if not os.path.exists(source):
            return f"Error: Source '{source}' does not exist."
        if os.path.isdir(destination):
            destination = os.path.join(destination, os.path.basename(source))
        shutil.move(source, destination)
        return f"Moved '{source}' to '{destination}'"
    except Exception as e:
        return f"Error: {str(e)}"
