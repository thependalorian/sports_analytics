"""
Pass Detector Module
Detects and analyzes passes between players
"""

import numpy as np
import csv
import os
from collections import defaultdict


class PassDetector:
    """
    Detects passes using ball possession changes and player proximity
    """

    def __init__(self, min_possession_frames=5, max_pass_distance=50):
        """
        Initialize pass detector

        Args:
            min_possession_frames: Minimum frames to confirm possession
            max_pass_distance: Maximum distance for valid pass (meters)
        """
        self.min_possession_frames = min_possession_frames
        self.max_pass_distance = max_pass_distance

        # Pass tracking
        self.passes = []
        self.current_possession = {
            'player_id': None,
            'team': None,
            'start_frame': None,
            'frames_held': 0
        }

        # Statistics
        self.team_passes = defaultdict(int)
        self.player_passes = defaultdict(int)
        self.successful_passes = defaultdict(int)
        self.failed_passes = defaultdict(int)

    def process_frame(self, frame_num, tracks, current_team):
        """
        Process a single frame for pass detection

        Args:
            frame_num: Current frame number
            tracks: Tracking data for current frame
            current_team: Team currently in possession
        """
        # Get player with ball
        player_with_ball = None
        ball_position = None

        if tracks.get('ball') and len(tracks['ball']) > 0:
            ball_data = tracks['ball'][0].get(1, {})
            ball_position = ball_data.get('position', None)

        if tracks.get('players') and len(tracks['players']) > 0:
            for player_id, player_data in tracks['players'][0].items():
                if player_data.get('has_ball', False):
                    player_with_ball = player_id
                    break

        # Update possession tracking
        if player_with_ball is not None:
            if self.current_possession['player_id'] == player_with_ball:
                # Same player still has ball
                self.current_possession['frames_held'] += 1
            else:
                # Possession changed
                prev_player = self.current_possession['player_id']
                prev_team = self.current_possession['team']
                frames_held = self.current_possession['frames_held']

                if prev_player is not None and frames_held >= self.min_possession_frames:
                    # Valid possession detected, check for pass
                    self._detect_pass(frame_num, prev_player, prev_team,
                                     player_with_ball, current_team, tracks)

                # Update current possession
                self.current_possession = {
                    'player_id': player_with_ball,
                    'team': current_team,
                    'start_frame': frame_num,
                    'frames_held': 1
                }

    def _detect_pass(self, frame_num, from_player, from_team, to_player, to_team, tracks):
        """
        Detect and record a pass

        Args:
            frame_num: Current frame number
            from_player: Player ID who passed
            from_team: Team of passer
            to_player: Player ID who received
            to_team: Team of receiver
            tracks: Current tracking data
        """
        # Get player positions
        players = tracks.get('players', [{}])[0]

        from_data = None
        to_data = None

        # Find player data (may need to look back a few frames)
        for player_id, player_data in players.items():
            if player_id == from_player:
                from_data = player_data
            if player_id == to_player:
                to_data = player_data

        if from_data is None or to_data is None:
            return

        from_pos = from_data.get('position_transformed', from_data.get('position', [0, 0]))
        to_pos = to_data.get('position_transformed', to_data.get('position', [0, 0]))

        # Calculate pass distance
        distance = np.linalg.norm(np.array(from_pos) - np.array(to_pos))

        # Check if valid pass distance
        if distance > self.max_pass_distance:
            return

        # Determine if pass was successful (same team)
        successful = (from_team == to_team)

        # Record pass
        pass_info = {
            'frame': frame_num,
            'from_player': from_player,
            'to_player': to_player,
            'from_team': from_team,
            'to_team': to_team,
            'from_position': from_pos,
            'to_position': to_pos,
            'distance': distance,
            'successful': successful,
            'from_jersey': from_data.get('jersey_number', ''),
            'to_jersey': to_data.get('jersey_number', '')
        }

        self.passes.append(pass_info)

        # Update statistics
        self.team_passes[from_team] += 1
        self.player_passes[from_player] += 1

        if successful:
            self.successful_passes[from_team] += 1
        else:
            self.failed_passes[from_team] += 1

    def export_passes_csv(self, output_path):
        """
        Export passes to CSV

        Args:
            output_path: CSV output path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='') as f:
            fieldnames = ['frame', 'from_player', 'to_player', 'from_team', 'to_team',
                         'from_jersey', 'to_jersey', 'distance', 'successful']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for pass_info in self.passes:
                writer.writerow({
                    'frame': pass_info['frame'],
                    'from_player': pass_info['from_player'],
                    'to_player': pass_info['to_player'],
                    'from_team': pass_info['from_team'],
                    'to_team': pass_info['to_team'],
                    'from_jersey': pass_info['from_jersey'],
                    'to_jersey': pass_info['to_jersey'],
                    'distance': f"{pass_info['distance']:.2f}",
                    'successful': pass_info['successful']
                })

        print(f"✓ Passes exported: {output_path} ({len(self.passes)} passes)")

    def get_pass_statistics(self):
        """
        Get pass statistics summary

        Returns:
            Dictionary with pass statistics
        """
        stats = {
            'total_passes': len(self.passes),
            'team1_passes': self.team_passes.get(1, 0),
            'team2_passes': self.team_passes.get(2, 0),
            'team1_successful': self.successful_passes.get(1, 0),
            'team2_successful': self.successful_passes.get(2, 0),
            'team1_accuracy': 0.0,
            'team2_accuracy': 0.0,
            'avg_pass_distance': 0.0
        }

        if stats['team1_passes'] > 0:
            stats['team1_accuracy'] = (stats['team1_successful'] / stats['team1_passes']) * 100

        if stats['team2_passes'] > 0:
            stats['team2_accuracy'] = (stats['team2_successful'] / stats['team2_passes']) * 100

        if len(self.passes) > 0:
            stats['avg_pass_distance'] = np.mean([p['distance'] for p in self.passes])

        return stats

    def get_player_pass_network(self, team):
        """
        Get pass network for a specific team

        Args:
            team: Team number (1 or 2)

        Returns:
            Dictionary mapping (from_player, to_player) -> pass_count
        """
        network = defaultdict(int)

        for pass_info in self.passes:
            if pass_info['from_team'] == team and pass_info['successful']:
                key = (pass_info['from_player'], pass_info['to_player'])
                network[key] += 1

        return dict(network)
