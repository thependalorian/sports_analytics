"""
API Routers Package
Location: /api/routers/
Purpose: FastAPI route handlers for all endpoints
"""

from . import auth
from . import matches
from . import players
from . import teams
from . import tournaments
from . import scouting
from . import payments
from . import notifications
from . import sync
from . import user
from . import settings
from . import unam
from . import analytics
from . import export

__all__ = [
    'auth',
    'matches',
    'players',
    'teams',
    'tournaments',
    'scouting',
    'payments',
    'notifications',
    'sync',
    'user',
    'settings',
    'unam',
    'analytics',
    'export',
]

