"""Data Models for UI Components and Relationships"""

from .ui_component import UIComponent, ComponentType, BoundingBox
from .spatial_relationship import SpatialRelationship, RelationType, UILayout

_all_ = [
    'UIComponent', 
    'ComponentType', 
    'BoundingBox',
    'SpatialRelationship', 
    'RelationType', 
    'UILayout'
]