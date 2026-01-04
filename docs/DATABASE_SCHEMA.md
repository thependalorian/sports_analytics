# Database Schema & Migrations Documentation
## Sports Analytics Web Dashboard Database

**Version:** 2.1 (Namibian Market Focus)  
**Last Updated:** January 2025  
**Primary Market:** 🇳🇦 Namibia (Africa)  
**Database:** PostgreSQL (Neon Serverless)  
**ORM:** SQLAlchemy (Python) / Prisma (TypeScript - optional)

**Related Documentation:**
- [API Documentation](API_DOCUMENTATION.md) - API endpoints and data structures
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - TypeScript type definitions
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [Architecture Documentation](architecture.md) - System architecture

---

## Table of Contents

1. [Database Overview](#database-overview)
2. [Migration Strategy](#migration-strategy)
3. [Complete Schema](#complete-schema)
4. [Type Definitions](#type-definitions)
5. [Indexes & Performance](#indexes--performance)
6. [Data Relationships](#data-relationships)
7. [Multi-Sport Support](#multi-sport-support)
8. [Namibian Market Extensions](#namibian-market-extensions)

---

## Database Overview

### Technology Stack
- **Database:** PostgreSQL 15+ (Neon Serverless)
- **Connection Pooling:** Neon HTTP driver for serverless
- **Migrations:** Alembic (Python) or Prisma Migrate (TypeScript)
- **Backup:** Hourly incremental, daily full (Cape Town replica)
- **Replication:** Real-time streaming to Cape Town backup

### Database Design Principles
1. **Multi-Sport Support:** Sport-agnostic schema with sport-specific extensions
2. **Offline-First:** Sync timestamps and conflict resolution fields
3. **Scalability:** UUID primary keys, proper indexing
4. **Data Integrity:** Foreign keys, constraints, check constraints
5. **Audit Trail:** Created/updated timestamps on all tables
6. **Soft Deletes:** `deleted_at` for data retention

---

## Migration Strategy

### Migration File Structure

```
backend/
├── migrations/
│   ├── versions/
│   │   ├── 001_initial_schema.py
│   │   ├── 002_add_multi_sport_support.py
│   │   ├── 003_add_tournaments.py
│   │   ├── 004_add_scouting.py
│   │   ├── 005_add_payments_namibian.py
│   │   ├── 006_add_notifications.py
│   │   ├── 007_add_unam_campuses.py
│   │   ├── 008_add_offline_sync.py
│   │   └── 009_add_indexes_performance.py
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
└── app/
    ├── models/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── user.py
    │   ├── match.py
    │   ├── player.py
    │   ├── team.py
    │   ├── tournament.py
    │   ├── scouting.py
    │   ├── payment.py
    │   ├── notification.py
    │   └── sync.py
```

### Migration Commands

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current version
alembic current

# View migration history
alembic history
```

### Migration Best Practices
1. **Always test migrations** on staging before production
2. **Backup database** before major migrations
3. **Use transactions** for data migrations
4. **Add indexes** in separate migrations for large tables
5. **Document breaking changes** in migration comments

---

## Complete Schema

### Core Tables

#### 1. Users & Authentication

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone_number VARCHAR(20),
    organization VARCHAR(255), -- 'UNAM', 'MTC', 'NFA', etc.
    campus VARCHAR(100), -- For UNAM: 'Windhoek Main', 'Oshakati', etc.
    avatar_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    language VARCHAR(10) DEFAULT 'en', -- 'en', 'af', 'osh'
    timezone VARCHAR(50) DEFAULT 'Africa/Windhoek',
    subscription_plan VARCHAR(50) DEFAULT 'free', -- 'free', 'university', 'pro', 'enterprise'
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_organization ON users(organization);
CREATE INDEX idx_users_campus ON users(campus);
CREATE INDEX idx_users_active ON users(is_active) WHERE deleted_at IS NULL;

-- User sessions (for JWT refresh tokens)
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(500) UNIQUE NOT NULL,
    device_info JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);
```

#### 2. Sports & Multi-Sport Support

```sql
-- Sports configuration
CREATE TABLE sports (
    id VARCHAR(50) PRIMARY KEY, -- 'football', 'basketball', 'rugby', etc.
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50), -- Emoji or icon identifier
    field_type VARCHAR(50), -- 'rectangular', 'court', 'pitch', 'track'
    field_width FLOAT,
    field_height FLOAT,
    field_unit VARCHAR(10), -- 'meters', 'yards'
    max_players INTEGER,
    config JSONB, -- Full SportConfig JSON
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sports (id, name, icon, field_type, field_width, field_height, field_unit, max_players) VALUES
('football', 'Football', '⚽', 'rectangular', 105, 68, 'meters', 22),
('basketball', 'Basketball', '🏀', 'court', 28, 15, 'meters', 10),
('rugby', 'Rugby', '🏉', 'rectangular', 100, 70, 'meters', 30),
('netball', 'Netball', '🏐', 'court', 30.5, 15.25, 'meters', 14),
('hockey', 'Field Hockey', '🏑', 'rectangular', 91.4, 55, 'meters', 22),
('cricket', 'Cricket', '🏏', 'oval', 137.16, 137.16, 'meters', 22),
('tennis', 'Tennis', '🎾', 'court', 23.77, 10.97, 'meters', 4),
('volleyball', 'Volleyball', '🏐', 'court', 18, 9, 'meters', 12);
```

#### 3. Teams

```sql
-- Teams table
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sport_id VARCHAR(50) NOT NULL REFERENCES sports(id),
    competition VARCHAR(255), -- 'Debmarine Namibia Premiership', 'MTC Maris Cup', etc.
    location VARCHAR(255), -- City/town
    stadium VARCHAR(255),
    logo_url TEXT,
    founded INTEGER,
    championships INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE(name, sport_id, competition)
);

CREATE INDEX idx_teams_sport_id ON teams(sport_id);
CREATE INDEX idx_teams_competition ON teams(competition);
CREATE INDEX idx_teams_name ON teams(name);

-- Team players (many-to-many relationship)
CREATE TABLE team_players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    jersey_number INTEGER,
    position VARCHAR(50),
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, player_id, start_date)
);

CREATE INDEX idx_team_players_team_id ON team_players(team_id);
CREATE INDEX idx_team_players_player_id ON team_players(player_id);
```

#### 4. Matches

```sql
-- Matches table (multi-sport)
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sport_id VARCHAR(50) NOT NULL REFERENCES sports(id),
    date TIMESTAMP NOT NULL,
    team1_id UUID REFERENCES teams(id),
    team2_id UUID REFERENCES teams(id),
    team1_name VARCHAR(255), -- Fallback if team not in database
    team2_name VARCHAR(255),
    competition VARCHAR(255), -- 'Debmarine Namibia Premiership', 'MTC Maris Cup', etc.
    venue VARCHAR(255), -- 'Sam Nujoma Stadium', 'Dr Hage Geingob Stadium', etc.
    video_path TEXT,
    video_url TEXT,
    status VARCHAR(50) DEFAULT 'uploaded', -- 'uploaded', 'processing', 'completed', 'failed'
    processing_progress INTEGER DEFAULT 0,
    processing_error TEXT,
    score_team1 INTEGER,
    score_team2 INTEGER,
    score_details JSONB, -- For complex scoring (sets, periods, etc.)
    metadata JSONB, -- Sport-specific metadata
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_matches_sport_id ON matches(sport_id);
CREATE INDEX idx_matches_date ON matches(date);
CREATE INDEX idx_matches_team1_id ON matches(team1_id);
CREATE INDEX idx_matches_team2_id ON matches(team2_id);
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_competition ON matches(competition);
CREATE INDEX idx_matches_created_by ON matches(created_by);
```

#### 5. Players

```sql
-- Players table (universal, multi-sport)
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sport_id VARCHAR(50) NOT NULL REFERENCES sports(id),
    jersey_number INTEGER,
    date_of_birth DATE,
    nationality VARCHAR(100) DEFAULT 'Namibian',
    height_cm INTEGER,
    weight_kg FLOAT,
    position VARCHAR(50),
    photo_url TEXT,
    metadata JSONB, -- Sport-specific player data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_players_sport_id ON players(sport_id);
CREATE INDEX idx_players_name ON players(name);
CREATE INDEX idx_players_nationality ON players(nationality);

-- Player statistics per match
CREATE TABLE player_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    team_id UUID REFERENCES teams(id),
    track_id INTEGER,
    team INTEGER, -- 1 or 2 (for match context)
    total_distance_m FLOAT,
    avg_speed_kmh FLOAT,
    max_speed_kmh FLOAT,
    passes_made INTEGER DEFAULT 0,
    passes_received INTEGER DEFAULT 0,
    successful_passes INTEGER DEFAULT 0,
    pass_accuracy_pct FLOAT,
    possession_time_sec FLOAT,
    possession_pct FLOAT,
    sprints INTEGER DEFAULT 0,
    stats JSONB, -- Sport-specific statistics
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(player_id, match_id)
);

CREATE INDEX idx_player_stats_player_id ON player_statistics(player_id);
CREATE INDEX idx_player_stats_match_id ON player_statistics(match_id);
CREATE INDEX idx_player_stats_team_id ON player_statistics(team_id);
```

#### 6. Passes

```sql
-- Passes table
CREATE TABLE passes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    from_player_id UUID REFERENCES players(id),
    to_player_id UUID REFERENCES players(id),
    from_jersey INTEGER,
    to_jersey INTEGER,
    frame INTEGER NOT NULL,
    timestamp FLOAT, -- Seconds into match
    distance_m FLOAT,
    successful BOOLEAN DEFAULT TRUE,
    from_team INTEGER, -- 1 or 2
    to_team INTEGER,
    position_x FLOAT, -- Field coordinates
    position_y FLOAT,
    metadata JSONB, -- Additional pass data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_passes_match_id ON passes(match_id);
CREATE INDEX idx_passes_from_player_id ON passes(from_player_id);
CREATE INDEX idx_passes_to_player_id ON passes(to_player_id);
CREATE INDEX idx_passes_frame ON passes(match_id, frame);
CREATE INDEX idx_passes_successful ON passes(successful);
```

#### 7. Events

```sql
-- Events table (universal event types)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    player_id UUID REFERENCES players(id),
    jersey_number INTEGER,
    team INTEGER, -- 1 or 2
    event_type VARCHAR(50) NOT NULL, -- 'sprint', 'cluster', 'shot', 'goal', 'foul', etc.
    frame INTEGER NOT NULL,
    timestamp FLOAT, -- Seconds into match
    position_x FLOAT,
    position_y FLOAT,
    metadata JSONB, -- Event-specific data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_match_id ON events(match_id);
CREATE INDEX idx_events_player_id ON events(player_id);
CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_events_frame ON events(match_id, frame);
CREATE INDEX idx_events_timestamp ON events(match_id, timestamp);
```

#### 8. Tournaments

```sql
-- Tournaments table
CREATE TABLE tournaments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sport_id VARCHAR(50) NOT NULL REFERENCES sports(id),
    organizer VARCHAR(255), -- 'MTC', 'NFA', 'UNAM', etc.
    format VARCHAR(50), -- 'knockout', 'round_robin', 'league'
    teams_count INTEGER,
    prize_money DECIMAL(12, 2),
    currency VARCHAR(10) DEFAULT 'NAD',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    venue VARCHAR(255),
    status VARCHAR(50) DEFAULT 'upcoming', -- 'upcoming', 'ongoing', 'completed'
    bracket JSONB, -- Tournament bracket structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tournaments_sport_id ON tournaments(sport_id);
CREATE INDEX idx_tournaments_status ON tournaments(status);
CREATE INDEX idx_tournaments_dates ON tournaments(start_date, end_date);

-- Tournament participants
CREATE TABLE tournament_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    team_id UUID REFERENCES teams(id),
    seed INTEGER,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'eliminated', 'winner'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tournament_id, team_id)
);

CREATE INDEX idx_tournament_participants_tournament_id ON tournament_participants(tournament_id);
CREATE INDEX idx_tournament_participants_team_id ON tournament_participants(team_id);
```

#### 9. Scouting

```sql
-- Scouting reports
CREATE TABLE scouting_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    match_id UUID REFERENCES matches(id),
    title VARCHAR(255) NOT NULL,
    notes TEXT,
    rating DECIMAL(3, 1), -- 0.0 to 10.0
    strengths TEXT[],
    weaknesses TEXT[],
    recommendation TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_scouting_reports_user_id ON scouting_reports(user_id);
CREATE INDEX idx_scouting_reports_player_id ON scouting_reports(player_id);
CREATE INDEX idx_scouting_reports_match_id ON scouting_reports(match_id);
CREATE INDEX idx_scouting_reports_rating ON scouting_reports(rating);
```

#### 10. Payments (Namibian Market)

```sql
-- Payments table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    payment_id VARCHAR(255) UNIQUE NOT NULL, -- External payment ID
    amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'NAD',
    payment_method VARCHAR(50) NOT NULL, -- 'mtc_mobile_money', 'bank_windhoek', 'card'
    phone_number VARCHAR(20), -- For MTC Mobile Money
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'completed', 'failed', 'refunded'
    transaction_id VARCHAR(255), -- External transaction ID
    description TEXT,
    return_url TEXT,
    metadata JSONB,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_payment_id ON payments(payment_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_created_at ON payments(created_at);
```

#### 11. Notifications (Namibian Market)

```sql
-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'whatsapp', 'sms', 'email', 'push'
    phone_number VARCHAR(20), -- For WhatsApp/SMS
    email VARCHAR(255), -- For email
    message TEXT NOT NULL,
    template_id VARCHAR(100), -- For WhatsApp templates
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'failed', 'delivered'
    message_id VARCHAR(255), -- External message ID
    error_message TEXT,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
```

#### 12. Offline Sync

```sql
-- Offline sync queue
CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- 'match', 'player', 'team', etc.
    entity_id UUID,
    action VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete'
    data JSONB NOT NULL,
    priority INTEGER DEFAULT 0, -- Higher = more important
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'synced', 'failed', 'conflict'
    conflict_resolution VARCHAR(50), -- 'server_wins', 'client_wins', 'merge'
    error_message TEXT,
    synced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sync_queue_user_id ON sync_queue(user_id);
CREATE INDEX idx_sync_queue_device_id ON sync_queue(device_id);
CREATE INDEX idx_sync_queue_status ON sync_queue(status);
CREATE INDEX idx_sync_queue_priority ON sync_queue(priority DESC, created_at ASC);

-- Sync history
CREATE TABLE sync_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    last_sync_at TIMESTAMP NOT NULL,
    entities_synced INTEGER DEFAULT 0,
    conflicts_resolved INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sync_history_user_device ON sync_history(user_id, device_id);
CREATE INDEX idx_sync_history_last_sync ON sync_history(last_sync_at);
```

#### 13. UNAM Campuses

```sql
-- UNAM campuses
CREATE TABLE unam_campuses (
    id VARCHAR(50) PRIMARY KEY, -- 'windhoek_main', 'oshakati', etc.
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO unam_campuses (id, name, location, region) VALUES
('windhoek_main', 'Windhoek Main Campus', 'Windhoek', 'Khomas'),
('oshakati', 'Oshakati Campus', 'Oshakati', 'Oshana'),
('hage_geingob', 'Hage Geingob Campus', 'Windhoek', 'Khomas'),
('katima_mulilo', 'Katima Mulilo Campus', 'Katima Mulilo', 'Zambezi'),
('neudamm', 'Neudamm Campus', 'Windhoek', 'Khomas'),
('southern', 'Southern Campus', 'Keetmanshoop', '//Karas'),
('sam_nujoma', 'Sam Nujoma Campus', 'Henties Bay', 'Erongo'),
('josef_kutako', 'Josef Kutako Campus', 'Gobabis', 'Omaheke'),
('ogongo', 'Ogongo Campus', 'Ogongo', 'Omusati'),
('khomasdal', 'Khomasdal Campus', 'Windhoek', 'Khomas'),
('rundu', 'Rundu Campus', 'Rundu', 'Kavango East'),
('ongwediva', 'Ongwediva Campus', 'Ongwediva', 'Oshana'),
('swakopmund', 'Swakopmund Campus', 'Swakopmund', 'Erongo');

-- Campus teams
CREATE TABLE campus_teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campus_id VARCHAR(50) NOT NULL REFERENCES unam_campuses(id),
    team_id UUID NOT NULL REFERENCES teams(id),
    sport_id VARCHAR(50) NOT NULL REFERENCES sports(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(campus_id, team_id, sport_id)
);

CREATE INDEX idx_campus_teams_campus_id ON campus_teams(campus_id);
CREATE INDEX idx_campus_teams_team_id ON campus_teams(team_id);
```

#### 14. User Settings

```sql
-- User settings
CREATE TABLE user_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    notifications JSONB DEFAULT '{}', -- Notification preferences
    data_quality JSONB DEFAULT '{}', -- Image/video quality settings
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'Africa/Windhoek',
    preferences JSONB DEFAULT '{}', -- Other user preferences
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_settings_user_id ON user_settings(user_id);
```

---

## Type Definitions

### Python Models (SQLAlchemy)

#### Base Model

```python
# app/models/base.py
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
```

#### User Model

```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone_number = Column(String(20))
    organization = Column(String(255), index=True)
    campus = Column(String(100), index=True)
    avatar_url = Column(String)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    language = Column(String(10), default='en')
    timezone = Column(String(50), default='Africa/Windhoek')
    subscription_plan = Column(String(50), default='free')
    subscription_expires_at = Column(DateTime)
```

#### Match Model

```python
# app/models/match.py
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel

class Match(BaseModel):
    __tablename__ = 'matches'
    
    name = Column(String(255), nullable=False)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    team1_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    team2_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    team1_name = Column(String(255))
    team2_name = Column(String(255))
    competition = Column(String(255), index=True)
    venue = Column(String(255))
    video_path = Column(Text)
    video_url = Column(Text)
    status = Column(String(50), default='uploaded', index=True)
    processing_progress = Column(Integer, default=0)
    processing_error = Column(Text)
    score_team1 = Column(Integer)
    score_team2 = Column(Integer)
    score_details = Column(JSONB)
    metadata = Column(JSONB)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
```

### TypeScript Types (Frontend)

```typescript
// src/types/database.ts

// User Types
export interface User {
  id: string;
  email: string;
  full_name: string | null;
  phone_number: string | null;
  organization: string | null;
  campus: string | null;
  avatar_url: string | null;
  is_verified: boolean;
  is_active: boolean;
  language: 'en' | 'af' | 'osh';
  timezone: string;
  subscription_plan: 'free' | 'university' | 'pro' | 'enterprise';
  subscription_expires_at: string | null;
  created_at: string;
  updated_at: string;
}

// Match Types
export interface Match {
  id: string;
  name: string;
  sport_id: string;
  date: string;
  team1_id: string | null;
  team2_id: string | null;
  team1_name: string | null;
  team2_name: string | null;
  competition: string | null;
  venue: string | null;
  video_path: string | null;
  video_url: string | null;
  status: 'uploaded' | 'processing' | 'completed' | 'failed';
  processing_progress: number;
  processing_error: string | null;
  score_team1: number | null;
  score_team2: number | null;
  score_details: Record<string, any> | null;
  metadata: Record<string, any> | null;
  created_by: string | null;
  created_at: string;
  updated_at: string;
}

// Player Types
export interface Player {
  id: string;
  name: string;
  sport_id: string;
  jersey_number: number | null;
  date_of_birth: string | null;
  nationality: string;
  height_cm: number | null;
  weight_kg: number | null;
  position: string | null;
  photo_url: string | null;
  metadata: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

// Team Types
export interface Team {
  id: string;
  name: string;
  sport_id: string;
  competition: string | null;
  location: string | null;
  stadium: string | null;
  logo_url: string | null;
  founded: number | null;
  championships: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Tournament Types
export interface Tournament {
  id: string;
  name: string;
  sport_id: string;
  organizer: string | null;
  format: 'knockout' | 'round_robin' | 'league';
  teams_count: number | null;
  prize_money: number | null;
  currency: string;
  start_date: string;
  end_date: string;
  venue: string | null;
  status: 'upcoming' | 'ongoing' | 'completed';
  bracket: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

// Payment Types (Namibian)
export interface Payment {
  id: string;
  user_id: string;
  payment_id: string;
  amount: number;
  currency: string;
  payment_method: 'mtc_mobile_money' | 'bank_windhoek' | 'card';
  phone_number: string | null;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  transaction_id: string | null;
  description: string | null;
  return_url: string | null;
  metadata: Record<string, any> | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

// Notification Types (Namibian)
export interface Notification {
  id: string;
  user_id: string;
  type: 'whatsapp' | 'sms' | 'email' | 'push';
  phone_number: string | null;
  email: string | null;
  message: string;
  template_id: string | null;
  status: 'pending' | 'sent' | 'failed' | 'delivered';
  message_id: string | null;
  error_message: string | null;
  sent_at: string | null;
  delivered_at: string | null;
  created_at: string;
}
```

---

## Indexes & Performance

### Critical Indexes

```sql
-- Composite indexes for common queries
CREATE INDEX idx_matches_sport_date ON matches(sport_id, date DESC);
CREATE INDEX idx_matches_status_date ON matches(status, date DESC);
CREATE INDEX idx_player_stats_match_player ON player_statistics(match_id, player_id);
CREATE INDEX idx_passes_match_timestamp ON passes(match_id, timestamp);
CREATE INDEX idx_events_match_type ON events(match_id, event_type);
CREATE INDEX idx_sync_queue_user_status ON sync_queue(user_id, status, priority DESC);
```

### Performance Optimization

1. **Partitioning:** Consider partitioning `passes` and `events` by `match_id` for large datasets
2. **Materialized Views:** For frequently accessed aggregated statistics
3. **Full-Text Search:** Add GIN indexes for text search on player names, team names
4. **Connection Pooling:** Use Neon HTTP driver for serverless environments

---

## Data Relationships

### Entity Relationship Diagram

```
users
  ├── matches (created_by)
  ├── scouting_reports
  ├── payments
  ├── notifications
  └── sync_queue

sports
  ├── matches
  ├── teams
  ├── players
  └── tournaments

teams
  ├── matches (team1_id, team2_id)
  ├── team_players
  ├── tournament_participants
  └── campus_teams

matches
  ├── player_statistics
  ├── passes
  ├── events
  └── scouting_reports

players
  ├── player_statistics
  ├── passes (from_player_id, to_player_id)
  ├── events
  ├── team_players
  └── scouting_reports

tournaments
  └── tournament_participants

unam_campuses
  └── campus_teams
```

---

## Multi-Sport Support

### Sport-Specific Extensions

The schema uses JSONB columns for sport-specific data:

- `matches.metadata` - Sport-specific match data
- `players.metadata` - Sport-specific player data
- `player_statistics.stats` - Sport-specific statistics
- `sports.config` - Full SportConfig JSON

### Example: Football vs Basketball

**Football Match Metadata:**
```json
{
  "periods": 2,
  "period_duration": 45,
  "stoppage_time": 3,
  "referee": "John Smith"
}
```

**Basketball Match Metadata:**
```json
{
  "periods": 4,
  "period_duration": 10,
  "overtime": true,
  "overtime_duration": 5
}
```

---

## Namibian Market Extensions

### Currency & Payments
- All monetary values in NAD (Namibian Dollar)
- MTC Mobile Money integration
- Bank Windhoek support
- Paygate Namibia for card payments

### Localization
- Language support: English, Afrikaans, Oshiwambo
- Timezone: Africa/Windhoek
- Date formats: DD/MM/YYYY (Namibian standard)

### UNAM Integration
- 13 campuses with dedicated tables
- Campus-specific team tracking
- Multi-campus statistics aggregation

---

## Migration Files

### Initial Schema Migration

```python
# migrations/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create all tables as defined in schema above
    op.create_table('sports', ...)
    op.create_table('users', ...)
    op.create_table('teams', ...)
    op.create_table('matches', ...)
    # ... etc

def downgrade():
    # Drop all tables in reverse order
    op.drop_table('matches')
    op.drop_table('teams')
    op.drop_table('users')
    op.drop_table('sports')
```

---

## Document Status

**Status:** ✅ COMPREHENSIVE - DATABASE READY  
**Last Updated:** January 2025  
**Version:** 2.1 (Namibian Market Focus)  
**Next Review:** Post-launch (Month 3)

---

**Related Documentation:**
- [API Documentation](API_DOCUMENTATION.md) - API endpoints using these types
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - TypeScript type definitions
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [Architecture Documentation](architecture.md) - System architecture

