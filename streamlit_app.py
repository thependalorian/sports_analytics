"""
Streamlit Application
Location: /streamlit_app.py
Purpose: Streamlit UI for Sports Analytics Dashboard
Date: 2026-01-04
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime
from uuid import UUID

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.lib.lancedb_adapter import get_lancedb

# Import database models directly to avoid video_utils dependency
SQLALCHEMY_AVAILABLE = False
SessionLocal = None
try:
    from api.database import get_db, _init_sqlalchemy
    # Initialize SQLAlchemy (lazy init)
    _init_sqlalchemy()
    from api.database import SessionLocal as _SessionLocal
    if _SessionLocal is not None:
        SessionLocal = _SessionLocal
        SQLALCHEMY_AVAILABLE = True
    from api.models.match import Match
    from api.models.player import Player
    from api.models.team import Team
    from api.models.tournament import Tournament
    from sqlalchemy import func, desc
except (ImportError, Exception) as e:
    # If SQLAlchemy models can't be imported, use LanceDB only
    SQLALCHEMY_AVAILABLE = False
    SessionLocal = None
    # Note: Can't use st.warning here as streamlit context not available yet

import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Sports Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database connections
@st.cache_resource
def get_lancedb_connection():
    """Get LanceDB connection"""
    return get_lancedb()

def get_database_session():
    """Get database session (if SQLAlchemy available)"""
    if SQLALCHEMY_AVAILABLE and SessionLocal is not None:
        try:
            return SessionLocal()
        except Exception:
            return None
    return None

# Main title
st.title("⚽ Sports Analytics Dashboard")
st.markdown("**Namibian Market Focus** - Debmarine Premiership, MTC Maris Cup, UNAM")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Matches", "Players", "Teams", "Tournaments", "Analytics", "Settings"]
)

lancedb = get_lancedb_connection()
db = get_database_session() if SQLALCHEMY_AVAILABLE else None

if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Get stats from LanceDB
    try:
        lancedb.register_lancedb_table("matches")
        matches_count = len(lancedb.query("matches"))
    except:
        matches_count = 0
    
    try:
        lancedb.register_lancedb_table("players")
        players_count = len(lancedb.query("players"))
    except:
        players_count = 0
    
    try:
        lancedb.register_lancedb_table("teams")
        teams_count = len(lancedb.query("teams"))
    except:
        teams_count = 0
    
    try:
        lancedb.register_lancedb_table("tournaments")
        tournaments_count = len(lancedb.query("tournaments"))
    except:
        tournaments_count = 0
    
    with col1:
        st.metric("Total Matches", matches_count)
    
    with col2:
        st.metric("Total Players", players_count)
    
    with col3:
        st.metric("Total Teams", teams_count)
    
    with col4:
        st.metric("Total Tournaments", tournaments_count)
    
    # Recent matches
    st.subheader("Recent Matches")
    try:
        lancedb.register_lancedb_table("matches")
        matches_df = lancedb.query("matches")
        if not matches_df.empty:
            # Sort by date if available
            if 'date' in matches_df.columns:
                matches_df = matches_df.sort_values('date', ascending=False).head(10)
            else:
                matches_df = matches_df.head(10)
            st.dataframe(matches_df, use_container_width=True)
        else:
            st.info("No matches found")
    except Exception as e:
        st.info("No matches found")

elif page == "Matches":
    st.header("🏆 Matches")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        sport_filter = st.selectbox("Sport", ["All", "football", "basketball", "rugby", "netball"])
    with col2:
        status_filter = st.selectbox("Status", ["All", "uploaded", "processing", "completed", "failed"])
    with col3:
        search_query = st.text_input("Search matches")
    
    # Get matches from LanceDB
    try:
        lancedb.register_lancedb_table("matches")
        matches_df = lancedb.query("matches")
        
        # Apply filters
        if sport_filter != "All" and 'sport' in matches_df.columns:
            matches_df = matches_df[matches_df['sport'] == sport_filter]
        if status_filter != "All" and 'status' in matches_df.columns:
            matches_df = matches_df[matches_df['status'] == status_filter]
        if search_query and 'name' in matches_df.columns:
            matches_df = matches_df[matches_df['name'].str.contains(search_query, case=False, na=False)]
        
        # Display matches
        if not matches_df.empty:
            for idx, match in matches_df.head(50).iterrows():
                match_name = match.get('name', 'Unknown Match')
                match_date = match.get('date', 'N/A')
                with st.expander(f"{match_name} - {match_date}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sport:** {match.get('sport', 'N/A')}")
                        st.write(f"**Status:** {match.get('status', 'N/A')}")
                    with col2:
                        st.write(f"**Team 1:** {match.get('team1_name', 'N/A')}")
                        st.write(f"**Team 2:** {match.get('team2_name', 'N/A')}")
        else:
            st.info("No matches found")
    except Exception as e:
        st.error(f"Error loading matches: {e}")
        st.info("No matches found")

elif page == "Players":
    st.header("👤 Players")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        sport_filter = st.selectbox("Sport", ["All", "football", "basketball", "rugby"], key="player_sport")
    with col2:
        search_query = st.text_input("Search players", key="player_search")
    
    # Get players from LanceDB
    try:
        lancedb.register_lancedb_table("players")
        players_df = lancedb.query("players")
        
        # Apply filters
        if sport_filter != "All" and 'sport' in players_df.columns:
            players_df = players_df[players_df['sport'] == sport_filter]
        if search_query and 'name' in players_df.columns:
            players_df = players_df[players_df['name'].str.contains(search_query, case=False, na=False)]
        
        # Display players
        if not players_df.empty:
            st.dataframe(players_df.head(100), use_container_width=True)
        else:
            st.info("No players found")
    except Exception as e:
        st.error(f"Error loading players: {e}")
        st.info("No players found")

elif page == "Teams":
    st.header("🏅 Teams")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        sport_filter = st.selectbox("Sport", ["All", "football", "basketball", "rugby"], key="team_sport")
    with col2:
        competition_filter = st.text_input("Competition", key="team_competition")
    
    # Get teams from LanceDB
    try:
        lancedb.register_lancedb_table("teams")
        teams_df = lancedb.query("teams")
        
        # Apply filters
        if sport_filter != "All" and 'sport' in teams_df.columns:
            teams_df = teams_df[teams_df['sport'] == sport_filter]
        if competition_filter and 'competition' in teams_df.columns:
            teams_df = teams_df[teams_df['competition'].str.contains(competition_filter, case=False, na=False)]
        
        # Display teams
        if not teams_df.empty:
            st.dataframe(teams_df.head(100), use_container_width=True)
        else:
            st.info("No teams found")
    except Exception as e:
        st.error(f"Error loading teams: {e}")
        st.info("No teams found")

elif page == "Tournaments":
    st.header("🏆 Tournaments")
    
    # Get tournaments from LanceDB
    try:
        lancedb.register_lancedb_table("tournaments")
        tournaments_df = lancedb.query("tournaments")
        
        if not tournaments_df.empty:
            for idx, tournament in tournaments_df.head(50).iterrows():
                tournament_name = tournament.get('name', 'Unknown Tournament')
                tournament_status = tournament.get('status', 'N/A')
                with st.expander(f"{tournament_name} - {tournament_status}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sport:** {tournament.get('sport', 'N/A')}")
                        st.write(f"**Organizer:** {tournament.get('organizer', 'N/A')}")
                    with col2:
                        st.write(f"**Status:** {tournament_status}")
        else:
            st.info("No tournaments found")
    except Exception as e:
        st.error(f"Error loading tournaments: {e}")
        st.info("No tournaments found")

elif page == "Analytics":
    st.header("📈 Analytics")
    
    # Match status distribution using DuckDB
    st.subheader("Match Status Distribution")
    try:
        lancedb.register_lancedb_table("matches")
        status_df = lancedb.execute_sql("""
            SELECT status as Status, COUNT(*) as Count
            FROM matches
            GROUP BY status
        """, "matches")
        
        if not status_df.empty:
            fig = px.pie(status_df, values="Count", names="Status", title="Match Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No match data available")
    except Exception as e:
        st.warning(f"Could not load status distribution: {e}")
    
    # Matches by sport using DuckDB
    st.subheader("Matches by Sport")
    try:
        lancedb.register_lancedb_table("matches")
        sport_df = lancedb.execute_sql("""
            SELECT sport as Sport, COUNT(*) as Count
            FROM matches
            GROUP BY sport
        """, "matches")
        
        if not sport_df.empty:
            fig = px.bar(sport_df, x="Sport", y="Count", title="Matches by Sport")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No match data available")
    except Exception as e:
        st.warning(f"Could not load sport statistics: {e}")

elif page == "Settings":
    st.header("⚙️ Settings")
    
    st.subheader("Database Status")
    
    # SQLAlchemy status
    if SQLALCHEMY_AVAILABLE and db:
        try:
            db.execute("SELECT 1")
            st.success("✅ SQLAlchemy Database: Connected")
        except Exception as e:
            st.warning(f"⚠️ SQLAlchemy Database: {str(e)}")
    else:
        st.info("ℹ️ SQLAlchemy: Not available (using LanceDB only)")
    
    # LanceDB status
    try:
        lancedb_health = lancedb.health_check()
        if lancedb_health.get("status") == "healthy":
            st.success(f"✅ LanceDB: Connected ({lancedb_health.get('tables_count', 0)} tables)")
            st.success(f"✅ DuckDB: {lancedb_health.get('duckdb', 'unknown')}")
        else:
            st.warning(f"⚠️ LanceDB: {lancedb_health.get('status')}")
    except Exception as e:
        st.error(f"❌ LanceDB: {str(e)}")
    
    st.subheader("System Information")
    st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"**Database Path:** {lancedb.db_path}")
    st.write(f"**Tables:** {', '.join(lancedb.list_tables())}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Sports Vision Analytics**")
st.sidebar.markdown("Version 2.1.0")
st.sidebar.markdown("🇳🇦 Namibian Market")

