# API Documentation
## Sports Analytics Web Dashboard API

**Version:** 2.1 (Namibian Market Focus)  
**Last Updated:** January 2025  
**Primary Market:** 🇳🇦 Namibia (Africa)  
**Currency:** N$ (Namibian Dollar)

**Base URLs:**
- **Development:** `http://localhost:8000/api/v1`
- **Staging:** `https://staging-api.sportsvision.na/api/v1`
- **Production:** `https://api.sportsvision.na/api/v1`
- **UNAM Pilot:** `https://unam-api.sportsvision.na/api/v1`

**Server Locations:**
- **Primary:** Windhoek, Namibia (Hosted on MTC servers)
- **CDN:** Cloudflare (Global edge caching)
- **Backup:** Cape Town, South Africa

**Related Documentation:**
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Frontend integration guide
- [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md) - Setup and implementation
- [Architecture Documentation](architecture.md) - System architecture overview
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements

---

## 🇳🇦 Namibian API Specifications

### Network Optimization for Namibia
- **Response Compression:** Gzip/Brotli enabled (80% size reduction)
- **Connection Keep-Alive:** Enabled (reduce 3G latency)
- **HTTP/2:** Enabled (multiplexing for 4G/5G)
- **Rate Limiting:** Relaxed for Namibian IPs (higher limits for UNAM, MTC)
- **Timeout:** 30s (accommodate 3G latency)
- **Retry Logic:** 3 attempts with exponential backoff

### Offline-First Support
- **Sync Endpoints:** `/api/v1/sync/matches`, `/api/v1/sync/players`
- **Delta Updates:** Only changed data since last sync
- **Conflict Resolution:** Last-write-wins with timestamp
- **Offline Queue:** Client can queue requests for later

### Data Response Formats
- **Compact Mode:** `?compact=true` (50% smaller, for 3G)
- **Image Quality:** `?quality=low|medium|high` (default: medium for Namibia)
- **Video Quality:** `?video_quality=480p|720p|1080p` (default: 480p)
- **Pagination:** Max 50 items per page (reduce payload)

---

## Authentication

All API endpoints require authentication except for public endpoints. Use JWT tokens in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "organization": "UNAM",
  "campus": "Windhoek Main"
}
```

**Response:**
```json
{
  "user_id": "990e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "message": "Registration successful. Please verify your email."
}
```

### Get Authentication Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "990e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "organization": "UNAM",
    "campus": "Windhoek Main"
  }
}
```

### Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Logout

```http
POST /api/v1/auth/logout
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

### Verify Email

```http
GET /api/v1/auth/verify?token=<verification_token>
```

**Response:**
```json
{
  "message": "Email verified successfully"
}
```

### Forgot Password

```http
POST /api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Password reset link sent to your email"
}
```

### Reset Password

```http
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "<reset_token>",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password reset successfully"
}
```

---

## Matches

### List Matches

```http
GET /api/v1/matches
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 50)
- `status` (string): Filter by status (`uploaded`, `processing`, `completed`, `failed`)
- `sport` (string): Filter by sport (`football`, `basketball`, `rugby`, `netball`, `hockey`, `cricket`, `tennis`, `volleyball`)
- `team` (string): Filter by team name (e.g., "African Stars", "UNAM FC")
- `competition` (string): Filter by competition (e.g., "Debmarine Namibia Premiership", "MTC Maris Cup")
- `date_from` (string): Filter from date (ISO 8601)
- `date_to` (string): Filter to date (ISO 8601)
- `search` (string): Search in match names
- `compact` (boolean): Return compact response (default: false)

**Response:**
```json
{
  "matches": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "African Stars vs Black Africa",
      "sport": "football",
      "date": "2024-01-15T15:00:00Z",
      "team1_name": "African Stars",
      "team2_name": "Black Africa",
      "competition": "Debmarine Namibia Premiership",
      "venue": "Sam Nujoma Stadium",
      "status": "completed",
      "score": {
        "team1": 2,
        "team2": 1
      },
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T16:30:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 20,
  "pages": 5
}
```

### Get Match Details

