# Nuke Script Loader

An automatic script loader for Nuke that creates a custom "My Tools" menu with all your gizmos, nuke scripts, and Python tools.

## Features

- 🚀 **Automatic Discovery**: Scans your `gizmos/`, `nk/`, and `py/` folders and adds them to the menu
- ⌨️ **Keyboard Shortcuts**: Define custom shortcuts for each tool
- 🖼️ **Custom Icons**: Automatically loads PNG icons from the `icons/` folder
- 🔄 **Live Reload**: Press F5 to reload all tools without restarting Nuke
- 📝 **Tool Metadata**: Each script can define its own tooltip and keyboard shortcut

## Installation

### 1. Copy Files to .nuke Folder

Copy the entire `User` folder to your Nuke preferences directory:

**Windows:**
```
C:\Users\<YourUsername>\.nuke\User\
```

**Mac/Linux:**
```
~/.nuke/User/
```

Your structure should look like:
```
.nuke/
├── init.py
└── User/
    ├── init.py
    ├── menu.py
    ├── LICENSE
    ├── gizmos/
    ├── icons/
    ├── nk/
    └── py/
        ├── Backdrop_Fast.py
        └── Retime_Setup.py
```

### 2. Edit Your Main init.py

Open (or create) the `init.py` file in your `.nuke` folder and add this line:

```python
import nuke

nuke.pluginAddPath('./User')
```

**Complete Example:**

If your `.nuke/init.py` doesn't exist yet, create it with this content:

```python
import nuke

# Load custom User folder
nuke.pluginAddPath('./User')
```

### 3. Restart Nuke

Restart Nuke and you should see a new "My Tools" menu in the Nodes menu.

## Usage

### Adding New Tools

#### Python Scripts (.py)
1. Place your Python script in `User/py/`
2. Add metadata at the top of your script:

```python
"""
Tool: My Tool Name
Shortcut: ctrl+shift+m
Tooltip: Description of what this tool does
"""

import nuke

# Your code here...
```

#### Nuke Scripts (.nk)
1. Save your node setup as a `.nk` file
2. Place it in `User/nk/`
3. Create a metadata file `User/nk/your_script_meta.py`:

```python
METADATA = {
    'shortcut': 'ctrl+shift+e',
    'tooltip': 'Description of your setup'
}
```

#### Gizmos (.gizmo)
1. Place your gizmo in `User/gizmos/`
2. Create a metadata file `User/gizmos/your_gizmo_meta.py`:

```python
METADATA = {
    'shortcut': 'alt+g',
    'tooltip': 'Description of your gizmo'
}
```

### Adding Icons

Place a PNG file with the same name as your tool in `User/icons/`:

- `User/py/Backdrop_Fast.py` → `User/icons/Backdrop_Fast.png`
- `User/nk/Exponential_Glow.nk` → `User/icons/Exponential_Glow.png`

### Reloading Tools

Press **F5** or select "Reload Custom Tools" from the My Tools menu to refresh all tools without restarting Nuke.

## Included Tools

### Backdrop Fast (Alt+B)
Quickly creates a backdrop around selected nodes with:
- Auto-calculated size with padding
- Smart font sizing based on backdrop width
- Random pastel colors
- Custom label prompt

### Retime Setup (Ctrl+Shift+R)
Creates a complete retime setup from a Read node:
- Auto-connects Retime node
- Sets start frame to 1001
- Updates project settings (resolution, fps, frame range)

## Folder Structure

```
User/
├── init.py          # Adds subfolders to Nuke's plugin path
├── menu.py          # Main script loader (creates the menu)
├── gizmos/          # Place .gizmo files here
├── icons/           # Place .png icon files here (same name as tools)
├── nk/              # Place .nk setup files here
└── py/              # Place .py Python scripts here
    ├── Backdrop_Fast.py
    └── Retime_Setup.py
```

## Troubleshooting

### Menu doesn't appear
- Verify `nuke.pluginAddPath('./User')` is in your main `.nuke/init.py`
- Check the Script Editor for error messages
- Ensure the `User` folder is directly inside `.nuke/`

### Icons not showing
- Verify icon filenames match tool names exactly (case-sensitive)
- Icons must be PNG format
- Icons must be in the `User/icons/` folder

### Shortcuts not working
- Make sure there's no conflict with existing Nuke shortcuts
- Check that metadata is properly defined in each script
- Try reloading tools with F5

## License

See [LICENSE](User/LICENSE) file for details.

## Contributing

To add your own tools:
1. Create your script/gizmo/setup
2. Add metadata defining shortcuts and tooltips
3. Optionally create an icon
4. Press F5 to reload
