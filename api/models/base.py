"""
Base Model
Location: /api/models/base.py
Purpose: Base SQLAlchemy model with common fields (lazy initialization)
"""

import uuid

# Lazy initialization to avoid psycopg2 requirement at import time
_Base = None
_BaseModel = None

def _get_base():
    """Get or create SQLAlchemy Base (lazy initialization)"""
    global _Base
    if _Base is None:
        try:
            from sqlalchemy.ext.declarative import declarative_base
            _Base = declarative_base()
        except Exception as e:
            # SQLAlchemy not available - create a dummy base
            class DummyBase:
                pass
            _Base = DummyBase
    return _Base

def _get_base_model():
    """Get or create BaseModel class (lazy initialization)"""
    global _BaseModel
    if _BaseModel is None:
        try:
            from sqlalchemy import Column, DateTime, func
            from sqlalchemy.dialects.postgresql import UUID
            Base = _get_base()
            
            class BaseModelClass(Base):
                """Base model with common fields"""
                __abstract__ = True
                
                id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
                created_at = Column(DateTime, default=func.now(), nullable=False)
                updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
                deleted_at = Column(DateTime, nullable=True)
            
            _BaseModel = BaseModelClass
        except Exception:
            # SQLAlchemy not available - create a dummy class
            class DummyBaseModel:
                __abstract__ = True
            _BaseModel = DummyBaseModel
    return _BaseModel

# Create Base and BaseModel on first access
Base = _get_base()
BaseModel = _get_base_model()

