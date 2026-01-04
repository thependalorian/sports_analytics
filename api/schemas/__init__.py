"""
API Schemas Package
Location: /api/schemas/
Purpose: Pydantic models for request/response validation
"""

from .auth import *
from .match import *
from .player import *
from .team import *
from .tournament import *
from .scouting import *
from .payment import *
from .notification import *
from .sync import *
from .user import *
from .settings import *

__all__ = [
    # Auth schemas
    'UserRegister',
    'UserLogin',
    'TokenResponse',
    'RefreshTokenRequest',
    # Match schemas
    'MatchCreate',
    'MatchUpdate',
    'MatchResponse',
    'MatchListResponse',
    # Player schemas
    'PlayerCreate',
    'PlayerUpdate',
    'PlayerResponse',
    'PlayerListResponse',
    'PlayerStatisticsResponse',
    # Team schemas
    'TeamCreate',
    'TeamUpdate',
    'TeamResponse',
    'TeamListResponse',
    # Tournament schemas
    'TournamentCreate',
    'TournamentUpdate',
    'TournamentResponse',
    'TournamentListResponse',
    # Scouting schemas
    'ScoutingReportCreate',
    'ScoutingReportUpdate',
    'ScoutingReportResponse',
    'ScoutingSearchRequest',
    # Payment schemas
    'PaymentInitiate',
    'PaymentResponse',
    'PaymentListResponse',
    # Notification schemas
    'NotificationSend',
    'NotificationResponse',
    'NotificationListResponse',
    # Sync schemas
    'SyncRequest',
    'SyncResponse',
    'SyncUploadRequest',
    # User schemas
    'UserProfileResponse',
    'UserProfileUpdate',
    'PasswordChange',
    # Settings schemas
    'UserSettingsResponse',
    'UserSettingsUpdate',
]

