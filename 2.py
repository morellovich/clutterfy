import os
from pathlib import Path
import logging
import json
from datetime import datetime

# Path to the configuration file
CONFIG_FILE = "file_categories.json"

# Load or create file categories
def load_categories():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        # Default categories
        categories = {
            "Documents": [
                ".pdf", ".docx", ".txt", ".doc", ".xlsx", ".pptx", ".odt", ".ods", ".odp",
                ".rtf", ".tex", ".wpd", ".csv", ".md", ".log", ".xml", ".json", ".html",
                ".htm", ".epub", ".xls"],
            "Images": [
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".psd",
                ".ai", ".eps", ".raw", ".ico", ".heif", ".indd", ".j2k", ".jfif", ".jpe",
                ".dib", ".dng"],
            "Videos": [
                ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".vob", ".ogv",
                ".mpg", ".mpeg", ".3gp", ".m4v", ".f4v", ".f4p", ".f4a", ".f4b", ".mpe",
                ".mpv", ".m2v"],
            "Music": [
                ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff", ".alac",
                ".dsd", ".pcm", ".opus", ".midi", ".ra", ".ram", ".aif", ".ape", ".au",
                ".cda", ".mid"],
            "Archives": [
                ".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz", ".iso",
                ".lz", ".tgz", ".tbz2", ".txz", ".tar.gz", ".tar.bz2", ".tar.xz",
                ".s7z", ".z", ".zipx", ".wim"],
            "Apps": [
                ".exe", ".msi", ".apk", ".bat", ".com", ".cmd", ".gadget", ".jar",
                ".wsf", ".cpl", ".msc", ".msu", ".msp", ".iso", ".dmg", ".deb",
                ".rpm", ".bin", ".run", ".sh", ".pkg", ".app"]
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(categories, file)
        return categories

# Save updated categories
def save_categories(categories):
    with open(CONFIG_FILE, "w") as file:
        json.dump(categories, file)

# Load categories
SUBDIR = load_categories()

# Logging setup
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_action(action):
    logging.info(action)

def pickDir(value):
    for category, extensions in SUBDIR.items():
        if value in extensions:
            return category
    return None

def organizeDir():
    for item in os.scandir():
        if item.is_dir():
            continue

        filePath = Path(item)
        fileType = filePath.suffix.lower()
        directory = pickDir(fileType)

        if directory is None:
            continue

        directoryPath = Path(directory)
        if not directoryPath.is_dir():
            directoryPath.mkdir()
        newPath = directoryPath.joinpath(filePath)
        filePath.rename(newPath)
        log_action(f"Moved {filePath} to {newPath}")

def delete_hidden_files(folder):
    for item in folder.iterdir():
        if item.is_file() and item.name.startswith('.'):
            try:
                item.unlink()
                log_action(f"Deleted hidden file: {item}")
            except Exception as e:
                log_action(f"Failed to delete hidden file: {item}, Error: {str(e)}")

def is_empty(folder):
    # Delete hidden files first
    delete_hidden_files(folder)
    # Check if the folder contains any files
    return not any(folder.iterdir())

def find_and_delete_empty_folders():
    empty_folders = [folder for folder in Path('.').iterdir() if folder.is_dir() and is_empty(folder)]
    
    if empty_folders:
        print("Empty folders found:")
        for folder in empty_folders:
            print(folder)
        
        print("\nDo you want to delete these folders? (yes/no)")
        choice = input().strip().lower()
        
        if choice == 'yes':
            for folder in empty_folders:
                try:
                    folder.rmdir()
                    log_action(f"Deleted empty folder: {folder}")
                except OSError as e:
                    print(f"Failed to delete folder: {folder}, Error: {str(e)}")
                    log_action(f"Failed to delete folder: {folder}, Error: {str(e)}")
            print("Empty folders deleted.")
        else:
            print("No folders were deleted.")
    else:
        print("No empty folders found.")


def edit_categories():
    print("Current file categories:")
    for category, extensions in SUBDIR.items():
        print(f"{category}: {', '.join(extensions)}")
    
    print("\nDo you want to edit categories? (yes/no)")
    choice = input().strip().lower()
    
    if choice == 'yes':
        print("Enter the category name to edit or 'new' to add a new category:")
        category = input().strip()
        
        if category == 'new':
            print("Enter the new category name:")
            new_category = input().strip()
            print(f"Enter the extensions for {new_category} (comma separated):")
            extensions = input().strip().split(',')
            SUBDIR[new_category] = [ext.strip() for ext in extensions]
        elif category in SUBDIR:
            print(f"Enter the new extensions for {category} (comma separated):")
            extensions = input().strip().split(',')
            SUBDIR[category] = [ext.strip() for ext in extensions]
        else:
            print("Category not found.")
        
        save_categories(SUBDIR)
        print("Categories updated.")
    else:
        print("No changes made.")

# Uncomment the following line to allow editing categories before organizing files
# edit_categories()

organizeDir()

# Find and delete empty folders
find_and_delete_empty_folders()