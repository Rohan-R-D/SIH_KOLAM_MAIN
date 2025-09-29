# kolam/exporter.py

import os
import json
import qrcode
from datetime import datetime
from typing import List, Dict, Any
import base64
from io import BytesIO

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def save_svg(svg_string: str, filename: str = "kolam.svg", output_dir: str = None) -> str:
    """Save SVG string to a file in exports/ and return filename."""
    if output_dir is None:
        output_dir = EXPORT_DIR
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_string)
    return filename  # return just the filename

def convert_svg_to_png(svg_string: str, filename: str = "kolam.png", output_dir: str = None) -> str:
    """Convert SVG string to PNG using an advanced SVG parser that handles paths and curves."""
    try:
        from PIL import Image, ImageDraw
        import xml.etree.ElementTree as ET
        import re
        import math
    except ImportError as e:
        raise ImportError(f"Please install Pillow: pip install Pillow. Error: {e}")

    if output_dir is None:
        output_dir = EXPORT_DIR
    filepath = os.path.join(output_dir, filename)
    
    def parse_color(color_str):
        """Parse color string to RGB tuple."""
        if not color_str or color_str == 'none':
            return None
        
        # Handle hsl colors
        if color_str.startswith('hsl('):
            # Extract HSL values
            match = re.match(r'hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)', color_str)
            if match:
                h, s, l = map(int, match.groups())
                # Convert HSL to RGB
                h = h / 360.0
                s = s / 100.0
                l = l / 100.0
                
                if s == 0:
                    r = g = b = l
                else:
                    def hue_to_rgb(p, q, t):
                        if t < 0: t += 1
                        if t > 1: t -= 1
                        if t < 1/6: return p + (q - p) * 6 * t
                        if t < 1/2: return q
                        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
                        return p
                    
                    q = l * (1 + s) if l < 0.5 else l + s - l * s
                    p = 2 * l - q
                    r = hue_to_rgb(p, q, h + 1/3)
                    g = hue_to_rgb(p, q, h)
                    b = hue_to_rgb(p, q, h - 1/3)
                
                return (int(r * 255), int(g * 255), int(b * 255))
        
        # Handle hex colors
        if color_str.startswith('#'):
            hex_color = color_str.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Handle named colors (basic)
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
        }
        return color_map.get(color_str.lower(), (0, 0, 0))
    
    def parse_path_data(path_data):
        """Parse SVG path data and return list of drawing commands."""
        commands = []
        # Simple regex to split path commands
        pattern = r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)'
        matches = re.findall(pattern, path_data)
        
        for cmd, params in matches:
            coords = [float(x) for x in re.findall(r'-?\d+\.?\d*', params)]
            commands.append((cmd, coords))
        
        return commands
    
    def draw_quadratic_bezier(draw, start, control, end, color, width, steps=20):
        """Draw a quadratic Bézier curve."""
        points = []
        for i in range(steps + 1):
            t = i / steps
            # Quadratic Bézier formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
            y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
            points.append((x, y))
        
        # Draw the curve as connected line segments
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=color, width=width)
    
    try:
        # Parse SVG
        root = ET.fromstring(svg_string)
        
        # Get SVG dimensions
        width = int(float(root.get('width', '400')))
        height = int(float(root.get('height', '400')))
        
        # Create image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Process all elements
        for elem in root.iter():
            if elem.tag.endswith('rect') and elem.get('width') == '100%':
                # Background rectangle
                fill_color = parse_color(elem.get('fill', 'white'))
                if fill_color:
                    draw.rectangle([0, 0, width, height], fill=fill_color)
            
            elif elem.tag.endswith('path'):
                # Handle path elements (most important for Kolam patterns)
                path_data = elem.get('d', '')
                stroke_color = parse_color(elem.get('stroke', 'black'))
                stroke_width = int(float(elem.get('stroke-width', '2')))
                fill_color = parse_color(elem.get('fill', 'none'))
                
                if path_data and stroke_color:
                    commands = parse_path_data(path_data)
                    current_pos = (0, 0)
                    
                    for cmd, coords in commands:
                        if cmd == 'M':  # Move to
                            current_pos = (coords[0], coords[1])
                        elif cmd == 'Q':  # Quadratic Bézier curve
                            if len(coords) >= 4:
                                control = (coords[0], coords[1])
                                end = (coords[2], coords[3])
                                draw_quadratic_bezier(draw, current_pos, control, end, stroke_color, stroke_width)
                                current_pos = end
                        elif cmd == 'L':  # Line to
                            if len(coords) >= 2:
                                end = (coords[0], coords[1])
                                draw.line([current_pos, end], fill=stroke_color, width=stroke_width)
                                current_pos = end
                        elif cmd == 'Z':  # Close path
                            pass  # Not needed for stroke-only paths
            
            elif elem.tag.endswith('circle'):
                cx = float(elem.get('cx', width/2))
                cy = float(elem.get('cy', height/2))
                r = float(elem.get('r', 50))
                fill_color = parse_color(elem.get('fill', 'black'))
                stroke_color = parse_color(elem.get('stroke', 'black'))
                stroke_width = int(float(elem.get('stroke-width', '1')))
                
                if fill_color:
                    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill_color)
                if stroke_color:
                    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=stroke_color, width=stroke_width)
            
            elif elem.tag.endswith('rect') and elem.get('width') != '100%':
                x = float(elem.get('x', 0))
                y = float(elem.get('y', 0))
                w = float(elem.get('width', 100))
                h = float(elem.get('height', 100))
                fill_color = parse_color(elem.get('fill', 'black'))
                stroke_color = parse_color(elem.get('stroke', 'black'))
                stroke_width = int(float(elem.get('stroke-width', '1')))
                
                if fill_color:
                    draw.rectangle([x, y, x+w, y+h], fill=fill_color)
                if stroke_color:
                    draw.rectangle([x, y, x+w, y+h], outline=stroke_color, width=stroke_width)
            
            elif elem.tag.endswith('line'):
                x1 = float(elem.get('x1', 0))
                y1 = float(elem.get('y1', 0))
                x2 = float(elem.get('x2', 100))
                y2 = float(elem.get('y2', 100))
                stroke_color = parse_color(elem.get('stroke', 'black'))
                stroke_width = int(float(elem.get('stroke-width', '1')))
                
                if stroke_color:
                    draw.line([x1, y1, x2, y2], fill=stroke_color, width=stroke_width)
        
        img.save(filepath, 'PNG')
        
    except Exception as e:
        # Fallback to simple placeholder if SVG parsing fails
        img = Image.new('RGB', (400, 400), color='white')
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 350, 350], outline='black', width=2)
        draw.text((200, 200), f"SVG Export Error: {str(e)[:50]}", fill='black', anchor='mm')
        img.save(filepath, 'PNG')
    
    return filename