```http
GET /api/v1/matches/{match_id}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "African Stars vs Black Africa",
  "sport": "football",
  "date": "2024-01-15T15:00:00Z",
  "team1_name": "African Stars",
  "team2_name": "Black Africa",
  "team1_id": "team_african_stars",
  "team2_id": "team_black_africa",
  "competition": "Debmarine Namibia Premiership",
  "venue": "Sam Nujoma Stadium",
  "video_path": "/videos/match_123.mp4",
  "status": "completed",
  "processing_progress": 100,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T16:30:00Z",
  "score": {
    "team1": 2,
    "team2": 1
  },
  "quick_stats": {
    "total_passes": 450,
    "possession_team1": 52.3,
    "possession_team2": 47.7,
    "total_distance_team1": 105.5,
    "total_distance_team2": 98.2
  }
}
```

### Upload Match Video

```http
POST /api/v1/matches
Content-Type: multipart/form-data

file: <video_file>
name: "African Stars vs Black Africa"
sport: "football"
date: "2024-01-15T15:00:00Z"
team1_name: "African Stars"
team2_name: "Black Africa"
team1_id: "team_african_stars"
team2_id: "team_black_africa"
competition: "Debmarine Namibia Premiership"
venue: "Sam Nujoma Stadium"
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded",
  "message": "Video uploaded successfully. Processing started."
}
```

### Get Match Processing Status

```http
GET /api/v1/matches/{match_id}/status
```

**Response:**
```json
{
  "status": "processing",
  "progress": 65,
  "current_step": "Calculating statistics",
  "estimated_time_remaining": 120
}
```

### Delete Match

```http
DELETE /api/v1/matches/{match_id}
```

**Response:**
```json
{
  "message": "Match deleted successfully"
}
```

### Update Match

```http
PATCH /api/v1/matches/{match_id}
Content-Type: application/json

{
  "name": "African Stars vs Black Africa",
  "date": "2024-01-15T15:00:00Z",
  "venue": "Sam Nujoma Stadium"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Match updated successfully"
}
```

---

## Players

### List All Players (Across Matches)

```http
GET /api/v1/players
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `sport` (string): Filter by sport
- `team` (string): Filter by team name
- `search` (string): Search by player name or jersey number
- `sort_by` (string): Sort field (`name`, `matches`, `distance`, `speed`)
- `order` (string): Sort order (`asc` or `desc`)

**Response:**
```json
{
  "players": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Panduleni Nekundi",
      "jersey_number": 10,
      "team": "African Stars",
      "sport": "football",
      "position": "Forward",
      "matches_count": 15,
      "total_distance_km": 157.5,
      "avg_speed_kmh": 8.2
    }
  ],
  "total": 250,
  "page": 1,
  "limit": 20
}
```

### Get Player Profile

```http
GET /api/v1/players/{player_id}
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "Panduleni Nekundi",
  "jersey_number": 10,
  "team": "African Stars",
  "sport": "football",
  "position": "Forward",
  "date_of_birth": "1995-05-15",
  "nationality": "Namibian",
  "height_cm": 175,
  "weight_kg": 72,
  "matches": [
    {
      "match_id": "550e8400-e29b-41d4-a716-446655440000",
      "date": "2024-01-15T15:00:00Z",
      "opponent": "Black Africa",
      "stats": {
        "total_distance_m": 10500.5,
        "avg_speed_kmh": 8.5,
        "passes_made": 45
      }
    }
  ],
  "career_stats": {
    "matches_played": 15,
    "total_distance_km": 157.5,
    "avg_distance_per_match_km": 10.5,
    "total_passes": 675,
    "pass_accuracy_pct": 92.3
  }
}
```

---

### List Players in Match

```http
GET /api/v1/matches/{match_id}/players
```

**Query Parameters:**
- `team` (integer): Filter by team (1 or 2)
- `jersey_number` (integer): Filter by jersey number
- `sort_by` (string): Sort field (`distance`, `speed`, `passes`)
- `order` (string): Sort order (`asc` or `desc`)

**Response:**
```json
{
  "players": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "match_id": "550e8400-e29b-41d4-a716-446655440000",
      "track_id": 10,
      "jersey_number": 10,
      "team": 1,
      "team_name": "Team A",
      "stats": {
        "total_distance_m": 10500.5,
        "avg_speed_kmh": 8.5,
        "max_speed_kmh": 32.1,
        "passes_made": 45,
        "passes_received": 38,
        "possession_time_sec": 180.5
      }
    }
  ],
  "total": 22
}
```

### Get Player Details

```http
GET /api/v1/matches/{match_id}/players/{player_id}
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "match_id": "550e8400-e29b-41d4-a716-446655440000",
  "track_id": 10,
  "jersey_number": 10,
  "team": 1,
  "team_name": "Team A",
  "stats": {
    "total_distance_m": 10500.5,
    "avg_speed_kmh": 8.5,
    "max_speed_kmh": 32.1,
    "passes_made": 45,
    "passes_received": 38,
    "successful_passes": 42,
    "pass_accuracy_pct": 93.3,
    "possession_time_sec": 180.5,
    "possession_pct": 3.3,
    "sprints": 12
  },
  "heatmap_url": "/api/v1/matches/{match_id}/players/{player_id}/heatmap",
  "pass_network_url": "/api/v1/matches/{match_id}/players/{player_id}/pass-network"
}
```

### Get Player Heatmap

```http
GET /api/v1/matches/{match_id}/players/{player_id}/heatmap
```

**Response:** PNG image file

### Get Player Pass Network

```http
GET /api/v1/matches/{match_id}/players/{player_id}/pass-network
```

**Response:**
```json
{
  "player_id": "660e8400-e29b-41d4-a716-446655440001",
  "passes_made": [
    {
      "to_player_id": "660e8400-e29b-41d4-a716-446655440002",
      "to_jersey": 7,
      "count": 12,
      "successful": 11
    }
  ],
  "passes_received": [
    {
      "from_player_id": "660e8400-e29b-41d4-a716-446655440003",
      "from_jersey": 8,
      "count": 8,
      "successful": 8
    }
  ]
}
```

---

## Teams

### List All Teams

```http
GET /api/v1/teams
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `sport` (string): Filter by sport
- `competition` (string): Filter by competition
- `search` (string): Search by team name
- `sort_by` (string): Sort field (`name`, `matches`, `wins`)
- `order` (string): Sort order (`asc` or `desc`)

