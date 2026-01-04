"""
Color Utilities Module
Helper functions for color space conversion and color operations
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans


def rgb_to_lab(image):
    """
    Convert BGR image to LAB color space
    
    Args:
        image: BGR image
        
    Returns:
        LAB image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)


def lab_to_bgr(image):
    """
    Convert LAB image to BGR color space
    
    Args:
        image: LAB image
        
    Returns:
        BGR image
    """
    return cv2.cvtColor(image, cv2.COLOR_LAB2BGR)


def bgr_to_rgb(image):
    """
    Convert BGR image to RGB color space
    
    Args:
        image: BGR image
        
    Returns:
        RGB image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(image):
    """
    Convert RGB image to BGR color space
    
    Args:
        image: RGB image
        
    Returns:
        BGR image
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def extract_dominant_color(image, n_clusters=2):
    """
    Extract dominant color using KMeans
    
    Args:
        image: Input image
        n_clusters: Number of color clusters to extract
        
    Returns:
        Array of dominant colors (cluster centers)
    """
    if image is None or image.size == 0:
        return None
    
    # Reshape to 2D array of pixels
    pixels = image.reshape(-1, 3)
    
    # Remove extreme values
    mask = (pixels.sum(axis=1) > 30) & (pixels.sum(axis=1) < 700)
    pixels = pixels[mask]
    
    if len(pixels) < n_clusters:
        return None
    
    # Apply KMeans
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    return kmeans.cluster_centers_


def get_average_color(image, region=None):
    """
    Get average color of image or region
    
    Args:
        image: Input image
        region: Optional bounding box [x1, y1, x2, y2]
        
    Returns:
        Average color as (B, G, R)
    """
    if region is not None:
        x1, y1, x2, y2 = region
        image = image[y1:y2, x1:x2]
    
    if image is None or image.size == 0:
        return None
    
    return tuple(map(int, image.mean(axis=(0, 1))))


def adjust_brightness(image, factor):
    """
    Adjust image brightness
    
    Args:
        image: Input image
        factor: Brightness factor (1.0 = no change, >1.0 = brighter, <1.0 = darker)
        
    Returns:
        Adjusted image
    """
    return cv2.convertScaleAbs(image, alpha=1, beta=int((factor - 1.0) * 255))


def adjust_contrast(image, factor):
    """
    Adjust image contrast
    
    Args:
        image: Input image
        factor: Contrast factor (1.0 = no change, >1.0 = more contrast)
        
    Returns:
        Adjusted image
    """
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

