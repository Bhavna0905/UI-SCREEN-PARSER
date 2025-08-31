import cv2
import numpy as np
import easyocr
from typing import List, Tuple, Dict
import os

class ImageProcessor:
    def _init_(self):
        self.ocr_reader = easyocr.Reader(['en'])
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess the image with error handling"""
        print(f"DEBUG: Loading image from: {image_path}")
        
        if not os.path.exists(image_path):
            raise ValueError(f"Image file does not exist: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            try:
                from PIL import Image as PILImage
                pil_image = PILImage.open(image_path)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                print("DEBUG: Loaded with PIL")
            except Exception as e:
                raise ValueError(f"Could not load image: {e}")
        else:
            print(f"DEBUG: Loaded with OpenCV. Shape: {image.shape}")
        
        return image
    
    def extract_text_regions(self, image: np.ndarray) -> List[Dict]:
        """Extract text regions using OCR"""
        if image is None or image.size == 0:
            return []
        
        try:
            results = self.ocr_reader.readtext(image)
            text_regions = []
            
            for (bbox, text, confidence) in results:
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
            
            print(f"DEBUG: Found {len(text_regions)} text regions")
            return text_regions
        except Exception as e:
            print(f"DEBUG: OCR failed: {e}")
            return []
    
    def detect_ui_elements(self, image: np.ndarray) -> List[Dict]:
        """Detect UI elements using computer vision"""
        if image is None or image.size == 0:
            return []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rectangles = self._detect_rectangles(gray)
            circles = self._detect_circles(gray)
            elements = rectangles + circles
            print(f"DEBUG: Found {len(elements)} UI elements")
            return elements
        except Exception as e:
            print(f"DEBUG: UI detection failed: {e}")
            return []
    
    def _detect_rectangles(self, gray_image: np.ndarray) -> List[Dict]:
        """Detect rectangular UI elements"""
        try:
            edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            rectangles = []
            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(contour)
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
        """Detect circular UI elements"""
        try:
            circles = cv2.HoughCircles(
                gray_image, cv2.HOUGH_GRADIENT, 1, 20,
                param1=50, param2=30, minRadius=10, maxRadius=100
            )
            
            circle_elements = []
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    x, y, r = int(x), int(y), int(r)
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
        """Extract dominant colors from a region"""
        try:
            x, y, w, h = bbox
            
            if (x < 0 or y < 0 or x + w > image.shape[1] or y + h > image.shape[0] or 
                w <= 0 or h <= 0):
                return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}
            
            roi = image[y:y+h, x:x+w]
            if roi.size == 0:
                return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}
            
            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            pixels = roi_rgb.reshape(-1, 3)
            dominant_color = np.mean(pixels, axis=0).astype(int)
            
            return {
                'dominant_rgb': f"rgb({dominant_color[0]}, {dominant_color[1]}, {dominant_color[2]})",
                'dominant_hex': f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"
            }
        except Exception as e:
            print(f"DEBUG: Color extraction failed: {e}")
            return {'dominant_rgb': 'rgb(128, 128, 128)', 'dominant_hex': '#808080'}