**Response:**
```json
{
  "teams": [
    {
      "id": "team_african_stars",
      "name": "African Stars",
      "sport": "football",
      "competition": "Debmarine Namibia Premiership",
      "location": "Windhoek",
      "stadium": "Sam Nujoma Stadium",
      "matches_count": 30,
      "wins": 18,
      "draws": 8,
      "losses": 4
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

### Get Team Profile

```http
GET /api/v1/teams/{team_id}
```

**Response:**
```json
{
  "id": "team_african_stars",
  "name": "African Stars",
  "sport": "football",
  "competition": "Debmarine Namibia Premiership",
  "location": "Windhoek",
  "stadium": "Sam Nujoma Stadium",
  "founded": 1958,
  "championships": 5,
  "logo_url": "/logos/african-stars.png",
  "squad": [
    {
      "player_id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Panduleni Nekundi",
      "jersey_number": 10,
      "position": "Forward"
    }
  ],
  "season_stats": {
    "matches_played": 30,
    "wins": 18,
    "draws": 8,
    "losses": 4,
    "goals_for": 52,
    "goals_against": 28,
    "points": 62
  }
}
```

---

### Get Team Details

```http
GET /api/v1/matches/{match_id}/teams/{team_id}
```

**Response:**
```json
{
  "team": 1,
  "team_name": "Team A",
  "stats": {
    "possession_pct": 52.3,
    "total_distance_km": 105.5,
    "avg_distance_per_player_km": 9.6,
    "avg_speed_ms": 2.1,
    "max_speed_ms": 8.9,
    "total_passes": 245,
    "successful_passes": 228,
    "pass_accuracy_pct": 93.1,
    "sprints": 45
  },
  "players": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "jersey_number": 10,
      "stats": {...}
    }
  ]
}
```

### Get Team Heatmap

```http
GET /api/v1/matches/{match_id}/teams/{team_id}/heatmap
```

**Response:** PNG image file

### Get Team Pass Network

```http
GET /api/v1/matches/{match_id}/teams/{team_id}/pass-network
```

**Response:**
```json
{
  "team": 1,
  "nodes": [
    {
      "player_id": "660e8400-e29b-41d4-a716-446655440001",
      "jersey_number": 10,
      "x": 0.5,
      "y": 0.3,
      "passes_made": 45
    }
  ],
  "edges": [
    {
      "from_player_id": "660e8400-e29b-41d4-a716-446655440001",
      "to_player_id": "660e8400-e29b-41d4-a716-446655440002",
      "passes": 12,
      "successful": 11
    }
  ]
}
```

---

## Tournaments

### List Tournaments

```http
GET /api/v1/tournaments
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `sport` (string): Filter by sport
- `status` (string): Filter by status (`upcoming`, `ongoing`, `completed`)
- `search` (string): Search by tournament name

