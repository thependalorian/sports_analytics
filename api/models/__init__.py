"""
Database Models Package
Location: /api/models/
Purpose: SQLAlchemy database models
"""

from api.models.base import BaseModel
Base = BaseModel  # Alias for Alembic compatibility
from api.models.user import User, UserSession, UserSettings
from api.models.sport import Sport
from api.models.team import Team, TeamPlayer
from api.models.match import Match
from api.models.player import Player, PlayerStatistics
from api.models.pass_model import Pass
from api.models.event import Event
from api.models.tournament import Tournament, TournamentParticipant
from api.models.scouting import ScoutingReport
from api.models.payment import Payment
from api.models.notification import Notification
from api.models.sync import SyncQueue, SyncHistory
from api.models.unam import UNAMCampus, CampusTeam
from api.models.password_reset import PasswordResetToken

__all__ = [
    "Base",
    "User",
    "UserSession",
    "UserSettings",
    "Sport",
    "Team",
    "TeamPlayer",
    "Match",
    "Player",
    "PlayerStatistics",
    "Pass",
    "Event",
    "Tournament",
    "TournamentParticipant",
    "ScoutingReport",
    "Payment",
    "Notification",
    "SyncQueue",
    "SyncHistory",
    "UNAMCampus",
    "CampusTeam",
    "PasswordResetToken",
]

