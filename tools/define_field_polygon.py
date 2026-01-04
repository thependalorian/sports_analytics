"""
Define Field Polygon Tool
Interactive tool to define field boundaries by clicking on video frames
"""

import cv2
import json
import os
import sys


def click_event(event, x, y, flags, param):
    """Mouse callback for clicking field corners"""
    frame, points = param
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Define Field Polygon", frame)


def main():
    """Main function to define field polygon"""
    if len(sys.argv) < 2:
        print("Usage: python tools/define_field_polygon.py input_videos/your_clip.mp4")
        return
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return
    
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("Could not read video")
        return
    
    points = []
    clone = frame.copy()
    
    cv2.imshow("Define Field Polygon", frame)
    cv2.setMouseCallback("Define Field Polygon", click_event, param=(frame, points))
    
    print("Click 4 field corners in order: bottom-left, top-left, top-right, bottom-right.")
    print("Press 'r' to reset, 's' to save, 'q' to quit.")
    
    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('r'):
            frame = clone.copy()
            points.clear()
            cv2.imshow("Define Field Polygon", frame)
            print("Reset. Click 4 corners again.")
        
        elif key == ord('s'):
            if len(points) == 4:
                config_path = 'config/field_config.json'
                os.makedirs('config', exist_ok=True)
                
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                else:
                    config = {}
                
                video_name = os.path.basename(video_path).replace('.mp4', '').replace('.avi', '').replace('.mov', '')
                
                config[video_name] = {
                    "pixel_vertices": points,
                    "court_length_m": 105,
                    "court_width_m": 68
                }
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"✓ Saved field polygon for {video_name} to {config_path}")
                break
            else:
                print(f"Please select exactly 4 points. Currently selected: {len(points)}")
        
        elif key == ord('q'):
            print("Quit without saving.")
            break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

