import math
from typing import List, Dict, Tuple
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.ui_component import UIComponent
from models.spatial_relationship import SpatialRelationship, RelationType


class RelationshipMapper:
    def __init__(self):
        self.threshold_adjacent = 20
        self.threshold_alignment = 10
    
    def map_relationships(self, components: List[UIComponent]) -> List[SpatialRelationship]:
        """Map spatial relationships between all components"""
        relationships = []
        
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i != j:
                    relationship = self._analyze_relationship(comp1, comp2)
                    if relationship:
                        relationships.append(relationship)
        
        return relationships
    
    def _analyze_relationship(self, comp1: UIComponent, comp2: UIComponent) -> SpatialRelationship:
        """Analyze relationship between two components"""
        bbox1, bbox2 = comp1.bounding_box, comp2.bounding_box
        
        # Calculate centers
        center1 = bbox1.center
        center2 = bbox2.center
        
        # Calculate distance
        distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
        # Determine primary relationship
        relation_type = self._determine_relation_type(bbox1, bbox2)
        
        if relation_type:
            description = self._generate_description(comp1, comp2, relation_type)
            
            return SpatialRelationship(
                component1_id=comp1.id,
                component2_id=comp2.id,
                relation_type=relation_type,
                distance=distance,
                confidence=0.8,
                description=description
            )
        
        return None
    
    def _determine_relation_type(self, bbox1, bbox2) -> RelationType:
        """Determine the primary spatial relationship"""
        # Check directional relationships
        center1 = bbox1.center
        center2 = bbox2.center
        
        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]
        
        # Determine primary direction
        if abs(dx) > abs(dy):
            return RelationType.RIGHT_OF if dx > 0 else RelationType.LEFT_OF
        else:
            return RelationType.BELOW if dy > 0 else RelationType.ABOVE
    
    def _generate_description(self, comp1: UIComponent, comp2: UIComponent, relation_type: RelationType) -> str:
        """Generate human-readable description of the relationship"""
        comp1_desc = self._get_component_description(comp1)
        comp2_desc = self._get_component_description(comp2)
        
        relation_phrases = {
            RelationType.ABOVE: f"{comp1_desc} is above {comp2_desc}",
            RelationType.BELOW: f"{comp1_desc} is below {comp2_desc}",
            RelationType.LEFT_OF: f"{comp1_desc} is to the left of {comp2_desc}",
            RelationType.RIGHT_OF: f"{comp1_desc} is to the right of {comp2_desc}",
        }
        
        return relation_phrases.get(relation_type, f"{comp1_desc} relates to {comp2_desc}")
    
    def _get_component_description(self, component: UIComponent) -> str:
        """Generate a description for a component"""
        desc = component.component_type.value
        
        if component.text_content:
            desc += f" with text '{component.text_content}'"
        
        return desc
