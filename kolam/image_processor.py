# kolam/image_processor.py

import cv2
import numpy as np
from typing import List, Tuple, Dict, Any
import json
from PIL import Image
import io
import base64

def process_uploaded_image(image_data: str) -> Dict[str, Any]:
    """Process uploaded image to detect dots and reconstruct pattern."""
    try:
        # Handle different base64 formats
        if ',' in image_data:
            # Data URL format: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
            header, encoded = image_data.split(',', 1)
        else:
            # Raw base64
            encoded = image_data
        
        # Decode base64 image
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect dots
        dots = detect_dots(cv_image)
        
        # Construct graph from dots
        graph = construct_graph_from_dots(dots)
        
        # Infer pattern
        pattern_info = infer_pattern_from_graph(graph, dots)
        
        return {
            "success": True,
            "dots": dots,
            "graph": graph,
            "pattern_info": pattern_info
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "error": f"Image processing failed: {str(e)}",
            "details": error_details
        }

def detect_dots(image: np.ndarray) -> List[Tuple[int, int]]:
    """Detect dots in the image using OpenCV."""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        dots = []
        
        # Method 1: HoughCircles to detect circular dots
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=3,
            maxRadius=15
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                dots.append((x, y))
        
        # Method 2: If HoughCircles doesn't work well, try contour detection
        if len(dots) < 4:
            dots = detect_dots_by_contours(gray)
        
        # Method 3: If still not enough dots, try adaptive thresholding
        if len(dots) < 3:
            dots = detect_dots_adaptive_threshold(blurred)
        
        # Remove duplicate dots (within 15 pixels of each other)
        unique_dots = []
        for dot in dots:
            is_duplicate = False
            for unique_dot in unique_dots:
                if ((dot[0] - unique_dot[0])**2 + (dot[1] - unique_dot[1])**2)**0.5 < 15:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_dots.append(dot)
        
        return unique_dots
        
    except Exception as e:
        # Return some default dots if detection fails
        return [(100, 100), (200, 100), (150, 200), (100, 200), (200, 200)]

def detect_dots_by_contours(gray_image: np.ndarray) -> List[Tuple[int, int]]:
    """Detect dots using contour detection as fallback."""
    # Apply threshold
    _, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    dots = []
    for contour in contours:
        # Calculate contour area
        area = cv2.contourArea(contour)
        
        # Filter by area (dots should be small)
        if 10 < area < 200:
            # Calculate centroid
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                dots.append((cx, cy))
    
    return dots

def detect_dots_adaptive_threshold(blurred_image: np.ndarray) -> List[Tuple[int, int]]:
    """Detect dots using adaptive thresholding as final fallback."""
    # Use adaptive thresholding to handle varying lighting
    thresh = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    dots = []
    for contour in contours:
        # Filter contours by area to identify dots
        area = cv2.contourArea(contour)
        if 5 < area < 1000:  # More flexible area range
            # Get the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                dots.append((cX, cY))
    
    return dots

def construct_graph_from_dots(dots: List[Tuple[int, int]]) -> Dict[str, Any]:
    """Construct a graph from detected dots."""
    if len(dots) < 2:
        return {"nodes": [], "edges": []}
    
    # Create nodes from dots
    nodes = [{"id": i, "x": x, "y": y} for i, (x, y) in enumerate(dots)]
    
    # Find edges by connecting nearby dots
    edges = []
    max_distance = 50  # Maximum distance to connect dots
    
    for i, dot1 in enumerate(dots):
        for j, dot2 in enumerate(dots[i+1:], i+1):
            distance = np.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
            if distance <= max_distance:
                edges.append({"from": i, "to": j, "distance": distance})
    
    return {
        "nodes": nodes,
        "edges": edges
    }

