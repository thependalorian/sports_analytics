"""
Color Clustering Module
Handles color extraction and clustering for team assignment
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans


class ColorExtractor:
    """Extracts dominant colors from image regions"""
    
    def __init__(self, use_lab=True):
        """
        Initialize color extractor
        
        Args:
            use_lab: Use LAB color space for better color clustering
        """
        self.use_lab = use_lab
    
    def extract_dominant_color(self, image, region_bbox=None):
        """
        Extract dominant color from image or region
        
        Args:
            image: Input image (BGR)
            region_bbox: Optional bounding box [x1, y1, x2, y2] to extract from
            
        Returns:
            Dominant color as numpy array or None
        """
        if region_bbox is not None:
            x1, y1, x2, y2 = [int(v) for v in region_bbox]
            h, w = image.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 <= x1 or y2 <= y1:
                return None
            
            image = image[y1:y2, x1:x2]
        
        if image.size == 0:
            return None
        
        # Convert to LAB if requested
        if self.use_lab:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Reshape to 2D array of pixels
        pixels = image.reshape(-1, 3)
        
        # Remove extreme values (likely background or noise)
        if self.use_lab:
            mask = (pixels[:, 0] > 20) & (pixels[:, 0] < 235)
        else:
            mask = (pixels.sum(axis=1) > 30) & (pixels.sum(axis=1) < 700)
        
        pixels = pixels[mask]
        
        if len(pixels) < 10:
            return None
        
        # Get dominant color using k-means
        kmeans = KMeans(n_clusters=1, init='k-means++', n_init=1, random_state=42)
        kmeans.fit(pixels)
        
        return kmeans.cluster_centers_[0]
    
    def extract_jersey_color(self, frame, bbox):
        """
        Extract jersey color from player bounding box
        
        Args:
            frame: Video frame
            bbox: Player bounding box [x1, y1, x2, y2]
            
        Returns:
            Dominant jersey color or None
        """
        try:
            x1, y1, x2, y2 = [int(v) for v in bbox]
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 <= x1 or y2 <= y1:
                return None
            
            # Extract player region
            player_img = frame[y1:y2, x1:x2]
            
            # Focus on upper body (jersey region)
            jersey_height = int((y2 - y1) * 0.5)  # Top 50% of bbox
            jersey_img = player_img[0:jersey_height, :]
            
            if jersey_img.size == 0:
                return None
            
            # Extract dominant color
            return self.extract_dominant_color(jersey_img)
        
        except Exception:
            return None


class TeamColorClusterer:
    """Clusters player colors into teams"""
    
    def __init__(self, use_lab=True):
        """
        Initialize team color clusterer
        
        Args:
            use_lab: Use LAB color space
        """
        self.use_lab = use_lab
        self.kmeans = None
        self.team_colors = {}
    
    def fit_teams(self, player_colors):
        """
        Fit KMeans model to cluster players into 2 teams
        
        Args:
            player_colors: List of player color arrays
            
        Returns:
            True if successful, False otherwise
        """
        if len(player_colors) < 2:
            # Default colors if not enough players
            self.team_colors[1] = (255, 0, 0)  # Red
            self.team_colors[2] = (0, 0, 255)  # Blue
            return False
        
        # Cluster into 2 teams
        self.kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, random_state=42)
        self.kmeans.fit(player_colors)
        
        # Assign team colors
        if self.use_lab:
            # Convert LAB centroids back to BGR for display
            team1_color_lab = self.kmeans.cluster_centers_[0].reshape(1, 1, 3).astype(np.uint8)
            team2_color_lab = self.kmeans.cluster_centers_[1].reshape(1, 1, 3).astype(np.uint8)
            
            team1_color_bgr = cv2.cvtColor(team1_color_lab, cv2.COLOR_LAB2BGR)[0, 0]
            team2_color_bgr = cv2.cvtColor(team2_color_lab, cv2.COLOR_LAB2BGR)[0, 0]
            
            self.team_colors[1] = tuple(map(int, team1_color_bgr))
            self.team_colors[2] = tuple(map(int, team2_color_bgr))
        else:
            self.team_colors[1] = tuple(map(int, self.kmeans.cluster_centers_[0]))
            self.team_colors[2] = tuple(map(int, self.kmeans.cluster_centers_[1]))
        
        return True
    
    def predict_team(self, player_color):
        """
        Predict team for a player color
        
        Args:
            player_color: Player color array
            
        Returns:
            Team number (1 or 2) or None if model not fitted
        """
        if self.kmeans is None:
            return None
        
        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        return team_id + 1  # Convert 0/1 to 1/2

