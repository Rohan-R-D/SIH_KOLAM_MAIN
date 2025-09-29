# 🎨 Kolam Generator - Advanced Mathematical Art Tool

A comprehensive web application that generates, analyzes, and visualizes Kolam/Rangoli patterns using advanced mathematical principles. This educational tool combines traditional Indian art with modern computational methods to create beautiful, mathematically precise patterns.

## ✨ Features

### 🎯 Pattern Generation
- **10+ Pattern Types**: Basic, Diamond, Spiral, Flower, Lotus, Rose, Star, Sunburst, Mandala, Compass
- **Flexible Grid Sizes**: 3x3 to 15x15 grids with automatic odd-number enforcement
- **SVG-based Rendering**: High-quality vector graphics with customizable colors
- **Modular Architecture**: Separate pattern files for easy extension

### 🔬 Mathematical Analysis
- **Symmetry Detection**: Horizontal, vertical, diagonal, and radial symmetry analysis
- **Repetition Detection**: Identifies repeating motifs and subgrids
- **Pattern Classification**: Tags patterns with attributes like "looped traversal", "grid repetition", "rotational symmetry"
- **Complexity Scoring**: Mathematical complexity analysis of generated patterns

### 📸 Image-Based Reconstruction
- **Image Upload**: Support for JPG/PNG hand-drawn Kolam images
- **OpenCV Integration**: Advanced dot detection using computer vision
- **Graph Construction**: Automatic pattern inference from detected dots
- **Pattern Recognition**: ML-based pattern classification from images

### 🎬 Animation & Visualization
- **Step-by-step Animation**: Frame-by-frame Kolam drawing animation
- **Speed Control**: Adjustable animation speed (0.5x to 5x)
- **Symmetry Highlighting**: Visual indication of symmetry axes during animation
- **Interactive Controls**: Play, pause, reset, and replay functionality

### 📤 Export & Sharing
- **Multiple Formats**: SVG, PNG, JPG export options
- **Batch Export**: Export multiple patterns simultaneously
- **QR Code Generation**: Create shareable QR codes for patterns
- **Shareable Links**: Generate URLs for pattern sharing
- **Metadata Export**: Comprehensive pattern information and analysis

### 🎨 UI/UX Features
- **Modern Interface**: Clean, responsive design with traditional Indian motifs
- **Theme Toggle**: Dark/Light mode support
- **Interactive Controls**: Dropdowns, sliders, and real-time preview
- **Tooltip Explanations**: Educational tooltips for mathematical concepts
- **Mobile Responsive**: Optimized for desktop, tablet, and mobile devices

## 🛠️ Technical Requirements

- **Python 3.8+**
- **Flask 2.3.2+**
- **OpenCV 4.8+** (for image processing)
- **NumPy 1.24+** (for mathematical operations)
- **Pillow 10.0+** (for image handling)
- **CairoSVG 2.7+** (for SVG to PNG conversion)

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd kolam-main
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Local Development
```bash
python app.py
```
The application will be available at http://localhost:5000/

### Docker Development
```bash
# Build development image
docker build -t kolam-dev -f Dockerfile.dev .

# Run development container
docker run -p 5000:5000 kolam-dev
```

### Docker Production
```bash
# Build production image
docker build -t kolam-prod .

# Run production container
docker run -p 5000:5000 kolam-prod
```

### Production Deployment
```bash
gunicorn app:app
```

## 📚 Usage Guide

### 1. Generate Patterns
- Select grid size (3x3 to 15x15)
- Choose pattern type from organized categories
- Enable mathematical analysis for detailed insights
- Click "Generate Kolam" to create your pattern

### 2. Analyze Patterns
- View comprehensive symmetry analysis
- Explore pattern classification and attributes
- Understand repetition patterns and motifs
- Learn about mathematical properties

### 3. Upload Images
- Upload hand-drawn Kolam images (JPG/PNG)
- Automatic dot detection and pattern reconstruction
- View analysis of detected patterns
- Export reconstructed patterns

### 4. Animate Patterns
- Generate step-by-step drawing animations
- Control animation speed and playback
- Highlight symmetry axes during animation
- Export animated sequences

### 5. Export & Share
- Download patterns in multiple formats
- Batch export multiple patterns
- Generate QR codes for sharing
- Create shareable links

## 🏗️ Project Structure

```
kolam-main/
├── app.py                          # Main Flask application
├── kolam/                          # Core Kolam modules
│   ├── __init__.py
│   ├── generator.py                # Pattern generation logic
│   ├── analyzer.py                 # Mathematical analysis
│   ├── exporter.py                 # Export functionality
│   ├── animation.py                # Animation system
│   ├── image_processor.py          # Image processing
│   ├── utils.py                    # Utility functions
│   └── patterns/                   # Pattern implementations
│       ├── basic.py               # Basic patterns
│       ├── flower.py              # Flower patterns
│       └── star.py                # Star patterns
├── templates/
│   └── index.html                 # Main UI template
├── static/
│   ├── style.css                  # Enhanced CSS styles
│   └── script.js                  # Interactive JavaScript
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Production Docker
├── Dockerfile.dev                 # Development Docker
└── README.md                      # This file
```

## 🔬 Mathematical Concepts

### Symmetry Analysis
- **Horizontal Symmetry**: Reflection across horizontal axis
- **Vertical Symmetry**: Reflection across vertical axis
- **Diagonal Symmetry**: Reflection across diagonal axes
- **Radial Symmetry**: Rotational symmetry around center

### Pattern Classification
- **Looped Traversal**: Patterns that form closed loops
- **Grid Repetition**: Repeating subgrid patterns
- **Rotational Symmetry**: Patterns with rotational properties
- **Bilateral Symmetry**: Patterns with bilateral symmetry

### Complexity Metrics
- **Node Count**: Number of pattern points
- **Edge Count**: Number of connections
- **Symmetry Score**: Quantitative symmetry measurement
- **Repetition Factor**: Degree of pattern repetition

## 🎓 Educational Value

This application serves as an educational tool demonstrating:
- **Mathematical Art**: Intersection of mathematics and visual art
- **Cultural Heritage**: Traditional Indian Kolam patterns
- **Computer Vision**: Image processing and pattern recognition
- **Algorithm Design**: Pattern generation algorithms
- **Data Visualization**: Mathematical analysis visualization

## 🚀 Advanced Features

### API Endpoints
- `GET /` - Main application interface
- `POST /generate` - Generate Kolam patterns
- `POST /analyze` - Analyze pattern properties
- `POST /animate` - Generate animation frames
- `POST /upload` - Process uploaded images
- `POST /export` - Export patterns
- `POST /share` - Create shareable links

### Extensibility
- **Modular Pattern System**: Easy to add new pattern types
- **Plugin Architecture**: Extensible analysis modules
- **Custom Exporters**: Add new export formats
- **Theme System**: Customizable UI themes

## 🐛 Troubleshooting

### Common Issues
1. **OpenCV Installation**: Ensure OpenCV is properly installed
2. **Memory Usage**: Large patterns may require more memory
3. **Image Processing**: Some images may not process correctly
4. **Animation Performance**: Complex animations may be slow

### Docker Issues
```bash
# View container logs
docker logs <container_id>

# Access container shell
docker exec -it <container_id> /bin/sh

# Restart container
docker restart <container_id>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Traditional Indian Kolam artists and cultural heritage
- Mathematical symmetry theory
- OpenCV and computer vision community
- Flask and Python web development community

---

**🎨 Kolam Generator - Where Mathematics Meets Art** 🎨