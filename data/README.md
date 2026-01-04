# Data Directory
## Sample Datasets and Calibration Data

**Purpose:** Storage for sample datasets, field calibration images, test data

---

## 📁 **DIRECTORY STRUCTURE**

```
data/
├── README.md                          # This file
├── sample_matches/                    # Sample match data for testing
│   ├── unam_fc_sample.csv
│   ├── mtc_maris_cup_sample.json
│   └── test_tracking_data.csv
├── calibration/                       # Field calibration images
│   ├── dr_hage_geingob_stadium.jpg
│   ├── unam_sam_nujoma_campus.jpg
│   └── field_templates/
├── test_videos/                       # Short test clips (<1 minute)
│   ├── test_kickoff_10sec.mp4
│   ├── test_corner_15sec.mp4
│   └── test_penalty_20sec.mp4
└── annotations/                       # Ground truth annotations (YOLO format)
    ├── images/
    ├── labels/
    └── dataset.yaml
```

---

## 🎥 **SAMPLE DATA**

### **Test Videos (Included):**

**Purpose:** Quick testing without full match processing

**test_kickoff_10sec.mp4** (10 seconds)
- Kickoff scenario
- 22 players visible
- Ball in center circle
- Use case: Test player detection, team assignment

**test_corner_15sec.mp4** (15 seconds)
- Corner kick scenario
- Player clustering in penalty area
- Use case: Test event detection (clusters)

**test_penalty_20sec.mp4** (20 seconds)
- Penalty scenario
- Goalkeeper + striker
- Use case: Test high-speed tracking (sprint detection)

### **Sample CSVs (Included):**

**unam_fc_sample.csv**
- 1,000 frames of tracking data
- Pre-analyzed UNAM FC match
- Use case: Test statistics calculation without video processing

**mtc_maris_cup_sample.json**
- Complete match statistics JSON
- MTC Maris Cup final
- Use case: Test API response format, frontend integration

---

## 🏟️ **CALIBRATION IMAGES**

### **Namibian Stadiums:**

**Dr Hage Geingob Stadium (Windhoek)**
- Main national stadium (10,000 capacity)
- MTC Maris Cup venue
- High-quality camera positions available
- Calibration: 4 corner coordinates marked

**UNAM Sam Nujoma Campus (Windhoek)**
- UNAM FC home ground
- University stadium (2,000 capacity)
- Standard pitch dimensions (105m × 68m)
- Calibration: Saved in config/field_config.json

**Regional Fields:**
- Oshakati Stadium (Northern Campus)
- Rundu Sports Complex (Eastern Campus)
- Use case: Test on various field conditions

### **Usage:**
```bash
# Use pre-calibrated stadium
python analyze_match.py input_videos/match.mp4 --field-config data/calibration/dr_hage_geingob_stadium.json

# Or calibrate your own
python tools/define_field_polygon.py input_videos/new_venue.mp4
```

---

## 🏷️ **GROUND TRUTH ANNOTATIONS**

### **Purpose:**
- Train custom YOLO models (Namibian-specific)
- Evaluate detection performance
- Fine-tune for local conditions (dusty pitches, poor lighting)

### **Format: YOLO (YOLOv11/v8 compatible)**

```
annotations/
├── images/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
├── labels/
│   ├── img_001.txt    # YOLO format: class x_center y_center width height
│   ├── img_002.txt
│   └── ...
└── dataset.yaml       # YOLO dataset configuration
```

**dataset.yaml:**
```yaml
# Namibian Football Dataset
path: /path/to/data/annotations
train: images/train
val: images/val
test: images/test

# Classes
names:
  0: goalkeeper
  1: player
  2: referee
  3: ball

# Metadata
nc: 4  # Number of classes
```

### **Annotation Tools:**
- **RoboFlow:** https://roboflow.com (web-based, easy)
- **CVAT:** https://cvat.ai (open-source, powerful)
- **LabelImg:** Desktop tool (simple, offline)
- **Makesense.ai:** Web-based (free, no account)