**Response:**
```json
{
  "tournaments": [
    {
      "id": "tournament_mtc_maris_2025",
      "name": "MTC Maris Cup 2025",
      "sport": "football",
      "format": "knockout",
      "teams": 16,
      "prize_money": 1500000,
      "currency": "NAD",
      "start_date": "2025-01-15T00:00:00Z",
      "end_date": "2025-02-15T00:00:00Z",
      "venue": "Dr Hage Geingob Stadium",
      "status": "upcoming"
    }
  ],
  "total": 10,
  "page": 1,
  "limit": 20
}
```

### Get Tournament Details

```http
GET /api/v1/tournaments/{tournament_id}
```

**Response:**
```json
{
  "id": "tournament_mtc_maris_2025",
  "name": "MTC Maris Cup 2025",
  "sport": "football",
  "format": "knockout",
  "organizer": "MTC",
  "teams": 16,
  "prize_money": 1500000,
  "currency": "NAD",
  "start_date": "2025-01-15T00:00:00Z",
  "end_date": "2025-02-15T00:00:00Z",
  "venue": "Dr Hage Geingob Stadium",
  "status": "upcoming",
  "participating_teams": [
    {
      "team_id": "team_african_stars",
      "name": "African Stars",
      "seed": 1
    }
  ],
  "bracket": {
    "rounds": [
      {
        "name": "Round of 16",
        "matches": [
          {
            "match_id": "550e8400-e29b-41d4-a716-446655440000",
            "team1": "African Stars",
            "team2": "Black Africa",
            "status": "scheduled"
          }
        ]
      }
    ]
  }
}
```

### Get Tournament Standings

```http
GET /api/v1/tournaments/{tournament_id}/standings
```

**Response:**
```json
{
  "tournament_id": "tournament_mtc_maris_2025",
  "standings": [
    {
      "team_id": "team_african_stars",
      "team_name": "African Stars",
      "matches_played": 3,
      "wins": 3,
      "draws": 0,
      "losses": 0,
      "goals_for": 8,
      "goals_against": 2,
      "points": 9,
      "position": 1
    }
  ]
}
```

---

## Analytics

### Get Match Statistics

```http
GET /api/v1/matches/{match_id}/analytics/stats
```

**Response:**
```json
{
  "match_stats": {
    "duration_min": 90.0,
    "total_frames": 162000,
    "ball_in_play_pct": 58.2,
    "total_passes": 450,
    "successful_passes": 420,
    "overall_pass_accuracy": 93.3,
    "avg_pass_distance_m": 18.5,
    "longest_pass_m": 45.2
  },
  "team_stats": {
    "team1": {
      "possession_pct": 52.3,
      "total_distance_km": 105.5,
      "total_passes": 245,
      "pass_accuracy_pct": 93.1
    },
    "team2": {
      "possession_pct": 47.7,
      "total_distance_km": 98.2,
      "total_passes": 205,
      "pass_accuracy_pct": 93.7
    }
  }
}
```

### Get Passes

```http
GET /api/v1/matches/{match_id}/analytics/passes
```

**Query Parameters:**
- `team` (integer): Filter by team
- `player_id` (string): Filter by player
- `successful` (boolean): Filter by success
- `frame_from` (integer): Filter from frame
- `frame_to` (integer): Filter to frame

**Response:**
```json
{
  "passes": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440001",
      "match_id": "550e8400-e29b-41d4-a716-446655440000",
      "from_player_id": "660e8400-e29b-41d4-a716-446655440001",
      "from_jersey": 10,
      "to_player_id": "660e8400-e29b-41d4-a716-446655440002",
      "to_jersey": 7,
      "frame": 1500,
      "distance_m": 18.5,
      "successful": true,
      "from_team": 1,
      "to_team": 1
    }
  ],
  "total": 450
}
```

