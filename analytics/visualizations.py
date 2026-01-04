"""
Visualization Generator Module
Generates pass networks, zone statistics, and other visual analytics
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from collections import defaultdict


class VisualizationGenerator:
    """
    Generates various analytical visualizations
    """

    def __init__(self, field_dims=(105, 68)):
        """
        Initialize visualization generator

        Args:
            field_dims: Field dimensions in meters (length, width)
        """
        self.field_length, self.field_width = field_dims

    def generate_pass_network(self, passes, output_path, team=1):
        """
        Generate pass network visualization

        Args:
            passes: List of pass dictionaries
            output_path: Path to save visualization
            team: Team number to visualize
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Filter passes for this team
        team_passes = [p for p in passes if p['from_team'] == team and p['successful']]

        if len(team_passes) == 0:
            print(f"⚠️  No passes found for Team {team}")
            return

        # Calculate player positions (average position during passes)
        player_positions = defaultdict(list)
        player_labels = {}

        for pass_info in team_passes:
            from_id = pass_info['from_player']
            to_id = pass_info['to_player']

            player_positions[from_id].append(pass_info['from_position'])
            player_positions[to_id].append(pass_info['to_position'])

            player_labels[from_id] = pass_info.get('from_jersey', f'P{from_id}')
            player_labels[to_id] = pass_info.get('to_jersey', f'P{to_id}')

        # Average positions
        avg_positions = {}
        for player_id, positions in player_positions.items():
            avg_positions[player_id] = np.mean(positions, axis=0)

        # Count passes between players
        pass_counts = defaultdict(int)
        for pass_info in team_passes:
            key = (pass_info['from_player'], pass_info['to_player'])
            pass_counts[key] += 1

        # Create visualization
        fig, ax = plt.subplots(figsize=(14, 9))
        self._draw_field(ax)

        # Draw pass connections
        max_passes = max(pass_counts.values()) if pass_counts else 1

        for (from_id, to_id), count in pass_counts.items():
            if from_id in avg_positions and to_id in avg_positions:
                from_pos = avg_positions[from_id]
                to_pos = avg_positions[to_id]

                # Line width based on pass frequency
                line_width = 0.5 + (count / max_passes) * 4

                ax.plot([from_pos[0], to_pos[0]],
                       [from_pos[1], to_pos[1]],
                       'b-', alpha=0.6, linewidth=line_width)

                # Arrow for direction
                dx = to_pos[0] - from_pos[0]
                dy = to_pos[1] - from_pos[1]
                ax.arrow(from_pos[0] + dx*0.4, from_pos[1] + dy*0.4,
                        dx*0.2, dy*0.2,
                        head_width=2, head_length=1.5, fc='blue', ec='blue', alpha=0.5)

        # Draw player nodes
        for player_id, pos in avg_positions.items():
            # Node size based on pass involvement
            total_passes = sum(count for (from_id, to_id), count in pass_counts.items()
                             if from_id == player_id or to_id == player_id)

            node_size = 100 + total_passes * 20

            ax.scatter(pos[0], pos[1], s=node_size, c='red', zorder=10,
                      edgecolors='white', linewidths=2, alpha=0.8)

            label = player_labels.get(player_id, f'P{player_id}')
            ax.text(pos[0], pos[1], str(label), ha='center', va='center',
                   fontsize=10, fontweight='bold', color='white', zorder=11)

        ax.set_title(f'Team {team} Pass Network', fontsize=16, fontweight='bold')
        ax.set_xlim(0, self.field_length)
        ax.set_ylim(0, self.field_width)
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Pass network generated: {output_path}")

    def generate_zone_statistics(self, tracks, output_path, team=1, zones=(3, 3)):
        """
        Generate field zone statistics visualization

        Args:
            tracks: Player tracking data
            output_path: Path to save visualization
            team: Team number to analyze
            zones: Grid dimensions (rows, cols)
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        rows, cols = zones
        zone_width = self.field_length / cols
        zone_height = self.field_width / rows

        # Count player presence in each zone
        zone_counts = np.zeros((rows, cols))

        for frame_tracks in tracks.get('players', []):
            for player_id, player_data in frame_tracks.items():
                if player_data.get('team') == team:
                    pos = player_data.get('position_transformed', player_data.get('position', None))

                    if pos:
                        x, y = pos

                        # Calculate zone indices
                        col_idx = int(x / zone_width)
                        row_idx = int(y / zone_height)

                        if 0 <= col_idx < cols and 0 <= row_idx < rows:
                            zone_counts[row_idx, col_idx] += 1

        # Create visualization
        fig, ax = plt.subplots(figsize=(14, 9))
        self._draw_field(ax)

        # Normalize counts
        if zone_counts.max() > 0:
            zone_counts_norm = zone_counts / zone_counts.max()
        else:
            zone_counts_norm = zone_counts

        # Draw zones
        for row in range(rows):
            for col in range(cols):
                x1 = col * zone_width
                y1 = row * zone_height

                intensity = zone_counts_norm[row, col]

                if intensity > 0:
                    rect = patches.Rectangle((x1, y1), zone_width, zone_height,
                                            linewidth=2, edgecolor='white',
                                            facecolor='red', alpha=intensity * 0.7)
                    ax.add_patch(rect)

                    # Add count text
                    count = int(zone_counts[row, col])
                    if count > 0:
                        ax.text(x1 + zone_width/2, y1 + zone_height/2,
                               str(count), ha='center', va='center',
                               fontsize=14, fontweight='bold', color='white')

        ax.set_title(f'Team {team} Field Zone Activity', fontsize=16, fontweight='bold')
        ax.set_xlim(0, self.field_length)
        ax.set_ylim(0, self.field_width)
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✓ Zone statistics generated: {output_path}")

    def _draw_field(self, ax):
        """
        Draw football field markings

        Args:
            ax: Matplotlib axes
        """
        # Field outline
        ax.plot([0, self.field_length, self.field_length, 0, 0],
               [0, 0, self.field_width, self.field_width, 0],
               'white', linewidth=2)

        # Halfway line
        ax.plot([self.field_length/2, self.field_length/2],
               [0, self.field_width],
               'white', linewidth=2)

        # Center circle
        center_circle = plt.Circle((self.field_length/2, self.field_width/2),
                                   9.15, fill=False, color='white', linewidth=2)
        ax.add_patch(center_circle)

        # Center spot
        ax.plot(self.field_length/2, self.field_width/2, 'wo', markersize=4)

        # Penalty areas
        penalty_length = 16.5
        penalty_width = 40.3

        # Left penalty area
        ax.plot([0, penalty_length, penalty_length, 0],
               [(self.field_width - penalty_width)/2,
                (self.field_width - penalty_width)/2,
                (self.field_width + penalty_width)/2,
                (self.field_width + penalty_width)/2],
               'white', linewidth=2)

        # Right penalty area
        ax.plot([self.field_length - penalty_length, self.field_length,
                self.field_length, self.field_length - penalty_length],
               [(self.field_width - penalty_width)/2,
                (self.field_width - penalty_width)/2,
                (self.field_width + penalty_width)/2,
                (self.field_width + penalty_width)/2],
               'white', linewidth=2)

        # Goal areas
        goal_length = 5.5
        goal_width = 18.3

        # Left goal area
        ax.plot([0, goal_length, goal_length, 0],
               [(self.field_width - goal_width)/2,
                (self.field_width - goal_width)/2,
                (self.field_width + goal_width)/2,
                (self.field_width + goal_width)/2],
               'white', linewidth=2)

        # Right goal area
        ax.plot([self.field_length - goal_length, self.field_length,
                self.field_length, self.field_length - goal_length],
               [(self.field_width - goal_width)/2,
                (self.field_width - goal_width)/2,
                (self.field_width + goal_width)/2,
                (self.field_width + goal_width)/2],
               'white', linewidth=2)

        # Set field appearance
        ax.set_facecolor('#2e7d32')  # Green field
        ax.set_xlabel('Length (m)', color='white', fontsize=12)
        ax.set_ylabel('Width (m)', color='white', fontsize=12)
        ax.tick_params(colors='white')
