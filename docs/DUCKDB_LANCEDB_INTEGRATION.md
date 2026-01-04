# DuckDB + LanceDB Integration Guide

**Date:** 2026-01-04  
**Purpose:** Leverage DuckDB's SQL analytics on LanceDB's efficient storage

---

## 🎯 Overview

This integration combines:
- **LanceDB**: Efficient vector storage and multimodal data lakehouse
- **DuckDB**: Fast SQL analytics engine for complex queries
- **Apache Arrow**: Zero-copy data sharing between them

---

## 🏗️ Architecture

```
┌─────────────┐
│  LanceDB    │  ← Efficient storage (vector + structured data)
│  (Storage)  │
└──────┬──────┘
       │ Apache Arrow (zero-copy)
       ↓
┌─────────────┐
│   DuckDB    │  ← SQL analytics engine
│  (Analytics)│
└─────────────┘
```

**Benefits:**
- ✅ Fast analytical queries on large datasets
- ✅ Zero-copy data transfer (Arrow format)
- ✅ Complex SQL aggregations, joins, window functions
- ✅ Streaming support for datasets larger than memory

---

## 📦 Installation

```bash
pip install duckdb lancedb pyarrow
```

---

## 💻 Usage Examples

### 1. Basic SQL Query

```python
from api.lib.lancedb_adapter import get_lancedb

lancedb = get_lancedb()

# Register LanceDB table as DuckDB view
lancedb.register_lancedb_table("matches", "matches_view")

# Execute SQL query
result = lancedb.execute_sql("""
    SELECT 
        sport_id,
        COUNT(*) as total_matches,
        AVG(score_team1 + score_team2) as avg_total_score
    FROM matches_view
    WHERE status = 'completed'
    GROUP BY sport_id
    ORDER BY total_matches DESC
""")

print(result)
```

### 2. Complex Analytics

```python
# Player performance trends
query = """
    SELECT 
        DATE(m.date) as match_date,
        AVG(ps.total_distance_m) as avg_distance,
        AVG(ps.passes_made) as avg_passes,
        AVG(ps.pass_accuracy_pct) as avg_accuracy
    FROM player_statistics ps
    JOIN matches m ON ps.match_id = m.id
    WHERE ps.player_id = 'player-uuid-here'
      AND m.date >= '2025-01-01'
    GROUP BY DATE(m.date)
    ORDER BY match_date DESC
"""

result = lancedb.execute_sql(query, "player_statistics")
```

### 3. Team Comparison

```python
query = """
    WITH team1_stats AS (
        SELECT AVG(distance) as avg_dist, COUNT(*) as matches
        FROM player_stats
        WHERE team_id = 'team1-uuid'
    ),
    team2_stats AS (
        SELECT AVG(distance) as avg_dist, COUNT(*) as matches
        FROM player_stats
        WHERE team_id = 'team2-uuid'
    )
    SELECT 
        t1.avg_dist as team1_avg_distance,
        t2.avg_dist as team2_avg_distance,
        t1.matches as team1_matches,
        t2.matches as team2_matches
    FROM team1_stats t1, team2_stats t2
"""

result = lancedb.execute_sql(query)
```

---

## 🔧 API Methods

### `register_lancedb_table(table_name, view_name=None)`
Register a LanceDB table as a DuckDB view for SQL queries.

### `execute_sql(sql_query, table_name=None)`
Execute SQL query on LanceDB data via DuckDB.

### `register_all_tables()`
Register all LanceDB tables as DuckDB views at once.

---

## 📊 Use Cases

### ✅ When to Use DuckDB + LanceDB

1. **Complex Analytics**: Aggregations, joins, window functions
2. **Large Dataset Queries**: Streaming support for memory-efficient processing
3. **Ad-hoc Analysis**: Fast SQL queries without ETL
4. **Performance Metrics**: Calculate complex KPIs across multiple tables

### ❌ When NOT to Use

1. **Simple Lookups**: Use LanceDB native queries
2. **Real-time Updates**: LanceDB handles writes better
3. **Vector Search**: Use LanceDB's native vector search

---

## 🚀 Performance Tips

1. **Register Tables Once**: Register tables at startup, reuse views
2. **Use Filters Early**: Push filters to LanceDB when possible
3. **Limit Results**: Use `LIMIT` in SQL queries
4. **Stream Large Results**: DuckDB supports streaming for large datasets

---

## 📚 References

- [DuckDB Documentation](https://duckdb.org/docs/)
- [LanceDB DuckDB Integration](https://docs.lancedb.com/integrations/platforms/duckdb)
- [Apache Arrow](https://arrow.apache.org/)

---

## 🔄 Migration from SQLAlchemy

For analytics queries, use DuckDB instead of SQLAlchemy:

**Before (SQLAlchemy):**
```python
from sqlalchemy import func
matches = db.query(func.count(Match.id)).filter(Match.status == 'completed').scalar()
```

**After (DuckDB):**
```python
result = lancedb.execute_sql("SELECT COUNT(*) FROM matches WHERE status = 'completed'")
```

**Benefits:**
- ✅ Faster for analytical queries
- ✅ More expressive SQL
- ✅ Better for complex aggregations
- ✅ Works with LanceDB storage directly

---

## 📝 Example: Analytics Service

See `api/services/analytics_service.py` for complete implementation with:
- Match analytics
- Player performance trends
- Team comparisons
- Sport statistics
- Top performers