### Get Events

```http
GET /api/v1/matches/{match_id}/analytics/events
```

**Query Parameters:**
- `event_type` (string): Filter by event type (`sprint`, `cluster`, `shot`, etc.)
- `team` (integer): Filter by team
- `player_id` (string): Filter by player
- `frame_from` (integer): Filter from frame
- `frame_to` (integer): Filter to frame

**Response:**
```json
{
  "events": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440001",
      "match_id": "550e8400-e29b-41d4-a716-446655440000",
      "player_id": "660e8400-e29b-41d4-a716-446655440001",
      "jersey_number": 10,
      "team": 1,
      "event_type": "sprint",
      "frame": 2500,
      "position_x": 45.2,
      "position_y": 30.5,
      "timestamp": "00:15:30"
    }
  ],
  "total": 120
}
```

### Get Possession Data

```http
GET /api/v1/matches/{match_id}/analytics/possession
```

**Query Parameters:**
- `frame_from` (integer): Filter from frame
- `frame_to` (integer): Filter to frame

**Response:**
```json
{
  "possession": [
    {
      "frame": 100,
      "team": 1,
      "player_id": "660e8400-e29b-41d4-a716-446655440001",
      "jersey_number": 10
    }
  ],
  "summary": {
    "team1_pct": 52.3,
    "team2_pct": 47.7,
    "total_frames": 162000
  }
}
```

---

## Scouting

### Create Scouting Report

```http
POST /api/v1/scouting/reports
Content-Type: application/json

{
  "player_id": "660e8400-e29b-41d4-a716-446655440001",
  "match_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Panduleni Nekundi - Performance Analysis",
  "notes": "Excellent pace and finishing ability",
  "rating": 8.5,
  "strengths": ["Speed", "Finishing", "Work rate"],
  "weaknesses": ["Aerial duels"],
  "recommendation": "Highly recommended for national team"
}
```

**Response:**
```json
{
  "id": "scout_report_001",
  "player_id": "660e8400-e29b-41d4-a716-446655440001",
  "match_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T16:00:00Z",
  "message": "Scouting report created successfully"
}
```

### List Scouting Reports

