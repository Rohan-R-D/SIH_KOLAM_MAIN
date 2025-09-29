import math

def generate_kolam(grid_size=7, pattern='basic'):
    """
    Generate a Kolam pattern as an SVG string.

    Args:
        grid_size (int): Size of the grid (number of dots in each row/column). Must be odd. Default is 7.
        pattern (str): Type of pattern to generate: 'basic', 'flower', or 'star'. Default is 'basic'.

    Returns:
        str: An SVG string representing the Kolam pattern.
    """
    # Ensure grid_size is odd for symmetry
    if grid_size % 2 == 0:
        grid_size += 1

    # SVG canvas size and scaling
    dot_spacing = 40  # Space between dots in pixels
    padding = 20      # Padding around the grid in pixels
    canvas_size = grid_size * dot_spacing + 2 * padding

    # Start SVG string
    svg = f'''
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white"/>
'''

    # Draw grid dots
    for y in range(grid_size):
        for x in range(grid_size):
            cx = x * dot_spacing + padding
            cy = y * dot_spacing + padding
            svg += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#333"/>\n'

    # Generate pattern based on type
    if pattern == 'basic':
        svg += _generate_basic_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'flower':
        svg += _generate_flower_pattern(grid_size, dot_spacing, padding)
    elif pattern == 'star':
        svg += _generate_star_pattern(grid_size, dot_spacing, padding)
    else:
        svg += _generate_basic_pattern(grid_size, dot_spacing, padding)

    # Close SVG
    svg += '</svg>'
    return svg


def _generate_basic_pattern(grid_size, dot_spacing, padding):
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


def _generate_flower_pattern(grid_size, dot_spacing, padding):
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


def _generate_star_pattern(grid_size, dot_spacing, padding):
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


# Example usage
if __name__ == "__main__":
    svg_code = generate_kolam(grid_size=7, pattern='flower')
    with open("kolam.svg", "w") as f:
        f.write(svg_code)
    print("Kolam SVG saved as kolam.svg")
