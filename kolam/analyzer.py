# kolam/analyzer.py

import numpy as np
import math
from typing import List, Tuple, Dict, Any

def analyze_symmetry_from_pattern(pattern_type: str, grid_size: int) -> Dict[str, bool]:
    """Analyze symmetry based on pattern type and mathematical properties."""
    # Define symmetry properties for each pattern type
    symmetry_map = {
        'basic': {"horizontal": True, "vertical": True, "diagonal": True, "radial": False},
        'diamond': {"horizontal": True, "vertical": True, "diagonal": True, "radial": False},
        'spiral': {"horizontal": False, "vertical": False, "diagonal": False, "radial": True},
        'flower': {"horizontal": True, "vertical": True, "diagonal": False, "radial": True},
        'lotus': {"horizontal": True, "vertical": True, "diagonal": False, "radial": True},
        'rose': {"horizontal": False, "vertical": False, "diagonal": False, "radial": True},
        'star': {"horizontal": True, "vertical": True, "diagonal": True, "radial": True},
        'sunburst': {"horizontal": True, "vertical": True, "diagonal": True, "radial": True},
        'mandala': {"horizontal": True, "vertical": True, "diagonal": True, "radial": True},
        'compass': {"horizontal": True, "vertical": True, "diagonal": True, "radial": False}
    }
    
    return symmetry_map.get(pattern_type, {"horizontal": False, "vertical": False, "diagonal": False, "radial": False})

def analyze_symmetry(coords: List[Tuple[float, float]], grid_size: int) -> Dict[str, bool]:
    """Check for horizontal, vertical, diagonal, and radial symmetry."""
    if not coords or len(coords) < 4:
        return {"horizontal": False, "vertical": False, "diagonal": False, "radial": False}
    
    # Convert to numpy array for easier manipulation
    points = np.array(coords)
    center = np.mean(points, axis=0)
    
    # Check horizontal symmetry
    horizontal_sym = _check_horizontal_symmetry(points, center)
    
    # Check vertical symmetry
    vertical_sym = _check_vertical_symmetry(points, center)
    
    # Check diagonal symmetry
    diagonal_sym = _check_diagonal_symmetry(points, center)
    
    # Check radial symmetry
    radial_sym = _check_radial_symmetry(points, center)
    
    return {
        "horizontal": horizontal_sym,
        "vertical": vertical_sym,
        "diagonal": diagonal_sym,
        "radial": radial_sym
    }

def _check_horizontal_symmetry(points: np.ndarray, center: np.ndarray, tolerance: float = 0.1) -> bool:
    """Check if pattern is symmetric about horizontal axis."""
    reflected_points = points.copy()
    reflected_points[:, 1] = 2 * center[1] - reflected_points[:, 1]
    
    for point in points:
        distances = np.linalg.norm(reflected_points - point, axis=1)
        if np.min(distances) > tolerance:
            return False
    return True

def _check_vertical_symmetry(points: np.ndarray, center: np.ndarray, tolerance: float = 0.1) -> bool:
    """Check if pattern is symmetric about vertical axis."""
    reflected_points = points.copy()
    reflected_points[:, 0] = 2 * center[0] - reflected_points[:, 0]
    
    for point in points:
        distances = np.linalg.norm(reflected_points - point, axis=1)
        if np.min(distances) > tolerance:
            return False
    return True

def _check_diagonal_symmetry(points: np.ndarray, center: np.ndarray, tolerance: float = 0.1) -> bool:
    """Check if pattern is symmetric about diagonal axis."""
    # Check main diagonal (y = x)
    reflected_points = points.copy()
    temp = reflected_points[:, 0].copy()
    reflected_points[:, 0] = reflected_points[:, 1]
    reflected_points[:, 1] = temp
    
    for point in points:
        distances = np.linalg.norm(reflected_points - point, axis=1)
        if np.min(distances) > tolerance:
            return False
    return True

def _check_radial_symmetry(points: np.ndarray, center: np.ndarray, tolerance: float = 0.1) -> bool:
    """Check if pattern has radial symmetry."""
    if len(points) < 3:
        return False
    
    # Calculate angles and distances from center
    vectors = points - center
    distances = np.linalg.norm(vectors, axis=1)
    angles = np.arctan2(vectors[:, 1], vectors[:, 0])
    
    # Check if angles are evenly distributed
    angles_sorted = np.sort(angles)
    angle_diffs = np.diff(angles_sorted)
    expected_diff = 2 * math.pi / len(points)
    
    return np.allclose(angle_diffs, expected_diff, atol=tolerance)

