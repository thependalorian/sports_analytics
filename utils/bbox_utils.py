"""
Bounding Box Utilities Module
Helper functions for bounding box operations
"""

import numpy as np


def get_center(bbox):
    """
    Get center point of bounding box

    Args:
        bbox: [x1, y1, x2, y2]

    Returns:
        (center_x, center_y)
    """
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def get_center_of_bbox(bbox):
    """
    Get center point (x, y) of bounding box (alias for get_center)
    
    Args:
        bbox: [x1, y1, x2, y2]
        
    Returns:
        (x_center, y_center) as integers
    """
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def get_width(bbox):
    """
    Get width of bounding box

    Args:
        bbox: [x1, y1, x2, y2]

    Returns:
        Width
    """
    return bbox[2] - bbox[0]


def get_bbox_width(bbox):
    """
    Get width of bounding box (alias for get_width)
    
    Args:
        bbox: [x1, y1, x2, y2]
        
    Returns:
        Width
    """
    return bbox[2] - bbox[0]


def get_height(bbox):
    """
    Get height of bounding box

    Args:
        bbox: [x1, y1, x2, y2]

    Returns:
        Height
    """
    return bbox[3] - bbox[1]


def get_foot_position(bbox):
    """
    Get foot position (bottom center) of bounding box

    Args:
        bbox: [x1, y1, x2, y2]

    Returns:
        (center_x, y2) as integers
    """
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)


def calculate_iou(bbox1, bbox2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes

    Args:
        bbox1: [x1, y1, x2, y2]
        bbox2: [x1, y1, x2, y2]

    Returns:
        IoU value (0 to 1)
    """
    x1_min, y1_min, x1_max, y1_max = bbox1
    x2_min, y2_min, x2_max, y2_max = bbox2

    # Calculate intersection area
    x_left = max(x1_min, x2_min)
    y_top = max(y1_min, y2_min)
    x_right = min(x1_max, x2_max)
    y_bottom = min(y1_max, y2_max)

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate union area
    bbox1_area = (x1_max - x1_min) * (y1_max - y1_min)
    bbox2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = bbox1_area + bbox2_area - intersection_area

    if union_area == 0:
        return 0.0

    return intersection_area / union_area


def expand_bbox(bbox, factor=1.2):
    """
    Expand bounding box by a factor

    Args:
        bbox: [x1, y1, x2, y2]
        factor: Expansion factor (1.0 = no change, 2.0 = double size)

    Returns:
        Expanded bbox
    """
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1

    center_x, center_y = get_center(bbox)

    new_width = width * factor
    new_height = height * factor

    new_x1 = center_x - new_width / 2
    new_y1 = center_y - new_height / 2
    new_x2 = center_x + new_width / 2
    new_y2 = center_y + new_height / 2

    return [new_x1, new_y1, new_x2, new_y2]


def clip_bbox(bbox, frame_width, frame_height):
    """
    Clip bounding box to frame boundaries

    Args:
        bbox: [x1, y1, x2, y2]
        frame_width: Frame width
        frame_height: Frame height

    Returns:
        Clipped bbox
    """
    x1, y1, x2, y2 = bbox

    x1 = max(0, min(x1, frame_width))
    y1 = max(0, min(y1, frame_height))
    x2 = max(0, min(x2, frame_width))
    y2 = max(0, min(y2, frame_height))

    return [x1, y1, x2, y2]


def bbox_to_xyxy(bbox):
    """
    Ensure bbox is in [x1, y1, x2, y2] format

    Args:
        bbox: Bounding box in any format

    Returns:
        [x1, y1, x2, y2]
    """
    if len(bbox) == 4:
        return bbox
    else:
        raise ValueError(f"Invalid bbox format: {bbox}")


def bbox_area(bbox):
    """
    Calculate area of bounding box

    Args:
        bbox: [x1, y1, x2, y2]

    Returns:
        Area
    """
    width = get_width(bbox)
    height = get_height(bbox)
    return width * height


def merge_bboxes(bboxes):
    """
    Merge multiple bounding boxes into one

    Args:
        bboxes: List of bounding boxes

    Returns:
        Merged bbox [x1, y1, x2, y2]
    """
    if not bboxes:
        return [0, 0, 0, 0]

    x1 = min(bbox[0] for bbox in bboxes)
    y1 = min(bbox[1] for bbox in bboxes)
    x2 = max(bbox[2] for bbox in bboxes)
    y2 = max(bbox[3] for bbox in bboxes)

    return [x1, y1, x2, y2]


def measure_distance(p1, p2):
    """
    Euclidean distance between two points
    
    Args:
        p1: (x1, y1) or [x1, y1]
        p2: (x2, y2) or [x2, y2]
        
    Returns:
        Distance
    """
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def measure_xy_distance(p1, p2):
    """
    Return (x_distance, y_distance) between points
    
    Args:
        p1: (x1, y1) or [x1, y1]
        p2: (x2, y2) or [x2, y2]
        
    Returns:
        (x_distance, y_distance)
    """
    return p1[0] - p2[0], p1[1] - p2[1]
