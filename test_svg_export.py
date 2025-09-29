#!/usr/bin/env python3
"""
Test script to verify SVG export functionality without Cairo dependency.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kolam.exporter import convert_svg_to_png, convert_svg_to_jpg, save_svg

def test_svg_export():
    """Test SVG export functions."""
    print("Testing SVG export functionality...")
    
    # Create a simple test SVG
    test_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="50" fill="red" stroke="black" stroke-width="2"/>
  <text x="100" y="110" text-anchor="middle" font-family="Arial" font-size="16" fill="white">Test</text>
</svg>'''
    
    try:
        # Test SVG save
        print("1. Testing SVG save...")
        svg_file = save_svg(test_svg, "test_kolam.svg")
        print(f"   ✓ SVG saved as: {svg_file}")
        
        # Test PNG conversion
        print("2. Testing SVG to PNG conversion...")
        png_file = convert_svg_to_png(test_svg, "test_kolam.png")
        print(f"   ✓ PNG created: {png_file}")
        
        # Test JPG conversion
        print("3. Testing SVG to JPG conversion...")
        jpg_file = convert_svg_to_jpg(test_svg, "test_kolam.jpg")
        print(f"   ✓ JPG created: {jpg_file}")
        
        print("\n✅ All SVG export tests passed!")
        print("The Cairo dependency issue has been resolved.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_svg_export()
    sys.exit(0 if success else 1)
