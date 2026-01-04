"""
Event Detector Module
Location: /analytics/event_detector.py
Purpose: Detects significant match events (sprints, clusters, ball trajectory changes)
Modular design for football-specific event detection
"""

import numpy as np
import csv
import os
from collections import deque


class EventDetector:
    """
    Detects match events using trajectory and position analysis
    Football-focused: sprints, player clusters (set pieces), trajectory changes (shots, clearances)
    """

    def __init__(self, sprint_threshold=7.0, cluster_threshold=5.0):
        """
        Initialize event detector

        Args:
            sprint_threshold: Speed threshold for sprint detection (m/s) - 7.0 m/s = ~25 km/h
            cluster_threshold: Distance threshold for player clustering (m) - 5.0m for corners/set pieces
        """
        self.sprint_threshold = sprint_threshold
        self.cluster_threshold = cluster_threshold

        # Event log
        self.events = []

        # Tracking for event detection
        self.ball_trajectory = deque(maxlen=30)  # Last 30 frames (~1 second at 30fps)
        self.player_speeds = {}

        # Cooldown to avoid duplicate events (frames)
        self.last_event_frame = {'sprint': {}, 'cluster': -100, 'trajectory_change': -100}
    
    def detect_events(self, tracks, fps=30):
        """
        Detect all events across entire match
        
        Args:
            tracks: Complete tracking dictionary
            fps: Frames per second
            
        Returns:
            List of detected events
        """
        self.events = []  # Reset
        
        for frame_idx in range(len(tracks.get('players', []))):
            # Create frame-specific tracks dict
            frame_tracks = {
                'players': [tracks['players'][frame_idx]] if frame_idx < len(tracks['players']) else [{}],
                'ball': [tracks['ball'][frame_idx]] if frame_idx < len(tracks['ball']) else [{}],
                'referees': [tracks['referees'][frame_idx]] if frame_idx < len(tracks['referees']) else [{}]
            }
            
            self.process_frame(frame_idx, frame_tracks, current_team=1)
        
        return self.events

    def process_frame(self, frame_num, tracks, current_team):
        """
        Process frame for event detection

        Args:
            frame_num: Current frame number
            tracks: Tracking data
            current_team: Team in possession
        """
        # Detect sprints
        self._detect_sprints(frame_num, tracks)

        # Detect player clusters
        self._detect_clusters(frame_num, tracks)

        # Detect ball trajectory changes
        self._detect_trajectory_changes(frame_num, tracks)

    def _detect_sprints(self, frame_num, tracks):
        """Detect player sprints"""
        if not tracks.get('players') or len(tracks['players']) == 0:
            return

        for player_id, player_data in tracks['players'][0].items():
            speed = player_data.get('speed', 0)

            if speed > self.sprint_threshold:
                # Check cooldown (don't report same player sprinting every frame)
                last_sprint = self.last_event_frame['sprint'].get(player_id, -100)

                if frame_num - last_sprint > 60:  # 2 seconds cooldown
                    team = player_data.get('team', 0)
                    jersey = player_data.get('jersey_number', '')

                    player_label = f"#{jersey}" if jersey else f"Player {player_id}"

                    event = {
                        'frame': frame_num,
                        'event_type': 'sprint',
                        'team': team,
                        'player_id': player_id,
                        'player_label': player_label,
                        'speed': speed,
                        'description': f"{player_label} (Team {team}) sprinting at {speed:.1f} m/s"
                    }

                    self.events.append(event)
                    self.last_event_frame['sprint'][player_id] = frame_num

    def _detect_clusters(self, frame_num, tracks):
        """Detect player clusters (e.g., for corners, set pieces)"""
        if not tracks.get('players') or len(tracks['players']) == 0:
            return

        # Check cooldown
        if frame_num - self.last_event_frame['cluster'] < 60:
            return

        players = tracks['players'][0]
        positions = []

        for player_id, player_data in players.items():
            pos = player_data.get('position_transformed', player_data.get('position', None))
            if pos:
                positions.append(pos)

        if len(positions) < 5:
            return

        positions = np.array(positions)

        # Find clusters using simple distance metric
        for i in range(len(positions)):
            nearby = 0
            for j in range(len(positions)):
                if i != j:
                    dist = np.linalg.norm(positions[i] - positions[j])
                    if dist < self.cluster_threshold:
                        nearby += 1

            # If 4+ players within cluster threshold
            if nearby >= 4:
                event = {
                    'frame': frame_num,
                    'event_type': 'cluster',
                    'team': None,
                    'player_count': nearby + 1,
                    'description': f"Player cluster detected ({nearby + 1} players within {self.cluster_threshold}m)"
                }

                self.events.append(event)
                self.last_event_frame['cluster'] = frame_num
                break

    def _detect_trajectory_changes(self, frame_num, tracks):
        """Detect significant ball trajectory changes (potential shots, clearances)"""
        if not tracks.get('ball') or len(tracks['ball']) == 0:
            return

        ball_data = tracks['ball'][0].get(1, {})
        ball_pos = ball_data.get('position', None)

        if ball_pos:
            self.ball_trajectory.append(ball_pos)

        # Need enough history
        if len(self.ball_trajectory) < 10:
            return

        # Check cooldown
        if frame_num - self.last_event_frame['trajectory_change'] < 30:
            return

        # Calculate trajectory vectors
        positions = np.array(list(self.ball_trajectory))

        # Recent trajectory (last 5 frames)
        recent_trajectory = positions[-5:] - positions[-6:-1]
        recent_angle = np.mean(np.arctan2(recent_trajectory[:, 1], recent_trajectory[:, 0]))

        # Previous trajectory (frames 5-10)
        if len(positions) >= 15:
            prev_trajectory = positions[-15:-10] - positions[-16:-11]
            prev_angle = np.mean(np.arctan2(prev_trajectory[:, 1], prev_trajectory[:, 0]))

            # Check for significant angle change
            angle_change = abs(recent_angle - prev_angle)

            if angle_change > np.pi / 3:  # > 60 degrees
                event = {
                    'frame': frame_num,
                    'event_type': 'trajectory_change',
                    'team': None,
                    'angle_change': np.degrees(angle_change),
                    'description': f"Ball trajectory change detected ({np.degrees(angle_change):.0f}°)"
                }

                self.events.append(event)
                self.last_event_frame['trajectory_change'] = frame_num

    @staticmethod
    def export_events_csv(events, output_path):
        """
        Export events to CSV (static method for consistency)

        Args:
            events: List of event dictionaries
            output_path: CSV output path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='') as f:
            fieldnames = ['frame', 'event_type', 'team', 'description']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()
            writer.writerows(events)

        print(f"✓ Events exported: {output_path} ({len(events)} events)")

    def get_event_statistics(self):
        """
        Get event statistics summary

        Returns:
            Dictionary with event statistics
        """
        stats = {
            'total_events': len(self.events),
            'sprints': len([e for e in self.events if e['event_type'] == 'sprint']),
            'clusters': len([e for e in self.events if e['event_type'] == 'cluster']),
            'trajectory_changes': len([e for e in self.events if e['event_type'] == 'trajectory_change']),
            'team1_sprints': len([e for e in self.events if e['event_type'] == 'sprint' and e.get('team') == 1]),
            'team2_sprints': len([e for e in self.events if e['event_type'] == 'sprint' and e.get('team') == 2]),
        }

        return stats
