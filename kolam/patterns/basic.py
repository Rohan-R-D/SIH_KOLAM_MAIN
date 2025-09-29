# kolam/patterns/basic.py

import math

def generate_basic_pattern(grid_size, dot_spacing, padding):
    """Generate a basic square pattern with nested squares."""
    pattern = ''
    center = grid_size // 2
    
    for i in range(center):
        x1 = (center - i) * dot_spacing + padding
        y1 = (center - i) * dot_spacing + padding
        x2 = (center + i) * dot_spacing + padding
        y2 = (center - i) * dot_spacing + padding
        x3 = (center + i) * dot_spacing + padding
        y3 = (center + i) * dot_spacing + padding
        x4 = (center - i) * dot_spacing + padding
        y4 = (center + i) * dot_spacing + padding

        path_color = f"hsl({(i * 30) % 360}, 70%, 50%)"
        path_width = 2 + (center - i) / 2

        pattern += f'''
    <path d="M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} Z" 
          fill="none" stroke="{path_color}" stroke-width="{path_width}" 
          stroke-linecap="round"/>
    '''
    return pattern

def generate_diamond_pattern(grid_size, dot_spacing, padding):
    """Generate a diamond pattern with diagonal connections."""
    pattern = ''
    center = grid_size // 2
    
    # Create diamond shape
    for i in range(1, center + 1):
        # Top to right
        x1 = center * dot_spacing + padding
        y1 = (center - i) * dot_spacing + padding
        x2 = (center + i) * dot_spacing + padding
        y2 = center * dot_spacing + padding
        
        # Right to bottom
        x3 = (center + i) * dot_spacing + padding
        y3 = center * dot_spacing + padding
        x4 = center * dot_spacing + padding
        y4 = (center + i) * dot_spacing + padding
        
        # Bottom to left
        x5 = center * dot_spacing + padding
        y5 = (center + i) * dot_spacing + padding
        x6 = (center - i) * dot_spacing + padding
        y6 = center * dot_spacing + padding
        
        # Left to top
        x7 = (center - i) * dot_spacing + padding
        y7 = center * dot_spacing + padding
        x8 = center * dot_spacing + padding
        y8 = (center - i) * dot_spacing + padding

        path_color = f"hsl({(i * 45) % 360}, 70%, 50%)"
        path_width = 2 + (center - i) / 3

        pattern += f'''
    <path d="M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} L{x5},{y5} L{x6},{y6} L{x7},{y7} L{x8},{y8} Z" 
          fill="none" stroke="{path_color}" stroke-width="{path_width}" 
          stroke-linecap="round"/>
    '''
    return pattern

def generate_spiral_pattern(grid_size, dot_spacing, padding):
    """Generate a spiral pattern."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    path = f"M{center_x},{center_y}"
    max_radius = (grid_size // 2) * dot_spacing * 0.8
    
    for angle in range(0, 720, 5):  # Two full rotations
        radius = (angle / 720) * max_radius
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        path += f" L{x},{y}"
    
    pattern += f'''
    <path d="{path}" fill="none" stroke="#8B4513" stroke-width="3" 
          stroke-linecap="round"/>
    '''
    return pattern
