import sys
import json
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.screen_analyzer import ScreenAnalyzer, NumpyEncoder

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path> [query]")
        return
    
    image_path = sys.argv[1]
    query = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        return
    
    # Initialize analyzer
    analyzer = ScreenAnalyzer()
    
    print("Analyzing screen...")
    
    # Analyze the screen
    layout = analyzer.analyze_screen(image_path)
    
    # Check for confused state
    if layout.confidence_score == 0.0:
        print("confused - Unable to analyze the screen properly")
        if layout.ambiguities:
            print("Issues:", "; ".join(layout.ambiguities))
        return
    
    # Export structured output
    structured_output = analyzer.export_structured_output(layout)
    
    # Save to JSON file
    output_path = Path(image_path).stem + "_analysis.json"
    try:
        with open(output_path, 'w') as f:
            json.dump(structured_output, f, indent=2, cls=NumpyEncoder)
    except Exception as e:
        print(f"Error saving JSON: {e}")
        # Try alternative method
        with open(output_path, 'w') as f:
            json.dump(structured_output, f, indent=2)
    
    print(f"Analysis saved to: {output_path}")
    print(f"Overall confidence: {layout.confidence_score}")
    print(f"Components found: {len(layout.components)}")
    print(f"Relationships mapped: {len(layout.relationships)}")
    
    if layout.ambiguities:
        print(f"Ambiguities: {'; '.join(layout.ambiguities)}")
    
    # Handle query if provided
    if query:
        print(f"\nQuery: {query}")
        response = analyzer.query_layout(layout, query)
        print(f"Response: {response}")
    else:
        # Interactive mode
        print("\nEntering interactive query mode. Type 'exit' to quit.")
        while True:
            try:
                user_query = input("\nQuery: ")
                if user_query.lower() in ['exit', 'quit']:
                    break
                
                response = analyzer.query_layout(layout, user_query)
                print(f"Response: {response}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
