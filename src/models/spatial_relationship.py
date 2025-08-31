from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

class RelationType(Enum):
    ABOVE = "above"
    BELOW = "below"
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    INSIDE = "inside"
    CONTAINS = "contains"
    OVERLAPS = "overlaps"
    ADJACENT = "adjacent"
    ALIGNED_HORIZONTAL = "aligned_horizontal"
    ALIGNED_VERTICAL = "aligned_vertical"

@dataclass
class SpatialRelationship:
    component1_id: str
    component2_id: str
    relation_type: RelationType
    distance: float
    confidence: float
    description: str

@dataclass
class UILayout:
    components: Dict[str, 'UIComponent']
    relationships: List[SpatialRelationship]
    screen_dimensions: Tuple[int, int]
    ambiguities: List[str]
    confidence_score: float