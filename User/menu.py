import nuke
import os
import re

try:
    from PySide6.QtCore import QTimer
except ImportError:
    from PySide2.QtCore import QTimer

# Define the root of your user folder
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(ROOT_DIR, 'icons')

# Store references to prevent garbage collection
_registered_shortcuts = []

def parse_metadata_from_file(file_path, tool_type):
    """
    Reads metadata from a script file or its companion metadata file.
    
    For Python scripts (.py): Looks for docstring at the top:
        '''
        Tool: Tool Name
        Shortcut: ctrl+shift+x
        Tooltip: Description
        '''
    
    For Gizmos/NK files: Looks for companion _meta.py file with:
        METADATA = {
            'shortcut': 'ctrl+shift+x',
            'tooltip': 'Description'
        }
    
    Returns a dict with 'shortcut' and 'tooltip' keys.
    """
    metadata = {'shortcut': '', 'tooltip': ''}
    
    if tool_type == 'py':
        # Read the Python file and parse docstring
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1000 chars
                
            # Look for docstring pattern
            docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if not docstring_match:
                docstring_match = re.search(r"'''(.*?)'''", content, re.DOTALL)
            
            if docstring_match:
                docstring = docstring_match.group(1)
                
                # Parse Tool, Shortcut, and Tooltip
                shortcut_match = re.search(r'Shortcut:\s*(.+)', docstring, re.IGNORECASE)
                tooltip_match = re.search(r'Tooltip:\s*(.+)', docstring, re.IGNORECASE)
                
                if shortcut_match:
                    metadata['shortcut'] = shortcut_match.group(1).strip()
                if tooltip_match:
                    metadata['tooltip'] = tooltip_match.group(1).strip()
        except Exception as e:
            pass
    
    else:  # gizmo or nk
        # Look for companion _meta.py file
        base_path = os.path.splitext(file_path)[0]
        meta_file = base_path + '_meta.py'
        
        if os.path.exists(meta_file):
            try:
                # Read and execute the metadata file
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta_content = f.read()
                
                # Create a namespace and execute
                namespace = {}
                exec(meta_content, namespace)
                
                if 'METADATA' in namespace:
                    meta_dict = namespace['METADATA']
                    metadata['shortcut'] = meta_dict.get('shortcut', '')
                    metadata['tooltip'] = meta_dict.get('tooltip', '')
            except Exception as e:
                pass
    
    return metadata

def get_icon_path(tool_name):
    """
    Looks for a .png file in the icons folder with the same name as the tool.
    Returns the filename (e.g. 'tool.png') if found, otherwise '' (empty string).
    """
    expected_icon = tool_name + ".png"
    full_icon_path = os.path.join(ICONS_DIR, expected_icon)
    
    # Check if the file actually exists on disk
    if os.path.exists(full_icon_path):
        return expected_icon 
    else:
        return ""

def get_tool_metadata(file_path, tool_name, tool_type):
    """
    Gets metadata for a tool by reading it from the file itself.
    Returns a dict with 'shortcut', 'tooltip', and 'icon' keys.
    """
    metadata = parse_metadata_from_file(file_path, tool_type)
    
    # If no tooltip was found, use the tool name as default
    if not metadata['tooltip']:
        metadata['tooltip'] = tool_name.replace('_', ' ')
    
    # Add icon
    metadata['icon'] = get_icon_path(tool_name)
    
    return metadata

