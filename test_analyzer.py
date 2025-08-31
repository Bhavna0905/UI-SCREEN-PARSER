import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

def test_imports():
    """Test that all imports work"""
    try:
        from models.ui_component import UIComponent, ComponentType, BoundingBox
        print("✅ UI Component imports successful")
        
        from models.spatial_relationship import UILayout, RelationType
        print("✅ Spatial relationship imports successful")
        
        from utils.query_handler import QueryHandler  
        print("✅ Query handler import successful")
        
        from core.screen_analyzer import ScreenAnalyzer
        print("✅ Screen analyzer import successful")
        
        analyzer = ScreenAnalyzer()
        print("✅ Screen analyzer instantiation successful")
        
        print("\n🎉 All imports working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_image():
    """Test with actual image if available"""
    image_path = "examples/sample_screens/test_image.png"
    
    if not os.path.exists(image_path):
        print(f"📷 Please add a test image to {image_path}")
        print("   You can use any screenshot of a UI (webpage, app, etc.)")
        return False
    
    try:
        from core.screen_analyzer import ScreenAnalyzer
        
        analyzer = ScreenAnalyzer()
        print("🔍 Analyzing image...")
        
        layout = analyzer.analyze_screen(image_path)
        
        print(f"📊 Analysis Results:")
        print(f"   - Components found: {len(layout.components)}")
        print(f"   - Relationships: {len(layout.relationships)}")
        print(f"   - Confidence: {layout.confidence_score}")
        print(f"   - Screen dimensions: {layout.screen_dimensions}")
        
        if layout.ambiguities:
            print(f"   - Ambiguities: {layout.ambiguities}")
        
       
        test_queries = [
            "how many components are there?",
            "where is the search bar?",
            "find the text 'Amazon'"
        ]
        
        print("\n❓ Testing queries:")
        for query in test_queries:
            response = analyzer.query_layout(layout, query)
            print(f"   Q: {query}")
            print(f"   A: {response}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during image analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "_main_":
    print("🚀 Starting UI Screen Parser Tests...\n")
    
    if test_imports():
        print("\n" + "="*50)
        test_with_image()