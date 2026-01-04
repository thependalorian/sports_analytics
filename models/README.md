# YOLO Models Directory
## Football/Soccer Player Detection

**Purpose:** Store YOLO model weights for player detection and tracking

---

## 🎯 **RECOMMENDED MODEL: YOLO11x**

### **Why YOLO11x Over YOLOv8?**

| Metric | YOLO11x | YOLOv8x | Improvement |
|--------|---------|---------|-------------|
| **Accuracy (mAP)** | 54.7 | ~53.9 | +1.5% better |
| **Parameters** | 56.9M | ~68M | 22% fewer parameters |
| **Speed (T4 GPU)** | 11.3ms | ~14ms | ~20% faster |
| **Speed (CPU)** | 462.8ms | ~520ms | ~10% faster |
| **Edge Deployment** | Optimized | Good | Better for stadiums |
| **Memory Usage** | Lower | Higher | Critical for Raspberry Pi |

**Verdict:** YOLO11x is **superior** for Namibian deployment:
- ✅ Better accuracy (54.7 vs 53.9 mAP)
- ✅ 22% fewer parameters (faster inference, lower memory)
- ✅ Optimized for edge devices (Raspberry Pi 5 at stadiums)
- ✅ Latest features (2024 release)

---

## 📥 **DOWNLOAD MODELS**

### **Method 1: From Repository (Git LFS) - Recommended**

If you cloned the repository, model files are already included via Git LFS:

```bash
# Ensure Git LFS is installed and initialized
git lfs install

# Pull LFS-tracked files (if not automatically downloaded)
git lfs pull

# Verify files are downloaded
ls -lh models/*.pt models/easyocr/*.pth
```

**Note:** This repository uses Git LFS for large model files. The `yolo11x.pt` file and EasyOCR models are automatically tracked by LFS.

### **Method 2: Automatic Download Script**

```bash
# Run from project root
python scripts/download_models.py
```

This script will:
1. Download YOLO11x (56.9M parameters, ~110MB file)
2. Verify integrity (SHA256 checksum)
3. Place in `models/yolo11x.pt`
4. Create backup of YOLOv8x (optional, for comparison)

### **Method 3: Manual Download**

**YOLO11x (Recommended):**
```bash
# Using Ultralytics CLI
pip install ultralytics
yolo task=detect mode=predict model=yolo11x.pt source=test.jpg

# The model will auto-download to ~/.ultralytics/weights/
# Then copy to project:
cp ~/.ultralytics/weights/yolo11x.pt models/
```

**Or download directly:**
- **YOLO11x:** https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11x.pt
- **YOLOv8x (legacy):** https://github.com/ultralytics/assets/releases/download/v8.0.0/yolov8x.pt

### **Method 4: Custom Trained Model**

For football-specific optimizations (Namibian conditions):

```bash
# Train on your dataset
yolo task=detect mode=train model=yolo11x.pt data=football_dataset.yaml epochs=100

# Result will be saved to runs/detect/train/weights/best.pt
# Copy to project:
cp runs/detect/train/weights/best.pt models/yolo11x_football_namibia.pt
```

**Training Dataset Recommendations:**
- Include Namibian match footage (dusty pitches, afternoon glare, faded jerseys)
- Augment with international datasets (RoboFlow Football Players)
- Minimum 10,000 annotated images (players, ball, referee classes)

---

## 📁 **Directory Structure**

```
models/
├── README.md                           # This file
├── yolo11x.pt                          # Main model (RECOMMENDED) - Download first
├── yolov8x.pt                          # Legacy model (optional, for comparison)
├── yolo11x_football_namibia.pt         # Custom trained (if available)
├── yolo11s.pt                          # Smaller model for testing (optional)
└── best.pt                             # Symlink to active model (auto-created)
```

---

## ⚙️ **MODEL CONFIGURATION**

Update `/config/settings.py` to use YOLO11x:

```python
# Model settings
DEFAULT_MODEL_PATH = MODELS_DIR / "yolo11x.pt"  # Changed from best.pt
CONFIDENCE_THRESHOLD = 0.5  # Detection confidence (0.0-1.0)

# Alternative models
FAST_MODEL_PATH = MODELS_DIR / "yolo11n.pt"  # Fast, lower accuracy
ACCURATE_MODEL_PATH = MODELS_DIR / "yolo11x.pt"  # Slow, higher accuracy
```

---

## 🚀 **USAGE**

### **Default (YOLO11x):**
```bash
python analyze_match.py input_videos/match.mp4
```

### **Specify Model:**
```bash
python analyze_match.py input_videos/match.mp4 --model models/yolo11x.pt
```

### **Test with Smaller Model (Faster):**
```bash
python analyze_match.py input_videos/match.mp4 --model models/yolo11n.pt
```

---

## 📊 **MODEL PERFORMANCE (Football Detection)**

**YOLO11x on COCO Dataset:**
- **mAP@50-95:** 54.7%
- **mAP@50:** ~72%
- **Precision:** ~68%
- **Recall:** ~65%