### **Namibian Dataset Recommendations:**
- **Minimum:** 2,000 images (500 per class)
- **Balanced:** Equal distribution (players, ball, referee, goalkeeper)
- **Diverse:** Multiple stadiums, lighting conditions, camera angles
- **Annotate:**
  - Dusty pitches (color variations)
  - Afternoon sun glare (overexposure)
  - Evening matches (poor lighting)
  - Faded jerseys (worn equipment)

---

## 🧪 **TESTING DATA**

### **Unit Test Fixtures:**
```python
# Load test data in pytest
import pytest
from pathlib import Path

@pytest.fixture
def sample_tracking_data():
    data_dir = Path(__file__).parent.parent / "data"
    df = pd.read_csv(data_dir / "sample_matches" / "unam_fc_sample.csv")
    return df

@pytest.fixture
def test_video_frames():
    from utils.video_utils import read_video
    frames = read_video("data/test_videos/test_kickoff_10sec.mp4")
    return frames
```

---

## 📈 **BENCHMARKING DATA**

### **Performance Baselines:**

**YOLO11x on Namibian Footage:**
- Player detection recall: 95%+ (if visible)
- Ball detection recall: 80-85% (small object)
- Referee detection recall: 90%+
- Jersey OCR accuracy: 70-80% (Namibian conditions)
- False positives: <5% (spectators, ads)

**Processing Speed (Various Hardware):**
- Desktop GPU (RTX 3060): 60-90 FPS
- Laptop CPU (i7): 3-5 FPS
- Raspberry Pi 5: 0.5-1 FPS (with optimization)
- Cloud GPU (T4): 30-40 FPS

**Store benchmarks in:**
```
data/benchmarks/
├── yolo11x_namibian_stadiums.json
├── detection_accuracy_by_venue.csv
└── processing_speed_hardware.csv
```

---

## 🔒 **DATA PRIVACY & SECURITY**

### **⚠️ IMPORTANT:**

**DO NOT COMMIT:**
- ❌ Full match videos (copyright, large files)
- ❌ Player personal information (names, IDs, contact)
- ❌ Sensitive tactical data (formation secrets)
- ❌ Proprietary training datasets (commercial value)

**SAFE TO COMMIT:**
- ✅ Sample/test videos (<1 minute, anonymized)
- ✅ Aggregated statistics (team-level, no individual)
- ✅ Calibration data (stadium coordinates)
- ✅ Model weights (if trained yourself, not proprietary)

### **.gitignore Configuration:**
```
# Add to .gitignore
data/sample_matches/*.mp4
data/test_videos/*.mp4
data/annotations/images/
data/private/
```

---

## 📊 **RECOMMENDED DATASETS**

### **For Training/Fine-Tuning:**

**Public Datasets:**
- **SoccerNet:** 550+ matches, 230K minutes (research use)
  - https://www.soccer-net.org
- **StatsBomb Open Data:** Tactical event data (free)
  - https://github.com/statsbomb/open-data
- **RoboFlow Universe:** Football player datasets
  - https://universe.roboflow.com/search?q=football

**Namibian Dataset (Custom):**
- Partner with UNAM, MTC, NFA
- Record 50+ matches (Debmarine Premiership, MTC Maris Cup)
- Annotate 5,000+ images
- Train Namibian-optimized YOLO11x
- **Commercial Value:** Unique dataset for Southern Africa

---

## 💡 **RESEARCH IDEAS**

1. **Namibian Football Characteristics**
   - Analyze 50 Debmarine Premiership matches
   - Compare to European football (English Premier League)
   - Identify unique patterns (physicality, pace, tactics)

2. **Field Condition Impact**
   - Dusty vs grass pitches (detection accuracy)
   - Quantify performance degradation
   - Develop dust-resistant models

3. **Multi-Sport Dataset**
   - UNAM sports (football, rugby, basketball, netball)
   - Unified annotation format
   - Cross-sport model transfer learning

---

**Last Updated:** January 2025  
**Recommended Storage:** Keep data/ directory <1GB (use external storage for large datasets)  
**Namibian Context:** Limited bandwidth (10GB upload = N$200-N$500 data cost), compress/share wisely
