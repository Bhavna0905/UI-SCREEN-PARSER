from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class ComponentType(Enum):
    BUTTON = "button"
    TEXT_INPUT = "text_input"
    TEXT_LABEL = "text_label"
    IMAGE = "image"
    ICON = "icon"
    CHECKBOX = "checkbox"
    RADIO_BUTTON = "radio_button"
    DROPDOWN = "dropdown"
    MENU = "menu"
    CONTAINER = "container"
    UNKNOWN = "unknown"

@dataclass
class BoundingBox:
    x: int
    y: int
    width: int
    height: int
    
    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def area(self) -> int:
        return self.width * self.height

@dataclass
class UIComponent:
    id: str
    component_type: ComponentType
    bounding_box: BoundingBox
    text_content: Optional[str] = None
    color_info: Optional[Dict[str, str]] = None
    confidence: float = 0.0
    attributes: Dict[str, any] = None
    
    def _post_init_(self):
        if self.attributes is None:
            self.attributes = {}