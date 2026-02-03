"""
Tool: Backdrop Fast
Shortcut: alt+b
Tooltip: Quickly create a backdrop around selected nodes
"""

import nuke
import random

def create_smart_backdrop():
    # 1. Get selected nodes
    sel_nodes = nuke.selectedNodes()
    if not sel_nodes:
        nuke.message("Select some nodes first!")
        return

    # 2. Calculate the bounding box
    x_min = min([n.xpos() for n in sel_nodes])
    y_min = min([n.ypos() for n in sel_nodes])
    x_max = max([n.xpos() + n.screenWidth() for n in sel_nodes])
    y_max = max([n.ypos() + n.screenHeight() for n in sel_nodes])

    # 3. Add padding
    padding = 50
    x_min -= padding
    y_min -= (padding * 2) 
    x_max += padding
    y_max += padding

    bd_width = x_max - x_min

    # 4. Prompt for a label
    label = nuke.getInput('Backdrop Label', 'Backdrop')
    if label is None:
        return

    # 5. DYNAMIC FONT SIZE CALCULATION
    # We want the text to fill roughly 80% of the backdrop width to leave side padding
    target_text_width = bd_width * 0.8
    char_count = len(label) if len(label) > 0 else 1
    
    # Heuristic: Average char width is ~0.6 of font size.
    # Formula: FontSize = TargetWidth / (CharCount * 0.6)
    calculated_font_size = target_text_width / (char_count * 0.6)
    
    # Clamp the font size so it doesn't get ridiculously small or large
    final_font_size = max(20, min(int(calculated_font_size), 150))

    # 6. Generate a random pastel color
    r = int(random.uniform(0.3, 0.7) * 255)
    g = int(random.uniform(0.3, 0.7) * 255)
    b = int(random.uniform(0.3, 0.7) * 255)
    hex_color = int('%02x%02x%02x%02x' % (r, g, b, 255), 16)

    # 7. Create the backdrop
    backdrop = nuke.nodes.BackdropNode(
        xpos = x_min,
        bdwidth = bd_width,
        ypos = y_min,
        bdheight = y_max - y_min,
        tile_color = hex_color,
        note_font_size = final_font_size,
        label = label
    )
    
    return backdrop

create_smart_backdrop()