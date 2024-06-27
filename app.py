import os
from pathlib import Path
from datetime import datetime
import time



# define the file categories with dictionary
SUBDIR = {
    "Documents":[
        ".pdf", ".docx", ".txt", ".doc", ".xlsx", ".pptx", ".odt", ".ods", ".odp", 
        ".rtf", ".tex", ".wpd", ".csv", ".md", ".log", ".xml", ".json", ".html", 
        ".htm", ".epub"],
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
        ".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz", ".iso", ".dmg", 
        ".lz", ".tgz", ".tbz2", ".txz", ".tar.gz", ".tar.bz2", ".tar.xz", 
        ".s7z", ".z", ".zipx", ".wim"],
    "Apps": [
        ".exe", ".msi", ".apk", ".bat", ".com", ".cmd", ".gadget", ".jar", 
        ".wsf", ".cpl", ".msc", ".msu", ".msp", ".iso", ".dmg", ".deb", 
        ".rpm", ".bin", ".run", ".sh"]
        }



def pickDir(value):
    '''
    value: str contain extension of the file.
    return name of the category who defined before.
    e.g. value = '.pdf' so the function will return DOCUMENTS.
    '''
    for category, ekstensi in SUBDIR.items():
        for suffix in ekstensi:
            if suffix == value:
                return category

def organizeDir():
    '''
    this function will scan any files in the same directory, and then
    look at every extension of files and move that file to the exact category from calling the pickDir function.
    '''
    for item in os.scandir():
                
        #just looking for file, skip the directory
        if item.is_dir():
                continue
                
        filePath = Path(item)
        fileType = filePath.suffix.lower()
        directory = pickDir(fileType)
        
        #just skip, if the file extension not defined.
        if directory == None:
            continue
        
        directoryPath = Path(directory)
        #make new directory if the category's directory not found.
        if directoryPath.is_dir() != True:
                directoryPath.mkdir()
        filePath.rename(directoryPath.joinpath(filePath))

organizeDir()

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

edit_categories()