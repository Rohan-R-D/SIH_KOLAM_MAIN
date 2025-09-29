# kolam/animation.py

import math
from typing import List, Tuple, Dict, Any
import json

def generate_animation_frames(svg_content: str, grid_size: int, 
                            pattern_type: str, frame_count: int = 30) -> List[str]:
    """Generate animation frames for step-by-step Kolam drawing."""
    frames = []
    
    if pattern_type == "basic":
        frames = _animate_basic_pattern(grid_size, frame_count)
    elif pattern_type == "flower":
        frames = _animate_flower_pattern(grid_size, frame_count)
    elif pattern_type == "star":
        frames = _animate_star_pattern(grid_size, frame_count)
    elif pattern_type == "diamond":
        frames = _animate_diamond_pattern(grid_size, frame_count)
    elif pattern_type == "spiral":
        frames = _animate_spiral_pattern(grid_size, frame_count)
    else:
        frames = _animate_basic_pattern(grid_size, frame_count)
    
    return frames

def _animate_basic_pattern(grid_size: int, frame_count: int) -> List[str]:
    """Animate basic square pattern."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Draw grid dots
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
        
        # Animate pattern drawing
        progress = frame / frame_count
        max_rings = center
        
        for ring in range(int(progress * max_rings)):
            i = ring
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

            svg += f'''
        <path d="M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} Z" 
              fill="none" stroke="{path_color}" stroke-width="{path_width}" 
              stroke-linecap="round"/>
        '''
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def _animate_flower_pattern(grid_size: int, frame_count: int) -> List[str]:
    """Animate flower pattern drawing."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Draw grid dots
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
        
        # Animate flower drawing
        progress = frame / frame_count
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

            svg += f'''
        <path d="M{center_x},{center_y} Q{cx},{cy} {x1},{y1}" 
              fill="none" stroke="{path_color}" stroke-width="2" 
              stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M{center_x},{center_y} Q{cx},{cy} {x2},{y2}" 
              fill="none" stroke="{path_color}" stroke-width="2" 
              stroke-linecap="round" stroke-linejoin="round"/>
        '''
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def _animate_star_pattern(grid_size: int, frame_count: int) -> List[str]:
    """Animate star pattern drawing."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Draw grid dots
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
        
        # Animate star drawing
        progress = frame / frame_count
        num_points = min(grid_size * 2, 16)
        outer_radius = (grid_size // 2) * dot_spacing * 0.9
        inner_radius = outer_radius * 0.4
        
        # Draw star path progressively
        path = f"M{center_x},{center_y}"
        points_to_draw = int(progress * num_points * 2)
        
        for i in range(points_to_draw):
            angle = (i * 360 / (num_points * 2)) * (math.pi / 180)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path += f" L{x},{y}"
        
        if points_to_draw > 0:
            path += " Z"
            svg += f'<path d="{path}" fill="none" stroke="#4B0082" stroke-width="2" stroke-linejoin="round"/>'
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def _animate_diamond_pattern(grid_size: int, frame_count: int) -> List[str]:
    """Animate diamond pattern drawing."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Draw grid dots
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
        
        # Animate diamond drawing
        progress = frame / frame_count
        max_diamonds = center
        
        for diamond in range(int(progress * max_diamonds)):
            i = diamond + 1
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

            svg += f'''
        <path d="M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} L{x5},{y5} L{x6},{y6} L{x7},{y7} L{x8},{y8} Z" 
              fill="none" stroke="{path_color}" stroke-width="{path_width}" 
              stroke-linecap="round"/>
        '''
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def _animate_spiral_pattern(grid_size: int, frame_count: int) -> List[str]:
    """Animate spiral pattern drawing."""
    frames = []
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    
    for frame in range(frame_count):
        svg = f'<svg width="{grid_size * dot_spacing + 2 * padding}" height="{grid_size * dot_spacing + 2 * padding}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<rect width="100%" height="100%" fill="white"/>'
        
        # Draw grid dots
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>'
        
        # Animate spiral drawing
        progress = frame / frame_count
        max_radius = (grid_size // 2) * dot_spacing * 0.8
        max_angle = int(progress * 720)  # Two full rotations
        
        if max_angle > 0:
            path = f"M{center_x},{center_y}"
            for angle in range(0, max_angle, 5):
                radius = (angle / 720) * max_radius
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y + radius * math.sin(math.radians(angle))
                path += f" L{x},{y}"
            
            svg += f'<path d="{path}" fill="none" stroke="#8B4513" stroke-width="3" stroke-linecap="round"/>'
        
        svg += '</svg>'
        frames.append(svg)
    
    return frames

def create_animation_svg(frames: List[str], duration: float = 3.0) -> str:
    """Create an animated SVG with all frames."""
    if not frames:
        return ""
    
    # Use the first frame as base
    base_svg = frames[0]
    
    # Add animation elements
    animated_svg = base_svg.replace('</svg>', '')
    
    # Add animation script
    animated_svg += '''
    <script>
        const frames = ''' + json.dumps(frames) + ''';
        let currentFrame = 0;
        const duration = ''' + str(duration) + ''' * 1000;
        const frameInterval = duration / frames.length;
        
        function animate() {
            if (currentFrame < frames.length) {
                // Update SVG content
                const svgElement = document.querySelector('svg');
                if (svgElement) {
                    svgElement.innerHTML = frames[currentFrame].match(/<svg[^>]*>(.*)<\/svg>/s)[1];
                }
                currentFrame++;
                setTimeout(animate, frameInterval);
            }
        }
        
        // Start animation
        setTimeout(animate, 100);
    </script>
    </svg>'''
    
    return animated_svg

def highlight_symmetry_axes(svg_content: str, symmetry_info: Dict[str, bool], 
                          grid_size: int) -> str:
    """Add symmetry axis highlights to SVG."""
    if not any(symmetry_info.values()):
        return svg_content
    
    dot_spacing = 40
    padding = 20
    center = grid_size // 2
    center_x = center * dot_spacing + padding
    center_y = center * dot_spacing + padding
    canvas_size = grid_size * dot_spacing + 2 * padding
    
    # Find the closing </svg> tag and insert symmetry lines before it
    svg_with_axes = svg_content.replace('</svg>', '')
    
    # Add horizontal axis
    if symmetry_info.get("horizontal", False):
        svg_with_axes += f'''
    <line x1="0" y1="{center_y}" x2="{canvas_size}" y2="{center_y}" 
          stroke="red" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
    '''
    
    # Add vertical axis
    if symmetry_info.get("vertical", False):
        svg_with_axes += f'''
    <line x1="{center_x}" y1="0" x2="{center_x}" y2="{canvas_size}" 
          stroke="red" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
    '''
    
    # Add diagonal axes
    if symmetry_info.get("diagonal", False):
        svg_with_axes += f'''
    <line x1="0" y1="0" x2="{canvas_size}" y2="{canvas_size}" 
          stroke="red" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
    <line x1="{canvas_size}" y1="0" x2="0" y2="{canvas_size}" 
          stroke="red" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
    '''
    
    # Add radial symmetry indicator
    if symmetry_info.get("radial", False):
        svg_with_axes += f'''
    <circle cx="{center_x}" cy="{center_y}" r="20" 
            fill="none" stroke="red" stroke-width="2" stroke-dasharray="5,5" opacity="0.7"/>
    '''
    
    svg_with_axes += '</svg>'
    return svg_with_axes
