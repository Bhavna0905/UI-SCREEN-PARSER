import sys
import os
import cv2

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from core.screen_analyzer import ScreenAnalyzer
from utils.image_processor import ImageProcessor

def debug_image_processing():
    """Debug what the image processor actually detects"""
    image_path = "examples/sample_screens/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    try:
        print("🔍 Starting detailed image analysis...\n")
        
        # Test image processor directly
        processor = ImageProcessor()
        
        # Load image
        print("📷 Loading image...")
        image = processor.preprocess_image(image_path)
        print(f"✓ Image loaded: {image.shape} (height, width, channels)")
        
        # Test OCR
        print("\n📝 Running OCR text detection...")
        text_regions = processor.extract_text_regions(image)
        print(f"✓ Found {len(text_regions)} text regions")
        
        if text_regions:
            print("\n📋 Text regions detected:")
            for i, region in enumerate(text_regions[:10]):  # Show first 10
                print(f"  {i+1}. Text: '{region['text']}' | Confidence: {region['confidence']:.2f} | Position: {region['bbox']}")
        else:
            print("❌ No text detected by OCR")
        
        # Test UI element detection
        print("\n🎯 Running UI element detection...")
        ui_elements = processor.detect_ui_elements(image)
        print(f"✓ Found {len(ui_elements)} UI elements")
        
        if ui_elements:
            print("\n🔲 UI elements detected:")
            for i, element in enumerate(ui_elements[:5]):  # Show first 5
                print(f"  {i+1}. Type: {element['type']} | Position: {element['bbox']} | Confidence: {element['confidence']:.2f}")
        
        # Now test full analyzer - THIS IS THE CORRECTED LINE
        print("\n🚀 Testing full screen analyzer...")
        analyzer = ScreenAnalyzer()
        layout = analyzer.analyze_screen(image_path)  # Fixed: Added parentheses
        
        print(f"\n📊 Full Analysis Results:")
        print(f"  - Total components: {len(layout.components)}")
        print(f"  - Relationships: {len(layout.relationships)}")
        print(f"  - Confidence score: {layout.confidence_score}")
        print(f"  - Screen dimensions: {layout.screen_dimensions}")
        
        if layout.components:
            print(f"\n🧩 Components found:")
            for i, (comp_id, comp) in enumerate(list(layout.components.items())[:5]):
                print(f"  {i+1}. ID: {comp_id[:8]}... | Type: {comp.component_type.value} | Text: '{comp.text_content}' | Position: ({comp.bounding_box.x}, {comp.bounding_box.y})")
        
        if layout.ambiguities:
            print(f"\n⚠️ Ambiguities: {layout.ambiguities}")
        
        # Test specific queries
        print(f"\n❓ Testing queries:")
        test_queries = [
            "how many components are there?",
            "where is the blue text?",
            "where is the text 'Register'?"
        ]
        
        for query in test_queries:
            response = analyzer.query_layout(layout, query)
            print(f"  Q: {query}")
            print(f"  A: {response}\n")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_image_processing()
