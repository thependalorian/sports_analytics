# Input Videos Directory
## Place Your Match Videos Here

**Purpose:** Storage for input match videos to be analyzed

---

## 📹 **SUPPORTED VIDEO FORMATS**

**Primary (Recommended):**
- **MP4** (H.264/H.265) - Most common, best compression
- **MOV** (QuickTime) - High quality, larger file size
- **AVI** (Uncompressed) - Highest quality, very large

**Secondary (Supported):**
- MKV, WebM, FLV, WMV (converted automatically)

**Not Recommended:**
- Heavily compressed (artifacts affect detection)
- Variable frame rate (inconsistent analysis)
- Vertical videos (portrait mode, wrong aspect ratio)

---

## 📊 **RECOMMENDED VIDEO SPECIFICATIONS**

### **For Best Results (UNAM, MTC Maris Cup, Professional Clubs):**
- **Resolution:** 1080p (1920×1080) or 720p (1280×720) minimum
- **Frame Rate:** 25-30 fps (PAL/NTSC standard)
- **Bitrate:** 5-10 Mbps (good quality, manageable file size)
- **Aspect Ratio:** 16:9 (standard HD)
- **Duration:** Full match (90 minutes) or highlights (5-45 minutes)
- **Camera Angle:** Elevated side view (halfway line, ~20m height)
- **Camera:** Static or slow pan (no handheld, no zoom)

### **Acceptable (Schools, Amateur Clubs):**
- **Resolution:** 720p (1280×720) or 480p (854×480)
- **Frame Rate:** 24-30 fps
- **Bitrate:** 2-5 Mbps
- **Camera:** Phone or basic camcorder (stationary, tripod-mounted)

### **Poor Quality (Will Affect Accuracy):**
- ❌ Below 480p (players too small)
- ❌ Below 15 fps (jerky motion, tracking fails)
- ❌ Handheld (shaky, detection issues)
- ❌ Too much zoom (limited field view)
- ❌ Night matches with poor lighting (low visibility)

---

## 🎥 **RECORDING TIPS (Namibian Context)**

### **Equipment Recommendations:**

**Budget (Schools): N$3,000-N$8,000**
- Smartphone: Samsung Galaxy A-series, Xiaomi (1080p 30fps)
- Tripod: Cheap aluminum tripod (N$500)
- Total: ~N$4,000

**Mid-Range (Amateur Clubs): N$10,000-N$25,000**
- Camcorder: Sony Handycam, Canon Vixia (1080p 60fps)
- Tripod: Sturdy video tripod (N$2,000)
- SD Card: 128GB UHS-II (N$1,500)
- Total: ~N$18,000

**Professional (UNAM, Premiership Clubs): N$50,000-N$150,000**
- Camera: Sony FDR-AX700, Canon XA55 (4K 30fps)
- Tripod: Manfrotto fluid head (N$15,000)
- External Recorder: Atomos Ninja (optional, N$30,000)
- Backup Camera: Second camera (opposite angle)
- Total: ~N$120,000

### **Camera Position:**
- **Height:** 15-25m (halfway line, elevated view)
- **Distance:** 30-50m from sideline (full pitch visible)
- **Angle:** Slight downward tilt (10-15°)
- **Coverage:** Both penalty areas visible, touchlines clear

### **Recording Settings:**
- **Resolution:** 1080p (best balance quality/file size)
- **Frame Rate:** 30 fps (NTSC) or 25 fps (PAL)
- **Exposure:** Manual (avoid auto-adjust during play)
- **White Balance:** Daylight or cloudy (not auto)
- **Focus:** Manual infinity (don't auto-focus on nearby objects)

### **Namibian-Specific Challenges:**

**☀️ Afternoon Sun Glare (Common at 3PM kickoffs):**
- Use ND filter (polarizing filter, N$500-N$1,500)
- Position camera with sun behind (avoid shooting into sun)
- Record morning matches (8AM-11AM) if possible

**💨 Dusty Pitches (Dry season May-October):**
- Clean camera lens every 15 minutes
- Use lens hood (reduce dust, flare)
- Higher shutter speed (freeze motion, reduce blur)

**🌙 Poor Stadium Lighting (Evening matches):**
- Increase ISO (1600-3200, accept some noise)
- Wider aperture (f/2.8 or lower)
- 30fps minimum (not 60fps, need light)
- Consider multiple smaller LED lights (N$5,000 each)

---

## 📏 **FILE SIZE GUIDELINES**

| Duration | Resolution | Bitrate | File Size | Upload Time (MTC 4G) |
|----------|------------|---------|-----------|----------------------|
| 90 min (full match) | 1080p 30fps | 10 Mbps | ~6.7GB | 90 minutes (10 Mbps) |
| 90 min | 720p 30fps | 5 Mbps | ~3.4GB | 45 minutes |
| 90 min | 480p 30fps | 2 Mbps | ~1.4GB | 19 minutes |
| 45 min (half) | 1080p 30fps | 10 Mbps | ~3.4GB | 45 minutes |
| 10 min (highlights) | 1080p 30fps | 10 Mbps | ~750MB | 10 minutes |

**Recommendation for Namibia:**
- Record in 1080p (best quality)
- Compress to 720p for upload (3.4GB, 45-minute upload on 4G)
- Platform auto-compresses to 480p for mobile viewing

---

## 🗂️ **FILE NAMING CONVENTION**

**Recommended Format:**
```
YYYY-MM-DD_Competition_HomeTeam_vs_AwayTeam.mp4
```

**Examples:**
```
2025-02-15_MTC_Maris_Cup_UNAM_FC_vs_African_Stars.mp4
2025-03-10_Debmarine_Prem_Blue_Waters_vs_Orlando_Pirates.mp4
2025-01-20_UNAM_Internal_Main_Campus_vs_Oshakati.mp4
```

**Avoid:**
- ❌ Generic names (match.mp4, video1.mp4)
- ❌ Special characters (spaces OK, but no: / \ : * ? " < > |)
- ❌ Very long names (>100 characters)

---

## 🚀 **QUICK START**

1. **Record match** (or obtain video from club/organization)
2. **Place video here** (input_videos/)
3. **Run calibration:**
   ```bash
   python tools/define_field_polygon.py input_videos/your_match.mp4
   ```
4. **Analyze:**
   ```bash
   python analyze_match.py input_videos/your_match.mp4
   ```
5. **Results** saved to: `output_videos/your_match/`

---

## ⚠️ **IMPORTANT NOTES**

### **Copyright & Consent:**
- ✅ Obtain permission to record (stadium, club, league)
- ✅ Player consent (adults) or parental consent (minors U-18)
- ✅ Signage at venue: "This match is being recorded for analytics"
- ✅ Clear ownership in contracts (who owns the footage?)

### **Data Privacy (Namibian Context):**
- No pending Data Protection Bill requirements yet, but use GDPR-equivalent standards
- Store videos securely (encrypted, access-controlled)
- Delete after retention period (2 years recommended)
- Right to deletion (players can request video removal)

### **Storage Management:**
- Full matches: 3-7GB each (expensive to store long-term)
- Recommendation: Keep raw video 90 days, then compress or delete
- Store analytics data (CSVs) indefinitely (only MB, not GB)

---

**Last Updated:** January 2025  
**For more info:** See [docs/PRD_WEB_DASHBOARD.md](../docs/PRD_WEB_DASHBOARD.md)
