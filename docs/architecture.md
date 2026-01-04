# Architecture Documentation

**Version:** 2.1 (Namibian Market Focus)  
**Last Updated:** January 2025  
**Primary Market:** 🇳🇦 Namibia (Africa)  
**Currency:** N$ (Namibian Dollar)

## System Architecture

The sports analytics pipeline follows a modular, layered architecture designed for maintainability, testability, and extensibility, with specific optimizations for the Namibian market including offline-first operation, low-bandwidth optimization, and multi-sport support.

**Namibian Deployment:**
- **Primary Hosting:** MTC Cloud Servers (Windhoek, Namibia)
- **Target Users:** UNAM, MTC Maris Cup, Debmarine Premiership, NFA
- **Network Optimization:** 3G/4G/5G support with offline-first design
- **Sports Supported:** Football, Basketball, Rugby, Netball, Hockey, Cricket, Tennis, Volleyball

**Related Documentation:**
- [API Documentation](API_DOCUMENTATION.md) - API endpoints and integration
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Web dashboard architecture
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Product requirements
- [UI/UX Design Documentation](UI_UX_DESIGN.md) - Complete design system
- [Feature Roadmap](FEATURE_ROADMAP.md) - Extended features

---

## 🇳🇦 Namibian Architecture Enhancements

### Edge Computing for Stadiums
**Problem:** Limited connectivity at Dr Hage Geingob Stadium and remote venues  
**Solution:** Local processing + batch upload

```
┌─────────────────────────────────────┐
│  Stadium (Dr Hage Geingob)         │
│  ┌───────────────────────────────┐ │
│  │ Local Server (Raspberry Pi 5) │ │
│  │ - Video recording             │ │
│  │ - Basic stats calculation     │ │
│  │ - Local storage (1TB SSD)     │ │
│  │ - WiFi hotspot                │ │
│  └──────────┬────────────────────┘ │
│             │ Batch Upload          │
└─────────────┼───────────────────────┘
              │ (When 4G/5G available)
              ▼
     ┌────────────────────┐
     │ MTC Cloud (Windhoek)│
     │ Full processing     │
     └────────────────────┘
```

### Offline-First Synchronization

```
Mobile App (Coach's Phone)
    ↓ (Offline Mode)
Queue Requests Locally
    ↓ (When Online)
Intelligent Sync:
  1. Priority: Stats & Events (< 1MB)
  2. Medium: Images & Heatmaps (< 10MB)
  3. Low: Video Highlights (WiFi only)
```

### Multi-Sport Processing Pipeline

```
Universal Input
    ↓
Sport Detection (AI Classification)
    ↓
Sport-Specific Config Loaded
    ↓
Detection (YOLOv8 - Sport Model)
    ↓
Tracking (ByteTrack)
    ↓
Sport-Specific Analytics
    ↓
Universal Component Rendering
```

### Infrastructure Resilience (Namibian Context)

#### Load Shedding & Power Management

**Problem:** Namibia experiences load shedding 2-3 times per week (2-4 hours per session)

**Power Supply Chain:**
```
National Grid (NamPower)
    ↓ (Primary, 99.5% uptime Windhoek CBD)
UPS System (10-minute backup)
    ↓ (Seamless switchover <5ms)
Diesel Generator (48-hour capacity)
    ↓ (Kicks in after 5 minutes)
Solar Backup (Future expansion)
    ↓ (20kW array, N$300K investment)
```

**Tier 1: MTC Data Center (Windhoek)**
- **Primary Power:** National grid (Windhoek CBD, 99.5% reliability)
- **UPS:** 10-minute battery backup (N$50,000)
- **Generator:** Diesel, 48-hour continuous operation (N$150,000)
- **Fuel Storage:** 500L tank (refilled weekly)
- **SLA:** 99.9% uptime (max 4.4 hours downtime/year)