def setup_auto_tools():
    global _registered_shortcuts
    
    # Clear previous shortcuts
    for shortcut_ref in _registered_shortcuts:
        try:
            shortcut_ref.setEnabled(False)
        except:
            pass
    _registered_shortcuts = []
    
    # 1. Create the Main Menu
    # We look for 'main.png' for the folder icon itself
    main_icon = 'main.png' if os.path.exists(os.path.join(ICONS_DIR, 'main.png')) else ''
    
    toolbar = nuke.menu('Nodes').addMenu('My Tools', icon=main_icon)
    toolbar.clearMenu() # Clear old items to prevent duplicates

    # ------------------------------------------------
    # 1. SCAN GIZMOS (.gizmo)
    # ------------------------------------------------
    gizmo_dir = os.path.join(ROOT_DIR, 'gizmos')
    if os.path.exists(gizmo_dir):
        for file in sorted(os.listdir(gizmo_dir)):
            if file.endswith('.gizmo'):
                name_no_ext = os.path.splitext(file)[0]
                full_path = os.path.join(gizmo_dir, file)
                
                # Get metadata from file
                meta = get_tool_metadata(full_path, name_no_ext, 'gizmo')
                
                # Command: Create the gizmo
                cmd = f"nuke.createNode('{name_no_ext}')"
                
                # Label: Replace underscores with spaces for readability
                label = name_no_ext.replace('_', ' ')
                
                # Add command without shortcut first
                menu_item = toolbar.addCommand(label, cmd, '', meta['icon'], meta['tooltip'])
                
                # Register shortcut separately if defined
                if meta['shortcut']:
                    shortcut_ref = nuke.menu('Nodes').addCommand('My Tools/' + label, cmd, meta['shortcut'])
                    _registered_shortcuts.append(shortcut_ref)

    # ------------------------------------------------
    # 2. SCAN NUKE SCRIPTS (.nk)
    # ------------------------------------------------
    nk_dir = os.path.join(ROOT_DIR, 'nk')
    if os.path.exists(nk_dir):
        for file in sorted(os.listdir(nk_dir)):
            if file.endswith('.nk'):
                name_no_ext = os.path.splitext(file)[0]
                full_path = os.path.join(nk_dir, file).replace('\\', '/')
                
                # Get metadata from file
                meta = get_tool_metadata(full_path, name_no_ext, 'nk')
                
                # Command: Paste the script
                cmd = f"nuke.nodePaste('{full_path}')"
                
                label = name_no_ext.replace('_', ' ')
                
                # Add command without shortcut first
                menu_item = toolbar.addCommand(label, cmd, '', meta['icon'], meta['tooltip'])
                
                # Register shortcut separately if defined
                if meta['shortcut']:
                    shortcut_ref = nuke.menu('Nodes').addCommand('My Tools/' + label, cmd, meta['shortcut'])
                    _registered_shortcuts.append(shortcut_ref)

    # ------------------------------------------------
    # 3. SCAN PYTHON SCRIPTS (.py)
    # ------------------------------------------------
    py_dir = os.path.join(ROOT_DIR, 'py')
    if os.path.exists(py_dir):
        for file in sorted(os.listdir(py_dir)):
            # Ignore __init__.py so it doesn't become a button
            if file.endswith('.py') and file != '__init__.py':
                name_no_ext = os.path.splitext(file)[0]
                full_path = os.path.join(py_dir, file).replace('\\', '/')
                
                # Get metadata from file
                meta = get_tool_metadata(full_path, name_no_ext, 'py')
                
                # Command: Execute the python file
                cmd = f"exec(open('{full_path}').read())"
                
                label = name_no_ext.replace('_', ' ')
                
                # Add command without shortcut first
                menu_item = toolbar.addCommand(label, cmd, '', meta['icon'], meta['tooltip'])
                
                # Register shortcut separately if defined
                if meta['shortcut']:
                    shortcut_ref = nuke.menu('Nodes').addCommand('My Tools/' + label, cmd, meta['shortcut'])
                    _registered_shortcuts.append(shortcut_ref)

    # ------------------------------------------------
    # 4. RELOAD BUTTON
    # ------------------------------------------------
    toolbar.addSeparator()
    # Note: We use 'menu.setup_auto_tools()' assuming this file is named menu.py
    reload_cmd = 'import menu; menu.setup_auto_tools()'
    toolbar.addCommand('Reload Custom Tools', reload_cmd, '', '', 'Reload all custom tools (F5)')
    
    # Register F5 shortcut separately
    reload_ref = nuke.menu('Nodes').addCommand('My Tools/Reload Custom Tools', reload_cmd, 'F5')
    _registered_shortcuts.append(reload_ref)
    
    print("Auto-tools loaded successfully.")

# Run setup

QTimer.singleShot(100, setup_auto_tools)