def infer_pattern_from_graph(graph: Dict[str, Any], dots: List[Tuple[int, int]]) -> Dict[str, Any]:
    """Infer pattern characteristics from the graph and suggest similar Kolam patterns."""
    nodes = graph["nodes"]
    edges = graph["edges"]
    
    if not nodes:
        return {"type": "unknown", "complexity": 0, "suggested_patterns": []}
    
    # Calculate basic statistics
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    # Analyze geometric properties
    if len(dots) >= 3:
        # Calculate bounding box
        x_coords = [dot[0] for dot in dots]
        y_coords = [dot[1] for dot in dots]
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        aspect_ratio = width / height if height > 0 else 1
        
        # Calculate center
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        # Calculate distances from center
        distances = [((x - center_x)**2 + (y - center_y)**2)**0.5 for x, y in dots]
        avg_distance = sum(distances) / len(distances)
        distance_variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
        
        # Determine pattern type based on geometric analysis
        if distance_variance < avg_distance * 0.1:
            # Points are roughly equidistant from center - likely radial pattern
            if num_edges > num_nodes * 2:
                pattern_type = "mandala"
            elif num_edges > num_nodes:
                pattern_type = "sunburst"
            else:
                pattern_type = "star"
        elif aspect_ratio > 1.5 or aspect_ratio < 0.67:
            # Non-square aspect ratio - likely linear pattern
            pattern_type = "spiral"
        elif num_edges == 0:
            pattern_type = "isolated_dots"
        elif num_edges == num_nodes - 1:
            pattern_type = "tree"
        elif num_edges > num_nodes * 1.5:
            pattern_type = "complex_graph"
        else:
            pattern_type = "simple_graph"
    else:
        pattern_type = "unknown"
    
    # Calculate complexity score
    complexity = (num_edges / max(num_nodes, 1)) * 10
    
    # Check for symmetry
    symmetry = check_image_symmetry(dots)
    
    # Suggest similar Kolam patterns based on analysis
    suggested_patterns = _suggest_patterns_from_analysis(pattern_type, symmetry, complexity, num_nodes)
    
    return {
        "type": pattern_type,
        "complexity": complexity,
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "symmetry": symmetry,
        "suggested_patterns": suggested_patterns
    }

def _suggest_patterns_from_analysis(pattern_type: str, symmetry: Dict[str, bool], 
                                  complexity: float, num_nodes: int) -> List[str]:
    """Suggest Kolam patterns based on image analysis."""
    suggestions = []
    
    # Based on symmetry analysis
    if symmetry.get("radial", False):
        if complexity > 5:
            suggestions.extend(["mandala", "sunburst"])
        else:
            suggestions.extend(["star", "flower"])
    
    if symmetry.get("horizontal", False) and symmetry.get("vertical", False):
        if complexity > 3:
            suggestions.extend(["basic", "diamond"])
        else:
            suggestions.extend(["compass"])
    
    # Based on pattern type
    if pattern_type == "mandala":
        suggestions.extend(["mandala", "sunburst", "star"])
    elif pattern_type == "star":
        suggestions.extend(["star", "sunburst", "compass"])
    elif pattern_type == "spiral":
        suggestions.extend(["spiral", "rose"])
    elif pattern_type == "tree":
        suggestions.extend(["flower", "lotus"])
    elif pattern_type == "complex_graph":
        suggestions.extend(["mandala", "basic", "diamond"])
    
    # Based on complexity
    if complexity > 7:
        suggestions.extend(["mandala", "lotus", "rose"])
    elif complexity > 4:
        suggestions.extend(["star", "sunburst", "flower"])
    else:
        suggestions.extend(["basic", "diamond", "compass"])
    
    # Based on number of nodes
    if num_nodes > 20:
        suggestions.extend(["mandala", "lotus"])
    elif num_nodes > 10:
        suggestions.extend(["star", "sunburst", "flower"])
    else:
        suggestions.extend(["basic", "diamond", "compass"])
    
    # Remove duplicates and return top suggestions
    unique_suggestions = list(dict.fromkeys(suggestions))
    return unique_suggestions[:5]  # Return top 5 suggestions