**Tier 2: Stadium Deployments (Match Day)**
- **Equipment:** Raspberry Pi 5 + 4TB SSD + 4G/5G modem
- **Power:**
  - Primary: Stadium grid (unreliable, especially rural venues)
  - Secondary: 12V deep-cycle battery (8-hour runtime, N$1,500)
  - Tertiary: 100W portable solar panel (N$2,000)
  - Total kit cost: N$8,000
- **Monitoring:** SMS alert when battery <30% (via MTC SIM)
- **Graceful Shutdown:** Auto-save all data when battery <10%
- **Post-Match Upload:** Batch upload when grid restored

**Tier 3: Mobile App (Battery Optimization)**
- **Target:** 6 hours continuous use on single charge
- **Techniques:**
  - Low-power mode (disable animations, reduce polling)
  - Background sync: WiFi-only default
  - Video: 480p default, 720p WiFi only
  - Auto-dim: Screen brightness reduction after 30 seconds
- **"Match Day Mode":** All non-essential features disabled

#### Network Connectivity & Failover

**Primary Internet Providers:**

**MTC (Mobile Telecommunications) - 60% Market Share**
- **Coverage:** 98% population, 85% geographic
- **Technologies:**
  - 5G: Windhoek CBD only (10km radius) - 100-300 Mbps
  - 4G LTE: Major cities - 5-50 Mbps
  - 3G: Nationwide - 1-5 Mbps
  - 2G: Remote areas - 0.1-0.5 Mbps
- **Data Costs:**
  - 1GB: N$99 (standard)
  - 50GB: N$999 (N$19.98/GB) ← Target for clubs
  - Unlimited: N$1,499/month (200GB FUP)

**TN Mobile (Telecom Namibia) - 30% Market Share**
- **Coverage:** 95% population, 75% geographic
- **Technologies:** 4G (major cities), 3G (rest)
- **Use Case:** Backup SIM cards for redundancy

**Connectivity Strategy:**
```
┌──────────────────────────────┐
│   MTC 5G/4G (Primary)        │
│   - Bonded 2-3 modems        │
│   - Automatic load balancing │
└──────────┬───────────────────┘
           ↓ (Failover if down >5 min)
┌──────────────────────────────┐
│   TN Mobile 4G (Secondary)   │
│   - Automatic switchover     │
└──────────┬───────────────────┘
           ↓ (If both fail)
┌──────────────────────────────┐
│   Starlink (Tertiary, Future)│
│   - N$5K setup + N$1K/month  │
└──────────┬───────────────────┘
           ↓ (Last resort)
┌──────────────────────────────┐
│   Offline Mode               │
│   - Queue all operations     │
│   - Sync when reconnected    │
└──────────────────────────────┘
```

**Office/Server Connectivity:**
- **Primary:** MTC Fiber 100 Mbps (N$5,000/month)
- **Secondary:** Paratus Fixed LTE 50 Mbps (N$2,500/month)
- **Monitoring:** Pingdom, UptimeRobot (alert if down >5 min)

**Stadium Match Day:**
- **Primary:** MTC 4G/5G (bonded, 2-3 modems for redundancy)
- **Secondary:** TN Mobile 4G (automatic failover)
- **Tertiary:** Starlink (if available, N$5K setup + N$1K/month)
- **Quaternary:** Offline mode (sync post-match)

#### Hardware Specifications (Namibian Market)

**Minimum Device Requirements:**
- **Mobile:** Android 8+ (70% market: Samsung A-series, Huawei, Xiaomi)
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB app + 5GB for offline data
- **Camera:** For match recording by coaches
- **Screen:** 5.5" minimum (usability)

**Stadium Equipment (Per Venue):**
- **Raspberry Pi 5:** Local processing (N$2,500)
- **4TB External SSD:** Video storage (N$3,000)
- **Portable WiFi Router:** TP-Link/Ubiquiti (N$1,500)
- **12V Deep-Cycle Battery:** 8-hour backup (N$1,500)
- **100W Solar Panel:** Portable (N$2,000)
- **4G/5G Modem:** MTC + TN Mobile SIMs (N$1,000)
- **Total Kit Cost:** N$11,500 per stadium

