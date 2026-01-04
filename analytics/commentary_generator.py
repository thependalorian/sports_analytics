"""
Commentary Generator Module
Location: /analytics/commentary_generator.py
Purpose: Generates automated match commentary based on events and tracking data
Modular design for natural language generation from analytics
"""

import csv
import os
from collections import deque


class CommentaryGenerator:
    """
    Generates natural language commentary for match events
    Football-focused: possession changes, passes, sprints, clusters, tactical insights
    """

    def __init__(self, fps=30):
        """
        Initialize commentary generator

        Args:
            fps: Video frames per second (default: 30)
        """
        self.fps = fps
        self.commentary_log = []

        # Recent events buffer to avoid repetition
        self.recent_events = deque(maxlen=10)

        # Possession tracking
        self.possession_start_frame = None
        self.current_possession_team = None
        self.last_commentary_frame = -100
    
    def generate_commentary(self, tracks, events, pass_stats, fps=30):
        """
        Generate complete match commentary from tracking data and events
        
        Args:
            tracks: Complete tracking dictionary
            events: List of detected events
            pass_stats: Pass statistics dictionary
            fps: Frames per second
            
        Returns:
            List of commentary entries
        """
        self.fps = fps
        self.commentary_log = []
        
        # Add events commentary
        for event in events:
            if event['event_type'] == 'sprint':
                player_label = event.get('player_label', f"Player {event['player_id']}")
                team = event.get('team', 0)
                speed = event.get('speed', 0)
                self.add_event_commentary(
                    event['frame'],
                    'sprint',
                    team,
                    f"⚡ {player_label} (Team {team}) sprinting at {speed:.1f} m/s ({speed * 3.6:.1f} km/h)"
                )
            
            elif event['event_type'] == 'cluster':
                player_count = event.get('player_count', 0)
                self.add_event_commentary(
                    event['frame'],
                    'cluster',
                    None,
                    f"👥 Player cluster detected: {player_count} players within 5m (potential set piece)"
                )
            
            elif event['event_type'] == 'trajectory_change':
                angle = event.get('angle_change', 0)
                self.add_event_commentary(
                    event['frame'],
                    'trajectory_change',
                    None,
                    f"⚽ Ball trajectory change: {angle:.0f}° (potential shot or clearance)"
                )
        
        # Add pass summary commentary
        if pass_stats['total_passes'] > 0:
            self.add_event_commentary(
                0,
                'match_summary',
                None,
                f"📊 Match Summary: {pass_stats['total_passes']} total passes detected"
            )
            self.add_event_commentary(
                10,
                'match_summary',
                1,
                f"Team 1: {pass_stats['team1_passes']} passes ({pass_stats['team1_accuracy']:.1f}% accuracy)"
            )
            self.add_event_commentary(
                20,
                'match_summary',
                2,
                f"Team 2: {pass_stats['team2_passes']} passes ({pass_stats['team2_accuracy']:.1f}% accuracy)"
            )
        
        return self.commentary_log

    def process_frame(self, frame_num, tracks, current_team):
        """
        Process frame and generate commentary if appropriate

        Args:
            frame_num: Current frame number
            tracks: Tracking data
            current_team: Team currently in possession
        """
        # Check for possession change
        if self.current_possession_team != current_team:
            if self.current_possession_team is not None:
                self._generate_possession_change_commentary(frame_num, current_team)

            self.current_possession_team = current_team
            self.possession_start_frame = frame_num

        # Check for long possession
        if self.possession_start_frame is not None:
            frames_since_possession = frame_num - self.possession_start_frame
            seconds_possession = frames_since_possession / self.fps

            # Commentary every 10 seconds of possession
            if seconds_possession > 0 and int(seconds_possession) % 10 == 0:
                if frame_num - self.last_commentary_frame > self.fps * 5:  # Don't spam
                    self._generate_possession_commentary(frame_num, current_team, seconds_possession)
                    self.last_commentary_frame = frame_num

    def _generate_possession_change_commentary(self, frame_num, new_team):
        """Generate commentary for possession change"""
        time_str = self._frame_to_time_string(frame_num)

        commentary_options = [
            f"{time_str} - Ball possession changes to Team {new_team}!",
            f"{time_str} - Team {new_team} wins the ball!",
            f"{time_str} - Possession switches to Team {new_team}",
            f"{time_str} - Team {new_team} now in control",
        ]

        # Avoid recent duplicates
        for comment in commentary_options:
            if comment not in self.recent_events:
                self.commentary_log.append({
                    'frame': frame_num,
                    'time': time_str,
                    'event_type': 'possession_change',
                    'team': new_team,
                    'commentary': comment
                })
                self.recent_events.append(comment)
                break

    def _generate_possession_commentary(self, frame_num, team, seconds):
        """Generate commentary for sustained possession"""
        time_str = self._frame_to_time_string(frame_num)

        commentary = f"{time_str} - Team {team} maintains possession for {int(seconds)} seconds"

        self.commentary_log.append({
            'frame': frame_num,
            'time': time_str,
            'event_type': 'possession_sustained',
            'team': team,
            'commentary': commentary
        })

    def add_pass_commentary(self, frame_num, pass_info):
        """
        Add commentary for a pass

        Args:
            frame_num: Frame number
            pass_info: Pass information dictionary
        """
        time_str = self._frame_to_time_string(frame_num)

        from_jersey = pass_info.get('from_jersey', '')
        to_jersey = pass_info.get('to_jersey', '')

        from_label = f"#{from_jersey}" if from_jersey else f"Player {pass_info['from_player']}"
        to_label = f"#{to_jersey}" if to_jersey else f"Player {pass_info['to_player']}"

        if pass_info['successful']:
            commentary = f"{time_str} - {from_label} passes to {to_label} ({pass_info['distance']:.1f}m)"
        else:
            commentary = f"{time_str} - {from_label} loses possession to Team {pass_info['to_team']}"

        self.commentary_log.append({
            'frame': frame_num,
            'time': time_str,
            'event_type': 'pass',
            'team': pass_info['from_team'],
            'commentary': commentary
        })

    def add_event_commentary(self, frame_num, event_type, team, description):
        """
        Add commentary for a detected event

        Args:
            frame_num: Frame number
            event_type: Type of event
            team: Team involved
            description: Event description
        """
        time_str = self._frame_to_time_string(frame_num)

        commentary = f"{time_str} - {description}"

        self.commentary_log.append({
            'frame': frame_num,
            'time': time_str,
            'event_type': event_type,
            'team': team,
            'commentary': commentary
        })

    def _frame_to_time_string(self, frame_num):
        """Convert frame number to MM:SS time string"""
        total_seconds = frame_num / self.fps
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def export_commentary_csv(self, output_path):
        """
        Export commentary to CSV

        Args:
            output_path: CSV output path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['frame', 'time', 'event_type', 'team', 'commentary']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.commentary_log)

        print(f"✓ Commentary exported: {output_path} ({len(self.commentary_log)} entries)")

    def export_match_report(self, output_path, match_stats, pass_stats):
        """
        Export a full match report with commentary and statistics

        Args:
            output_path: Text file output path
            match_stats: Match statistics dictionary
            pass_stats: Pass statistics dictionary
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(" " * 25 + "MATCH REPORT\n")
            f.write("=" * 80 + "\n\n")

            # Match Statistics
            f.write("MATCH STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Team 1 Possession: {match_stats.get('team1_possession_pct', 0):.1f}%\n")
            f.write(f"Team 2 Possession: {match_stats.get('team2_possession_pct', 0):.1f}%\n\n")

            f.write(f"Team 1 Passes: {pass_stats.get('team1_passes', 0)} "
                   f"({pass_stats.get('team1_accuracy', 0):.1f}% accuracy)\n")
            f.write(f"Team 2 Passes: {pass_stats.get('team2_passes', 0)} "
                   f"({pass_stats.get('team2_accuracy', 0):.1f}% accuracy)\n\n")

            f.write(f"Average Pass Distance: {pass_stats.get('avg_pass_distance', 0):.1f}m\n\n")

            # Match Commentary
            f.write("\nMATCH COMMENTARY\n")
            f.write("-" * 80 + "\n")

            for entry in self.commentary_log:
                f.write(f"{entry['commentary']}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write(" " * 25 + "END OF REPORT\n")
            f.write("=" * 80 + "\n")

        print(f"✓ Match report exported: {output_path}")
