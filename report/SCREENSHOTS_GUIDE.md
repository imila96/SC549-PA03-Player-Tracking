# Screenshots & Output Visualization Guide

## 📸 How to Capture Screenshots for Report

### Location of Outputs

All annotated outputs are saved in:
- **Detection Results:** `outputs/detections/`
- **Pose Results:** `outputs/poses/`
- **Original Frames:** `data/frames/`

---

## 🎬 Viewing Annotated Videos

### Detection Videos
1. Navigate to `outputs/detections/`
2. Open `.avi` or `.mp4` files using:
   - Windows Media Player
   - VLC Player
   - Any video player
3. Look for videos with bounding boxes around detected players

### Pose Estimation Videos
1. Navigate to `outputs/poses/`
2. Open video files showing:
   - Skeleton overlays on players
   - 17 keypoint markers
   - Connection lines between joints

---

## 📷 Taking Screenshots for Report

### Recommended Tools
- **Snipping Tool** (Windows built-in): `Win + Shift + S`
- **VLC Player:** Tools → Take Snapshot
- **Media Player:** Pause + Screenshot

### What to Capture

#### 1. Detection Examples (4-5 screenshots)
- **Good Detection:** Frame with multiple players clearly detected
- **Occlusion Case:** Dense player formation showing detection challenges
- **Different Sports:** One example each from football, rugby, hockey
- **Confidence Scores:** Frame showing bounding boxes with confidence values

Suggested filenames:
- `detection_football_good.png`
- `detection_rugby_occlusion.png`
- `detection_hockey_distance.png`
- `detection_badminton_clear.png`

#### 2. Pose Estimation Examples (4-5 screenshots)
- **Full Skeleton:** Player with all 17 keypoints visible
- **Partial Pose:** Player with some keypoints occluded
- **Action Pose:** Dynamic pose (jumping, running, hitting)
- **Multiple Players:** Frame showing poses for multiple players

Suggested filenames:
- `pose_full_skeleton.png`
- `pose_action_badminton.png`
- `pose_multiple_football.png`
- `pose_partial_hockey.png`

#### 3. Comparison Examples (2-3 screenshots)
- **Side-by-side:** Original frame vs. Detection vs. Pose
- **Challenge Showcase:** Before/after showing difficult scenarios

---

## 🖼️ Organizing Screenshots

### Save Location
Save all screenshots to: `report/figures/`

### File Naming Convention
```
<type>_<sport>_<description>.png

Examples:
- detection_football_10players.png
- pose_badminton_smash.png
- comparison_rugby_haka.png
- metrics_training_curves.png
```

---

## 📊 Additional Visuals to Include

### 1. Training Curves (If Available)
- Loss curves
- mAP curves
- Precision/Recall curves
Location: `outputs/metrics/training_curves.png`

### 2. Performance Charts (If Generated)
- Bar charts comparing metrics
- Confidence distributions
- Detection counts per frame
Location: `outputs/metrics/`

### 3. Keypoint Heatmaps (Optional)
- Confidence distribution across keypoints
- Visibility statistics

---

## 🎥 Creating Screenshot Examples from Videos

### Using VLC Player

1. **Open video** in VLC
2. **Pause** at desired frame (`Space` key)
3. **Take snapshot:**
   - Go to: `Video → Take Snapshot`
   - Or press: `Shift + S`
4. **Find screenshot:**
   - Default location: `C:\Users\<Username>\Pictures\`
   - Or check: `Tools → Preferences → Video → Directory`

### Using Windows Snipping Tool

1. **Open video** and pause at frame
2. **Press:** `Win + Shift + S`
3. **Select area** to capture
4. **Paste** into Paint or image editor
5. **Save** to `report/figures/`

### Using Python (Automated)

If you want to extract specific frames programmatically:

```python
import cv2

# Open video
cap = cv2.VideoCapture('outputs/detections/26.avi')

# Go to specific frame (e.g., frame 100)
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
ret, frame = cap.read()

if ret:
    cv2.imwrite('report/figures/screenshot_frame100.png', frame)

cap.release()
```

---

## 📋 Screenshot Checklist for Report

Before finalizing report, ensure you have:

### Detection Outputs (Minimum 3)
- [ ] Clear detection with multiple players
- [ ] Challenging scenario (occlusion/distance)
- [ ] Different sport examples

### Pose Outputs (Minimum 3)
- [ ] Full skeleton visible
- [ ] Action pose captured
- [ ] Multiple player poses

### Performance Visualizations (Optional)
- [ ] Training curves (if fine-tuned)
- [ ] Metrics comparison charts
- [ ] Confidence distributions

### Comparison Shots (Optional)
- [ ] Original vs. Annotated
- [ ] Detection vs. Pose overlay

---

## 🔗 Linking Screenshots in Report

In `report.md`, use relative paths:

```markdown
![Detection Example - Football](figures/detection_football_10players.png)
*Figure 1: YOLOv8 detection on football match showing 12 players*

![Pose Example - Badminton](figures/pose_badminton_smash.png)
*Figure 2: YOLOv8-Pose keypoint detection during badminton smash*
```

---

## 💡 Tips for High-Quality Screenshots

1. **Resolution:** Pause video in fullscreen for better quality
2. **Clarity:** Choose frames without motion blur
3. **Visibility:** Ensure annotations (boxes, keypoints) are clearly visible
4. **Variety:** Show different sports, player counts, scenarios
5. **Context:** Include frame number or timestamp if relevant

---

## ⚠️ Important Notes

1. **Copyright:** Screenshots are for educational purposes (fair use)
2. **Attribution:** Mention video sources in report captions
3. **File Size:** Keep images <2MB each for GitHub
4. **Format:** PNG preferred for quality, JPEG for smaller size
5. **Annotation:** Add captions explaining what screenshot demonstrates

---

## 🎯 Quick Workflow

1. ✅ Open detection video in VLC
2. ✅ Pause at interesting frame
3. ✅ Press `Shift + S` to snapshot
4. ✅ Move to `report/figures/`
5. ✅ Rename descriptively
6. ✅ Repeat for pose videos
7. ✅ Add to report.md with captions

---

**Ready to capture?** Start with the detection videos in `outputs/detections/` and work through this checklist systematically!