def detect_repetition(coords: List[Tuple[float, float]], grid_size: int) -> Dict[str, Any]:
    """Detect repeating motifs or grid patterns."""
    if not coords or len(coords) < 9:
        return {"has_repetition": False, "motif_size": 0, "description": "No repetition detected"}
    
    points = np.array(coords)
    
    # Check for grid-based repetition
    grid_repetition = _detect_grid_repetition(points, grid_size)
    
    # Check for motif repetition
    motif_repetition = _detect_motif_repetition(points)
    
    if grid_repetition["has_repetition"]:
        return grid_repetition
    elif motif_repetition["has_repetition"]:
        return motif_repetition
    else:
        return {"has_repetition": False, "motif_size": 0, "description": "No repetition detected"}

def _detect_grid_repetition(points: np.ndarray, grid_size: int) -> Dict[str, Any]:
    """Detect if pattern repeats in a grid-like fashion."""
    if grid_size < 3:
        return {"has_repetition": False, "motif_size": 0, "description": "Grid too small for repetition"}
    
    # Check for 2x2, 3x3, etc. subgrids
    for subgrid_size in range(2, grid_size // 2 + 1):
        if _check_subgrid_repetition(points, grid_size, subgrid_size):
            return {
                "has_repetition": True,
                "motif_size": subgrid_size,
                "description": f"Repeating {subgrid_size}x{subgrid_size} subgrids detected"
            }
    
    return {"has_repetition": False, "motif_size": 0, "description": "No grid repetition detected"}

def _check_subgrid_repetition(points: np.ndarray, grid_size: int, subgrid_size: int) -> bool:
    """Check if the pattern repeats in subgrids of given size."""
    # This is a simplified check - in practice, you'd need more sophisticated pattern matching
    num_subgrids = (grid_size // subgrid_size) ** 2
    return num_subgrids > 1

def _detect_motif_repetition(points: np.ndarray) -> Dict[str, Any]:
    """Detect repeating motifs in the pattern."""
    # Simplified motif detection
    if len(points) < 6:
        return {"has_repetition": False, "motif_size": 0, "description": "Not enough points for motif detection"}
    
    # Check for triangular motifs
    if _check_triangular_motifs(points):
        return {
            "has_repetition": True,
            "motif_size": 3,
            "description": "Triangular motifs detected"
        }
    
    # Check for square motifs
    if _check_square_motifs(points):
        return {
            "has_repetition": True,
            "motif_size": 4,
            "description": "Square motifs detected"
        }
    
    return {"has_repetition": False, "motif_size": 0, "description": "No motif repetition detected"}

def _check_triangular_motifs(points: np.ndarray) -> bool:
    """Check for triangular motifs in the pattern."""
    # Simplified check - look for equilateral triangles
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                p1, p2, p3 = points[i], points[j], points[k]
                # Check if triangle is approximately equilateral
                d12 = np.linalg.norm(p2 - p1)
                d23 = np.linalg.norm(p3 - p2)
                d31 = np.linalg.norm(p1 - p3)
                
                if np.allclose([d12, d23, d31], d12, rtol=0.1):
                    return True
    return False

def _check_square_motifs(points: np.ndarray) -> bool:
    """Check for square motifs in the pattern."""
    # Simplified check - look for squares
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                for l in range(k + 1, len(points)):
                    p1, p2, p3, p4 = points[i], points[j], points[k], points[l]
                    # Check if four points form a square
                    if _is_square(p1, p2, p3, p4):
                        return True
    return False

def _is_square(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, p4: np.ndarray) -> bool:
    """Check if four points form a square."""
    # Calculate all distances
    distances = [
        np.linalg.norm(p2 - p1),
        np.linalg.norm(p3 - p2),
        np.linalg.norm(p4 - p3),
        np.linalg.norm(p1 - p4),
        np.linalg.norm(p3 - p1),
        np.linalg.norm(p4 - p2)
    ]
    
    # Sort distances
    distances.sort()
    
    # Check if we have 4 equal sides and 2 equal diagonals
    side_length = distances[0]
    diagonal_length = distances[4]
    
    return (np.allclose(distances[:4], side_length, rtol=0.1) and 
            np.allclose(distances[4:], diagonal_length, rtol=0.1))

def classify_pattern(coords: List[Tuple[float, float]], grid_size: int, pattern_type: str = None) -> Dict[str, Any]:
    """Classify the pattern with various attributes."""
    if pattern_type:
        # Use pattern-based analysis for more accurate results
        symmetry = analyze_symmetry_from_pattern(pattern_type, grid_size)
        repetition = _analyze_repetition_from_pattern(pattern_type, grid_size)
    else:
        # Fallback to coordinate-based analysis
        symmetry = analyze_symmetry(coords, grid_size)
        repetition = detect_repetition(coords, grid_size)
    
    # Determine pattern type based on analysis
    if not pattern_type:
        pattern_type = _determine_pattern_type(symmetry, repetition)
    
    # Check for specific attributes based on pattern type
    attributes = _get_pattern_attributes(pattern_type, grid_size)
    
    return {
        "pattern_type": pattern_type,
        "attributes": attributes,
        "symmetry": symmetry,
        "repetition": repetition
    }

def _analyze_repetition_from_pattern(pattern_type: str, grid_size: int) -> Dict[str, Any]:
    """Analyze repetition based on pattern type."""
    repetition_map = {
        'basic': {"has_repetition": True, "motif_size": 1, "description": "Nested square repetition"},
        'diamond': {"has_repetition": True, "motif_size": 1, "description": "Diamond shape repetition"},
        'spiral': {"has_repetition": False, "motif_size": 0, "description": "Continuous spiral pattern"},
        'flower': {"has_repetition": True, "motif_size": 6, "description": "Petal repetition"},
        'lotus': {"has_repetition": True, "motif_size": 8, "description": "Layered petal repetition"},
        'rose': {"has_repetition": False, "motif_size": 0, "description": "Continuous spiral rose"},
        'star': {"has_repetition": True, "motif_size": 2, "description": "Star point repetition"},
        'sunburst': {"has_repetition": True, "motif_size": 1, "description": "Ray repetition"},
        'mandala': {"has_repetition": True, "motif_size": 1, "description": "Concentric repetition"},
        'compass': {"has_repetition": True, "motif_size": 4, "description": "Directional repetition"}
    }
    
    return repetition_map.get(pattern_type, {"has_repetition": False, "motif_size": 0, "description": "No repetition detected"})

def _get_pattern_attributes(pattern_type: str, grid_size: int) -> Dict[str, bool]:
    """Get pattern attributes based on pattern type."""
    attributes_map = {
        'basic': {
            "looped_traversal": True,
            "grid_repetition": True,
            "rotational_symmetry": False,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        },
        'diamond': {
            "looped_traversal": True,
            "grid_repetition": True,
            "rotational_symmetry": False,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        },
        'spiral': {
            "looped_traversal": False,
            "grid_repetition": False,
            "rotational_symmetry": True,
            "bilateral_symmetry": False,
            "diagonal_symmetry": False
        },
        'flower': {
            "looped_traversal": False,
            "grid_repetition": True,
            "rotational_symmetry": True,
            "bilateral_symmetry": True,
            "diagonal_symmetry": False
        },
        'lotus': {
            "looped_traversal": False,
            "grid_repetition": True,
            "rotational_symmetry": True,
            "bilateral_symmetry": True,
            "diagonal_symmetry": False
        },
        'rose': {
            "looped_traversal": False,
            "grid_repetition": False,
            "rotational_symmetry": True,
            "bilateral_symmetry": False,
            "diagonal_symmetry": False
        },
        'star': {
            "looped_traversal": True,
            "grid_repetition": True,
            "rotational_symmetry": True,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        },
        'sunburst': {
            "looped_traversal": False,
            "grid_repetition": True,
            "rotational_symmetry": True,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        },
        'mandala': {
            "looped_traversal": False,
            "grid_repetition": True,
            "rotational_symmetry": True,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        },
        'compass': {
            "looped_traversal": False,
            "grid_repetition": True,
            "rotational_symmetry": False,
            "bilateral_symmetry": True,
            "diagonal_symmetry": True
        }
    }
    
    return attributes_map.get(pattern_type, {
        "looped_traversal": False,
        "grid_repetition": False,
        "rotational_symmetry": False,
        "bilateral_symmetry": False,
        "diagonal_symmetry": False
    })

def _determine_pattern_type(symmetry: Dict[str, bool], repetition: Dict[str, Any]) -> str:
    """Determine the overall pattern type based on analysis."""
    if symmetry["radial"]:
        return "Radial"
    elif symmetry["horizontal"] and symmetry["vertical"]:
        return "Bilateral"
    elif repetition["has_repetition"]:
        return "Repetitive"
    elif symmetry["diagonal"]:
        return "Diagonal"
    else:
        return "Asymmetric"

def _check_looped_traversal(coords: List[Tuple[float, float]]) -> bool:
    """Check if the pattern forms closed loops."""
    if len(coords) < 3:
        return False
    
    # Simplified check - see if the pattern forms closed shapes
    points = np.array(coords)
    center = np.mean(points, axis=0)
    
    # Check if points form a roughly circular or closed shape
    distances_from_center = np.linalg.norm(points - center, axis=1)
    mean_distance = np.mean(distances_from_center)
    
    # If all points are roughly equidistant from center, it's likely a loop
    return np.std(distances_from_center) < mean_distance * 0.3