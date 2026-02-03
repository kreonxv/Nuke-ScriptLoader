"""
Tool: Retime Setup
Shortcut: ctrl+shift+r
Tooltip: Create a retime node setup
"""

import nuke

def setup_read_with_retime():
    """
    Selects a Read node and:
    1. Creates a Retime node connected to it
    2. Sets the Retime start to 1001 (auto-calculating the end)
    3. Updates project settings with resolution, fps, and frame range
    """
    
    # Get selected node
    try:
        selected = nuke.selectedNode()
    except ValueError:
        nuke.message('Please select a Read node!')
        return
    
    # Check if it's a Read node
    if selected.Class() != 'Read':
        nuke.message('Please select a Read node!')
        return
    
    read_node = selected
    
    # Get Read node properties
    first_frame = int(read_node['first'].value())
    last_frame = int(read_node['last'].value())
    duration = last_frame - first_frame
    
    # Resolution and FPS
    width = int(read_node.width())
    height = int(read_node.height())
    fps = read_node.metadata('input/frame_rate') or 24
    
    # Create Retime node
    retime_node = nuke.nodes.Retime()
    retime_node.setXYpos(read_node.xpos(), read_node.ypos() + 100)
    retime_node.setInput(0, read_node)
    
    # Set Retime parameters
    # We only lock the first frame to 1001; Nuke calculates the last frame automatically
    retime_node['output.first_lock'].setValue(True)
    
    
    retime_node['input.first'].setValue(first_frame)
    retime_node['input.last'].setValue(last_frame)
    
    output_first = 1001
    output_last = output_first + duration
    retime_node['output.first'].setValue(output_first)
    retime_node['output.last_lock'].setValue(True)
    retime_node['output.last'].setValue(output_last)
    
    # Even though we don't lock it, we need the value for Project Settings
    # Nuke will have calculated it as: 1001 + (last_frame - first_frame)
     
    
    # Update project settings
    root = nuke.root()
    root['first_frame'].setValue(output_first)
    root['last_frame'].setValue(output_last)
    root['fps'].setValue(float(fps))
    
    # Fix Format: Add a custom format string that Nuke accepts reliably
    fmt_string = f"{width} {height} custom_res"
    new_fmt = nuke.addFormat(fmt_string)
    root['format'].setValue(new_fmt)
    
    # Selection cleanup
    [n.setSelected(False) for n in nuke.allNodes()]
    retime_node.setSelected(True)
    
    # Set timeline position to 1001
    nuke.frame(1001)
    
    # Connect retime node to viewer
    nuke.connectViewer(0, retime_node)
    
    print(f"Retime Setup Complete: {output_first} to {output_last}")

if __name__ == '__main__':
    setup_read_with_retime()