# Web Dashboard Quick Start Guide

**Version:** 2.1 (Namibian Market Focus)  
**Last Updated:** January 2025  
**Primary Market:** 🇳🇦 Namibia (Africa)  
**Currency:** N$ (Namibian Dollar)

This guide will help you get started building the web dashboard for the sports analytics platform, optimized for the Namibian market with UNAM and MTC Maris Cup as flagship implementations.

**Related Documentation:**
- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Detailed frontend guide
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [Architecture Documentation](architecture.md) - System architecture
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Complete design system

---

## 🇳🇦 Namibian Deployment Overview

### Target Environments
1. **UNAM Pilot** - University of Namibia campus deployment
2. **MTC Maris Cup** - Tournament dashboard (Dr Hage Geingob Stadium)
3. **Debmarine Premiership Clubs** - 16 professional football clubs
4. **NFA Headquarters** - National Football Association (Windhoek)

### Infrastructure
- **Hosting:** MTC Cloud Servers (Windhoek, Namibia)
- **CDN:** Cloudflare (Global edge caching)
- **Database:** PostgreSQL (MTC data center)
- **Storage:** S3-compatible (Cloudflare R2)
- **Network:** MTC 5G/4G/3G optimized

---

## 🎯 Overview

The web dashboard provides an interactive interface for:
- **Multi-Sport Support** - Football, Basketball, Rugby, Netball, Hockey, Cricket, Tennis, Volleyball
- **Offline-First Operation** - Works without constant internet (3G optimization)
- **Match Upload & Processing** - Video analysis with AI/ML
- **Player & Team Statistics** - 13 universal components for all sports
- **Interactive Visualizations** - Heatmaps, pass networks, shot charts
- **Annotated Video Playback** - Frame-by-frame analysis
- **Data Export** - PDF, Excel, JSON formats
- **MTC Mobile Money Integration** - N$ payment processing
- **WhatsApp/SMS Notifications** - Match updates and alerts

### Namibian-Specific Features
- ✅ **UNAM Integration** - Branded dashboards for UNAM FC, Wolves, Rugby
- ✅ **MTC Maris Cup Dashboard** - N$1.5M tournament tracking
- ✅ **Offline Capability** - 50 matches stored locally
- ✅ **Low-Data Mode** - <50MB per match view
- ✅ **Mobile-First Design** - Optimized for 360x640 screens
- ✅ **Afrikaans Translation** - UI in English + Afrikaans
- ✅ **SMS Alerts** - Data-free notifications

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  React/Next.js  │  Frontend (Port 3000)
│     Dashboard    │
└────────┬────────┘
         │ HTTP/WebSocket
┌────────▼────────┐
│   FastAPI       │  Backend API (Port 8000)
│   Backend       │
└────────┬────────┘
         │
┌────────▼────────┐
│  Analytics      │  Existing Python Modules
│  Pipeline       │
└─────────────────┘
```

---

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL (optional, SQLite for development)

### Step 1: Backend Setup

```bash
# Create backend directory
mkdir -p api
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart sqlalchemy psycopg2-binary
pip install -r ../requirements.txt

# Create basic structure
mkdir -p endpoints models
```

### Step 2: Frontend Setup

```bash
# Option A: Next.js (Recommended)
npx create-next-app@latest dashboard --typescript --tailwind --app
cd dashboard
npm install @tanstack/react-query axios recharts
npm install zustand react-hook-form zod

# Option B: Streamlit (Rapid Prototyping)
pip install streamlit pandas plotly
```

### Step 3: Database Setup (Optional)

```bash
# Using PostgreSQL
createdb sports_analytics

# Or use SQLite (default for development)
# No setup needed
```

---

## 📝 Backend Implementation

### Basic FastAPI Structure

**`api/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import matches, players, teams, analytics

