# ~/.nuke/user/init.py
import nuke
import os

# Get the path of THIS folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List of subfolders you want Nuke to search through
sub_folders = ['gizmos', 'py', 'nk', 'icons']

for folder in sub_folders:
    full_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(full_path):
        nuke.pluginAddPath(full_path)