def convert_svg_to_jpg(svg_string: str, filename: str = "kolam.jpg", output_dir: str = None) -> str:
    """Convert SVG string to JPG using a simple fallback method and return filename."""
    try:
        from PIL import Image, ImageDraw
    except ImportError as e:
        raise ImportError(f"Please install Pillow: pip install Pillow. Error: {e}")

    if output_dir is None:
        output_dir = EXPORT_DIR
    
    # Convert to PNG first using our fallback method
    png_path = os.path.join(output_dir, filename.replace('.jpg', '.png'))
    png_file = convert_svg_to_png(svg_string, os.path.basename(png_path), output_dir)

    # Convert PNG to JPG
    with Image.open(os.path.join(output_dir, png_file)) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        jpg_path = os.path.join(output_dir, filename)
        img.save(jpg_path, 'JPEG', quality=95)

    os.remove(os.path.join(output_dir, png_file))  # cleanup temp PNG
    return filename



def batch_export_patterns(patterns: List[Dict[str, Any]], output_dir: str = "exports") -> Dict[str, List[str]]:
    """Export multiple patterns in batch."""
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "svg_files": [],
        "png_files": [],
        "jpg_files": [],
        "metadata_files": []
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, pattern_data in enumerate(patterns):
        pattern_name = pattern_data.get("name", f"pattern_{i+1}")
        svg_content = pattern_data.get("svg", "")
        metadata = pattern_data.get("metadata", {})
        
        if svg_content:
            # Export SVG
            svg_filename = f"{pattern_name}_{timestamp}.svg"
            svg_path = save_svg(svg_content, svg_filename, output_dir)
            results["svg_files"].append(svg_path)
            
            # Export PNG
            png_filename = f"{pattern_name}_{timestamp}.png"
            png_path = convert_svg_to_png(svg_content, png_filename, output_dir)
            results["png_files"].append(png_path)
            
            # Export JPG
            jpg_filename = f"{pattern_name}_{timestamp}.jpg"
            jpg_path = convert_svg_to_jpg(svg_content, jpg_filename, output_dir)
            results["jpg_files"].append(jpg_path)
            
            # Save metadata
            metadata_filename = f"{pattern_name}_{timestamp}_metadata.json"
            metadata_path = os.path.join(output_dir, metadata_filename)
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
            results["metadata_files"].append(metadata_path)
    
    return results