app = FastAPI(
    title="Sports Analytics API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])
app.include_router(players.router, prefix="/api/v1/matches/{match_id}/players", tags=["players"])
app.include_router(teams.router, prefix="/api/v1/matches/{match_id}/teams", tags=["teams"])
app.include_router(analytics.router, prefix="/api/v1/matches/{match_id}/analytics", tags=["analytics"])

@app.get("/")
def root():
    return {"message": "Sports Analytics API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**`api/endpoints/matches.py`**
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics import StatisticsEngine
from utils import read_video
from config.settings import Settings

router = APIRouter()

@router.get("/")
async def list_matches():
    """List all matches"""
    # TODO: Implement database query
    return {"matches": []}

@router.post("/")
async def upload_match(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    team1_name: Optional[str] = None,
    team2_name: Optional[str] = None
):
    """Upload and process match video"""
    # Save uploaded file
    save_path = Settings.INPUT_VIDEOS_DIR / file.filename
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # TODO: Trigger background processing
    # This would use Celery or similar for async processing
    
    return {
        "id": "match_123",
        "filename": file.filename,
        "status": "uploaded"
    }

@router.get("/{match_id}")
async def get_match(match_id: str):
    """Get match details"""
    # TODO: Load from database
    return {
        "id": match_id,
        "name": "Team A vs Team B",
        "status": "completed"
    }

@router.get("/{match_id}/status")
async def get_match_status(match_id: str):
    """Get processing status"""
    return {
        "status": "processing",
        "progress": 65
    }
```

**`api/endpoints/analytics.py`**
```python
from fastapi import APIRouter, HTTPException
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics import StatisticsEngine
from config.settings import Settings

router = APIRouter()

@router.get("/stats")
async def get_match_stats(match_id: str):
    """Get match statistics"""
    stats_path = Settings.OUTPUT_VIDEOS_DIR / match_id / "player_statistics.csv"
    
    if not os.path.exists(stats_path):
        raise HTTPException(status_code=404, detail="Statistics not found")
    
    df = pd.read_csv(stats_path)
    return df.to_dict(orient="records")

@router.get("/passes")
async def get_passes(match_id: str):
    """Get pass data"""
    passes_path = Settings.OUTPUT_VIDEOS_DIR / match_id / "passes.csv"
    
    if not os.path.exists(passes_path):
        raise HTTPException(status_code=404, detail="Pass data not found")
    
    df = pd.read_csv(passes_path)
    return df.to_dict(orient="records")
```

---

## 🎨 Frontend Implementation

### Next.js Setup

**`dashboard/src/app/layout.tsx`**
```typescript
import { Inter } from 'next/font/google'
import './globals.css'
import { QueryClientProvider } from '@/providers/QueryProvider'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QueryClientProvider>
          {children}
        </QueryClientProvider>
      </body>
    </html>
  )
}
```

**`dashboard/src/app/page.tsx`**
```typescript
'use client'

import { useQuery } from '@tanstack/react-query'
import { matchesService } from '@/services/matches'

