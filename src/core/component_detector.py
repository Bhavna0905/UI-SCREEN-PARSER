import uuid
from typing import List, Dict, Tuple
import sys
import os

# Ensure proper path resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import custom modules
from models.ui_component import UIComponent, ComponentType, BoundingBox
from utils.image_processor import ImageProcessor

class ComponentDetector:
    def _init_(self):
        self.image_processor = ImageProcessor()
    
    # ... rest of your methods



import uuid
from typing import List, Dict, Tuple
import sys
import os

# Fix the path imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.ui_component import UIComponent, ComponentType, BoundingBox
from utils.image_processor import ImageProcessor


class ComponentDetector:
    def _init_(self):
        self.image_processor = ImageProcessor()
    
    def detect_components(self, image_path: str) -> List[UIComponent]:
        """Main method to detect all UI components"""
        image = self.image_processor.preprocess_image(image_path)
        
        # Extract different types of elements
        text_regions = self.image_processor.extract_text_regions(image)
        ui_elements = self.image_processor.detect_ui_elements(image)
        
        components = []
        
        # Process text regions
        for text_region in text_regions:
            component = self._create_text_component(image, text_region)
            components.append(component)
        
        # Process UI elements
        for element in ui_elements:
            component = self._create_ui_component(image, element)
            components.append(component)
        
        # Remove duplicates and overlapping components
        components = self._remove_duplicates(components)
        
        return components
    
    def _create_text_component(self, image, text_region: Dict) -> UIComponent:
        """Create a text component from OCR results"""
        bbox_tuple = text_region['bbox']
        bbox = BoundingBox(bbox_tuple[0], bbox_tuple[1], bbox_tuple[2], bbox_tuple[3])
        
        color_info = self.image_processor.extract_color_info(image, bbox_tuple)
        
        # Classify if it's a label or input based on context
        component_type = self._classify_text_type(text_region['text'], bbox)
        
        return UIComponent(
            id=str(uuid.uuid4()),
            component_type=component_type,
            bounding_box=bbox,
            text_content=text_region['text'],
            color_info=color_info,
            confidence=text_region['confidence']
        )
    
    def _create_ui_component(self, image, element: Dict) -> UIComponent:
        """Create a UI component from detected elements"""
        bbox_tuple = element['bbox']
        bbox = BoundingBox(bbox_tuple[0], bbox_tuple[1], bbox_tuple[2], bbox_tuple[3])
        
        color_info = self.image_processor.extract_color_info(image, bbox_tuple)
        
        # Classify component type
        component_type = self._classify_component_type(element, bbox)
        
        return UIComponent(
            id=str(uuid.uuid4()),
            component_type=component_type,
            bounding_box=bbox,
            color_info=color_info,
            confidence=element['confidence'],
            attributes={'shape': element['type']}
        )
    
    def _classify_text_type(self, text: str, bbox: BoundingBox) -> ComponentType:
        """Classify whether text is a label, button, or input"""
        if bbox.width > bbox.height * 3:  # Wide text likely input
            return ComponentType.TEXT_INPUT
        elif any(word in text.lower() for word in ['click', 'submit', 'cancel', 'ok']):
            return ComponentType.BUTTON
        else:
            return ComponentType.TEXT_LABEL
    
    def _classify_component_type(self, element: Dict, bbox: BoundingBox) -> ComponentType:
        """Classify UI component type based on shape and size"""
        if element['type'] == 'circle':
            return ComponentType.ICON if bbox.width < 50 else ComponentType.BUTTON
        elif element['type'] == 'rectangle':
            aspect_ratio = bbox.width / bbox.height
            if aspect_ratio > 3:  # Very wide rectangle
                return ComponentType.TEXT_INPUT
            elif 0.5 < aspect_ratio < 2:  # Square-ish
                return ComponentType.BUTTON
            else:
                return ComponentType.CONTAINER
        
        return ComponentType.UNKNOWN
    
    def _remove_duplicates(self, components: List[UIComponent]) -> List[UIComponent]:
        """Remove duplicate or heavily overlapping components"""
        filtered_components = []
        
        for i, comp1 in enumerate(components):
            is_duplicate = False
            
            for j, comp2 in enumerate(components):
                if i != j and self._calculate_overlap(comp1.bounding_box, comp2.bounding_box) > 0.8:
                    if comp1.confidence < comp2.confidence:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                filtered_components.append(comp1)
        
        return filtered_components
    
    def _calculate_overlap(self, bbox1: BoundingBox, bbox2: BoundingBox) -> float:
        """Calculate overlap ratio between two bounding boxes"""
        x1_min, y1_min = bbox1.x, bbox1.y
        x1_max, y1_max = bbox1.x + bbox1.width, bbox1.y + bbox1.height
        
        x2_min, y2_min = bbox2.x, bbox2.y
        x2_max, y2_max = bbox2.x + bbox2.width, bbox2.y + bbox2.height
        
        # Calculate intersection
        x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
        y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))
        
        intersection = x_overlap * y_overlap
        union = bbox1.area + bbox2.area - intersection
        
        return intersection / union if union > 0 else 0