def generate_qr_code(data: str, filename: str = "kolam_qr.png", output_dir: str = "exports") -> str:
    """Generate QR code for sharing Kolam patterns."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Limit data size to prevent version overflow
    if len(data) > 2000:  # Limit to prevent version 41+ error
        data = data[:2000]
    
    qr = qrcode.QRCode(
        version=None,  # Let it auto-determine version
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    return filepath

def create_shareable_link(pattern_data: Dict[str, Any], base_url: str = "http://localhost:5000") -> str:
    """Create a shareable link for a Kolam pattern."""
    # Encode pattern data as base64
    pattern_json = json.dumps(pattern_data)
    encoded_data = base64.b64encode(pattern_json.encode()).decode()
    
    # Create shareable URL
    shareable_url = f"{base_url}/shared/{encoded_data}"
    return shareable_url

def export_pattern_with_metadata(svg_string: str, metadata: Dict[str, Any], 
                               filename_prefix: str = "kolam", output_dir: str = "exports") -> Dict[str, str]:
    """Export pattern with comprehensive metadata."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}
    
    # Export SVG
    svg_filename = f"{filename_prefix}_{timestamp}.svg"
    svg_path = save_svg(svg_string, svg_filename, output_dir)
    results["svg"] = svg_path
    
    # Export PNG
    png_filename = f"{filename_prefix}_{timestamp}.png"
    png_path = convert_svg_to_png(svg_string, png_filename, output_dir)
    results["png"] = png_path
    
    # Export JPG
    jpg_filename = f"{filename_prefix}_{timestamp}.jpg"
    jpg_path = convert_svg_to_jpg(svg_string, jpg_filename, output_dir)
    results["jpg"] = jpg_path
    
    # Save metadata
    metadata_filename = f"{filename_prefix}_{timestamp}_metadata.json"
    metadata_path = os.path.join(output_dir, metadata_filename)
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    results["metadata"] = metadata_path
    
    # Generate QR code
    qr_data = json.dumps({
        "pattern": svg_string,
        "metadata": metadata,
        "timestamp": timestamp
    })
    qr_filename = f"{filename_prefix}_{timestamp}_qr.png"
    qr_path = generate_qr_code(qr_data, qr_filename, output_dir)
    results["qr_code"] = qr_path
    
    return results

def create_zip_archive(file_paths: List[str], zip_filename: str = "kolam_patterns.zip", 
                      output_dir: str = "exports") -> str:
    """Create a ZIP archive of exported files."""
    import zipfile
    
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if os.path.exists(file_path):
                # Get relative path for archive
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname)
    
    return zip_path

def generate_shareable_link(pattern_data: Dict[str, Any], base_url: str = "http://localhost:5000") -> str:
    """Generate a shareable link for a pattern."""
    import base64
    import json
    
    # Encode pattern data as base64
    pattern_json = json.dumps(pattern_data)
    encoded_data = base64.b64encode(pattern_json.encode()).decode()
    
    # Create shareable link
    shareable_link = f"{base_url}/shared/{encoded_data}"
    return shareable_link

def generate_qr_code_for_sharing(shareable_link: str, filename: str = "kolam_qr.png") -> str:
    """Generate QR code for sharing."""
    import qrcode
    import os
    
    # Limit link size to prevent version overflow
    if len(shareable_link) > 2000:
        shareable_link = shareable_link[:2000]
    
    qr = qrcode.QRCode(
        version=None,  # Let it auto-determine version
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(shareable_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(EXPORT_DIR, filename)
    img.save(qr_path)
    
    return qr_path

def batch_export_with_sharing(patterns: List[Dict[str, Any]], include_qr: bool = True, 
                            include_shareable_link: bool = True) -> Dict[str, Any]:
    """Export multiple patterns with sharing options."""
    results = {
        "files": [],
        "qr_codes": [],
        "shareable_links": [],
        "zip_archive": None
    }
    
    # Export each pattern
    for i, pattern in enumerate(patterns):
        pattern_results = export_pattern_with_metadata(
            pattern['svg'], 
            pattern.get('metadata', {}), 
            f"pattern_{i+1}"
        )
        results["files"].extend(list(pattern_results.values()))
        
        # Generate QR code if requested
        if include_qr:
            qr_data = json.dumps({
                "pattern": pattern['svg'],
                "metadata": pattern.get('metadata', {}),
                "timestamp": datetime.now().isoformat()
            })
            qr_filename = f"pattern_{i+1}_qr.png"
            qr_path = generate_qr_code(qr_data, qr_filename)
            results["qr_codes"].append(qr_path)
        
        # Generate shareable link if requested
        if include_shareable_link:
            shareable_link = generate_shareable_link(pattern)
            results["shareable_links"].append(shareable_link)
    
    # Create ZIP archive
    zip_path = create_zip_archive(patterns, "kolam_batch_export")
    results["zip_archive"] = zip_path
    
    return results