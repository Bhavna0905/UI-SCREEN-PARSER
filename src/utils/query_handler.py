import re
from typing import List, Dict, Optional
import sys
import os

# Ensure proper path resolution
current_dir = os.path.dirname(os.path.abspath(_file_))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from models.spatial_relationship import UILayout, RelationType
from models.ui_component import UIComponent, ComponentType

class QueryHandler:
    def _init_(self):
        self.color_patterns = {
            'red': ['#ff', '#f00', 'rgb(255', 'red', '#ff0000'],
            'blue': ['#00f', '#0000ff', 'rgb(0', 'blue', '#0066cc', '#4169e1'],
            'green': ['#0f0', '#00ff00', 'rgb(0', 'green'],
            'black': ['#000', '#000000', 'rgb(0,0,0)', 'black'],
            'white': ['#fff', '#ffffff', 'rgb(255,255,255)', 'white'],
            'orange': ['#ffa500', '#ff8c00', 'orange', '#ff6600'],
            'yellow': ['#ffff00', '#ffd700', 'yellow', '#fff200']
        }
    
    def process_query(self, layout: UILayout, query: str) -> str:
        """Process natural language queries about the UI layout"""
        query = query.lower().strip()
        
        try:
            print(f"DEBUG: Processing query '{query}' with {len(layout.components)} components")
            
            if 'how many' in query:
                return self._handle_count_query(layout, query)
            elif 'where' in query or 'position' in query or 'find' in query or 'locate' in query:
                return self._handle_location_query(layout, query)
            elif 'above' in query or 'below' in query or 'left' in query or 'right' in query:
                return self._handle_relationship_query(layout, query)
            else:
                return self._handle_general_query(layout, query)
                
        except Exception as e:
            return f"confused - Could not parse query: {str(e)}"
    
    def _handle_count_query(self, layout: UILayout, query: str) -> str:
        """Handle queries asking about counts"""
        if not layout.components:
            return "No components found in the layout"
            
        component_counts = {}
        for component in layout.components.values():
            comp_type = component.component_type.value
            component_counts[comp_type] = component_counts.get(comp_type, 0) + 1
        
        total = sum(component_counts.values())
        breakdown = ", ".join([f"{count} {comp_type}{'s' if count > 1 else ''}" 
                             for comp_type, count in component_counts.items()])
        
        return f"Total components: {total}. Breakdown: {breakdown}"
    
    def _handle_location_query(self, layout: UILayout, query: str) -> str:
        """Handle queries asking about component locations"""
        if not layout.components:
            return "No components found in the layout"
        
        # Search for specific text content
        if 'text' in query:
            text_to_find = None
            quote_match = re.search(r"'([^'])'|\"([^\"])\"", query)
            if quote_match:
                text_to_find = quote_match.group(1) or quote_match.group(2)
            
            if text_to_find:
                matching_components = []
                for comp in layout.components.values():
                    if comp.text_content and text_to_find.lower() in comp.text_content.lower():
                        matching_components.append(comp)
                
                if matching_components:
                    comp = matching_components[0]
                    return f"Found text '{text_to_find}' at position ({comp.bounding_box.x}, {comp.bounding_box.y}) in a {comp.component_type.value}"
                else:
                    available_texts = [comp.text_content for comp in layout.components.values() if comp.text_content]
                    return f"Text '{text_to_find}' not found. Available texts: {available_texts[:5]}"
        
        # Search for colors
        for color_name, patterns in self.color_patterns.items():
            if color_name in query:
                matching_components = []
                
                for comp in layout.components.values():
                    if comp.color_info:
                        color_hex = comp.color_info.get('dominant_hex', '').lower()
                        if any(pattern.lower() in color_hex for pattern in patterns):
                            matching_components.append(comp)
                
                if matching_components:
                    descriptions = []
                    for comp in matching_components[:3]:
                        desc = f"{comp.component_type.value}"
                        if comp.text_content:
                            desc += f" with text '{comp.text_content}'"
                        desc += f" at ({comp.bounding_box.x}, {comp.bounding_box.y})"
                        descriptions.append(desc)
                    return f"Found {color_name} elements: " + "; ".join(descriptions)
        
        # Search for component types
        if 'button' in query:
            buttons = [comp for comp in layout.components.values() 
                      if comp.component_type == ComponentType.BUTTON]
            if buttons:
                button = buttons[0]
                desc = f"Found button at position ({button.bounding_box.x}, {button.bounding_box.y})"
                if button.text_content:
                    desc += f" with text '{button.text_content}'"
                return desc
        
        return "confused - Could not find the specified component"
    
    def _handle_relationship_query(self, layout: UILayout, query: str) -> str:
        """Handle queries asking about relationships"""
        relationships_text = []
        for rel in layout.relationships[:5]:
            relationships_text.append(rel.description)
        
        if relationships_text:
            return "Found relationships: " + "; ".join(relationships_text)
        else:
            return "No clear relationships found between components"
    
    def _handle_general_query(self, layout: UILayout, query: str) -> str:
        """Handle general queries"""
        if 'confused' in query or 'ambiguities' in query:
            if layout.ambiguities:
                return f"Identified ambiguities: {'; '.join(layout.ambiguities)}"
            else:
                return "No significant ambiguities detected"
        
        return "confused - Could not understand the query"