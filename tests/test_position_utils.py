"""
Tests for position utilities
"""

import pytest
import numpy as np
from utils.position_utils import PositionCalculator, BallInterpolator


class TestPositionCalculator:
    """Test position calculation utilities"""
    
    def test_get_bbox_center(self):
        """Test bbox center calculation"""
        calc = PositionCalculator()
        bbox = [10, 20, 30, 40]
        center = calc.get_bbox_center(bbox)
        assert center == [20, 30]
    
    def test_get_foot_position(self):
        """Test foot position calculation"""
        calc = PositionCalculator()
        bbox = [10, 20, 30, 40]
        foot = calc.get_foot_position(bbox)
        assert foot == [20, 40]
    
    def test_calculate_distance(self):
        """Test distance calculation"""
        calc = PositionCalculator()
        pos1 = [0, 0]
        pos2 = [3, 4]
        distance = calc.calculate_distance(pos1, pos2)
        assert abs(distance - 5.0) < 0.001


class TestBallInterpolator:
    """Test ball position interpolation"""
    
    def test_interpolate_ball_positions(self):
        """Test ball position interpolation"""
        interpolator = BallInterpolator()
        
        # Create test data with missing positions
        ball_positions = [
            {1: {"bbox": [100, 100, 110, 110]}},
            {1: {"bbox": []}},  # Missing
            {1: {"bbox": []}},  # Missing
            {1: {"bbox": [130, 130, 140, 140]}}
        ]
        
        result = interpolator.interpolate_ball_positions(ball_positions)
        
        # Should have interpolated positions
        assert len(result) == 4
        assert 1 in result[0]
        assert 1 in result[3]

