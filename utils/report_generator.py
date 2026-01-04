"""
Report Generator Module
Generates human-readable text reports from statistics
"""

import os


class StatisticsReportGenerator:
    """Generates text reports from statistics"""
    
    @staticmethod
    def generate_report(player_stats, team_stats, output_path):
        """
        Generate a comprehensive statistics report
        
        Args:
            player_stats: Dictionary of player statistics
            team_stats: Dictionary of team statistics
            output_path: Output file path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            # Header
            f.write("=" * 60 + "\n")
            f.write("STATISTICS REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Team Statistics
            f.write("TEAM STATISTICS\n")
            f.write("-" * 30 + "\n")
            
            for team, stats in sorted(team_stats.items()):
                f.write(f"\nTeam {team}:\n")
                f.write(f"  Players: {stats['num_players']}\n")
                f.write(f"  Total Distance: {stats['total_distance_m']:.1f}m\n")
                f.write(f"  Avg Speed: {stats['avg_speed_kmh']:.1f} km/h\n")
                if 'total_time_with_ball_sec' in stats:
                    f.write(f"  Time with Ball: {stats['total_time_with_ball_sec']:.1f}s\n")
            
            # Top Players
            f.write("\n\nTOP PLAYERS BY DISTANCE\n")
            f.write("-" * 30 + "\n")
            
            sorted_players = sorted(
                player_stats.values(),
                key=lambda x: x['total_distance_m'],
                reverse=True
            )[:10]
            
            for i, player in enumerate(sorted_players, 1):
                track_id = player['track_id']
                team = player['team']
                distance = player['total_distance_m']
                f.write(f"{i}. #{track_id} (Team {team}): {distance:.1f}m\n")
            
            # Top Players by Speed
            f.write("\n\nTOP PLAYERS BY MAX SPEED\n")
            f.write("-" * 30 + "\n")
            
            sorted_by_speed = sorted(
                player_stats.values(),
                key=lambda x: x.get('max_speed_kmh', 0),
                reverse=True
            )[:10]
            
            for i, player in enumerate(sorted_by_speed, 1):
                track_id = player['track_id']
                team = player['team']
                speed = player.get('max_speed_kmh', 0)
                f.write(f"{i}. #{track_id} (Team {team}): {speed:.1f} km/h\n")
            
            # Top Players by Ball Possession
            f.write("\n\nTOP PLAYERS BY BALL POSSESSION\n")
            f.write("-" * 30 + "\n")
            
            sorted_by_ball = sorted(
                player_stats.values(),
                key=lambda x: x.get('time_with_ball_sec', 0),
                reverse=True
            )[:10]
            
            for i, player in enumerate(sorted_by_ball, 1):
                track_id = player['track_id']
                team = player['team']
                time_ball = player.get('time_with_ball_sec', 0)
                f.write(f"{i}. #{track_id} (Team {team}): {time_ball:.1f}s\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 60 + "\n")
        
        print(f"✓ Statistics report generated: {output_path}")

