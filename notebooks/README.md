# Jupyter Notebooks Directory
## Research, Prototyping, and Interactive Analysis

**Purpose:** Jupyter notebooks for experimentation, data exploration, and interactive visualization

---

## 📓 **TYPICAL NOTEBOOKS**

### **Recommended Structure:**
```
notebooks/
├── 01_data_exploration.ipynb          # Explore tracking data, statistics
├── 02_model_comparison.ipynb          # Compare YOLO11x vs YOLOv8
├── 03_heatmap_analysis.ipynb          # Interactive heatmap generation
├── 04_pass_network_viz.ipynb          # Pass network visualization
├── 05_player_performance.ipynb        # Player metrics analysis
├── 06_tactical_analysis.ipynb         # Formation, positioning, tactics
├── 07_event_detection_tuning.ipynb    # Tune event detection parameters
└── 08_namibian_dataset_analysis.ipynb # Analyze Namibian match characteristics
```

---

## 🚀 **GETTING STARTED**

### **Install Jupyter:**
```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Jupyter
pip install jupyter notebook jupyterlab ipywidgets

# Start Jupyter Lab (recommended)
jupyter lab

# Or Jupyter Notebook (classic)
jupyter notebook
```

### **Create First Notebook:**

```python
# Cell 1: Imports
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path.cwd().parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.video_utils import read_video, get_video_properties
from analytics import JerseyTracker, HeatmapGenerator
import matplotlib.pyplot as plt
import pandas as pd

# Cell 2: Load Data
video_path = PROJECT_ROOT / "input_videos" / "test_match.mp4"
props = get_video_properties(str(video_path))
print(f"FPS: {props['fps']}, Frames: {props['total_frames']}")

# Cell 3: Run Analysis
tracker = JerseyTracker(
    model_path=str(PROJECT_ROOT / "models" / "yolo11x.pt"),
    confidence_threshold=0.5
)

frames = read_video(str(video_path))[:300]  # First 10 seconds
tracks = tracker.process_chunk(frames, chunk_idx=0)

# Cell 4: Visualize
plt.figure(figsize=(12, 6))
player_counts = [len(frame_tracks) for frame_tracks in tracks['players']]
plt.plot(player_counts)
plt.title('Players Detected Per Frame')
plt.xlabel('Frame')
plt.ylabel('Player Count')
plt.grid(True)
plt.show()
```

---

## 📊 **USEFUL ANALYSES**

### **1. Data Exploration**

**Tracking Data Analysis:**
```python
import pandas as pd

# Load tracking CSV
df = pd.read_csv('output_videos/match1/tracking_data.csv')

# Player statistics
player_distances = df.groupby('track_id')['distance_covered'].max()
player_speeds = df.groupby('track_id')['speed_kmh'].max()

# Visualize
player_distances.sort_values(ascending=False).head(10).plot(kind='barh')
plt.title('Top 10 Players by Distance Covered')
plt.xlabel('Distance (m)')
```

**Pass Analysis:**
```python
passes_df = pd.read_csv('output_videos/match1/passes.csv')

# Pass accuracy by team
team1_accuracy = passes_df[passes_df['from_team'] == 1]['successful'].mean() * 100
team2_accuracy = passes_df[passes_df['from_team'] == 2]['successful'].mean() * 100

print(f"Team 1 Pass Accuracy: {team1_accuracy:.1f}%")
print(f"Team 2 Pass Accuracy: {team2_accuracy:.1f}%")
```

### **2. Model Performance Testing**

**YOLO11x vs YOLOv8 Comparison:**
```python
from ultralytics import YOLO
import time

models = {
    'YOLO11x': YOLO('models/yolo11x.pt'),
    'YOLOv8x': YOLO('models/yolov8x.pt')
}

test_frames = frames[:100]  # First 100 frames

for name, model in models.items():
    start = time.time()
    results = model.predict(test_frames, verbose=False)
    elapsed = time.time() - start
    
    print(f"{name}:")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  FPS: {len(test_frames) / elapsed:.1f}")
    print(f"  Detections: {sum(len(r.boxes) for r in results)}")
```

### **3. Interactive Heatmap Tuning**

