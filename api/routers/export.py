"""
Export Router
Location: /api/routers/export.py
Purpose: Data export endpoints (CSV, JSON, PDF)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from api.database import get_db
from api.models.match import Match
from api.services.export_service import ExportService

router = APIRouter()

@router.get("/matches/{match_id}/export/csv")
async def export_csv(
    match_id: UUID,
    type: str = Query("all", pattern="^(tracking|players|teams|passes|events|all)$"),
    format: str = Query("standard", pattern="^(standard|excel)$"),
    db: Session = Depends(get_db)
):
    """Export match data as CSV"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    service = ExportService(db)
    csv_data = service.export_csv(match_id, export_type=type, format=format)
    
    return Response(
        content=csv_data.read(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=match_{match_id}_{type}.csv"
        }
    )

@router.get("/matches/{match_id}/export/json")
async def export_json(
    match_id: UUID,
    include: Optional[str] = Query(None, description="Comma-separated: tracking,players,teams,passes,events"),
    db: Session = Depends(get_db)
):
    """Export match data as JSON"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    service = ExportService(db)
    include_list = include.split(",") if include else None
    json_data = service.export_json(match_id, include=include_list)
    
    return json_data

@router.get("/matches/{match_id}/export/pdf")
async def export_pdf(
    match_id: UUID,
    sections: Optional[str] = Query(None, description="Comma-separated: overview,players,teams,passes,events"),
    db: Session = Depends(get_db)
):
    """Export match report as PDF"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    service = ExportService(db)
    sections_list = sections.split(",") if sections else None
    pdf_data = service.export_pdf(match_id, sections=sections_list)
    
    return Response(
        content=pdf_data.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=match_{match_id}_report.pdf"
        }
    )