**Office Equipment:**
- **Laptops:** MacBook Pro / Dell XPS (N$25K each, 3-year replacement)
- **Monitors:** 27" 4K (N$5K each)
- **Server:** Dedicated (hosted at MTC data center)
- **Networking:** UPS for office router (N$3K)

#### Disaster Recovery & Business Continuity

**RTO (Recovery Time Objective):** 4 hours
**RPO (Recovery Point Objective):** 1 hour (max data loss)

**Backup Strategy:**
- **Primary:** MTC Windhoek (live database)
- **Secondary:** Cape Town, South Africa (hourly replication)
- **Tertiary:** Cloudflare R2 (EU, daily backups)
- **Frequency:**
  - Database: Real-time replication (streaming)
  - Files: Hourly incremental, daily full
  - Configuration: On change (version controlled)

**Failover Testing:**
- **Quarterly:** Simulated data center failure
- **Monthly:** Database restore drill
- **Weekly:** Backup verification

**Incident Response Plan:**
1. **Detection:** Auto-alert via monitoring (Datadog, New Relic)
2. **Assessment:** On-call engineer (5-minute response)
3. **Communication:** Status page update (status.sportsvision.na)
4. **Resolution:** Failover to Cape Town if Windhoek down
5. **Post-Mortem:** Document incident, improve processes

---

## Architecture Layers

### 1. Input Layer
- **Video Input**: Reads video files using OpenCV
- **Configuration**: Loads field calibration and settings
- **Model Loading**: Loads YOLOv8 detection model

### 2. Detection & Tracking Layer
- **Object Detection**: YOLOv8 for player, ball, referee detection
- **Multi-Object Tracking**: ByteTrack for persistent ID tracking
- **Jersey Recognition**: EasyOCR for jersey number detection

### 3. Processing Layer
- **Team Assignment**: Color clustering for team identification
- **Ball Assignment**: Proximity-based ball possession
- **Camera Compensation**: Optical flow for camera movement
- **Perspective Transformation**: Pixel to field coordinate conversion
- **Speed/Distance Calculation**: Player movement metrics

### 4. Analytics Layer
- **Pass Detection**: Automatic pass identification
- **Event Detection**: Sprint, cluster, and trajectory events
- **Heatmap Generation**: Position-based heatmaps
- **Statistics Calculation**: Player, team, and match statistics

### 5. Visualization Layer
- **Annotation Drawing**: Video frame annotations
- **Pass Networks**: Visual pass pattern representation
- **Zone Statistics**: Field zone analysis
- **Report Generation**: Text and visual reports

### 6. Export Layer
- **CSV Export**: Structured data export
- **JSON Export**: Machine-readable data
- **Report Export**: Human-readable reports
- **Video Export**: Annotated video output

## Data Flow

```
Video Input
    ↓
Detection (YOLO)
    ↓
Tracking (ByteTrack)
    ↓
Team Assignment
    ↓
Ball Assignment
    ↓
Camera Compensation
    ↓
Perspective Transformation
    ↓
Speed/Distance Calculation
    ↓
Analytics (Passes, Events, Stats)
    ↓
Visualization
    ↓
Export (CSV, JSON, Reports, Video)
```

## Module Dependencies

```
analytics/
├── jersey_tracker.py
│   ├── utils.field_mask
│   ├── utils.jersey_detector
│   ├── utils.position_utils
│   └── utils.annotation_drawer
│
├── heatmap_generator.py
│   └── (standalone)
│
├── pass_detector.py
│   └── (standalone)
│
└── statistics_engine.py
    ├── utils.statistics_calculator
    ├── utils.statistics_exporter
    └── utils.report_generator
```

## Design Patterns

### 1. Modular Design
Each module has a single responsibility and can be used independently.

### 2. Dependency Injection
Components receive dependencies through constructors for testability.

### 3. Factory Pattern
Utility modules provide factory functions for common operations.

### 4. Strategy Pattern
Different algorithms (e.g., color clustering) can be swapped.

## Performance Considerations

