# kolam/patterns/flower.py

import math

def generate_flower_pattern(grid_size, dot_spacing, padding):
    """Generate a flower pattern with petals and center."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_petals = min(grid_size - 2, 8)
    radius = (grid_size // 2) * dot_spacing * 0.8

    for i in range(num_petals):
        angle1 = (i * 360 / num_petals) * (math.pi / 180)
        angle2 = ((i + 1) * 360 / num_petals) * (math.pi / 180)

        x1 = center_x + radius * 0.8 * math.cos(angle1)
        y1 = center_y + radius * 0.8 * math.sin(angle1)
        x2 = center_x + radius * 0.8 * math.cos(angle2)
        y2 = center_y + radius * 0.8 * math.sin(angle2)
        cx = center_x + radius * 1.2 * math.cos((angle1 + angle2) / 2)
        cy = center_y + radius * 1.2 * math.sin((angle1 + angle2) / 2)

        path_color = f"hsl({(i * 45) % 360}, 70%, 50%)"

        pattern += f'''
    <path d="M{center_x},{center_y} Q{cx},{cy} {x1},{y1}" 
          fill="none" stroke="{path_color}" stroke-width="2" 
          stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{center_x},{center_y} Q{cx},{cy} {x2},{y2}" 
          fill="none" stroke="{path_color}" stroke-width="2" 
          stroke-linecap="round" stroke-linejoin="round"/>
    '''
    return pattern

def generate_lotus_pattern(grid_size, dot_spacing, padding):
    """Generate a lotus pattern with layered petals."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    # Outer petals
    num_petals = 8
    for layer in range(3):
        radius = (grid_size // 2) * dot_spacing * (0.6 + layer * 0.2)
        for i in range(num_petals):
            angle = (i * 360 / num_petals) * (math.pi / 180)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            # Create petal shape
            petal_path = f"M{center_x},{center_y} Q{x},{y} {center_x + radius * 0.7 * math.cos(angle + math.pi/8)},{center_y + radius * 0.7 * math.sin(angle + math.pi/8)} Q{x},{y} {center_x},{center_y}"
            
            path_color = f"hsl({(i * 45 + layer * 30) % 360}, 70%, {60 - layer * 10}%)"
            
            pattern += f'''
    <path d="{petal_path}" 
          fill="none" stroke="{path_color}" stroke-width="{3 - layer}" 
          stroke-linecap="round" stroke-linejoin="round"/>
    '''
    
    # Center
    pattern += f'<circle cx="{center_x}" cy="{center_y}" r="8" fill="#FFD700"/>'
    
    return pattern

def generate_rose_pattern(grid_size, dot_spacing, padding):
    """Generate a rose pattern with spiral petals."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    # Create spiral rose pattern
    max_radius = (grid_size // 2) * dot_spacing * 0.7
    for angle in range(0, 1440, 2):  # 4 full rotations
        radius = (angle / 1440) * max_radius
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        
        # Create petal-like curves
        if angle % 20 == 0:
            petal_angle = math.radians(angle)
            petal_radius = radius * 0.3
            x1 = x + petal_radius * math.cos(petal_angle + math.pi/4)
            y1 = y + petal_radius * math.sin(petal_angle + math.pi/4)
            x2 = x + petal_radius * math.cos(petal_angle - math.pi/4)
            y2 = y + petal_radius * math.sin(petal_angle - math.pi/4)
            
            path_color = f"hsl({(angle * 0.5) % 360}, 80%, 60%)"
            
            pattern += f'''
    <path d="M{x},{y} Q{x1},{y1} {x},{y} Q{x2},{y2} {x},{y}" 
          fill="none" stroke="{path_color}" stroke-width="1.5" 
          stroke-linecap="round"/>
    '''
    
    return pattern