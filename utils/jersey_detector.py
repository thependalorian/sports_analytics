"""
Jersey Number Detector Module
Handles OCR-based jersey number detection using EasyOCR
"""

import cv2
import numpy as np
import re
from collections import defaultdict, Counter

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("⚠️  EasyOCR not installed. Jersey number detection disabled.")


class JerseyNumberDetector:
    """
    Detects jersey numbers from player bounding boxes using OCR
    """
    
    def __init__(self, languages=['en'], gpu=True, confidence_threshold=0.5,
                 model_storage_dir='models/easyocr'):
        """
        Initialize jersey number detector
        
        Args:
            languages: List of languages for OCR
            gpu: Whether to use GPU acceleration
            confidence_threshold: Minimum confidence for number detection
            model_storage_dir: Directory for EasyOCR models
        """
        self.enabled = EASYOCR_AVAILABLE
        self.confidence_threshold = confidence_threshold
        self.reader = None
        
        if self.enabled:
            self._init_ocr_reader(languages, gpu, model_storage_dir)
        
        # Track jersey number mappings and history
        self.original_to_jersey = {}
        self.jersey_history = defaultdict(list)
        self.validation_frames = 3
        self.max_history = 50
    
    def _init_ocr_reader(self, languages, gpu, model_storage_dir):
        """Initialize EasyOCR reader"""
        try:
            self.reader = easyocr.Reader(
                languages,
                gpu=gpu,
                model_storage_directory=model_storage_dir,
                verbose=False
            )
        except Exception as e:
            print(f"⚠️  EasyOCR initialization failed: {e}")
            if gpu:
                # Fallback to CPU
                try:
                    self.reader = easyocr.Reader(
                        languages,
                        gpu=False,
                        model_storage_directory=model_storage_dir,
                        verbose=False
                    )
                except Exception:
                    self.enabled = False
                    print("❌ EasyOCR failed completely. Jersey detection disabled.")
            else:
                self.enabled = False
    
    def extract_jersey_region(self, frame, bbox):
        """
        Extract jersey region from player bounding box
        
        Args:
            frame: Video frame
            bbox: Bounding box [x1, y1, x2, y2]
            
        Returns:
            Extracted jersey ROI or None
        """
        x1, y1, x2, y2 = [int(v) for v in bbox]
        h, w = frame.shape[:2]
        
        # Clamp to frame boundaries
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return None
        
        # Extract player region
        player_roi = frame[y1:y2, x1:x2]
        if player_roi.size == 0:
            return None
        
        # Focus on upper torso (where jersey numbers are)
        height, width = player_roi.shape[:2]
        y_start = int(height * 0.15)
        y_end = int(height * 0.50)
        x_start = int(width * 0.15)
        x_end = int(width * 0.85)
        
        if y_end <= y_start or x_end <= x_start:
            return None
        
        jersey_roi = player_roi[y_start:y_end, x_start:x_end]
        return jersey_roi if jersey_roi.size > 0 else None
    
    def enhance_for_ocr(self, image):
        """
        Enhance image for better OCR results
        
        Args:
            image: Input image (BGR or grayscale)
            
        Returns:
            Enhanced grayscale image
        """
        if image is None or image.size == 0:
            return None
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        h, w = gray.shape
        if h < 10 or w < 10:
            return None
        
        # Upscale for better OCR
        scale = 4
        upscaled = cv2.resize(gray, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
        
        # Apply CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(upscaled)
        
        # Bilateral filter to reduce noise
        filtered = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(filtered, -1, kernel)
        
        return sharpened
    
    def detect_number(self, frame, bbox, original_track_id):
        """
        Detect jersey number from player bounding box
        
        Args:
            frame: Video frame
            bbox: Bounding box [x1, y1, x2, y2]
            original_track_id: Original tracking ID
            
        Returns:
            Detected jersey number or None
        """
        if not self.enabled or self.reader is None:
            return self.original_to_jersey.get(original_track_id)
        
        # Extract jersey region
        jersey_roi = self.extract_jersey_region(frame, bbox)
        if jersey_roi is None:
            return self.original_to_jersey.get(original_track_id)
        
        try:
            # Enhance image
            enhanced = self.enhance_for_ocr(jersey_roi)
            if enhanced is None:
                return self.original_to_jersey.get(original_track_id)
            
            # Run OCR
            results = self.reader.readtext(
                enhanced,
                allowlist='0123456789',
                paragraph=False,
                min_size=15,
                text_threshold=0.6,
                low_text=0.3
            )
            
            # Extract valid numbers
            detected_numbers = []
            for (_, text, confidence) in results:
                cleaned = re.sub(r'\D', '', text)
                if cleaned and confidence >= self.confidence_threshold:
                    number = int(cleaned)
                    if 1 <= number <= 99:  # Valid jersey number range
                        detected_numbers.append((number, confidence))
            
            if detected_numbers:
                # Use highest confidence detection
                detected_numbers.sort(key=lambda x: x[1], reverse=True)
                number, conf = detected_numbers[0]
                
                # Add to history
                self.jersey_history[original_track_id].append(number)
                if len(self.jersey_history[original_track_id]) > self.max_history:
                    self.jersey_history[original_track_id].pop(0)
                
                # Validate and return
                return self._validate_number(original_track_id)
        
        except Exception as e:
            # Silently fail - OCR can be noisy
            pass
        
        return self.original_to_jersey.get(original_track_id)
    
    def _validate_number(self, original_track_id):
        """
        Validate jersey number using majority voting
        
        Args:
            original_track_id: Tracking ID
            
        Returns:
            Validated jersey number or None
        """
        history = self.jersey_history[original_track_id]
        
        if len(history) < self.validation_frames:
            return self.original_to_jersey.get(original_track_id)
        
        # Use recent history for validation
        recent = history[-15:]
        counter = Counter(recent)
        most_common = counter.most_common(1)[0]
        number, count = most_common
        
        # Require 40% consensus
        if count / len(recent) > 0.4:
            if (original_track_id not in self.original_to_jersey or
                self.original_to_jersey[original_track_id] != number):
                self.original_to_jersey[original_track_id] = number
            return number
        
        return self.original_to_jersey.get(original_track_id)
    
    def get_jersey_mapping(self):
        """Get current jersey number to track ID mapping"""
        return self.original_to_jersey.copy()
    
    def get_detection_stats(self, track_id):
        """
        Get detection statistics for a track ID
        
        Args:
            track_id: Tracking ID
            
        Returns:
            Dictionary with detection statistics
        """
        history = self.jersey_history.get(track_id, [])
        jersey = self.original_to_jersey.get(track_id)
        
        if not history:
            return {
                'jersey_number': None,
                'detections': 0,
                'confidence': 0.0
            }
        
        detections = len(history)
        conf = history.count(jersey) / len(history) if jersey else 0.0
        
        return {
            'jersey_number': jersey,
            'detections': detections,
            'confidence': conf
        }