- **Chunked Processing**: Videos processed in chunks to manage memory
- **Caching**: Camera movement and other computations cached
- **Batch Processing**: YOLO inference batched for efficiency
- **Lazy Loading**: Models loaded only when needed

## Extension Points

1. **New Event Types**: Add to `event_detector.py`
2. **New Statistics**: Extend `statistics_calculator.py`
3. **New Visualizations**: Add to `visualizations.py`
4. **New Export Formats**: Extend `statistics_exporter.py`
5. **New Tracking Algorithms**: Implement in `jersey_tracker.py`
6. **New Sports**: Implement sport-specific modules using the modular sport engine
7. **Custom Analytics**: Extend `analytics/` directory with new analysis modules

## Integration with Web Dashboard

The analytics pipeline integrates with the web dashboard through:

1. **FastAPI Backend** (`api/` directory)
   - RESTful endpoints for match management
   - Analytics data retrieval
   - Real-time processing status updates
   - WebSocket support for live updates

2. **Data Storage**
   - CSV/JSON exports in `output_videos/` directory
   - Database integration (optional) for persistent storage
   - File-based storage for heatmaps and visualizations

3. **Processing Pipeline**
   - Asynchronous processing for video analysis
   - Background job queue (Celery or similar)
   - Progress tracking and status updates

For detailed web dashboard architecture, see [Frontend Architecture](FRONTEND_ARCHITECTURE.md).

## Configuration Management

The system uses a centralized configuration approach:

- **`config/settings.py`**: Global settings and paths
- **`config/field_config.json`**: Field calibration data
- **Environment Variables**: For sensitive configuration

See the main [README](../README.md) for configuration details.

## Testing Architecture

- **Unit Tests**: `tests/` directory with test files for each module
- **Integration Tests**: End-to-end pipeline testing
- **API Tests**: FastAPI endpoint testing
- **Frontend Tests**: React component testing

## Deployment Architecture

- **Backend**: FastAPI with uvicorn/gunicorn
- **Frontend**: Next.js with static export or SSR
- **Processing**: Background workers for video analysis
- **Storage**: File system or cloud storage (S3, etc.)

For deployment details, see [Web Dashboard Quick Start](WEB_DASHBOARD_QUICKSTART.md).

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial architecture documentation |
| 1.1 | December 2024 | Added web dashboard integration |
| 2.0 | January 2025 | Namibian market optimizations (offline-first, multi-sport) |
| 2.1 | January 2025 | Infrastructure resilience (load shedding, power backup, connectivity failover), disaster recovery (RTO 4hrs, RPO 1hr), hardware specifications (stadium kits N$11.5K), network optimization (MTC 60%, TN Mobile 30% backup) |

**Major Updates in v2.1:**
- ✅ Load shedding mitigation strategy (UPS, generators, solar backup)
- ✅ Network failover chain (MTC → TN Mobile → Starlink → Offline)
- ✅ Stadium edge computing (Raspberry Pi 5, battery backup, graceful shutdown)
- ✅ Disaster recovery procedures (hourly backups, quarterly testing)
- ✅ Hardware specifications for Namibian market (Android 8+, 2GB RAM minimum)
- ✅ Power resilience for 99.9% uptime (despite 2-3× weekly load shedding)

---

**Related Documentation:**
- [PRD - Web Dashboard](PRD_WEB_DASHBOARD.md) - Regulatory compliance, financial analysis, market research
- [API Documentation](API_DOCUMENTATION.md) - Offline-first sync endpoints
- [Frontend Architecture](FRONTEND_ARCHITECTURE.md) - Localization (Oshiwambo), PWA implementation
- [Feature Roadmap](FEATURE_ROADMAP.md) - Namibian launch features
- [UNAM 13 Campuses Strategy](UNAM_13_CAMPUSES_STRATEGY.md) - Anchor client strategy

---

**Document Status:** ✅ COMPREHENSIVE - INFRASTRUCTURE READY  
**Last Updated:** January 2025  
**Version:** 2.1 (Namibian Infrastructure Focus)

