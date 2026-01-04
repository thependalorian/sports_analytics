# 🚀 Quick Start Guide

**Date:** 2026-01-04  
**Status:** ✅ All systems ready  
**Repository:** [https://github.com/thependalorian/sports_analytics](https://github.com/thependalorian/sports_analytics)

---

## ⚡ Quick Setup

### 0. Clone Repository (First Time)

```bash
git clone https://github.com/thependalorian/sports_analytics.git
cd sports_analytics

# Install Git LFS (required for model files)
# macOS: brew install git-lfs
# Linux: sudo apt install git-lfs
git lfs install
git lfs pull  # Download large model files
```

### 1. Activate Environment
```bash
cd sports_analytics
source sva/bin/activate
```

### 2. Setup Database
```bash
python scripts/setup_database.py
```

### 3. Start Services

**FastAPI (Backend):**
```bash
./scripts/start_api.sh
# Access at: http://localhost:8000/docs
```

**Streamlit (UI):**
```bash
./scripts/start_streamlit.sh
# Access at: http://localhost:8501
```

---

## ✅ What's Ready

- ✅ Repository on GitHub with Git LFS for large files
- ✅ Virtual environment (sva) created and activated
- ✅ All dependencies installed
- ✅ LanceDB + DuckDB integrated
- ✅ All TODOs implemented (no mocks)
- ✅ Database migration scripts ready
- ✅ FastAPI server ready
- ✅ Streamlit dashboard ready
- ✅ Model files tracked via Git LFS

---

## 📊 Database Status

**LanceDB:** Storage for vectors and structured data  
**DuckDB:** SQL analytics engine  
**Integration:** Zero-copy via Apache Arrow

---

## 🎯 Next Actions

1. Run `python scripts/setup_database.py` to create tables
2. Start API: `./scripts/start_api.sh`
3. Start UI: `./scripts/start_streamlit.sh`
4. Add sample data (optional)

---

**Ready to launch! 🚀**

