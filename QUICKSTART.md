# SC549-PA03: Quick Start Guide

## 🚀 Fastest Path to Results

### Step 1: Install Dependencies (5 minutes)

```powershell
cd C:\Users\Public\SC549-PA03-Player-Tracking
pip install -r requirements.txt
```

### Step 2: Test Environment (2 minutes)

```powershell
python test_environment.py
```

This will:
- Verify all packages are installed
- Download YOLOv8 models automatically
- Test inference if sample images exist

### Step 3: Download Videos (10-15 minutes)

**Open:** `VIDEO_SOURCES.md` for curated links

**Quick recommendations:**
1. Visit https://www.pexels.com/videos/
2. Search: "soccer players" (5 videos, 5-10 sec each)
3. Search: "cricket match" (5 videos, 5-10 sec each)
4. Download to: `data/raw_videos/`
5. Name: `football_01.mp4`, `cricket_01.mp4`, etc.

### Step 4: Run Complete Workflow (10-20 minutes)

**Option A: Automated Script (Recommended)**

```powershell
.\run_workflow.ps1
```

This runs everything automatically:
- Frame extraction
- Detection inference
- Pose estimation
- Evaluation & metrics

**Option B: Manual Step-by-Step**

```powershell
# Extract frames
python src/01_frame_extraction.py --video_dir data/raw_videos --fps 5

# Run detection
python src/03_inference_detection.py --weights yolov8n.pt --source data/raw_videos

# Run pose estimation
python src/04_pose_inference.py --weights yolov8n-pose.pt --source data/raw_videos --frame-by-frame

# Generate metrics
python src/05_evaluation.py --pose-keypoints outputs/poses/football_01_pose.json
```

### Step 5: Collect Results (5 minutes)

1. **Screenshots:**
   - Detection: `outputs/detections/predict/`
   - Pose: `outputs/poses/`
   - Copy 3-5 best examples to: `report/figures/`

2. **Metrics:**
   - Plots: `outputs/metrics/`
   - Review JSON files for statistics

### Step 6: Complete Report (30-60 minutes)

1. Open: `report/report.md`
2. Fill in **PLACEHOLDER** sections:
   - Dataset description (video sources)
   - Results tables (copy from JSON)
   - Discussion (based on outputs)
3. Insert screenshots: `![Description](figures/image.png)`
4. Review for completeness

---

## 📊 Expected Timeline

| Task | Time | Cumulative |
|------|------|------------|
| Setup & install | 5 min | 5 min |
| Download videos | 15 min | 20 min |
| Run workflow | 20 min | 40 min |
| Review outputs | 10 min | 50 min |
| Complete report | 45 min | 95 min |

**Total: ~1.5 hours** (excluding report writing)

---

## 🎯 Deliverables Checklist

Before submission, ensure you have:

- [ ] 10+ video clips (5 football, 5 cricket)
- [ ] Dataset link/description in report
- [ ] All Python scripts in `src/` (already provided)
- [ ] Detection output screenshots (3-5 examples)
- [ ] Pose output screenshots (3-5 examples)
- [ ] Metrics plots in `outputs/metrics/`
- [ ] Completed `report/report.md` with:
  - [ ] Dataset description
  - [ ] Methodology explanation
  - [ ] Results tables (quantitative)
  - [ ] Screenshots (qualitative)
  - [ ] Discussion on challenges
  - [ ] Proposed improvements
  - [ ] References

---

## 🆘 Troubleshooting

**Issue: "Module not found"**
```powershell
pip install -r requirements.txt
```

**Issue: "CUDA not available"**
- Expected on CPU-only setup
- Models will run slower but work fine

**Issue: "No videos found"**
- Check videos are in `data/raw_videos/`
- Supported formats: `.mp4`, `.avi`, `.mov`, `.mkv`

**Issue: "Low detection accuracy"**
- Normal for pre-trained models
- Discuss limitations in report
- Suggest fine-tuning as improvement

**Issue: "Slow inference"**
- Expected on CPU
- Reduce `--imgsz` to 320 or 416
- Process fewer frames (`--max_frames 50`)

---

## 📧 Support Resources

- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **COCO Keypoints:** https://cocodataset.org/#keypoints-2020
- **PyTorch Docs:** https://pytorch.org/docs/

---

## 🎓 Academic Notes

- All code is original or properly attributed
- Using pre-trained models is academically acceptable
- Cite Ultralytics YOLOv8 in references
- No fabricated results - report actual outputs
- Discuss limitations honestly in report

---

Good luck! 🚀
