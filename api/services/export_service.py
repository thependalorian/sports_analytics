"""
Export Service
Location: /api/services/export_service.py
Purpose: Business logic for data export (CSV, JSON, PDF)
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List
from uuid import UUID
import csv
import json
from io import StringIO, BytesIO
from datetime import datetime

from api.models.match import Match
from api.models.player import PlayerStatistics
from api.models.pass_model import Pass
from api.models.event import Event
from utils.logger import get_logger

logger = get_logger(__name__)

class ExportService:
    """Export service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def export_csv(
        self,
        match_id: UUID,
        export_type: str = "all",
        format: str = "standard"
    ) -> BytesIO:
        """Export match data as CSV"""
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        output = StringIO()
        writer = csv.writer(output)
        
        if export_type in ["players", "all"]:
            # Export player statistics
            players = self.db.query(PlayerStatistics).filter(
                PlayerStatistics.match_id == match_id
            ).all()
            
            writer.writerow([
                "Player ID", "Jersey Number", "Team", "Distance (m)", "Avg Speed (km/h)",
                "Max Speed (km/h)", "Passes Made", "Passes Received", "Pass Accuracy (%)"
            ])
            
            for player_stat in players:
                writer.writerow([
                    str(player_stat.player_id),
                    player_stat.track_id,
                    player_stat.team,
                    player_stat.total_distance_m,
                    player_stat.avg_speed_kmh,
                    player_stat.max_speed_kmh,
                    player_stat.passes_made,
                    player_stat.passes_received,
                    player_stat.pass_accuracy_pct
                ])
        
        if export_type in ["passes", "all"]:
            # Export passes
            passes = self.db.query(Pass).filter(Pass.match_id == match_id).all()
            
            writer.writerow([
                "Pass ID", "From Player", "To Player", "Frame", "Distance (m)", "Successful"
            ])
            
            for pass_obj in passes:
                writer.writerow([
                    str(pass_obj.id),
                    pass_obj.from_jersey,
                    pass_obj.to_jersey,
                    pass_obj.frame,
                    pass_obj.distance_m,
                    pass_obj.successful
                ])
        
        # Convert to BytesIO
        output.seek(0)
        bytes_output = BytesIO()
        bytes_output.write(output.getvalue().encode('utf-8'))
        bytes_output.seek(0)
        
        return bytes_output
    
    def export_json(
        self,
        match_id: UUID,
        include: List[str] = None
    ) -> Dict[str, Any]:
        """Export match data as JSON"""
        if include is None:
            include = ["tracking", "players", "teams", "passes", "events"]
        
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        result = {}
        
        if "match" in include or "tracking" in include:
            result["match"] = {
                "id": str(match.id),
                "name": match.name,
                "sport": match.sport_id,
                "date": match.date.isoformat(),
                "status": match.status
            }
        
        if "players" in include:
            players = self.db.query(PlayerStatistics).filter(
                PlayerStatistics.match_id == match_id
            ).all()
            result["players"] = [
                {
                    "player_id": str(p.player_id),
                    "jersey_number": p.track_id,
                    "team": p.team,
                    "stats": {
                        "distance_m": p.total_distance_m,
                        "avg_speed_kmh": p.avg_speed_kmh,
                        "passes_made": p.passes_made
                    }
                }
                for p in players
            ]
        
        if "passes" in include:
            passes = self.db.query(Pass).filter(Pass.match_id == match_id).all()
            result["passes"] = [
                {
                    "id": str(p.id),
                    "from_player": p.from_jersey,
                    "to_player": p.to_jersey,
                    "frame": p.frame,
                    "distance_m": p.distance_m,
                    "successful": p.successful
                }
                for p in passes
            ]
        
        if "events" in include:
            events = self.db.query(Event).filter(Event.match_id == match_id).all()
            result["events"] = [
                {
                    "id": str(e.id),
                    "player": e.jersey_number,
                    "event_type": e.event_type,
                    "frame": e.frame,
                    "timestamp": e.timestamp
                }
                for e in events
            ]
        
        return result
    
    def export_pdf(
        self,
        match_id: UUID,
        sections: List[str] = None
    ) -> BytesIO:
        """Export match report as PDF"""
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        logger.info(f"Generating PDF report for match {match_id}")
        
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        # Create PDF buffer
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph(f"Match Report: {match.name}", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Match details
        if "overview" in (sections or ["overview"]):
            story.append(Paragraph("Match Overview", styles['Heading2']))
            match_data = [
                ["Date", match.date.strftime("%Y-%m-%d %H:%M") if match.date else "N/A"],
                ["Sport", match.sport_id],
                ["Team 1", match.team1_name or "N/A"],
                ["Team 2", match.team2_name or "N/A"],
                ["Score", f"{match.score_team1 or 0} - {match.score_team2 or 0}"],
                ["Status", match.status],
                ["Venue", match.venue or "N/A"]
            ]
            match_table = Table(match_data, colWidths=[2*inch, 4*inch])
            match_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(match_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Player statistics
        if "players" in (sections or ["players"]):
            story.append(Paragraph("Player Statistics", styles['Heading2']))
            players = self.db.query(PlayerStatistics).filter(
                PlayerStatistics.match_id == match_id
            ).limit(20).all()
            
            if players:
                player_data = [["Jersey", "Team", "Distance (km)", "Avg Speed (km/h)", "Passes Made"]]
                for p in players:
                    player_data.append([
                        str(p.track_id or "N/A"),
                        str(p.team or "N/A"),
                        f"{(p.total_distance_m or 0) / 1000:.1f}",
                        f"{p.avg_speed_kmh or 0:.1f}",
                        str(p.passes_made or 0)
                    ])
                
                player_table = Table(player_data, colWidths=[0.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1*inch])
                player_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(player_table)
                story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        
        logger.info(f"PDF report generated for match {match_id}")
        return pdf_buffer

