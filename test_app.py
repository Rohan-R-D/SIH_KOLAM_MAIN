#!/usr/bin/env python3
"""
Simple test script to verify the Kolam application works correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        from kolam.generator import generate_kolam, generate_kolam_with_analysis
        from kolam.analyzer import analyze_symmetry, detect_repetition, classify_pattern
        from kolam.exporter import save_svg, convert_svg_to_png
        from kolam.animation import generate_animation_frames
        from kolam.image_processor import process_uploaded_image
        from kolam.utils import get_pattern_categories, get_pattern_description
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_pattern_generation():
    """Test basic pattern generation."""
    try:
        from kolam.generator import generate_kolam
        
        # Test basic pattern
        svg = generate_kolam(grid_size=5, pattern='basic')
        assert '<svg' in svg
        assert '</svg>' in svg
        print("✅ Basic pattern generation works")
        
        # Test flower pattern
        svg = generate_kolam(grid_size=7, pattern='flower')
        assert '<svg' in svg
        print("✅ Flower pattern generation works")
        
        # Test star pattern
        svg = generate_kolam(grid_size=9, pattern='star')
        assert '<svg' in svg
        print("✅ Star pattern generation works")
        
        return True
    except Exception as e:
        print(f"❌ Pattern generation error: {e}")
        return False

def test_analysis():
    """Test pattern analysis functionality."""
    try:
        from kolam.analyzer import classify_pattern
        from kolam.utils import generate_grid_coordinates
        
        # Generate test coordinates
        coords = generate_grid_coordinates(5)
        
        # Test analysis
        analysis = classify_pattern(coords, 5)
        assert 'pattern_type' in analysis
        assert 'symmetry' in analysis
        assert 'repetition' in analysis
        print("✅ Pattern analysis works")
        
        return True
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_utils():
    """Test utility functions."""
    try:
        from kolam.utils import get_pattern_categories, get_pattern_description
        
        # Test pattern categories
        categories = get_pattern_categories()
        assert isinstance(categories, dict)
        assert len(categories) > 0
        print("✅ Pattern categories work")
        
        # Test pattern description
        description = get_pattern_description('basic')
        assert isinstance(description, str)
        assert len(description) > 0
        print("✅ Pattern descriptions work")
        
        return True
    except Exception as e:
        print(f"❌ Utils error: {e}")
        return False

def test_flask_app():
    """Test Flask app creation."""
    try:
        from app import app
        
        # Test app creation
        assert app is not None
        print("✅ Flask app creation works")
        
        # Test routes exist
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Main route works")
        
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Kolam Application...")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Pattern Generation", test_pattern_generation),
        ("Analysis", test_analysis),
        ("Utils", test_utils),
        ("Flask App", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


