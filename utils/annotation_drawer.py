"""
Annotation Drawer Module
Handles drawing annotations on video frames
"""

import cv2
import numpy as np


class AnnotationDrawer:
    """Draws tracking annotations on video frames"""
    
    def __init__(self):
        """Initialize annotation drawer"""
        self.ball_color = (0, 255, 0)  # Green
        self.referee_color = (0, 255, 255)  # Yellow
        self.ball_possession_color = (0, 0, 255)  # Red
    
    def draw_player(self, frame, bbox, track_id, team_color=(0, 0, 255),
                   jersey_number=None, has_ball=False):
        """
        Draw player annotation
        
        Args:
            frame: Video frame
            bbox: Bounding box [x1, y1, x2, y2]
            track_id: Player tracking ID
            team_color: Team color (BGR)
            jersey_number: Jersey number if detected
            has_ball: Whether player has ball
        """
        y2 = int(bbox[3])
        x_center = int((bbox[0] + bbox[2]) / 2)
        width = int(bbox[2] - bbox[0])
        
        # Draw foot ellipse
        cv2.ellipse(
            frame,
            (x_center, y2),
            (int(width/2), int(0.35*width/2)),
            0, -45, 235,
            team_color, 2
        )
        
        # Draw jersey number label
        if isinstance(track_id, int) and track_id < 100:
            text = str(track_id)
            bg_color = (0, 255, 0)  # Green for detected jersey
        else:
            text = "?"
            bg_color = team_color
        
        rect_w, rect_h = 35, 20
        x1_rect = x_center - rect_w // 2
        y1_rect = y2 + 5
        
        cv2.rectangle(
            frame,
            (x1_rect, y1_rect),
            (x1_rect + rect_w, y1_rect + rect_h),
            bg_color, cv2.FILLED
        )
        
        cv2.putText(
            frame, text,
            (x1_rect + 5, y1_rect + 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 0, 0), 2
        )
        
        # Draw ball possession indicator
        if has_ball:
            y = int(bbox[1])
            pts = np.array([
                [x_center, y],
                [x_center - 10, y - 20],
                [x_center + 10, y - 20]
            ])
            cv2.drawContours(frame, [pts], 0, self.ball_possession_color, cv2.FILLED)
    
    def draw_referee(self, frame, bbox):
        """
        Draw referee annotation
        
        Args:
            frame: Video frame
            bbox: Bounding box [x1, y1, x2, y2]
        """
        y2 = int(bbox[3])
        x_center = int((bbox[0] + bbox[2]) / 2)
        width = int(bbox[2] - bbox[0])
        
        cv2.ellipse(
            frame,
            (x_center, y2),
            (int(width/2), int(0.35*width/2)),
            0, -45, 235,
            self.referee_color, 2
        )
    
    def draw_ball(self, frame, bbox, interpolated=False):
        """
        Draw ball annotation
        
        Args:
            frame: Video frame
            bbox: Bounding box [x1, y1, x2, y2]
            interpolated: Whether position is interpolated
        """
        y = int(bbox[1])
        x = int((bbox[0] + bbox[2]) / 2)
        
        color = self.ball_color if not interpolated else (0, 165, 255)  # Orange if interpolated
        
        pts = np.array([
            [x, y],
            [x - 10, y - 20],
            [x + 10, y - 20]
        ])
        
        cv2.drawContours(frame, [pts], 0, color, cv2.FILLED)
        cv2.drawContours(frame, [pts], 0, (0, 0, 0), 2)
    
    def draw_possession_stats(self, frame, team1_pct, team2_pct):
        """
        Draw team possession statistics
        
        Args:
            frame: Video frame
            team1_pct: Team 1 possession percentage
            team2_pct: Team 2 possession percentage
        """
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 80), (255, 255, 255), cv2.FILLED)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(
            frame, f"Team 1: {team1_pct:.1f}%",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (0, 0, 0), 2
        )
        
        cv2.putText(
            frame, f"Team 2: {team2_pct:.1f}%",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (0, 0, 0), 2
        )
    
    def draw_annotations(self, video_frames, tracks, team_ball_control):
        """
        Draw all annotations on video frames
        
        Args:
            video_frames: List of video frames
            tracks: Dictionary of tracks
            team_ball_control: Array of team possession per frame
            
        Returns:
            List of annotated frames
        """
        output_frames = []
        
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            
            # Draw players
            if frame_num < len(tracks["players"]):
                for track_id, player in tracks["players"][frame_num].items():
                    self.draw_player(
                        frame,
                        player["bbox"],
                        track_id,
                        player.get("team_color", (0, 0, 255)),
                        player.get("jersey_number"),
                        player.get('has_ball', False)
                    )
            
            # Draw referees
            if frame_num < len(tracks["referees"]):
                for _, referee in tracks["referees"][frame_num].items():
                    self.draw_referee(frame, referee["bbox"])
            
            # Draw ball
            if frame_num < len(tracks["ball"]) and 1 in tracks["ball"][frame_num]:
                ball = tracks["ball"][frame_num][1]
                self.draw_ball(
                    frame,
                    ball["bbox"],
                    ball.get('interpolated', False)
                )
            
            # Draw possession stats
            if len(team_ball_control) > 0:
                control = team_ball_control[:frame_num + 1]
                t1 = np.sum(control == 1)
                t2 = np.sum(control == 2)
                total = t1 + t2
                t1_pct = t1 / total * 100 if total > 0 else 50
                t2_pct = t2 / total * 100 if total > 0 else 50
            else:
                t1_pct = t2_pct = 50
            
            self.draw_possession_stats(frame, t1_pct, t2_pct)
            output_frames.append(frame)
        
        return output_frames


