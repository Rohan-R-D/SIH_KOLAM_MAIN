#!/usr/bin/env python3
"""
Test script to verify clean export functionality.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_clean_export():
    """Test that clean export generates patterns without grid dots."""
    try:
        from kolam.generator import generate_kolam, generate_kolam_clean
        
        # Test regular generation (with grid)
        svg_with_grid = generate_kolam(grid_size=5, pattern='basic')
        print("✅ Regular generation (with grid) works")
        
        # Test clean generation (without grid)
        svg_clean = generate_kolam_clean(grid_size=5, pattern='basic')
        print("✅ Clean generation (without grid) works")
        
        # Verify grid dots are present in regular version
        assert 'fill="#333"' in svg_with_grid, "Grid dots should be present in regular version"
        print("✅ Grid dots present in regular version")
        
        # Verify grid dots are absent in clean version
        assert 'fill="#333"' not in svg_clean, "Grid dots should be absent in clean version"
        print("✅ Grid dots absent in clean version")
        
        # Verify both have the same pattern content (just different grid)
        pattern_start = svg_with_grid.find('<path')
        pattern_end = svg_with_grid.find('</svg>')
        pattern_with_grid = svg_with_grid[pattern_start:pattern_end]
        
        clean_pattern_start = svg_clean.find('<path')
        clean_pattern_end = svg_clean.find('</svg>')
        pattern_clean = svg_clean[clean_pattern_start:clean_pattern_end]
        
        # Both should have the same pattern content
        assert pattern_with_grid == pattern_clean, "Pattern content should be identical"
        print("✅ Pattern content identical between versions")
        
        return True
        
    except Exception as e:
        print(f"❌ Clean export test failed: {e}")
        return False

def test_animated_generation():
    """Test animated generation works."""
    try:
        from kolam.animated_generator import generate_animated_kolam
        
        # Test animated generation
        animated_svg = generate_animated_kolam(grid_size=5, pattern='basic')
        assert '<svg' in animated_svg
        assert '</svg>' in animated_svg
        print("✅ Animated generation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Animated generation test failed: {e}")
        return False

def main():
    """Run export tests."""
    print("🧪 Testing Export Functionality...")
    print("=" * 50)
    
    tests = [
        ("Clean Export", test_clean_export),
        ("Animated Generation", test_animated_generation)
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
        print("🎉 All export tests passed! Export functionality is working correctly.")
        return True
    else:
        print("⚠️  Some export tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

