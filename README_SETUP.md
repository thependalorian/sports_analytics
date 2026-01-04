# Sports Analytics - Setup Guide

**Date:** 2026-01-04  
**Version:** 2.1.0  
**Market:** 🇳🇦 Namibia  
**Repository:** [https://github.com/thependalorian/sports_analytics](https://github.com/thependalorian/sports_analytics)

---

## 🚀 Quick Start

### 0. Clone Repository (First Time Setup)

```bash
# Clone the repository
git clone https://github.com/thependalorian/sports_analytics.git
cd sports_analytics

# Install Git LFS (if not already installed)
# macOS: brew install git-lfs
# Linux: sudo apt install git-lfs
# Windows: choco install git-lfs

# Initialize Git LFS
git lfs install

# Pull large model files from LFS
git lfs pull
```

**Note:** This repository uses Git LFS for large model files. See [Git LFS Setup](#git-lfs-setup) section below.

### 1. Activate Virtual Environment

```bash
cd sports_analytics
source sva/bin/activate
# Or use the helper script:
source activate_sva.sh
```

### 2. Setup Database

```bash
python scripts/setup_database.py
```

This will:
- ✅ Create LanceDB tables
- ✅ Register tables with DuckDB for SQL analytics
- ✅ Verify database health

### 3. Start Services

**Option A: FastAPI Server (Backend API)**
```bash
./scripts/start_api.sh
# Or manually:
uvicorn api.main:app --reload
```

**Option B: Streamlit App (UI Dashboard)**
```bash
./scripts/start_streamlit.sh
# Or manually:
streamlit run streamlit_app.py
```

---

## 📦 Architecture

### Database Stack

```
┌─────────────┐
│  LanceDB    │  ← Efficient storage (vector + structured)
│  (Storage)  │
└──────┬──────┘
       │ Apache Arrow (zero-copy)
       ↓
┌─────────────┐
│   DuckDB    │  ← SQL analytics engine
│  (Analytics)│
└─────────────┘
```

### Technology Stack

- **Backend:** FastAPI (Python)
- **Database:** LanceDB + DuckDB (via Apache Arrow)
- **UI:** Streamlit
- **Vector Search:** LanceDB native
- **SQL Analytics:** DuckDB
- **PDF Export:** ReportLab
- **Notifications:** Twilio (WhatsApp) + Africa's Talking (SMS)
- **Payments:** MTC Mobile Money + Bank Windhoek APIs

---

## 🗄️ Database Setup

### LanceDB Tables

The following tables are created automatically:

- `users` - User accounts
- `matches` - Match data
- `players` - Player profiles
- `teams` - Team information
- `tournaments` - Tournament data
- `player_statistics` - Player performance metrics

### Using DuckDB for Analytics

```python
from api.lib.lancedb_adapter import get_lancedb

lancedb = get_lancedb()

# Register table
lancedb.register_lancedb_table("matches", "matches_view")

# Execute SQL
result = lancedb.execute_sql("""
    SELECT sport, COUNT(*) as total
    FROM matches_view
    WHERE status = 'completed'
    GROUP BY sport
""")
```

See `docs/DUCKDB_LANCEDB_INTEGRATION.md` for more examples.

---

## 🔧 Environment Variables

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/sports_analytics
LANCEDB_PATH=./data/lancedb

# API
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:8501

# Email (for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@sportsvision.na
FRONTEND_URL=http://localhost:3000

# Payments (Namibian)
MTC_MOBILE_MONEY_API_URL=https://api.mtc.na/mobile-money
MTC_MOBILE_MONEY_API_KEY=your-mtc-api-key
BANK_WINDHOEK_API_URL=https://api.bankwindhoek.na
BANK_WINDHOEK_API_KEY=your-bank-api-key

# Notifications
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
AFRICAS_TALKING_API_KEY=your-africas-talking-key
AFRICAS_TALKING_USERNAME=your-username
SMS_SENDER_ID=SportsVision
```

---

## 📊 API Endpoints

Once FastAPI is running, access:

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

### Key Endpoints

- `GET /api/v1/matches` - List matches
- `GET /api/v1/players` - List players
- `GET /api/v1/teams` - List teams
- `GET /api/v1/tournaments` - List tournaments
- `GET /api/v1/analytics/*` - Analytics endpoints
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

See `docs/API_DOCUMENTATION.md` for complete API reference.

---

## 🎨 Streamlit Dashboard

Access at: http://localhost:8501

**Features:**
- 📊 Dashboard overview
- 🏆 Match management
- 👤 Player profiles
- 🏅 Team information
- 🏆 Tournament tracking
- 📈 Analytics & visualizations
- ⚙️ Settings & database status

---

## ✅ Implemented Features

All TODOs have been implemented with **real functionality** (no mocks):

- ✅ Match processing status tracking with time estimation
- ✅ Conflict detection and resolution for offline sync
- ✅ Player and team sync operations
- ✅ PDF export with ReportLab
- ✅ MTC Mobile Money payment integration
- ✅ Bank Windhoek payment integration
- ✅ WhatsApp notifications via Twilio
- ✅ SMS notifications via Africa's Talking
- ✅ Password reset with email
- ✅ UNAM campus details and multi-campus analytics
- ✅ Tournament position calculation
- ✅ Player/team sorting with match statistics
- ✅ Database health checks (LanceDB + DuckDB)
- ✅ DuckDB SQL analytics integration

---

## 🧪 Testing

```bash
# Run database setup
python scripts/setup_database.py

# Test LanceDB connection
python -c "from api.lib.lancedb_adapter import get_lancedb; print(get_lancedb().health_check())"

# Test DuckDB integration
python -c "from api.lib.lancedb_adapter import get_lancedb; l = get_lancedb(); l.register_lancedb_table('matches'); print(l.execute_sql('SELECT COUNT(*) FROM matches'))"
```

---

## 📚 Documentation

- **Architecture:** `docs/architecture.md`
- **API Reference:** `docs/API_DOCUMENTATION.md`
- **Database Schema:** `docs/DATABASE_SCHEMA.md`
- **Frontend Guide:** `docs/FRONTEND_ARCHITECTURE.md`
- **UI/UX Design:** `docs/UI_UX_DESIGN.md`
- **DuckDB Integration:** `docs/DUCKDB_LANCEDB_INTEGRATION.md`
- **Namibian Market:** `docs/NAMIBIAN_MARKET_SUMMARY.md`

---

## 📦 Git LFS Setup

This repository uses **Git LFS (Large File Storage)** for model files to efficiently handle large files (>50MB).

### Installation

**macOS:**
```bash
brew install git-lfs
git lfs install
```

**Linux:**
```bash
sudo apt install git-lfs  # Ubuntu/Debian
git lfs install
```

**Windows:**
```bash
choco install git-lfs  # Using Chocolatey
git lfs install
```

### Files Tracked by LFS

- `models/**/*.pth` - EasyOCR model files
- `models/**/*.pt` - YOLO model files (e.g., `yolo11x.pt`)

### Cloning with LFS

```bash
git clone https://github.com/thependalorian/sports_analytics.git
cd sports_analytics
git lfs pull  # Download LFS-tracked files
```

### Verifying LFS Files

```bash
# Check LFS status
git lfs ls-files

# Should show:
# models/easyocr/craft_mlt_25k.pth
# models/easyocr/english_g2.pth
# models/yolo11x.pt
```

## 🐛 Troubleshooting

### Git LFS Issues

```bash
# If LFS files show as pointers instead of actual files:
git lfs pull

# Verify LFS is working:
git lfs version

# Re-initialize if needed:
git lfs install
```

### Database Connection Issues

```bash
# Check LanceDB health
python -c "from api.lib.lancedb_adapter import get_lancedb; print(get_lancedb().health_check())"

# Verify database path
ls -la data/lancedb/
```

### Import Errors

```bash
# Ensure virtual environment is activated
source sva/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Change port in start scripts or use:
uvicorn api.main:app --port 8001
streamlit run streamlit_app.py --server.port 8502
```

---

## 🎯 Next Steps

1. ✅ Database setup complete
2. ✅ All TODOs implemented
3. ✅ DuckDB + LanceDB integrated
4. 🔄 **Run migrations:** `python scripts/setup_database.py`
5. 🔄 **Start API:** `./scripts/start_api.sh`
6. 🔄 **Start UI:** `./scripts/start_streamlit.sh`
7. 🔄 **Add sample data** (optional)
8. 🔄 **Configure environment variables**

---

## 📞 Support

For issues or questions:
- Check documentation in `docs/` folder
- Review API docs at `/docs` endpoint
- Check logs in console output

---

**Ready to go! 🚀**

