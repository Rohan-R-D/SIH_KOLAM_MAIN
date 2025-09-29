# kolam/utils.py

def validate_pattern(pattern):
    """Ensure the pattern is one of the supported types."""
    valid_patterns = [
        'basic', 'diamond', 'spiral',
        'flower', 'lotus', 'rose',
        'star', 'sunburst', 'mandala', 'compass'
    ]
    return pattern if pattern in valid_patterns else 'basic'


def clamp_grid_size(size, min_size=3, max_size=15):
    """Clamp grid size to a reasonable range."""
    try:
        size = int(size)
    except ValueError:
        size = 7
    return max(min(size, max_size), min_size)


def generate_grid_coordinates(grid_size):
    """Generate (x, y) coordinates for a square grid."""
    spacing = 40
    padding = 20
    coords = []
    for row in range(grid_size):
        for col in range(grid_size):
            x = padding + col * spacing
            y = padding + row * spacing
            coords.append((x, y))
    return coords


def wrap_svg(content, width=400, height=400):
    """Wrap SVG content in a full SVG tag."""
    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{content}
</svg>"""


def get_pattern_categories():
    """Get organized pattern categories."""
    return {
        "Basic Patterns": ["basic", "diamond", "spiral"],
        "Flower Patterns": ["flower", "lotus", "rose"],
        "Star Patterns": ["star", "sunburst", "mandala", "compass"]
    }


def get_pattern_description(pattern):
    """Get description for a pattern type."""
    descriptions = {
        "basic": "Nested squares with geometric symmetry",
        "diamond": "Diamond shapes with diagonal connections",
        "spiral": "Spiral patterns with continuous curves",
        "flower": "Flower patterns with petal arrangements",
        "lotus": "Layered lotus patterns with multiple petals",
        "rose": "Spiral rose patterns with intricate curves",
        "star": "Multi-pointed star patterns",
        "sunburst": "Radiating lines from center",
        "mandala": "Concentric circles with geometric shapes",
        "compass": "Compass patterns with cardinal directions"
    }
    return descriptions.get(pattern, "Traditional Kolam pattern")


def get_symmetry_explanation(symmetry_type):
    """Get explanation for symmetry types."""
    explanations = {
        "horizontal": "Pattern is symmetric about a horizontal line",
        "vertical": "Pattern is symmetric about a vertical line",
        "diagonal": "Pattern is symmetric about diagonal axes",
        "radial": "Pattern has rotational symmetry around center"
    }
    return explanations.get(symmetry_type, "Unknown symmetry type")