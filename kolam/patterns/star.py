# kolam/patterns/star.py

import math

def generate_star_pattern(grid_size, dot_spacing, padding):
    """Generate a star pattern with multiple points."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_points = min(grid_size * 2, 16)
    outer_radius = (grid_size // 2) * dot_spacing * 0.9
    inner_radius = outer_radius * 0.4

    path = f"M"
    for i in range(num_points * 2):
        angle = (i * 360 / (num_points * 2)) * (math.pi / 180)
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        path += f"{x},{y} "
        if i == 0:
            path += "L"
    path += "Z"

    pattern += f'''
    <path d="{path}" fill="none" stroke="#4B0082" stroke-width="2" stroke-linejoin="round"/>
    '''

    for i in range(num_points):
        angle = (i * 360 / num_points) * (math.pi / 180)
        x = center_x + outer_radius * 1.1 * math.cos(angle)
        y = center_y + outer_radius * 1.1 * math.sin(angle)
        pattern += f'<circle cx="{x}" cy="{y}" r="3" fill="#CD5C5C"/>\n'

    return pattern

def generate_sunburst_pattern(grid_size, dot_spacing, padding):
    """Generate a sunburst pattern with radiating lines."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_rays = min(grid_size * 2, 24)
    radius = (grid_size // 2) * dot_spacing * 0.8

    for i in range(num_rays):
        angle = (i * 360 / num_rays) * (math.pi / 180)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        path_color = f"hsl({(i * 15) % 360}, 80%, 50%)"
        
        pattern += f'''
    <line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" 
          stroke="{path_color}" stroke-width="2" stroke-linecap="round"/>
    '''
    
    # Add center circle
    pattern += f'<circle cx="{center_x}" cy="{center_y}" r="6" fill="#FFD700"/>'
    
    return pattern

def generate_mandala_pattern(grid_size, dot_spacing, padding):
    """Generate a mandala pattern with concentric circles and geometric shapes."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    # Concentric circles
    for i in range(1, center + 1):
        radius = i * dot_spacing * 0.8
        pattern += f'''
    <circle cx="{center_x}" cy="{center_y}" r="{radius}" 
            fill="none" stroke="hsl({i * 30 % 360}, 60%, 50%)" stroke-width="1"/>
    '''
    
    # Geometric shapes
    for i in range(3, center + 1, 2):
        radius = i * dot_spacing * 0.6
        num_sides = 6 + i
        for j in range(num_sides):
            angle1 = (j * 360 / num_sides) * (math.pi / 180)
            angle2 = ((j + 1) * 360 / num_sides) * (math.pi / 180)
            
            x1 = center_x + radius * math.cos(angle1)
            y1 = center_y + radius * math.sin(angle1)
            x2 = center_x + radius * math.cos(angle2)
            y2 = center_y + radius * math.sin(angle2)
            
            path_color = f"hsl({(i * 45 + j * 30) % 360}, 70%, 60%)"
            
            pattern += f'''
    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
          stroke="{path_color}" stroke-width="1.5"/>
    '''
    
    return pattern

def generate_compass_pattern(grid_size, dot_spacing, padding):
    """Generate a compass pattern with cardinal directions."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    # Cardinal directions
    directions = [
        (0, "North", "#FF0000"),
        (90, "East", "#00FF00"),
        (180, "South", "#0000FF"),
        (270, "West", "#FFFF00")
    ]
    
    radius = (grid_size // 2) * dot_spacing * 0.7
    
    for angle, direction, color in directions:
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        
        # Main direction line
        pattern += f'''
    <line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" 
          stroke="{color}" stroke-width="3" stroke-linecap="round"/>
    '''
        
        # Direction marker
        pattern += f'''
    <circle cx="{x}" cy="{y}" r="4" fill="{color}"/>
    <text x="{x + 10}" y="{y + 5}" font-size="12" fill="{color}">{direction}</text>
    '''
    
    # Center compass rose
    pattern += f'''
    <circle cx="{center_x}" cy="{center_y}" r="8" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
    <text x="{center_x - 5}" y="{center_y + 3}" font-size="10" fill="#000000">N</text>
    '''
    
    return pattern
