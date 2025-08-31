import cv2
import numpy as np
from PIL import Image
import easyocr
from typing import List, Tuple, Dict

class ImageProcessor:
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['en'])
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess the image with better error handling"""
        print(f"DEBUG: Attempting to load image from: {image_path}")
        
        # Check if file exists
        import os
        if not os.path.exists(image_path):
            raise ValueError(f"Image file does not exist: {image_path}")
        
        # Try loading with OpenCV
        image = cv2.imread(image_path)
        if image is None:
            print(f"DEBUG: OpenCV failed to load {image_path}")
            
            # Try loading with PIL as backup
            try:
                from PIL import Image as PILImage
                pil_image = PILImage.open(image_path)
                # Convert PIL to OpenCV format
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                print("DEBUG: Successfully loaded with PIL")
            except Exception as e:
                raise ValueError(f"Could not load image from {image_path}. Error: {e}")
        else:
            print(f"DEBUG: Successfully loaded with OpenCV. Shape: {image.shape}")
        
        return image
    
    def extract_text_regions(self, image: np.ndarray) -> List[Dict]:
        """Extract text regions using OCR with error handling"""
        if image is None or image.size == 0:
            print("DEBUG: Empty image passed to extract_text_regions")
            return []
        
        try:
            results = self.ocr_reader.readtext(image)
            text_regions = []
            
            for (bbox, text, confidence) in results:
                # Convert bbox to our format
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                x = int(min(x_coords))
                y = int(min(y_coords))
                width = int(max(x_coords) - min(x_coords))
                height = int(max(y_coords) - min(y_coords))
                
                text_regions.append({
                    'bbox': (x, y, width, height),
                    'text': text,
                    'confidence': confidence
                })
            
            return text_regions
        except Exception as e:
            print(f"DEBUG: OCR failed: {e}")
            return []
    
    def detect_ui_elements(self, image: np.ndarray) -> List[Dict]:
        """Detect UI elements using computer vision techniques"""
        if image is None or image.size == 0:
            print("DEBUG: Empty image passed to detect_ui_elements")
            return []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect rectangles (potential buttons, input fields)
            rectangles = self._detect_rectangles(gray)
            
            # Detect circular elements (potential buttons, icons)
            circles = self._detect_circles(gray)
            
            # Combine all detected elements
            elements = rectangles + circles
            
            return elements
        except Exception as e:
            print(f"DEBUG: UI element detection failed: {e}")
            return []
    
    def _detect_rectangles(self, gray_image: np.ndarray) -> List[Dict]:
        """Detect rectangular UI elements with overflow protection"""
        try:
            # Edge detection
            edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            rectangles = []
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # If polygon has 4 points, it might be a rectangle
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Filter by size (avoid too small or too large elements)
                    if 20 < w < 500 and 20 < h < 200:
                        rectangles.append({
                            'bbox': (x, y, w, h),
                            'type': 'rectangle',
                            'confidence': 0.7
                        })
            
            return rectangles
        except Exception as e:
            print(f"DEBUG: Rectangle detection failed: {e}")
            return []
    
    def _detect_circles(self, gray_image: np.ndarray) -> List[Dict]:
        """Detect circular UI elements with overflow protection"""
        try:
            circles = cv2.HoughCircles(
                gray_image, cv2.HOUGH_GRADIENT, 1, 20,
                param1=50, param2=30, minRadius=10, maxRadius=100
            )
            
            circle_elements = []
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")  # Fix overflow issue
                for (x, y, r) in circles:
                    # Check bounds to prevent overflow
                    if r > 0 and x-r >= 0 and y-r >= 0:
                        circle_elements.append({
                            'bbox': (x-r, y-r, 2*r, 2*r),
                            'type': 'circle',
                            'confidence': 0.6
                        })
            
            return circle_elements
        except Exception as e:
            print(f"DEBUG: Circle detection failed: {e}")
            return []
    
    def extract_color_info(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> Dict[str, str]:
        """Extract dominant colors from a region with bounds checking"""
        try:
            x, y, w, h = bbox
            
            # Check bounds
            if (x < 0 or y < 0 or x + w > image.shape[1] or y + h > image.shape[0] or 
                w <= 0 or h <= 0):
                print(f"DEBUG: Invalid bbox {bbox} for image shape {image.shape}")
                return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}
            
            roi = image[y:y+h, x:x+w]
            
            if roi.size == 0:
                return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}
            
            # Convert to RGB
            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = roi_rgb.reshape(-1, 3)
            
            # Simple dominant color extraction
            dominant_color = np.mean(pixels, axis=0).astype(int)
            
            return {
                'dominant_rgb': f"rgb({dominant_color[0]}, {dominant_color[1]}, {dominant_color[2]})",
                'dominant_hex': f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"
            }
        except Exception as e:
            print(f"DEBUG: Color extraction failed: {e}")
            return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}
