"""
Video Utilities Module
Helper functions for video processing
"""

import cv2
import numpy as np


def read_video(video_path):
    """
    Read video file and return frames

    Args:
        video_path: Path to video file

    Returns:
        List of frames
    """
    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames


def save_video(output_path, frames, fps=30):
    """
    Save frames to video file

    Args:
        output_path: Output video path
        frames: List of frames
        fps: Frames per second
    """
    if not frames:
        print("⚠️  No frames to save")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    height, width = frames[0].shape[:2]
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"✓ Video saved: {output_path}")


def save_video_frames(output_video_frames, output_video_path, fps=24):
    """
    Save frames to video file (alternative function name for compatibility)
    
    Args:
        output_video_frames: List of frames
        output_video_path: Output video path
        fps: Frames per second
    """
    save_video(output_video_path, output_video_frames, fps)


def get_video_properties(video_path):
    """
    Get video properties

    Args:
        video_path: Path to video file

    Returns:
        Dictionary with video properties
    """
    cap = cv2.VideoCapture(video_path)

    props = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration_sec': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    }

    cap.release()
    return props


def resize_frame(frame, width=None, height=None, scale=None):
    """
    Resize frame

    Args:
        frame: Input frame
        width: Target width (optional)
        height: Target height (optional)
        scale: Scale factor (optional)

    Returns:
        Resized frame
    """
    if scale is not None:
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
    elif width is not None and height is None:
        height = int(frame.shape[0] * (width / frame.shape[1]))
    elif height is not None and width is None:
        width = int(frame.shape[1] * (height / frame.shape[0]))

    if width is None or height is None:
        return frame

    return cv2.resize(frame, (width, height))


def crop_frame(frame, x, y, width, height):
    """
    Crop frame to region of interest

    Args:
        frame: Input frame
        x, y: Top-left corner
        width, height: Crop dimensions

    Returns:
        Cropped frame
    """
    return frame[y:y+height, x:x+width]


def draw_text(frame, text, position, font_scale=1.0, color=(255, 255, 255), thickness=2):
    """
    Draw text on frame with background

    Args:
        frame: Input frame
        text: Text to draw
        position: (x, y) position
        font_scale: Font size scale
        color: Text color (B, G, R)
        thickness: Text thickness

    Returns:
        Frame with text
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Get text size
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    # Draw background rectangle
    x, y = position
    cv2.rectangle(frame,
                 (x, y - text_size[1] - 10),
                 (x + text_size[0] + 10, y + 5),
                 (0, 0, 0),
                 cv2.FILLED)

    # Draw text
    cv2.putText(frame, text, (x + 5, y), font, font_scale, color, thickness)

    return frame


def create_side_by_side(frame1, frame2, text1="Original", text2="Processed"):
    """
    Create side-by-side comparison

    Args:
        frame1: First frame
        frame2: Second frame
        text1: Label for first frame
        text2: Label for second frame

    Returns:
        Combined frame
    """
    # Resize frames to same height
    h1, w1 = frame1.shape[:2]
    h2, w2 = frame2.shape[:2]

    if h1 != h2:
        frame2 = resize_frame(frame2, height=h1)
        h2, w2 = frame2.shape[:2]

    # Create combined frame
    combined = np.hstack([frame1, frame2])

    # Add labels
    combined = draw_text(combined, text1, (20, 40))
    combined = draw_text(combined, text2, (w1 + 20, 40))

    return combined