```http
GET /api/v1/scouting/reports
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `player_id` (string): Filter by player
- `match_id` (string): Filter by match
- `rating_min` (float): Minimum rating
- `sort_by` (string): Sort field (`rating`, `created_at`)
- `order` (string): Sort order (`asc` or `desc`)

**Response:**
```json
{
  "reports": [
    {
      "id": "scout_report_001",
      "player_id": "660e8400-e29b-41d4-a716-446655440001",
      "player_name": "Panduleni Nekundi",
      "match_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Panduleni Nekundi - Performance Analysis",
      "rating": 8.5,
      "created_at": "2024-01-15T16:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

### Get Scouting Report

```http
GET /api/v1/scouting/reports/{report_id}
```

**Response:**
```json
{
  "id": "scout_report_001",
  "player_id": "660e8400-e29b-41d4-a716-446655440001",
  "player_name": "Panduleni Nekundi",
  "match_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Panduleni Nekundi - Performance Analysis",
  "notes": "Excellent pace and finishing ability",
  "rating": 8.5,
  "strengths": ["Speed", "Finishing", "Work rate"],
  "weaknesses": ["Aerial duels"],
  "recommendation": "Highly recommended for national team",
  "created_at": "2024-01-15T16:00:00Z",
  "updated_at": "2024-01-15T16:00:00Z"
}
```

### Search Players (Scouting)

```http
GET /api/v1/scouting/search
```

**Query Parameters:**
- `sport` (string): Filter by sport
- `position` (string): Filter by position
- `age_min` (integer): Minimum age
- `age_max` (integer): Maximum age
- `distance_min` (float): Minimum distance (km)
- `speed_min` (float): Minimum speed (km/h)
- `pass_accuracy_min` (float): Minimum pass accuracy (%)
- `team` (string): Filter by team
- `competition` (string): Filter by competition

**Response:**
```json
{
  "players": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Panduleni Nekundi",
      "team": "African Stars",
      "position": "Forward",
      "age": 29,
      "matches_analyzed": 15,
      "avg_stats": {
        "distance_km": 10.5,
        "speed_kmh": 8.2,
        "pass_accuracy_pct": 92.3
      },
      "scout_rating": 8.5
    }
  ],
  "total": 25
}
```

---

## Export

### Export CSV

```http
GET /api/v1/matches/{match_id}/export/csv
```

**Query Parameters:**
- `type` (string): Export type (`tracking`, `players`, `teams`, `passes`, `events`, `all`)
- `format` (string): CSV format (`standard`, `excel`)

**Response:** CSV file download

### Export JSON

```http
GET /api/v1/matches/{match_id}/export/json
```

**Query Parameters:**
- `include` (string): Comma-separated list (`tracking`, `players`, `teams`, `passes`, `events`)

**Response:**
```json
{
  "match": {...},
  "players": [...],
  "teams": {...},
  "passes": [...],
  "events": [...],
  "statistics": {...}
}
```

### Export PDF Report

```http
GET /api/v1/matches/{match_id}/export/pdf
```

**Query Parameters:**
- `sections` (string): Comma-separated list (`overview`, `players`, `teams`, `passes`, `events`)

**Response:** PDF file download

---

## Sync (Offline-First)

### Sync Matches

```http
POST /api/v1/sync/matches
Content-Type: application/json

{
  "last_sync": "2024-01-15T10:00:00Z",
  "device_id": "device_123"
}
```

**Response:**
```json
{
  "matches": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "updated_at": "2024-01-15T16:00:00Z",
      "data": {
        "name": "African Stars vs Black Africa",
        "status": "completed"
      }
    }
  ],
  "deleted": ["550e8400-e29b-41d4-a716-446655440001"],
  "sync_timestamp": "2024-01-15T16:30:00Z"
}
```

### Sync Players

```http
POST /api/v1/sync/players
Content-Type: application/json

{
  "last_sync": "2024-01-15T10:00:00Z",
  "device_id": "device_123"
}
```

**Response:**
```json
{
  "players": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "updated_at": "2024-01-15T16:00:00Z",
      "data": {
        "name": "Panduleni Nekundi",
        "stats": {...}
      }
    }
  ],
  "sync_timestamp": "2024-01-15T16:30:00Z"
}
```

### Upload Offline Data

```http
POST /api/v1/sync/upload
Content-Type: application/json

{
  "device_id": "device_123",
  "data": [
    {
      "type": "match",
      "action": "create",
      "data": {
        "name": "African Stars vs Black Africa",
        "date": "2024-01-15T15:00:00Z"
      },
      "timestamp": "2024-01-15T14:00:00Z"
    }
  ]
}
```

**Response:**
```json
{
  "synced": 5,
  "failed": 0,
  "conflicts": [],
  "sync_timestamp": "2024-01-15T16:30:00Z"
}
```

---

## Payments (Namibian Market)

### Initiate Payment (MTC Mobile Money)

```http
POST /api/v1/payments/initiate
Content-Type: application/json

{
  "amount": 500.00,
  "currency": "NAD",
  "payment_method": "mtc_mobile_money",
  "phone_number": "+264811234567",
  "description": "Monthly subscription",
  "return_url": "https://app.sportsvision.na/payment/success"
}
```

**Response:**
```json
{
  "payment_id": "payment_123",
  "status": "pending",
  "payment_url": "https://mtc-payment-gateway.na/pay/payment_123",
  "expires_at": "2024-01-15T17:00:00Z"
}
```

### Check Payment Status

```http
GET /api/v1/payments/{payment_id}
```

**Response:**
```json
{
  "payment_id": "payment_123",
  "status": "completed",
  "amount": 500.00,
  "currency": "NAD",
  "payment_method": "mtc_mobile_money",
  "transaction_id": "MTC_TXN_123456",
  "completed_at": "2024-01-15T16:15:00Z"
}
```

### List Payments

```http
GET /api/v1/payments
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `status` (string): Filter by status (`pending`, `completed`, `failed`)
- `date_from` (string): Filter from date
- `date_to` (string): Filter to date

**Response:**
```json
{
  "payments": [
    {
      "payment_id": "payment_123",
      "amount": 500.00,
      "currency": "NAD",
      "status": "completed",
      "payment_method": "mtc_mobile_money",
      "created_at": "2024-01-15T16:00:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "limit": 20
}
```

---

## Notifications (Namibian Market)

### Send WhatsApp Notification

```http
POST /api/v1/notifications/whatsapp
Content-Type: application/json

{
  "phone_number": "+264811234567",
  "message": "Your match analysis is ready! View it here: https://app.sportsvision.na/matches/123",
  "template_id": "match_ready_template"
}
```

**Response:**
```json
{
  "notification_id": "notif_123",
  "status": "sent",
  "message_id": "WA_MSG_123456",
  "sent_at": "2024-01-15T16:30:00Z"
}
```

### Send SMS Notification

```http
POST /api/v1/notifications/sms
Content-Type: application/json

{
  "phone_number": "+264811234567",
  "message": "Your match analysis is ready! View: https://app.sportsvision.na/matches/123"
}
```

**Response:**
```json
{
  "notification_id": "notif_124",
  "status": "sent",
  "message_id": "SMS_123456",
  "sent_at": "2024-01-15T16:30:00Z"
}
```

### List Notifications

```http
GET /api/v1/notifications
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `type` (string): Filter by type (`whatsapp`, `sms`, `email`)
- `status` (string): Filter by status (`sent`, `failed`, `pending`)

**Response:**
```json
{
  "notifications": [
    {
      "id": "notif_123",
      "type": "whatsapp",
      "phone_number": "+264811234567",
      "message": "Your match analysis is ready!",
      "status": "sent",
      "sent_at": "2024-01-15T16:30:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

---

## User & Profile

### Get User Profile

```http
GET /api/v1/user/profile
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "organization": "UNAM",
  "campus": "Windhoek Main",
  "phone_number": "+264811234567",
  "subscription": {
    "plan": "pro",
    "status": "active",
    "expires_at": "2024-12-31T23:59:59Z"
  },
  "preferences": {
    "language": "en",
    "sport": "football",
    "notifications": {
      "whatsapp": true,
      "sms": false,
      "email": true
    }
  }
}
```

### Update User Profile

```http
PATCH /api/v1/user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Doe",
  "phone_number": "+264811234567",
  "preferences": {
    "language": "af",
    "sport": "basketball"
  }
}
```

**Response:**
```json
{
  "message": "Profile updated successfully"
}
```

### Change Password

```http
POST /api/v1/user/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

---

## Settings

### Get User Settings

```http
GET /api/v1/settings
Authorization: Bearer <token>
```

**Response:**
```json
{
  "notifications": {
    "whatsapp": true,
    "sms": false,
    "email": true,
    "match_completed": true,
    "processing_failed": true
  },
  "data_quality": {
    "image_quality": "medium",
    "video_quality": "480p",
    "compact_mode": false
  },
  "language": "en",
  "timezone": "Africa/Windhoek"
}
```

### Update User Settings

```http
PATCH /api/v1/settings
Authorization: Bearer <token>
Content-Type: application/json

{
  "notifications": {
    "whatsapp": true,
    "sms": true
  },
  "data_quality": {
    "image_quality": "low",
    "compact_mode": true
  },
  "language": "af"
}
```

**Response:**
```json
{
  "message": "Settings updated successfully"
}
```

---

## UNAM-Specific Endpoints

### Get UNAM Campus Teams

```http
GET /api/v1/unam/campuses/{campus_id}/teams
```

**Response:**
```json
{
  "campus_id": "windhoek_main",
  "campus_name": "Windhoek Main Campus",
  "teams": [
    {
      "team_id": "team_unam_fc",
      "name": "UNAM FC",
      "sport": "football",
      "competition": "Debmarine Namibia Premiership"
    },
    {
      "team_id": "team_unam_wolves",
      "name": "UNAM Wolves",
      "sport": "basketball",
      "competition": "KBA League"
    }
  ]
}
```

### Get UNAM Multi-Campus Statistics

```http
GET /api/v1/unam/statistics
```

**Query Parameters:**
- `campus` (string): Filter by campus
- `sport` (string): Filter by sport
- `date_from` (string): Filter from date
- `date_to` (string): Filter to date

**Response:**
```json
{
  "total_matches": 150,
  "total_players": 500,
  "campuses": [
    {
      "campus_id": "windhoek_main",
      "matches": 50,
      "players": 200
    }
  ],
  "sports": [
    {
      "sport": "football",
      "matches": 80,
      "players": 300
    }
  ]
}
```

---

## WebSocket

### Real-Time Match Updates

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/matches/{match_id}/stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};

// Message format:
{
  "type": "processing_update",
  "progress": 65,
  "current_step": "Calculating statistics",
  "timestamp": "2024-01-15T16:00:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Common Error Codes

- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

---

## Rate Limiting

API requests are rate-limited:
- **Authenticated users:** 1000 requests/hour
- **Unauthenticated:** 100 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)

**Response Headers:**
```
X-Total-Count: 100
X-Page: 1
X-Per-Page: 20
X-Total-Pages: 5
```

---

## Versioning

API versioning is done via URL path:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

---

## OpenAPI/Swagger Documentation

Interactive API documentation available at:
- Development: `http://localhost:8000/docs`
- Staging: `https://staging-api.sportsvision.na/docs`
- Production: `https://api.sportsvision.na/docs`
- UNAM Pilot: `https://unam-api.sportsvision.na/docs`

---

## API Client Libraries

### JavaScript/TypeScript

```typescript
// Example API client setup
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Python

```python
# Example Python client
import requests

BASE_URL = "http://localhost:8000/api/v1"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(f"{BASE_URL}/matches", headers=headers)
matches = response.json()
```

## SDK Development

Future SDKs will be available for:
- JavaScript/TypeScript (npm)
- Python (PyPI)
- Go (Go modules)
- Ruby (RubyGems)

## API Versioning Strategy

- **Current Version:** v1
- **Versioning Method:** URL path (`/api/v1/`)
- **Backward Compatibility:** Maintained for at least 6 months
- **Deprecation Policy:** 3 months notice before breaking changes

## Rate Limiting Details

Rate limits are enforced per API key/user:
- **Tier 1 (Free):** 100 requests/hour
- **Tier 2 (Pro):** 1,000 requests/hour
- **Tier 3 (Enterprise):** 10,000 requests/hour

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Error Handling Best Practices

1. **Always check status codes** before processing responses
2. **Handle rate limiting** with exponential backoff
3. **Implement retry logic** for transient errors (5xx)
4. **Log errors** with request context for debugging
5. **Use error codes** for programmatic error handling

## Webhook Integration

Webhooks allow real-time notifications for:
- Match processing completion
- Error notifications
- Status updates

**Webhook Setup:**
```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["match.completed", "match.failed"],
  "secret": "your_webhook_secret"
}
```

## API Changelog

### Version 1.0 (December 2024)
- Initial API release
- Match management endpoints
- Player and team analytics
- Export functionality
- WebSocket support for real-time updates

### Version 2.0 (January 2025)
- Namibian market optimizations
- Offline-first sync endpoints (`/api/v1/sync/*`)
- Compact response mode (`?compact=true`)
- Network-aware responses (3G optimization)

### Version 2.1 (January 2025)
- Delta updates for bandwidth savings
- Multi-sport support (8 sports: Football, Basketball, Rugby, Netball, Hockey, Cricket, Tennis, Volleyball)
- UNAM institutional endpoints (multi-campus support)
- Response compression (gzip/brotli, 80% reduction)
- Namibian server deployment (MTC Windhoek data center)
- Connection keep-alive for 3G latency reduction
- Graceful timeout handling (30s for 3G networks)
- Tournament endpoints (MTC Maris Cup, league standings)
- Scouting endpoints (player search, reports)
- Payment endpoints (MTC Mobile Money integration)
- Notification endpoints (WhatsApp Business API, SMS via Africa's Talking)
- User profile and settings endpoints
- Comprehensive sync endpoints for offline-first support

---

**Document Status:** ✅ COMPREHENSIVE - API READY  
**Last Updated:** January 2025  
**API Version:** 2.1 (Namibian Market Focus)  
**Next Review:** Post-launch (Month 3)

---

**For implementation examples, see:**
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Regulatory compliance, offline requirements
- [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md) - Setup guide
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Client-side integration
- [Architecture Documentation](architecture.md) - Infrastructure and network resilience
- [UNAM 13 Campuses Strategy](UNAM_13_CAMPUSES_STRATEGY.md) - Enterprise API usage patterns

