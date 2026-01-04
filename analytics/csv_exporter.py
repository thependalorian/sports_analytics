"""
CSV Exporter Module
Location: /analytics/csv_exporter.py
Purpose: Exports tracking data to CSV format for further analysis
Modular design for easy maintenance and extensibility
"""

import csv
import os
from collections import defaultdict
import pandas as pd


class CSVExporter:
    """
    Exports tracking data to CSV files
    Modular exporter for tracking, passes, events, and summaries
    """

    def __init__(self):
        """Initialize CSV exporter with no state (stateless design)"""
        pass

    def export_chunk(self, tracks, frame_offset, chunk_idx, team_ball_control):
        """
        Export a chunk of tracking data to CSV

        Args:
            tracks: Tracking data dictionary
            frame_offset: Starting frame number for this chunk
            chunk_idx: Chunk index
            team_ball_control: Array of team possession per frame
        """
        chunk_path = self.output_path.replace('.csv', f'_chunk_{chunk_idx}.csv')
        self.chunk_files.append(chunk_path)

        with open(chunk_path, 'w', newline='') as f:
            fieldnames = [
                'frame', 'object_type', 'track_id', 'team', 'jersey_number',
                'x', 'y', 'x_transformed', 'y_transformed',
                'speed', 'distance_covered', 'has_ball', 'possession_team'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Export players
            for frame_idx, frame_tracks in enumerate(tracks.get('players', [])):
                global_frame = frame_offset + frame_idx
                possession_team = team_ball_control[frame_idx] if frame_idx < len(team_ball_control) else 0

                for track_id, player_data in frame_tracks.items():
                    position = player_data.get('position', [0, 0])
                    position_transformed = player_data.get('position_transformed', [0, 0])

                    row = {
                        'frame': global_frame,
                        'object_type': 'player',
                        'track_id': track_id,
                        'team': player_data.get('team', 0),
                        'jersey_number': player_data.get('jersey_number', ''),
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': player_data.get('speed', 0),
                        'distance_covered': player_data.get('distance_covered', 0),
                        'has_ball': player_data.get('has_ball', False),
                        'possession_team': possession_team
                    }
                    writer.writerow(row)

            # Export ball
            for frame_idx, frame_tracks in enumerate(tracks.get('ball', [])):
                global_frame = frame_offset + frame_idx
                possession_team = team_ball_control[frame_idx] if frame_idx < len(team_ball_control) else 0

                if 1 in frame_tracks:
                    ball_data = frame_tracks[1]
                    position = ball_data.get('position', [0, 0])
                    position_transformed = ball_data.get('position_transformed', [0, 0])

                    row = {
                        'frame': global_frame,
                        'object_type': 'ball',
                        'track_id': 1,
                        'team': 0,
                        'jersey_number': '',
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': 0,
                        'distance_covered': 0,
                        'has_ball': False,
                        'possession_team': possession_team
                    }
                    writer.writerow(row)

            # Export referees
            for frame_idx, frame_tracks in enumerate(tracks.get('referees', [])):
                global_frame = frame_offset + frame_idx
                possession_team = team_ball_control[frame_idx] if frame_idx < len(team_ball_control) else 0

                for track_id, referee_data in frame_tracks.items():
                    position = referee_data.get('position', [0, 0])
                    position_transformed = referee_data.get('position_transformed', [0, 0])

                    row = {
                        'frame': global_frame,
                        'object_type': 'referee',
                        'track_id': track_id,
                        'team': 0,
                        'jersey_number': '',
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': 0,
                        'distance_covered': 0,
                        'has_ball': False,
                        'possession_team': possession_team
                    }
                    writer.writerow(row)

        print(f"  ✓ Chunk {chunk_idx} exported to CSV")

    @staticmethod
    def export_tracking_data(tracks, output_path):
        """
        Export complete tracking data to CSV
        
        Args:
            tracks: Dictionary with 'players', 'ball', 'referees' tracking data
            output_path: CSV output file path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='') as f:
            fieldnames = [
                'frame', 'object_type', 'track_id', 'team', 'jersey_number',
                'x', 'y', 'x_transformed', 'y_transformed',
                'speed', 'speed_kmh', 'distance_covered', 'has_ball'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Export players
            for frame_idx, frame_tracks in enumerate(tracks.get('players', [])):
                for track_id, player_data in frame_tracks.items():
                    position = player_data.get('position', [0, 0])
                    position_transformed = player_data.get('position_transformed', [0, 0])
                    
                    row = {
                        'frame': frame_idx,
                        'object_type': 'player',
                        'track_id': track_id,
                        'team': player_data.get('team', 0),
                        'jersey_number': player_data.get('jersey_number', ''),
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': player_data.get('speed', 0),
                        'speed_kmh': player_data.get('speed_kmh', 0),
                        'distance_covered': player_data.get('distance_covered', 0),
                        'has_ball': player_data.get('has_ball', False)
                    }
                    writer.writerow(row)
            
            # Export ball
            for frame_idx, frame_tracks in enumerate(tracks.get('ball', [])):
                if 1 in frame_tracks:
                    ball_data = frame_tracks[1]
                    position = ball_data.get('position', [0, 0])
                    position_transformed = ball_data.get('position_transformed', [0, 0])
                    
                    row = {
                        'frame': frame_idx,
                        'object_type': 'ball',
                        'track_id': 1,
                        'team': 0,
                        'jersey_number': '',
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': 0,
                        'speed_kmh': 0,
                        'distance_covered': 0,
                        'has_ball': False
                    }
                    writer.writerow(row)
            
            # Export referees
            for frame_idx, frame_tracks in enumerate(tracks.get('referees', [])):
                for track_id, referee_data in frame_tracks.items():
                    position = referee_data.get('position', [0, 0])
                    position_transformed = referee_data.get('position_transformed', [0, 0])
                    
                    row = {
                        'frame': frame_idx,
                        'object_type': 'referee',
                        'track_id': track_id,
                        'team': 0,
                        'jersey_number': '',
                        'x': position[0] if len(position) > 0 else 0,
                        'y': position[1] if len(position) > 1 else 0,
                        'x_transformed': position_transformed[0] if len(position_transformed) > 0 else 0,
                        'y_transformed': position_transformed[1] if len(position_transformed) > 1 else 0,
                        'speed': 0,
                        'speed_kmh': 0,
                        'distance_covered': 0,
                        'has_ball': False
                    }
                    writer.writerow(row)
        
        print(f"✓ Tracking data exported: {output_path}")

    def export_player_summary(self, tracking_data, output_path):
        """
        Export per-player summary statistics

        Args:
            tracking_data: Full tracking data (pandas DataFrame expected)
            output_path: Output CSV path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Group by player
        player_stats = defaultdict(lambda: {
            'team': 0,
            'jersey_number': '',
            'total_distance': 0,
            'avg_speed': 0,
            'max_speed': 0,
            'frames_with_ball': 0,
            'total_frames': 0
        })

        try:
            import pandas as pd

            if isinstance(tracking_data, str):
                df = pd.read_csv(tracking_data)
            else:
                df = tracking_data

            players_df = df[df['object_type'] == 'player']

            for track_id in players_df['track_id'].unique():
                player_df = players_df[players_df['track_id'] == track_id]

                if len(player_df) > 0:
                    player_stats[track_id] = {
                        'team': player_df['team'].mode()[0] if len(player_df['team'].mode()) > 0 else 0,
                        'jersey_number': player_df['jersey_number'].mode()[0] if len(player_df['jersey_number'].mode()) > 0 else '',
                        'total_distance': player_df['distance_covered'].max(),
                        'avg_speed': player_df['speed'].mean(),
                        'max_speed': player_df['speed'].max(),
                        'frames_with_ball': player_df['has_ball'].sum(),
                        'total_frames': len(player_df)
                    }

        except ImportError:
            print("⚠️  Pandas not available for player summary export")
            return

        # Write summary
        with open(output_path, 'w', newline='') as f:
            fieldnames = ['track_id', 'team', 'jersey_number', 'total_distance_m',
                         'avg_speed_ms', 'max_speed_ms', 'frames_with_ball', 'total_frames']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for track_id, stats in player_stats.items():
                writer.writerow({
                    'track_id': track_id,
                    'team': stats['team'],
                    'jersey_number': stats['jersey_number'],
                    'total_distance_m': f"{stats['total_distance']:.2f}",
                    'avg_speed_ms': f"{stats['avg_speed']:.2f}",
                    'max_speed_ms': f"{stats['max_speed']:.2f}",
                    'frames_with_ball': stats['frames_with_ball'],
                    'total_frames': stats['total_frames']
                })

        print(f"✓ Player summary exported: {output_path}")
