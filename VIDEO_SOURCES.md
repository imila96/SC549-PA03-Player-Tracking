# SC549-PA03: Recommended Video Sources

## Free Sports Video Sources (No Copyright Issues)

### 🎯 Recommended Platforms

1. **Pexels Videos** (https://www.pexels.com/videos/)
   - Completely free, no attribution required
   - High quality, diverse content
   - Direct download

2. **Pixabay Videos** (https://pixabay.com/videos/)
   - Free for commercial use
   - Good quality stock footage
   - Easy download

3. **Videvo** (https://www.videvo.net/)
   - Free HD stock footage
   - Filter by "Free" license
   - Sports category available

---

## 📹 Specific Video Recommendations

### Football Videos (5 clips minimum)

**Search terms on Pexels/Pixabay:**
- "soccer players"
- "football match"
- "soccer game"
- "football training"
- "soccer field"

**Recommended videos (examples):**

1. **Pexels - Football Match Action**
   - URL: https://www.pexels.com/video/soccer-players-in-action-3621043/
   - Duration: 11 seconds ✅
   - Quality: Multiple players, good visibility

2. **Pexels - Soccer Training**
   - URL: https://www.pexels.com/video/boys-playing-soccer-5608846/
   - Duration: 15 seconds (use first 10)
   - Quality: Clear player movements

3. **Pexels - Football Game**
   - URL: https://www.pexels.com/video/football-players-in-green-and-white-jersey-shirt-4753994/
   - Duration: 10 seconds ✅
   - Quality: Good contrast, multiple players

4. **Pixabay - Soccer Match**
   - URL: https://pixabay.com/videos/soccer-football-game-sport-ball-7529/
   - Duration: 8 seconds ✅
   - Quality: Stadium view, clear players

5. **Pexels - Football Players**
   - URL: https://www.pexels.com/video/a-soccer-player-dribbling-a-ball-4753989/
   - Duration: 8 seconds ✅
   - Quality: Close-up, good for pose detection

### Cricket Videos (5 clips minimum)

**Search terms:**
- "cricket match"
- "cricket players"
- "cricket game"
- "cricket batting"
- "cricket bowling"

**Recommended videos:**

1. **Pexels - Cricket Match**
   - URL: https://www.pexels.com/video/men-playing-cricket-5607247/
   - Duration: 14 seconds (use 5-10 sec)
   - Quality: Multiple players visible

2. **Pexels - Cricket Game**
   - URL: https://www.pexels.com/video/a-group-of-men-playing-cricket-8313314/
   - Duration: 10 seconds ✅
   - Quality: Good field view

3. **Pexels - Cricket Players**
   - URL: https://www.pexels.com/video/men-playing-cricket-on-field-5663317/
   - Duration: 7 seconds ✅
   - Quality: Close players, good lighting

4. **Videvo - Cricket Action**
   - Search on Videvo: "cricket"
   - Filter: Free, 5-15 seconds
   - Download: MP4 format

5. **Pexels - Cricket Practice**
   - URL: https://www.pexels.com/video/people-playing-cricket-5663270/
   - Duration: 6 seconds ✅
   - Quality: Clear player poses

---

## 📥 Download Instructions

### Method 1: Direct Browser Download (Easiest)

1. Click video link
2. Click **Download** button
3. Select **HD** or **Full HD** quality (smaller file size okay)
4. Save to: `C:\Users\Public\SC549-PA03-Player-Tracking\data\raw_videos\`

**Naming convention:**
- `football_01.mp4`, `football_02.mp4`, etc.
- `cricket_01.mp4`, `cricket_02.mp4`, etc.

### Method 2: Using PowerShell (Bulk Download)

If you have video URLs, use this script:

```powershell
# Navigate to project
cd "C:\Users\Public\SC549-PA03-Player-Tracking\data\raw_videos"

# Download using Invoke-WebRequest (example)
# Replace with actual direct download URLs
Invoke-WebRequest -Uri "VIDEO_URL" -OutFile "football_01.mp4"
```

**Note:** Pexels/Pixabay require clicking download button (no direct URL), so manual download is easier.

---

## ✅ Checklist

Once downloaded, verify:

- [ ] At least 5 football videos in `data/raw_videos/`
- [ ] At least 5 cricket videos in `data/raw_videos/`
- [ ] Each video is 5-15 seconds long
- [ ] Videos are in `.mp4` format (or `.avi`, `.mov`)
- [ ] Total: 10 videos minimum

---

## 🎬 Alternative: Use Sample Videos

If you prefer, you can also:

1. Record phone videos of sports on TV (5-10 seconds each)
2. Use YouTube clips (download with `yt-dlp` tool, ensure fair use)
3. Search university/open datasets (less variety)

---

## 🚀 Next Steps

After downloading videos:

1. Run frame extraction:
   ```bash
   python src/01_frame_extraction.py --video_dir data/raw_videos --fps 5
   ```

2. Proceed to detection and pose inference (I'll guide you)

---

## ⚠️ Important Notes

- **Copyright:** Only use videos with free/commercial licenses
- **Academic Use:** These sources are acceptable for educational projects
- **Dataset Link:** In your report, cite Pexels/Pixabay as sources
- **Quality:** Prefer videos with:
  - Multiple players visible
  - Good lighting
  - Minimal camera shake
  - Resolution ≥720p
