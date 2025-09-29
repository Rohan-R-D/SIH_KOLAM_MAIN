# kolam/generator.py
import math
from kolam.utils import (
    validate_pattern,
    clamp_grid_size,
    generate_grid_coordinates,
    wrap_svg
)
from kolam.patterns.basic import (
    generate_basic_pattern,
    generate_diamond_pattern,
    generate_spiral_pattern
)
from kolam.patterns.flower import (
    generate_flower_pattern,
    generate_lotus_pattern,
    generate_rose_pattern
)
from kolam.patterns.star import (
    generate_star_pattern,
    generate_sunburst_pattern,
    generate_mandala_pattern,
    generate_compass_pattern
)

def generate_kolam(grid_size=7, pattern='basic', show_grid=True):
    """Generate a Kolam pattern with enhanced pattern types."""
    grid_size = clamp_grid_size(grid_size)
    pattern = validate_pattern(pattern)
    
    # SVG canvas size and scaling
    dot_spacing = 40
    padding = 20
    canvas_size = grid_size * dot_spacing + 2 * padding

    # Start SVG string
    svg = f'''
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white"/>
'''

    # Draw grid dots only if show_grid is True
    if show_grid:
        for y in range(grid_size):
            for x in range(grid_size):
                cx = x * dot_spacing + padding
                cy = y * dot_spacing + padding
                svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>\n'

    # Generate pattern based on type
    if pattern == 'basic':
        svg += generate_basic_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'diamond':
        svg += generate_diamond_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'spiral':
        svg += generate_spiral_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'flower':
        svg += generate_flower_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'lotus':
        svg += generate_lotus_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'rose':
        svg += generate_rose_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'star':
        svg += generate_star_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'sunburst':
        svg += generate_sunburst_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'mandala':
        svg += generate_mandala_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'compass':
        svg += generate_compass_pattern(grid_size, dot_spacing, padding)
    else:
        svg += generate_basic_pattern(grid_size, dot_spacing, padding)

    # Close SVG
    svg += '</svg>'
    return svg

def generate_kolam_clean(grid_size=7, pattern='basic'):
    """Generate a clean Kolam pattern without grid dots for export."""
    return generate_kolam(grid_size, pattern, show_grid=False)

def generate_kolam_with_analysis(grid_size=7, pattern='basic'):
    """Generate Kolam with mathematical analysis."""
    from kolam.analyzer import classify_pattern
    
    # Generate the pattern
    svg_content = generate_kolam(grid_size, pattern)
    
    # Generate coordinates for analysis
    coords = generate_grid_coordinates(grid_size)
    
    # Analyze the pattern with pattern type for accurate analysis
    analysis = classify_pattern(coords, grid_size, pattern)
    
    return {
        "svg": svg_content,
        "analysis": analysis,
        "grid_size": grid_size,
        "pattern": pattern
    }