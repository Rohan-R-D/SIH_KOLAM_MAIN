#!/usr/bin/env python3
"""
Test script for image upload functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kolam.image_processor import process_uploaded_image
import base64
from PIL import Image
import io

def create_test_image():
    """Create a simple test image with dots"""
    # Create a simple white image with black dots
    img = Image.new('RGB', (400, 400), 'white')
    
    # Add some dots manually
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Draw some dots in a grid pattern
    for x in range(50, 400, 50):
        for y in range(50, 400, 50):
            draw.ellipse([x-5, y-5, x+5, y+5], fill='black')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_image_processing():
    """Test the image processing functionality"""
    print("🧪 Testing Image Upload Functionality...")
    print("=" * 50)
    
    try:
        # Create test image
        print("📸 Creating test image...")
        test_image_data = create_test_image()
        print(f"✅ Test image created (length: {len(test_image_data)})")
        
        # Process the image
        print("🔍 Processing image...")
        result = process_uploaded_image(test_image_data)
        
        if result['success']:
            print("✅ Image processing successful!")
            print(f"   - Dots detected: {len(result['dots'])}")
            print(f"   - Graph nodes: {len(result['graph']['nodes'])}")
            print(f"   - Graph edges: {len(result['graph']['edges'])}")
            
            if 'pattern_info' in result:
                pattern_info = result['pattern_info']
                print(f"   - Pattern type: {pattern_info.get('type', 'unknown')}")
                print(f"   - Complexity: {pattern_info.get('complexity', 0):.2f}")
                print(f"   - Suggested patterns: {pattern_info.get('suggested_patterns', [])}")
        else:
            print("❌ Image processing failed!")
            print(f"   - Error: {result.get('error', 'Unknown error')}")
            if 'details' in result:
                print(f"   - Details: {result['details']}")
        
        return result['success']
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        print(f"   - Details: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_image_processing()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Image upload test passed!")
    else:
        print("💥 Image upload test failed!")
    sys.exit(0 if success else 1)

