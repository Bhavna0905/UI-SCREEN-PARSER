from typing import List, Dict, Optional, Any, Union
import sys
import os
import json
import numpy as np

# Ensure proper path resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import custom modules
from models.ui_component import UIComponent
from models.spatial_relationship import SpatialRelationship, UILayout
from core.component_detector import ComponentDetector
from core.relationship_mapper import RelationshipMapper
from utils.query_handler import QueryHandler





from typing import List, Dict, Optional, Any, Union
import sys
import os
import json
import numpy as np

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from models.ui_component import UIComponent
from models.spatial_relationship import SpatialRelationship, UILayout
from core.component_detector import ComponentDetector
from core.relationship_mapper import RelationshipMapper
from utils.query_handler import QueryHandler

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class ScreenAnalyzer:
    def _init_(self):
        self.component_detector = ComponentDetector()
        self.relationship_mapper = RelationshipMapper()
        self.query_handler = QueryHandler()
        
    def analyze_screen(self, image_path: str) -> UILayout:
        """Main method to analyze a screen and return structured output"""
        try:
            # Step 1: Detect UI components
            print("Detecting UI components...")
            components = self.component_detector.detect_components(image_path)
            
            # Step 2: Map relationships
            print("Mapping relationships...")
            relationships = self.relationship_mapper.map_relationships(components)
            
            # Step 3: Detect ambiguities
            ambiguities = self._detect_ambiguities(components, relationships)
            
            # Step 4: Calculate overall confidence
            confidence_score = self._calculate_confidence(components, relationships)
            
            # Step 5: Get screen dimensions
            import cv2
            image = cv2.imread(image_path)
            if image is not None:
                screen_dimensions = (image.shape[1], image.shape[0])  # width, height
            else:
                screen_dimensions = (0, 0)
            
            # Create component dictionary
            component_dict = {comp.id: comp for comp in components}
            
            return UILayout(
                components=component_dict,
                relationships=relationships,
                screen_dimensions=screen_dimensions,
                ambiguities=ambiguities,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            # Return confused state
            return UILayout(
                components={},
                relationships=[],
                screen_dimensions=(0, 0),
                ambiguities=[f"Error analyzing screen: {str(e)}"],
                confidence_score=0.0
            )
    
    def query_layout(self, layout: UILayout, query: str) -> str:
        """Handle natural language queries about the layout"""
        return self.query_handler.process_query(layout, query)
    
    def _detect_ambiguities(self, components: List[UIComponent], 
                          relationships: List[SpatialRelationship]) -> List[str]:
        """Detect potential ambiguities in the analysis"""
        ambiguities = []
        
        # Check for components with very low confidence
        low_confidence_components = [
            comp for comp in components if comp.confidence < 0.5
        ]
        if low_confidence_components:
            ambiguities.append(f"Low confidence detection for {len(low_confidence_components)} components")
        
        return ambiguities
    
    def _calculate_confidence(self, components: List[UIComponent], 
                            relationships: List[SpatialRelationship]) -> float:
        """Calculate overall confidence score for the analysis"""
        if not components:
            return 0.0
        
        # Average component confidence
        component_confidence = sum(comp.confidence for comp in components) / len(components)
        
        return round(component_confidence, 2)
    
    @staticmethod
    def _convert_numpy_types(obj: Any) -> Any:
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (list, tuple)):
            return [ScreenAnalyzer._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: ScreenAnalyzer._convert_numpy_types(value) for key, value in obj.items()}
        else:
            return obj
    
    def export_structured_output(self, layout: UILayout) -> Dict[str, Any]:
        """Export the layout analysis as structured JSON with proper type conversion"""
        
        output = {
            "screen_analysis": {
                "dimensions": {
                    "width": int(layout.screen_dimensions[0]),
                    "height": int(layout.screen_dimensions[1])
                },
                "confidence_score": float(layout.confidence_score),
                "components": [
                    {
                        "id": comp.id,
                        "type": comp.component_type.value,
                        "position": {
                            "x": int(comp.bounding_box.x),
                            "y": int(comp.bounding_box.y),
                            "width": int(comp.bounding_box.width),
                            "height": int(comp.bounding_box.height),
                            "center": [int(comp.bounding_box.center[0]), int(comp.bounding_box.center[1])]
                        },
                        "text_content": comp.text_content,
                        "color_info": comp.color_info,
                        "confidence": float(comp.confidence),
                        "attributes": self._convert_numpy_types(comp.attributes) if comp.attributes else {}
                    }
                    for comp in layout.components.values()
                ],
                "relationships": [
                    {
                        "from_component": rel.component1_id,
                        "to_component": rel.component2_id,
                        "relationship": rel.relation_type.value,
                        "distance": float(rel.distance),
                        "confidence": float(rel.confidence),
                        "description": rel.description
                    }
                    for rel in layout.relationships
                ],
                "ambiguities": layout.ambiguities
            }
        }
        
        return self._convert_numpy_types(output)