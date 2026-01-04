"""
Frame Quality Module
Utilities for assessing and improving frame quality
"""

import cv2
import numpy as np


def calculate_frame_quality(image):
    """
    Calculate image quality score (lower = better)
    Uses Laplacian variance to measure sharpness
    
    Args:
        image: Input image (BGR or grayscale)
        
    Returns:
        Quality score (lower is better, higher variance = sharper image)
    """
    if image is None or image.size == 0:
        return float('inf')
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Calculate Laplacian variance (measure of sharpness)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Return inverse quality score (lower = better)
    return 1.0 / (laplacian_var + 1)


def is_frame_blurry(image, threshold=100):
    """
    Check if frame is blurry
    
    Args:
        image: Input image
        threshold: Laplacian variance threshold (default: 100)
        
    Returns:
        True if blurry, False otherwise
    """
    if image is None or image.size == 0:
        return True
    
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    return laplacian_var < threshold


def enhance_frame_quality(image):
    """
    Enhance frame quality using various techniques
    
    Args:
        image: Input image
        
    Returns:
        Enhanced image
    """
    if image is None or image.size == 0:
        return image
    
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced_lab = cv2.merge([l, a, b])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Apply slight sharpening
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    return sharpened


def get_best_frames(frames, n=10):
    """
    Get the n best quality frames from a list
    
    Args:
        frames: List of frames
        n: Number of best frames to return
        
    Returns:
        List of best frames
    """
    if not frames:
        return []
    
    # Calculate quality for each frame
    frame_qualities = [(i, calculate_frame_quality(frame)) for i, frame in enumerate(frames)]
    
    # Sort by quality (lower score = better)
    frame_qualities.sort(key=lambda x: x[1])
    
    # Get indices of best frames
    best_indices = [idx for idx, _ in frame_qualities[:n]]
    
    # Return frames in original order
    return [frames[i] for i in sorted(best_indices)]

