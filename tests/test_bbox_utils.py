"""
Tests for bounding box utilities
"""

import pytest
import numpy as np
from utils.bbox_utils import (
    get_center_of_bbox,
    get_foot_position,
    measure_distance,
    measure_xy_distance,
    calculate_iou
)


class TestBBoxUtils:
    """Test bounding box utility functions"""
    
    def test_get_center_of_bbox(self):
        """Test center calculation"""
        bbox = [10, 20, 30, 40]
        center = get_center_of_bbox(bbox)
        assert center == (20, 30)
    
    def test_get_foot_position(self):
        """Test foot position calculation"""
        bbox = [10, 20, 30, 40]
        foot = get_foot_position(bbox)
        assert foot == (20, 40)
    
    def test_measure_distance(self):
        """Test distance calculation"""
        p1 = (0, 0)
        p2 = (3, 4)
        distance = measure_distance(p1, p2)
        assert abs(distance - 5.0) < 0.001
    
    def test_measure_xy_distance(self):
        """Test x/y distance calculation"""
        p1 = (10, 20)
        p2 = (15, 25)
        x_dist, y_dist = measure_xy_distance(p1, p2)
        assert x_dist == -5
        assert y_dist == -5
    
    def test_calculate_iou(self):
        """Test IoU calculation"""
        bbox1 = [10, 10, 30, 30]
        bbox2 = [20, 20, 40, 40]
        iou = calculate_iou(bbox1, bbox2)
        assert 0 <= iou <= 1
        
        # Same bbox should have IoU = 1
        iou_same = calculate_iou(bbox1, bbox1)
        assert abs(iou_same - 1.0) < 0.001
        
        # Non-overlapping should have IoU = 0
        bbox3 = [100, 100, 120, 120]
        iou_no_overlap = calculate_iou(bbox1, bbox3)
        assert iou_no_overlap == 0.0