def check_image_symmetry(dots: List[Tuple[int, int]]) -> Dict[str, bool]:
    """Check symmetry of detected dots."""
    if len(dots) < 4:
        return {"horizontal": False, "vertical": False, "radial": False}
    
    points = np.array(dots)
    center = np.mean(points, axis=0)
    
    # Check horizontal symmetry
    horizontal_sym = _check_horizontal_symmetry_image(points, center)
    
    # Check vertical symmetry
    vertical_sym = _check_vertical_symmetry_image(points, center)
    
    # Check radial symmetry
    radial_sym = _check_radial_symmetry_image(points, center)
    
    return {
        "horizontal": horizontal_sym,
        "vertical": vertical_sym,
        "radial": radial_sym
    }

def _check_horizontal_symmetry_image(points: np.ndarray, center: np.ndarray, tolerance: float = 20) -> bool:
    """Check horizontal symmetry for image dots."""
    reflected_points = points.copy()
    reflected_points[:, 1] = 2 * center[1] - reflected_points[:, 1]
    
    for point in points:
        distances = np.linalg.norm(reflected_points - point, axis=1)
        if np.min(distances) > tolerance:
            return False
    return True

def _check_vertical_symmetry_image(points: np.ndarray, center: np.ndarray, tolerance: float = 20) -> bool:
    """Check vertical symmetry for image dots."""
    reflected_points = points.copy()
    reflected_points[:, 0] = 2 * center[0] - reflected_points[:, 0]
    
    for point in points:
        distances = np.linalg.norm(reflected_points - point, axis=1)
        if np.min(distances) > tolerance:
            return False
    return True

def _check_radial_symmetry_image(points: np.ndarray, center: np.ndarray, tolerance: float = 20) -> bool:
    """Check radial symmetry for image dots."""
    if len(points) < 3:
        return False
    
    # Calculate angles and distances from center
    vectors = points - center
    distances = np.linalg.norm(vectors, axis=1)
    angles = np.arctan2(vectors[:, 1], vectors[:, 0])
    
    # Check if angles are evenly distributed
    angles_sorted = np.sort(angles)
    angle_diffs = np.diff(angles_sorted)
    expected_diff = 2 * np.pi / len(points)
    
    return np.allclose(angle_diffs, expected_diff, atol=tolerance)

def generate_svg_from_detected_pattern(dots: List[Tuple[int, int]], 
                                     graph: Dict[str, Any]) -> str:
    """Generate SVG from detected pattern."""
    if not dots:
        return ""
    
    # Calculate bounding box
    x_coords = [dot[0] for dot in dots]
    y_coords = [dot[1] for dot in dots]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    width = max_x - min_x + 40
    height = max_y - min_y + 40
    
    # Start SVG
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += f'<rect width="100%" height="100%" fill="white"/>'
    
    # Draw edges
    for edge in graph["edges"]:
        from_node = graph["nodes"][edge["from"]]
        to_node = graph["nodes"][edge["to"]]
        
        x1 = from_node["x"] - min_x + 20
        y1 = from_node["y"] - min_y + 20
        x2 = to_node["x"] - min_x + 20
        y2 = to_node["y"] - min_y + 20
        
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="blue" stroke-width="2"/>'
    
    # Draw nodes
    for node in graph["nodes"]:
        x = node["x"] - min_x + 20
        y = node["y"] - min_y + 20
        svg += f'<circle cx="{x}" cy="{y}" r="3" fill="red"/>'
    
    svg += '</svg>'
    return svg

def enhance_image_for_detection(image: np.ndarray) -> np.ndarray:
    """Enhance image to improve dot detection."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization
    equalized = cv2.equalizeHist(gray)
    
    # Apply bilateral filter to reduce noise while preserving edges
    filtered = cv2.bilateralFilter(equalized, 9, 75, 75)
    
    # Apply morphological operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
    
    return cleaned