**Expected Performance (Football):**
- **Player Detection:** 95%+ recall (if visible)
- **Ball Detection:** 80-90% (small object, difficult)
- **Referee Detection:** 90%+ (distinctive uniform)
- **Jersey Numbers:** 70-85% (depends on camera, lighting, jersey condition)

**Namibian-Specific Challenges:**
- Dusty/muddy pitches (affects color-based detection)
- Afternoon sun glare (overexposure, shadows)
- Faded jerseys (poor OCR performance)
- Single-camera setup (no multi-angle verification)
- Poor stadium lighting (evening matches)

**Recommendation:** Fine-tune YOLO11x on 2,000+ Namibian match images (Dr Hage Geingob Stadium, UNAM matches, MTC Maris Cup footage).

---

## 🔧 **OPTIMIZATION FOR NAMIBIA**

### **Edge Deployment (Raspberry Pi 5 at Stadiums):**

**Hardware:**
- Raspberry Pi 5 (8GB RAM)
- Coral Edge TPU (optional, 4× speed boost)
- 4TB SSD (video storage)

**Model Optimization:**
- Convert to TensorRT (NVIDIA) or ONNX (CPU/Edge TPU)
- Quantization: FP16 or INT8 (2-4× speed, minimal accuracy loss)
- Pruning: Remove 20-30% of weights (smaller model, 5-10% accuracy loss acceptable)

```bash
# Export to ONNX for edge deployment
yolo export model=yolo11x.pt format=onnx simplify=True

# Export to TensorRT for NVIDIA Jetson (if using instead of Raspberry Pi)
yolo export model=yolo11x.pt format=engine device=0
```

### **Battery Optimization (Mobile App):**
- Use YOLO11n (smallest, fastest) for real-time on-device detection
- YOLO11x for cloud processing (after WiFi upload)
- Frame sampling (analyze every 2nd or 3rd frame to save power)

---

## 💾 **MODEL SIZE & DOWNLOAD TIME**

| Model | Size | Download Time (MTC 4G, 10 Mbps) | Download Time (3G, 2 Mbps) |
|-------|------|----------------------------------|----------------------------|
| YOLO11n | ~6MB | 5 seconds | 24 seconds |
| YOLO11s | ~22MB | 18 seconds | 88 seconds |
| YOLO11m | ~50MB | 40 seconds | 200 seconds (~3 min) |
| YOLO11l | ~60MB | 48 seconds | 240 seconds (~4 min) |
| **YOLO11x** | **~110MB** | **88 seconds** | **440 seconds (~7 min)** |

**Recommendation:** Pre-install YOLO11x during app setup (WiFi-only download), not on first use.

---

## 🧪 **MODEL TESTING**

### **Quick Test:**
```bash
# Test detection on single image
yolo task=detect mode=predict model=models/yolo11x.pt source=test_image.jpg

# Test on video clip (first 100 frames)
python -c "
from ultralytics import YOLO
model = YOLO('models/yolo11x.pt')
results = model.predict(source='input_videos/test.mp4', save=True, max_det=50)
"
```

### **Benchmark Performance:**
```bash
# Benchmark speed on your hardware
yolo benchmark model=models/yolo11x.pt device=0  # GPU
yolo benchmark model=models/yolo11x.pt device=cpu  # CPU
```

---

## 📝 **MODEL CHANGELOG**

| Date | Model | Changes |
|------|-------|---------|
| Jan 2025 | YOLO11x | Initial recommendation (v8.1.0, 54.7 mAP) |
| Dec 2024 | YOLOv8x | Legacy model (v8.0.0, 53.9 mAP) |

---

## 🆘 **TROUBLESHOOTING**

**Git LFS files showing as pointers:**
- Ensure Git LFS is installed: `git lfs version`
- Initialize LFS: `git lfs install`
- Pull LFS files: `git lfs pull`
- Verify files: `git lfs ls-files` should show actual files, not pointers

**Model won't download:**
- Check internet connection (MTC 4G/5G required, 3G too slow)
- Use VPN if GitHub blocked
- Manual download from Ultralytics releases page
- If using Git LFS, ensure LFS is properly configured

**Out of memory:**
- Use YOLO11m or YOLO11s (smaller models)
- Reduce image size (`imgsz=640` → `imgsz=480`)
- Process fewer frames (`chunk_size=300` → `chunk_size=100`)

**Poor detection accuracy:**
- Lower confidence threshold (`confidence=0.5` → `confidence=0.3`)
- Increase max detections (`max_det=50` → `max_det=100`)
- Fine-tune on Namibian football footage

**Slow inference:**
- Use GPU (CUDA) if available
- Export to TensorRT or ONNX
- Use smaller model (YOLO11n, YOLO11s)
- Reduce image size

---

**Last Updated:** January 2025  
**Recommended Model:** YOLO11x (yolo11x.pt)  
**Model Version:** Ultralytics v8.1.0+
