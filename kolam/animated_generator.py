# kolam/animated_generator.py

import math
from kolam.generator import generate_kolam
from kolam.animation import generate_animation_frames, create_animation_svg

def generate_animated_kolam(grid_size=7, pattern='basic', frame_count=30):
    """Generate an animated Kolam pattern that draws step by step."""
    # Generate animation frames
    frames = generate_clean_animation_frames(grid_size, pattern, frame_count)
    
    # Return the final frame (complete pattern) for display
    if frames:
        return frames[-1]  # Return the last frame (complete pattern)
    else:
        # Fallback to regular generation
        from kolam.generator import generate_kolam
        return generate_kolam(grid_size, pattern)

def generate_animated_kolam_clean(grid_size=7, pattern='basic', frame_count=30):
    """Generate a clean animated Kolam pattern without grid dots for export."""
    # Generate clean frames without grid dots
    frames = generate_clean_animation_frames(grid_size, pattern, frame_count)
    
    # Create animated SVG
    animated_svg = create_animation_svg(frames, duration=3.0)
    
    return animated_svg

def generate_clean_animation_frames(grid_size, pattern, frame_count=30):
    """Generate clean animation frames without grid dots."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Add grid dots for reference during animation
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>\n'
        
        # Animate pattern drawing based on type
        progress = frame / frame_count
        
        if pattern == 'basic':
            svg += _animate_basic_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'diamond':
            svg += _animate_diamond_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'spiral':
            svg += _animate_spiral_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'flower':
            svg += _animate_flower_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'lotus':
            svg += _animate_lotus_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'rose':
            svg += _animate_rose_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'star':
            svg += _animate_star_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'sunburst':
            svg += _animate_sunburst_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'mandala':
            svg += _animate_mandala_pattern_clean(grid_size, dot_spacing, padding, progress)
        elif pattern == 'compass':
            svg += _animate_compass_pattern_clean(grid_size, dot_spacing, padding, progress)
        else:
            svg += _animate_basic_pattern_clean(grid_size, dot_spacing, padding, progress)
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def _animate_basic_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate basic square pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    
    max_rings = center
    rings_to_draw = int(progress * max_rings)
    
    for i in range(rings_to_draw):
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

def _animate_diamond_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate diamond pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    
    max_diamonds = center
    diamonds_to_draw = int(progress * max_diamonds)
    
    for diamond in range(diamonds_to_draw):
        i = diamond + 1
        # Create diamond shape
        x1 = center * dot_spacing + padding
        y1 = (center - i) * dot_spacing + padding
        x2 = (center + i) * dot_spacing + padding
        y2 = center * dot_spacing + padding
        x3 = center * dot_spacing + padding
        y3 = (center + i) * dot_spacing + padding
        x4 = (center - i) * dot_spacing + padding
        y4 = center * dot_spacing + padding

        path_color = f"hsl({(i * 45) % 360}, 70%, 50%)"
        path_width = 2 + (center - i) / 3

        pattern += f'''
    <path d="M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} Z" 
          fill="none" stroke="{path_color}" stroke-width="{path_width}" 
          stroke-linecap="round"/>
    '''
    return pattern

def _animate_spiral_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate spiral pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    max_angle = int(progress * 720)  # Two full rotations
    max_radius = (grid_size // 2) * dot_spacing * 0.8
    
    if max_angle > 0:
        path = f"M{center_x},{center_y}"
        for angle in range(0, max_angle, 5):
            radius = (angle / 720) * max_radius
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            path += f" L{x},{y}"
        
        pattern += f'<path d="{path}" fill="none" stroke="#8B4513" stroke-width="3" stroke-linecap="round"/>'
    
    return pattern

def _animate_flower_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate flower pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_petals = min(grid_size - 2, 8)
    radius = (grid_size // 2) * dot_spacing * 0.8
    
    petals_to_draw = int(progress * num_petals)
    
    for i in range(petals_to_draw):
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

def _animate_lotus_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate lotus pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_petals = 8
    layers_to_draw = int(progress * 3)
    
    for layer in range(layers_to_draw):
        radius = (grid_size // 2) * dot_spacing * (0.6 + layer * 0.2)
        for i in range(num_petals):
            angle = (i * 360 / num_petals) * (math.pi / 180)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            petal_path = f"M{center_x},{center_y} Q{x},{y} {center_x + radius * 0.7 * math.cos(angle + math.pi/8)},{center_y + radius * 0.7 * math.sin(angle + math.pi/8)} Q{x},{y} {center_x},{center_y}"
            
            path_color = f"hsl({(i * 45 + layer * 30) % 360}, 70%, {60 - layer * 10}%)"
            
            pattern += f'''
    <path d="{petal_path}" 
          fill="none" stroke="{path_color}" stroke-width="{3 - layer}" 
          stroke-linecap="round" stroke-linejoin="round"/>
    '''
    
    if progress > 0.8:
        pattern += f'<circle cx="{center_x}" cy="{center_y}" r="8" fill="#FFD700"/>'
    
    return pattern

def _animate_rose_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate rose pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    max_radius = (grid_size // 2) * dot_spacing * 0.7
    max_angle = int(progress * 1440)  # 4 full rotations
    
    if max_angle > 0:
        for angle in range(0, max_angle, 2):
            radius = (angle / 1440) * max_radius
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            
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

def _animate_star_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate star pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_points = min(grid_size * 2, 16)
    outer_radius = (grid_size // 2) * dot_spacing * 0.9
    inner_radius = outer_radius * 0.4
    
    points_to_draw = int(progress * num_points * 2)
    
    if points_to_draw > 0:
        path = f"M{center_x},{center_y}"
        for i in range(points_to_draw):
            angle = (i * 360 / (num_points * 2)) * (math.pi / 180)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path += f" L{x},{y}"
        
        if points_to_draw > 0:
            path += " Z"
            pattern += f'<path d="{path}" fill="none" stroke="#4B0082" stroke-width="2" stroke-linejoin="round"/>'
    
    return pattern

def _animate_sunburst_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate sunburst pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    num_rays = min(grid_size * 2, 24)
    radius = (grid_size // 2) * dot_spacing * 0.8
    
    rays_to_draw = int(progress * num_rays)
    
    for i in range(rays_to_draw):
        angle = (i * 360 / num_rays) * (math.pi / 180)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        path_color = f"hsl({(i * 15) % 360}, 80%, 50%)"
        
        pattern += f'''
    <line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" 
          stroke="{path_color}" stroke-width="2" stroke-linecap="round"/>
    '''
    
    if progress > 0.8:
        pattern += f'<circle cx="{center_x}" cy="{center_y}" r="6" fill="#FFD700"/>'
    
    return pattern

def _animate_mandala_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate mandala pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    # Animate concentric circles
    max_circles = center
    circles_to_draw = int(progress * max_circles)
    
    for i in range(1, circles_to_draw + 1):
        radius = i * dot_spacing * 0.8
        pattern += f'''
    <circle cx="{center_x}" cy="{center_y}" r="{radius}" 
            fill="none" stroke="hsl({i * 30 % 360}, 60%, 50%)" stroke-width="1"/>
    '''
    
    # Animate geometric shapes
    if progress > 0.5:
        shapes_to_draw = int((progress - 0.5) * 2 * max_circles)
        for i in range(3, min(shapes_to_draw + 3, center + 1), 2):
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

def _animate_compass_pattern_clean(grid_size, dot_spacing, padding, progress):
    """Animate compass pattern without grid dots."""
    pattern = ''
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding

    directions = [
        (0, "North", "#FF0000"),
        (90, "East", "#00FF00"),
        (180, "South", "#0000FF"),
        (270, "West", "#FFFF00")
    ]
    
    radius = (grid_size // 2) * dot_spacing * 0.7
    directions_to_draw = int(progress * len(directions))
    
    for i, (angle, direction, color) in enumerate(directions[:directions_to_draw]):
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y + radius * math.sin(math.radians(angle))
        
        pattern += f'''
    <line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}" 
          stroke="{color}" stroke-width="3" stroke-linecap="round"/>
    '''
        
        pattern += f'''
    <circle cx="{x}" cy="{y}" r="4" fill="{color}"/>
    <text x="{x + 10}" y="{y + 5}" font-size="12" fill="{color}">{direction}</text>
    '''
    
    if progress > 0.8:
        pattern += f'''
    <circle cx="{center_x}" cy="{center_y}" r="8" fill="#FFFFFF" stroke="#000000" stroke-width="2"/>
    <text x="{center_x - 5}" y="{center_y + 3}" font-size="10" fill="#000000">N</text>
    '''
    
    return pattern