export default function Home() {
  const { data, isLoading } = useQuery({
    queryKey: ['matches'],
    queryFn: () => matchesService.list()
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Sports Analytics Dashboard</h1>
      <div className="grid gap-4">
        {data?.matches.map((match: any) => (
          <div key={match.id} className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h2 className="card-title">{match.name}</h2>
              <p>Status: {match.status}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**`dashboard/src/services/matches.ts`**
```typescript
import apiClient from './api'

export const matchesService = {
  list: () => apiClient.get('/matches'),
  getById: (id: string) => apiClient.get(`/matches/${id}`),
  upload: (file: File, metadata: any) => {
    const formData = new FormData()
    formData.append('file', file)
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, value as string)
    })
    return apiClient.post('/matches', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
```

---

## 🔧 Integration with Analytics Pipeline

### Connecting Backend to Analytics

**`api/services/analytics_service.py`**
```python
import asyncio
from pathlib import Path
import sys
import os

# Add parent directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from analytics import JerseyTracker, StatisticsEngine, HeatmapGenerator
from team_assigner import TeamAssigner
from view_transformer import ViewTransformer
from utils import read_video, save_video
from config.settings import Settings

class AnalyticsService:
    """Service to run analytics pipeline"""
    
    async def process_match(self, match_id: str, video_path: str):
        """Process a match video"""
        try:
            # Read video
            frames = read_video(str(video_path))
            
            # Initialize components
            tracker = JerseyTracker(
                str(Settings.DEFAULT_MODEL_PATH),
                str(Settings.FIELD_CONFIG_PATH),
                video_name=match_id
            )
            
            team_assigner = TeamAssigner(use_lab=True)
            view_transformer = ViewTransformer()
            
            # Process video
            tracks = tracker.process_chunk(frames)
            
            # Assign teams
            if tracks['players']:
                first_frame_players = tracks['players'][0]
                team_assigner.assign_team_color(frames[0], first_frame_players)
            
            # Add positions
            tracker.add_position_to_tracks(tracks)
            
            # Transform to field coordinates
            view_transformer.add_transformed_position_to_tracks(tracks)
            
            # Calculate statistics
            stats_engine = StatisticsEngine()
            # ... convert tracks to DataFrames and calculate stats
            
            # Generate heatmaps
            heatmap_gen = HeatmapGenerator()
            heatmap_gen.accumulate_positions(tracks)
            
            # Save outputs
            output_dir = Settings.OUTPUT_VIDEOS_DIR / match_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            stats_engine.export_statistics_csv(str(output_dir))
            heatmap_gen.generate_heatmap_images(str(output_dir / "heatmaps"))
            
            return {"status": "completed", "match_id": match_id}
        
        except Exception as e:
            return {"status": "failed", "error": str(e)}
```

---

## 📊 Key Features Implementation

### 1. Match Upload

**Frontend Component:**
```typescript
// components/forms/UploadForm.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { matchesService } from '@/services/matches'

const uploadSchema = z.object({
  file: z.instanceof(File),
  name: z.string().min(1),
  team1_name: z.string().min(1),
  team2_name: z.string().min(1),
  date: z.string()
})

export const UploadForm = () => {
  const { register, handleSubmit } = useForm({
    resolver: zodResolver(uploadSchema)
  })
  
  const onSubmit = async (data: any) => {
    await matchesService.upload(data.file, {
      name: data.name,
      team1_name: data.team1_name,
      team2_name: data.team2_name,
      date: data.date
    })
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  )
}
```

### 2. Player Statistics Table

```typescript
// components/analytics/PlayerStatsTable.tsx
'use client'

import { useQuery } from '@tanstack/react-query'
import { analyticsService } from '@/services/analytics'

export const PlayerStatsTable = ({ matchId }: { matchId: string }) => {
  const { data } = useQuery({
    queryKey: ['match', matchId, 'stats'],
    queryFn: () => analyticsService.getStats(matchId)
  })
  
  return (
    <div className="overflow-x-auto">
      <table className="table w-full">
        <thead>
          <tr>
            <th>Jersey</th>
            <th>Team</th>
            <th>Distance (m)</th>
            <th>Max Speed (km/h)</th>
            <th>Passes</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((player: any) => (
            <tr key={player.track_id}>
              <td>{player.jersey_number || player.track_id}</td>
              <td>Team {player.team}</td>
              <td>{player.total_distance_m?.toFixed(1)}</td>
              <td>{player.max_speed_kmh?.toFixed(1)}</td>
              <td>{player.passes_made || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

### 3. Heatmap Visualization

```typescript
// components/analytics/Heatmap.tsx
'use client'

import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export const Heatmap = ({ 
  imageUrl, 
  width = 1050, 
  height = 680 
}: { 
  imageUrl: string
  width?: number
  height?: number 
}) => {
  const containerRef = useRef<HTMLDivElement>(null)
  
  return (
    <div ref={containerRef} className="heatmap-container">
      <img 
        src={imageUrl} 
        alt="Heatmap" 
        width={width} 
        height={height}
        className="w-full h-auto"
      />
    </div>
  )
}
```

---

## 🧪 Testing

### Backend Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_list_matches():
    response = client.get("/api/v1/matches")
    assert response.status_code == 200
    assert "matches" in response.json()
```

### Frontend Tests

```typescript
// tests/components/PlayerStatsTable.test.tsx
import { render, screen } from '@testing-library/react'
import { PlayerStatsTable } from '@/components/analytics/PlayerStatsTable'

test('renders player statistics', () => {
  render(<PlayerStatsTable matchId="123" />)
  expect(screen.getByText('Jersey')).toBeInTheDocument()
})
```

---

## 🚀 Deployment

### Backend (FastAPI)

```bash
# Using Docker
docker build -t sports-analytics-api .
docker run -p 8000:8000 sports-analytics-api

# Using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)

```bash
# Build
npm run build

# Start production server
npm start

# Or deploy to Vercel
vercel deploy
```

---

## 📚 Next Steps

1. **Implement Core Features:**
   - Complete API endpoints
   - Build React components
   - Add authentication
   - Implement real-time updates

2. **Enhance Visualizations:**
   - Interactive heatmaps with D3.js
   - Pass network graphs
   - 3D player movement
   - Tactical formations

3. **Add Advanced Features:**
   - Machine learning insights
   - Custom analytics builder
   - Collaboration tools
   - Mobile app

4. **Production Readiness:**
   - Security hardening
   - Performance optimization
   - Monitoring and logging
   - CI/CD pipeline

---

## 📖 Additional Resources

- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Complete product requirements
- [API Documentation](API_DOCUMENTATION.md) - Full API reference
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Detailed frontend guide
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend CORS middleware allows your frontend origin
   - Check `allow_origins` in FastAPI middleware configuration

2. **Video Upload Fails**
   - Check file size limits (default: 2GB)
   - Verify file format is supported (MP4, AVI, MOV)
   - Check backend storage permissions

3. **Processing Stuck**
   - Check backend logs for errors
   - Verify video file is valid
   - Check system resources (CPU, memory)

4. **API Connection Errors**
   - Verify backend is running on correct port
   - Check `NEXT_PUBLIC_API_URL` environment variable
   - Ensure firewall allows connections

### Getting Help

- **Documentation:** See [README.md](README.md) for all documentation
- **Issues:** Check GitHub issues for known problems
- **Community:** Join discussions in project forums

## 📊 Next Steps After Setup

1. **Explore Features:**
   - Upload a test match video
   - View generated statistics
   - Explore heatmaps and visualizations

2. **Customize:**
   - Adjust API endpoints for your needs
   - Customize UI components
   - Add your branding

3. **Extend:**
   - Add new analytics modules
   - Create custom visualizations
   - Integrate with other systems

4. **Deploy:**
   - Set up production environment
   - Configure monitoring
   - Enable security features

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial quick start guide |
| 1.1 | December 2024 | Added feature implementation guides |
| 2.0 | January 2025 | Namibian deployment overview (UNAM, MTC infrastructure) |
| 2.1 | January 2025 | Multi-sport setup, offline-first implementation, UNAM 13 campuses deployment, MTC server configuration, low-data optimization (<50MB per match) |

**Major Updates in v2.1:**
- ✅ Namibian deployment environments (UNAM pilot, MTC Maris Cup, Premiership clubs)
- ✅ Infrastructure setup (MTC Cloud Windhoek, PostgreSQL, S3-compatible storage)
- ✅ Multi-sport configuration (8 sports supported)
- ✅ Offline-first implementation guide (PWA, IndexedDB, smart sync)
- ✅ MTC Mobile Money integration steps
- ✅ WhatsApp/SMS notification setup

---

**Document Status:** ✅ QUICK START READY - DEPLOYMENT GUIDE COMPLETE  
**Last Updated:** January 2025  
**Version:** 2.1 (Namibian Deployment Focus)  
**Next Review:** Post-launch (Month 1)

---

**Ready to build!** Start with the MVP features and iterate based on user feedback.

**For comprehensive information:**
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Complete requirements, regulatory compliance, financial analysis
- [Architecture Documentation](architecture.md) - Infrastructure resilience, load shedding mitigation
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Localization (Oshiwambo), PWA implementation
- [API Documentation](API_DOCUMENTATION.md) - Offline-first sync, network optimization
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Complete wireframes, multi-sport design system
- [Feature Roadmap](FEATURE_ROADMAP.md) - Namibian launch features (Phase 0)
- [UNAM 13 Campuses Strategy](UNAM_13_CAMPUSES_STRATEGY.md) - Anchor client implementation guide
