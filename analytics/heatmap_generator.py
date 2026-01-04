"""
Heatmap Generator Module
Generates heatmaps for player positions and team activity
"""

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from collections import defaultdict


class HeatmapGenerator:
    """
    Generates heatmaps from player tracking data
    """

    def __init__(self, field_dims=(105, 68), resolution=(1050, 680)):
        """
        Initialize heatmap generator

        Args:
            field_dims: Field dimensions in meters (length, width)
            resolution: Heatmap resolution in pixels
        """
        self.field_length, self.field_width = field_dims
        self.resolution = resolution

        # Heatmap grids for each team
        self.team1_heatmap = np.zeros(resolution[::-1])  # (height, width)
        self.team2_heatmap = np.zeros(resolution[::-1])
        self.all_players_heatmap = np.zeros(resolution[::-1])

        # Player-specific heatmaps
        self.player_heatmaps = defaultdict(lambda: np.zeros(resolution[::-1]))

    def accumulate_positions(self, tracks, frame_offset=0):
        """
        Accumulate player positions for heatmap generation

        Args:
            tracks: Dictionary containing player tracks
            frame_offset: Offset for global frame numbering
        """
        for frame_idx, frame_tracks in enumerate(tracks.get('players', [])):
            for track_id, player_data in frame_tracks.items():
                # Get transformed position (field coordinates)
                position = player_data.get('position_transformed', None)

                if position is None:
                    # Fallback to pixel position
                    position = player_data.get('position', None)

                if position is None:
                    continue

                # Convert position to heatmap coordinates
                x, y = self._position_to_heatmap_coords(position)

                if 0 <= x < self.resolution[0] and 0 <= y < self.resolution[1]:
                    # Add to team heatmap
                    team = player_data.get('team', 0)

                    if team == 1:
                        self.team1_heatmap[y, x] += 1
                    elif team == 2:
                        self.team2_heatmap[y, x] += 1

                    # Add to all players heatmap
                    self.all_players_heatmap[y, x] += 1

                    # Add to player-specific heatmap
                    jersey_num = player_data.get('jersey_number', f'ID_{track_id}')
                    self.player_heatmaps[f"team{team}_player{jersey_num}"][y, x] += 1

    def _position_to_heatmap_coords(self, position):
        """
        Convert field position to heatmap pixel coordinates

        Args:
            position: [x, y] in field coordinates or pixel coordinates

        Returns:
            (x, y) in heatmap coordinates
        """
        x, y = position

        # Normalize to field dimensions (assuming position is in meters)
        # If position is in pixels, we'll need to scale appropriately
        # For now, assume position is in meters from field transformation

        # Map to heatmap resolution
        heatmap_x = int((x / self.field_length) * self.resolution[0])
        heatmap_y = int((y / self.field_width) * self.resolution[1])

        return heatmap_x, heatmap_y

    def generate_heatmap_images(self, output_dir):
        """
        Generate and save heatmap images

        Args:
            output_dir: Directory to save heatmap images
        """
        os.makedirs(output_dir, exist_ok=True)

        # Apply Gaussian blur for smooth heatmaps
        kernel_size = 51
        sigma = 15

        team1_smooth = cv2.GaussianBlur(self.team1_heatmap, (kernel_size, kernel_size), sigma)
        team2_smooth = cv2.GaussianBlur(self.team2_heatmap, (kernel_size, kernel_size), sigma)
        all_smooth = cv2.GaussianBlur(self.all_players_heatmap, (kernel_size, kernel_size), sigma)

        # Normalize
        if team1_smooth.max() > 0:
            team1_smooth = team1_smooth / team1_smooth.max()
        if team2_smooth.max() > 0:
            team2_smooth = team2_smooth / team2_smooth.max()
        if all_smooth.max() > 0:
            all_smooth = all_smooth / all_smooth.max()

        # Generate team 1 heatmap
        self._save_heatmap(team1_smooth, os.path.join(output_dir, 'team1_heatmap.png'),
                          'Team 1 Position Heatmap', cmap='Reds')

        # Generate team 2 heatmap
        self._save_heatmap(team2_smooth, os.path.join(output_dir, 'team2_heatmap.png'),
                          'Team 2 Position Heatmap', cmap='Blues')

        # Generate combined heatmap
        self._save_heatmap(all_smooth, os.path.join(output_dir, 'all_players_heatmap.png'),
                          'All Players Position Heatmap', cmap='hot')

        print(f"✓ Heatmaps generated: {output_dir}")

    def _save_heatmap(self, heatmap_data, output_path, title, cmap='hot'):
        """
        Save a single heatmap image

        Args:
            heatmap_data: 2D numpy array
            output_path: Path to save image
            title: Plot title
            cmap: Matplotlib colormap
        """
        plt.figure(figsize=(12, 8))
        plt.imshow(heatmap_data, cmap=cmap, aspect='auto', origin='lower')
        plt.colorbar(label='Density')
        plt.title(title)
        plt.xlabel('Field Length (m)')
        plt.ylabel('Field Width (m)')

        # Add field markings overlay
        self._draw_field_overlay(plt.gca(), heatmap_data.shape)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()

    def _draw_field_overlay(self, ax, shape):
        """
        Draw field markings on heatmap

        Args:
            ax: Matplotlib axes
            shape: Heatmap shape (height, width)
        """
        height, width = shape

        # Field outline
        ax.plot([0, width-1, width-1, 0, 0],
               [0, 0, height-1, height-1, 0],
               'white', linewidth=2, alpha=0.5)

        # Halfway line
        ax.plot([width/2, width/2], [0, height-1], 'white', linewidth=1, alpha=0.5)

        # Center circle (approximate)
        center_x, center_y = width / 2, height / 2
        circle_radius = 9.15 * width / self.field_length  # 9.15m radius
        circle = plt.Circle((center_x, center_y), circle_radius,
                           fill=False, color='white', linewidth=1, alpha=0.5)
        ax.add_patch(circle)

    def export_team_heatmaps(self, output_dir):
        """
        Export separate heatmaps for each player

        Args:
            output_dir: Directory to save player heatmaps
        """
        player_dir = os.path.join(output_dir, 'players')
        os.makedirs(player_dir, exist_ok=True)

        for player_key, heatmap in self.player_heatmaps.items():
            if heatmap.max() > 0:
                heatmap_smooth = cv2.GaussianBlur(heatmap, (51, 51), 15)
                heatmap_norm = heatmap_smooth / heatmap_smooth.max()

                output_path = os.path.join(player_dir, f'{player_key}_heatmap.png')
                self._save_heatmap(heatmap_norm, output_path,
                                  f'{player_key} Position Heatmap', cmap='viridis')

        print(f"✓ Player heatmaps exported: {player_dir}")

    def get_heatmap_statistics(self):
        """
        Calculate heatmap statistics

        Returns:
            Dictionary with heatmap statistics
        """
        stats = {
            'team1_total_presence': np.sum(self.team1_heatmap),
            'team2_total_presence': np.sum(self.team2_heatmap),
            'team1_coverage_area': np.sum(self.team1_heatmap > 0),
            'team2_coverage_area': np.sum(self.team2_heatmap > 0),
            'team1_avg_density': np.mean(self.team1_heatmap[self.team1_heatmap > 0]) if np.any(self.team1_heatmap > 0) else 0,
            'team2_avg_density': np.mean(self.team2_heatmap[self.team2_heatmap > 0]) if np.any(self.team2_heatmap > 0) else 0,
        }
        return stats

