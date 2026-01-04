"""
Initial Database Schema
Revision ID: 001_initial
Revises: 
Create Date: 2025-01-15 10:00:00.000000

Creates all initial tables for sports analytics platform:
- Users & Authentication
- Sports & Multi-Sport Support
- Teams
- Matches
- Players
- Passes
- Events
- Tournaments
- Scouting
- Payments (Namibian Market)
- Notifications (Namibian Market)
- Offline Sync
- UNAM Campuses
- User Settings
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Sports table
    op.create_table(
        'sports',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('field_type', sa.String(50)),
        sa.Column('field_width', sa.Float()),
        sa.Column('field_height', sa.Float()),
        sa.Column('field_unit', sa.String(10)),
        sa.Column('max_players', sa.Integer()),
        sa.Column('config', postgresql.JSONB),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255)),
        sa.Column('phone_number', sa.String(20)),
        sa.Column('organization', sa.String(255)),
        sa.Column('campus', sa.String(100)),
        sa.Column('avatar_url', sa.Text()),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('two_factor_enabled', sa.Boolean(), default=False),
        sa.Column('two_factor_secret', sa.String(255)),
        sa.Column('language', sa.String(10), default='en'),
        sa.Column('timezone', sa.String(50), default='Africa/Windhoek'),
        sa.Column('subscription_plan', sa.String(50), default='free'),
        sa.Column('subscription_expires_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime()),
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_organization', 'users', ['organization'])
    op.create_index('idx_users_campus', 'users', ['campus'])
    
    # User sessions
    op.create_table(
        'user_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('refresh_token', sa.String(500), unique=True, nullable=False),
        sa.Column('device_info', postgresql.JSONB),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('user_agent', sa.Text()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), default=False),
        sa.Column('revoked_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_sessions_user_id', 'user_sessions', ['user_id'])
    op.create_index('idx_sessions_refresh_token', 'user_sessions', ['refresh_token'])
    
    # Teams table
    op.create_table(
        'teams',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('sport_id', sa.String(50), sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('competition', sa.String(255)),
        sa.Column('location', sa.String(255)),
        sa.Column('stadium', sa.String(255)),
        sa.Column('logo_url', sa.Text()),
        sa.Column('founded', sa.Integer()),
        sa.Column('championships', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime()),
        sa.UniqueConstraint('name', 'sport_id', 'competition', name='uq_team_name_sport_competition'),
    )
    op.create_index('idx_teams_sport_id', 'teams', ['sport_id'])
    op.create_index('idx_teams_competition', 'teams', ['competition'])
    
    # Matches table
    op.create_table(
        'matches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('sport_id', sa.String(50), sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('team1_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id')),
        sa.Column('team2_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id')),
        sa.Column('team1_name', sa.String(255)),
        sa.Column('team2_name', sa.String(255)),
        sa.Column('competition', sa.String(255)),
        sa.Column('venue', sa.String(255)),
        sa.Column('video_path', sa.Text()),
        sa.Column('video_url', sa.Text()),
        sa.Column('status', sa.String(50), default='uploaded'),
        sa.Column('processing_progress', sa.Integer(), default=0),
        sa.Column('processing_error', sa.Text()),
        sa.Column('score_team1', sa.Integer()),
        sa.Column('score_team2', sa.Integer()),
        sa.Column('score_details', postgresql.JSONB),
        sa.Column('metadata', postgresql.JSONB),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime()),
    )
    op.create_index('idx_matches_sport_id', 'matches', ['sport_id'])
    op.create_index('idx_matches_date', 'matches', ['date'])
    op.create_index('idx_matches_status', 'matches', ['status'])
    
    # Players table
    op.create_table(
        'players',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('sport_id', sa.String(50), sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('jersey_number', sa.Integer()),
        sa.Column('date_of_birth', sa.Date()),
        sa.Column('nationality', sa.String(100), default='Namibian'),
        sa.Column('height_cm', sa.Integer()),
        sa.Column('weight_kg', sa.Float()),
        sa.Column('position', sa.String(50)),
        sa.Column('photo_url', sa.Text()),
        sa.Column('metadata', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime()),
    )
    op.create_index('idx_players_sport_id', 'players', ['sport_id'])
    op.create_index('idx_players_name', 'players', ['name'])
    
    # Player statistics
    op.create_table(
        'player_statistics',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id')),
        sa.Column('track_id', sa.Integer()),
        sa.Column('team', sa.Integer()),
        sa.Column('total_distance_m', sa.Float()),
        sa.Column('avg_speed_kmh', sa.Float()),
        sa.Column('max_speed_kmh', sa.Float()),
        sa.Column('passes_made', sa.Integer(), default=0),
        sa.Column('passes_received', sa.Integer(), default=0),
        sa.Column('successful_passes', sa.Integer(), default=0),
        sa.Column('pass_accuracy_pct', sa.Float()),
        sa.Column('possession_time_sec', sa.Float()),
        sa.Column('possession_pct', sa.Float()),
        sa.Column('sprints', sa.Integer(), default=0),
        sa.Column('stats', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('player_id', 'match_id', name='uq_player_match'),
    )
    op.create_index('idx_player_stats_player_id', 'player_statistics', ['player_id'])
    op.create_index('idx_player_stats_match_id', 'player_statistics', ['match_id'])
    
    # Passes table
    op.create_table(
        'passes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('from_player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id')),
        sa.Column('to_player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id')),
        sa.Column('from_jersey', sa.Integer()),
        sa.Column('to_jersey', sa.Integer()),
        sa.Column('frame', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Float()),
        sa.Column('distance_m', sa.Float()),
        sa.Column('successful', sa.Boolean(), default=True),
        sa.Column('from_team', sa.Integer()),
        sa.Column('to_team', sa.Integer()),
        sa.Column('position_x', sa.Float()),
        sa.Column('position_y', sa.Float()),
        sa.Column('metadata', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_passes_match_id', 'passes', ['match_id'])
    op.create_index('idx_passes_from_player_id', 'passes', ['from_player_id'])
    op.create_index('idx_passes_to_player_id', 'passes', ['to_player_id'])
    
    # Events table
    op.create_table(
        'events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id')),
        sa.Column('jersey_number', sa.Integer()),
        sa.Column('team', sa.Integer()),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('frame', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Float()),
        sa.Column('position_x', sa.Float()),
        sa.Column('position_y', sa.Float()),
        sa.Column('metadata', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_events_match_id', 'events', ['match_id'])
    op.create_index('idx_events_event_type', 'events', ['event_type'])
    
    # Tournaments table
    op.create_table(
        'tournaments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('sport_id', sa.String(50), sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('organizer', sa.String(255)),
        sa.Column('format', sa.String(50)),
        sa.Column('teams_count', sa.Integer()),
        sa.Column('prize_money', sa.Numeric(12, 2)),
        sa.Column('currency', sa.String(10), default='NAD'),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('venue', sa.String(255)),
        sa.Column('status', sa.String(50), default='upcoming'),
        sa.Column('bracket', postgresql.JSONB),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_tournaments_sport_id', 'tournaments', ['sport_id'])
    op.create_index('idx_tournaments_status', 'tournaments', ['status'])
    
    # Tournament participants
    op.create_table(
        'tournament_participants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tournament_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('seed', sa.Integer()),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('tournament_id', 'team_id', name='uq_tournament_team'),
    )
    
    # Scouting reports
    op.create_table(
        'scouting_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('match_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('matches.id')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('notes', sa.Text()),
        sa.Column('rating', sa.Float()),
        sa.Column('strengths', postgresql.ARRAY(sa.Text)),
        sa.Column('weaknesses', postgresql.ARRAY(sa.Text)),
        sa.Column('recommendation', sa.Text()),
        sa.Column('is_public', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime()),
    )
    op.create_index('idx_scouting_reports_user_id', 'scouting_reports', ['user_id'])
    op.create_index('idx_scouting_reports_player_id', 'scouting_reports', ['player_id'])
    
    # Payments (Namibian Market)
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('payment_id', sa.String(255), unique=True, nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(10), default='NAD'),
        sa.Column('payment_method', sa.String(50), nullable=False),
        sa.Column('phone_number', sa.String(20)),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('transaction_id', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('return_url', sa.Text()),
        sa.Column('metadata', postgresql.JSONB),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_payments_user_id', 'payments', ['user_id'])
    op.create_index('idx_payments_payment_id', 'payments', ['payment_id'])
    op.create_index('idx_payments_status', 'payments', ['status'])
    
    # Notifications (Namibian Market)
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('phone_number', sa.String(20)),
        sa.Column('email', sa.String(255)),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('template_id', sa.String(100)),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('message_id', sa.String(255)),
        sa.Column('error_message', sa.Text()),
        sa.Column('sent_at', sa.DateTime()),
        sa.Column('delivered_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_notifications_user_id', 'notifications', ['user_id'])
    op.create_index('idx_notifications_status', 'notifications', ['status'])
    
    # Sync queue (Offline-First)
    op.create_table(
        'sync_queue',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True)),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('data', postgresql.JSONB, nullable=False),
        sa.Column('priority', sa.Integer(), default=0),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('conflict_resolution', sa.String(50)),
        sa.Column('error_message', sa.Text()),
        sa.Column('synced_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_sync_queue_user_id', 'sync_queue', ['user_id'])
    op.create_index('idx_sync_queue_device_id', 'sync_queue', ['device_id'])
    op.create_index('idx_sync_queue_status', 'sync_queue', ['status'])
    
    # Sync history
    op.create_table(
        'sync_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('device_id', sa.String(255), nullable=False),
        sa.Column('last_sync_at', sa.DateTime(), nullable=False),
        sa.Column('entities_synced', sa.Integer(), default=0),
        sa.Column('conflicts_resolved', sa.Integer(), default=0),
        sa.Column('errors', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_sync_history_user_device', 'sync_history', ['user_id', 'device_id'])
    
    # UNAM campuses
    op.create_table(
        'unam_campuses',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('region', sa.String(100)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    
    # Campus teams
    op.create_table(
        'campus_teams',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('campus_id', sa.String(50), sa.ForeignKey('unam_campuses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sport_id', sa.String(50), sa.ForeignKey('sports.id'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('campus_id', 'team_id', 'sport_id', name='uq_campus_team_sport'),
    )
    
    # User settings
    op.create_table(
        'user_settings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('notifications', postgresql.JSONB, default={}),
        sa.Column('data_quality', postgresql.JSONB, default={}),
        sa.Column('language', sa.String(10), default='en'),
        sa.Column('timezone', sa.String(50), default='Africa/Windhoek'),
        sa.Column('preferences', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_user_settings_user_id', 'user_settings', ['user_id'])
    
    # Team players
    op.create_table(
        'team_players',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('team_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False),
        sa.Column('player_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('jersey_number', sa.Integer()),
        sa.Column('position', sa.String(50)),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('team_id', 'player_id', 'start_date', name='uq_team_player_start_date'),
    )
    op.create_index('idx_team_players_team_id', 'team_players', ['team_id'])
    op.create_index('idx_team_players_player_id', 'team_players', ['player_id'])


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table('team_players')
    op.drop_table('user_settings')
    op.drop_table('campus_teams')
    op.drop_table('unam_campuses')
    op.drop_table('sync_history')
    op.drop_table('sync_queue')
    op.drop_table('notifications')
    op.drop_table('payments')
    op.drop_table('scouting_reports')
    op.drop_table('tournament_participants')
    op.drop_table('tournaments')
    op.drop_table('events')
    op.drop_table('passes')
    op.drop_table('player_statistics')
    op.drop_table('players')
    op.drop_table('matches')
    op.drop_table('teams')
    op.drop_table('user_sessions')
    op.drop_table('users')
    op.drop_table('sports')