```python
from ipywidgets import interact, IntSlider
import matplotlib.pyplot as plt

# Load heatmap data
heatmap_gen = HeatmapGenerator()
heatmap_gen.accumulate_positions(tracks)

@interact(
    blur=IntSlider(min=11, max=101, step=10, value=51),
    sigma=IntSlider(min=5, max=30, step=5, value=15)
)
def show_heatmap(blur, sigma):
    import cv2
    heatmap = cv2.GaussianBlur(heatmap_gen.team1_heatmap, (blur, blur), sigma)
    heatmap_norm = heatmap / heatmap.max() if heatmap.max() > 0 else heatmap
    
    plt.figure(figsize=(12, 8))
    plt.imshow(heatmap_norm, cmap='Reds', origin='lower')
    plt.title(f'Team 1 Heatmap (blur={blur}, sigma={sigma})')
    plt.colorbar()
    plt.show()
```

---

## 🇳🇦 **NAMIBIAN RESEARCH NOTEBOOKS**

### **Namibian Dataset Characteristics:**

**Notebook: `namibian_dataset_analysis.ipynb`**

Analyze challenges unique to Namibian football:
- Dusty/muddy pitches (color detection issues)
- Afternoon sun glare (overexposure)
- Faded jerseys (OCR performance)
- Poor stadium lighting (evening matches)
- Single-camera setup (no multi-angle)

```python
# Analyze detection performance on Namibian matches
namibian_matches = [
    'unam_fc_vs_african_stars.mp4',
    'blue_waters_vs_chiefs.mp4',
    'mtc_maris_cup_final.mp4'
]

results = {}
for match in namibian_matches:
    # Run detection
    # Calculate metrics
    # Compare to international datasets
    pass
```

### **UNAM-Specific Analysis:**

**Notebook: `unam_multi_campus_analysis.ipynb`**

Compare performance across UNAM's 13 campuses:
- Camera quality (Windhoek vs rural campuses)
- Connectivity (online processing vs offline)
- Player detection rates (field conditions vary)
- Jersey OCR accuracy (equipment quality varies)

---

## 🔬 **RESEARCH IDEAS**

### **Model Fine-Tuning:**
1. Collect 2,000+ Namibian match images
2. Annotate players, ball, referees
3. Fine-tune YOLO11x on Namibian dataset
4. Compare performance (before/after)

### **Tactical Analysis:**
1. Formation detection using player positions
2. Pressing intensity measurement
3. Build-up play classification
4. Set piece analysis

### **Performance Optimization:**
1. Frame sampling (analyze every Nth frame)
2. ROI detection (only analyze field region)
3. Model quantization (FP16, INT8 for edge)
4. Batch processing optimization

---

## 💾 **SHARING NOTEBOOKS**

### **With UNAM Sports Science Students:**
- Use nbviewer or Google Colab
- Include sample data (anonymized)
- Document dependencies (requirements.txt)
- Add markdown explanations

### **For Academic Papers:**
- Export to PDF (File → Export → PDF)
- Include methodology notebooks as supplementary materials
- Cite Ultralytics, supervision, EasyOCR

---

## ⚙️ **BEST PRACTICES**

**Notebook Structure:**
1. **Title & Description** (Markdown cell)
2. **Imports** (Single cell, all imports)
3. **Configuration** (Paths, parameters)
4. **Data Loading** (Read video, CSVs)
5. **Analysis** (Multiple cells, one concept each)
6. **Visualization** (Plots, charts)
7. **Conclusions** (Summary, insights)
8. **Next Steps** (Future work, TODOs)

**Code Quality:**
- ✅ Clear variable names
- ✅ Docstrings for functions
- ✅ Comments for complex logic
- ✅ Restart kernel & run all (verify reproducibility)
- ❌ Don't commit large files (.gitignore: *.mp4, *.csv)

**Version Control:**
- ✅ Commit notebooks (code, markdown)
- ✅ Clear output before commit (smaller diffs)
- ❌ Don't commit data files (use data/ directory)
- ❌ Don't commit credentials (.env files)

---

**Last Updated:** January 2025  
**Recommended:** JupyterLab 4.0+ (better interface than classic Notebook)  
**Namibian Context:** Document connectivity workarounds (offline development, batch uploads)
