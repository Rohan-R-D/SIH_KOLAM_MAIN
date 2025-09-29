from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import base64
from kolam.generator import generate_kolam, generate_kolam_with_analysis, generate_kolam_clean
from kolam.animated_generator import generate_animated_kolam
from kolam.analyzer import analyze_symmetry, detect_repetition, classify_pattern
from kolam.exporter import (
    save_svg, convert_svg_to_png, convert_svg_to_jpg, 
    batch_export_patterns, export_pattern_with_metadata,
    create_shareable_link, generate_qr_code
)
from kolam.animation import generate_animation_frames, create_animation_svg, highlight_symmetry_axes
from kolam.image_processor import process_uploaded_image, generate_svg_from_detected_pattern
from kolam.utils import get_pattern_categories, get_pattern_description, get_symmetry_explanation
import pathlib

# Explicitly set template and static folder paths for Vercel serverless environment
template_dir = pathlib.Path(__file__).parent.parent / 'templates'
static_dir = pathlib.Path(__file__).parent.parent / 'static'

app = Flask(__name__, template_folder=str(template_dir), static_folder=str(static_dir))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    pattern_categories = get_pattern_categories()
    return render_template('index.html', 
                         svg=None, 
                         grid_size=7, 
                         pattern='basic',
                         pattern_categories=pattern_categories,
                         analysis=None,
                         get_pattern_description=get_pattern_description,
                         get_symmetry_explanation=get_symmetry_explanation)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        grid_size = request.form.get('grid_size', 7)
        pattern = request.form.get('pattern', 'basic')
        include_analysis = request.form.get('include_analysis', 'false') == 'true'
    else:
        grid_size = request.args.get('grid_size', 7)
        pattern = request.args.get('pattern', 'basic')
        include_analysis = request.args.get('include_analysis', 'false') == 'true'

    try:
        grid_size = int(grid_size)
    except ValueError:
        grid_size = 7

    if include_analysis:
        result = generate_kolam_with_analysis(grid_size=grid_size, pattern=pattern)
        svg = result['svg']
        analysis = result['analysis']
    else:
        svg = generate_animated_kolam(grid_size=grid_size, pattern=pattern)
        analysis = None

    pattern_categories = get_pattern_categories()
    return render_template('index.html', 
                         svg=svg, 
                         grid_size=grid_size, 
                         pattern=pattern,
                         pattern_categories=pattern_categories,
                         analysis=analysis,
                         get_pattern_description=get_pattern_description,
                         get_symmetry_explanation=get_symmetry_explanation)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    svg_content = data.get('svg', '')
    grid_size = data.get('grid_size', 7)
    
    from kolam.utils import generate_grid_coordinates
    coords = generate_grid_coordinates(grid_size)
    
    analysis = classify_pattern(coords, grid_size)
    
    return jsonify(analysis)

@app.route('/animate', methods=['POST'])
def animate():
    data = request.get_json()
    pattern = data.get('pattern', 'basic').lower()
    grid_size = data.get('grid_size', 7)
    frame_count = data.get('frame_count', 30)
    
    frames = generate_animation_frames('', grid_size, pattern, frame_count)
    
    animated_svg = create_animation_svg(frames, duration=3.0)
    
    return jsonify({'animated_svg': animated_svg, 'frames': frames})

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data received'})
        
        image_data = data.get('image', '')
        if not image_data:
            return jsonify({'success': False, 'error': 'No image data provided'})
        
        result = process_uploaded_image(image_data)
        
        if result['success']:
            svg_content = generate_svg_from_detected_pattern(
                result['dots'], 
                result['graph']
            )
            result['svg'] = svg_content
            
            if 'pattern_info' in result and 'suggested_patterns' in result['pattern_info']:
                result['suggested_patterns'] = result['pattern_info']['suggested_patterns']
        else:
            print(f"Image processing error: {result.get('error', 'Unknown error')}")
            if 'details' in result:
                print(f"Error details: {result['details']}")
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Upload route error: {str(e)}")
        print(f"Error details: {error_details}")
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'})

@app.route('/export', methods=['POST'])
def export_pattern():
    data = request.get_json()
    svg_content = data.get('svg', '')
    format_type = data.get('format', 'svg')
    filename = data.get('filename', 'kolam')
    metadata = data.get('metadata', {})
    grid_size = data.get('grid_size', 7)
    pattern = data.get('pattern', 'basic')

    try:
        clean_svg = generate_kolam_clean(grid_size, pattern)
        
        if format_type == 'svg':
            fname = save_svg(clean_svg, f"{filename}.svg")
        elif format_type == 'png':
            fname = convert_svg_to_png(clean_svg, f"{filename}.png")
        elif format_type == 'jpg':
            fname = convert_svg_to_jpg(clean_svg, f"{filename}.jpg")
        elif format_type == 'all':
            results = export_pattern_with_metadata(clean_svg, metadata, filename)
            return jsonify({'success': True, 'files': results})
        else:
            return jsonify({'success': False, 'error': 'Unsupported format'})
        
        return jsonify({'success': True, 'filepath': fname})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/shared/<encoded>')
def shared(encoded):
    try:
        raw = base64.b64decode(encoded.encode()).decode()
        data = json.loads(raw)
        svg = data.get('svg') or data.get('pattern')
        analysis = data.get('analysis') or data.get('metadata', {}).get('analysis')
        pattern_categories = get_pattern_categories()
        return render_template('index.html',
                               svg=svg,
                               grid_size=7,
                               pattern='basic',
                               pattern_categories=pattern_categories,
                               analysis=analysis,
                               get_pattern_description=get_pattern_description,
                               get_symmetry_explanation=get_symmetry_explanation)
    except Exception as e:
        return f"Invalid shared link: {e}", 400

@app.route('/qr_code', methods=['POST'])
def generate_qr():
    data = request.get_json()
    pattern_data = data.get('pattern_data', '')
    
    try:
        qr_path = generate_qr_code(pattern_data, 'kolam_qr.png')
        return jsonify({'success': True, 'qr_path': qr_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/batch_export', methods=['POST'])
def batch_export():
    data = request.get_json()
    patterns = data.get('patterns', [])
    include_qr = data.get('include_qr', True)
    include_shareable_link = data.get('include_shareable_link', True)
    
    try:
        results = batch_export_patterns(patterns, include_qr, include_shareable_link)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/shared/<encoded_data>')
def shared_pattern(encoded_data):
    try:
        import base64
        import json
        
        pattern_json = base64.b64decode(encoded_data).decode()
        pattern_data = json.loads(pattern_json)
        
        svg_content = pattern_data.get('svg', '')
        metadata = pattern_data.get('metadata', {})
        
        return render_template('shared_pattern.html', 
                             svg=svg_content, 
                             metadata=metadata)
    except Exception as e:
        return f"Error loading shared pattern: {str(e)}", 400

@app.route('/share', methods=['POST'])
def create_share():
    data = request.get_json()
    pattern_data = data.get('pattern_data', {})
    
    try:
        shareable_link = create_shareable_link(pattern_data)
        return jsonify({'success': True, 'shareable_link': shareable_link})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/pattern_info/<pattern>')
def get_pattern_info(pattern):
    description = get_pattern_description(pattern)
    return jsonify({
        'pattern': pattern,
        'description': description
    })

@app.route('/symmetry_info/<symmetry_type>')
def get_symmetry_info(symmetry_type):
    explanation = get_symmetry_explanation(symmetry_type)
    return jsonify({
        'type': symmetry_type,
        'explanation': explanation
    })

@app.route('/download/<path:filename>')
def download_file(filename):
    filepath = os.path.join('exports', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

# Vercel serverless handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
