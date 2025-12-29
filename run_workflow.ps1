# SC549-PA03: Complete Workflow Script
# Automates the entire pipeline from frame extraction to evaluation

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "SC549-PA03: Player Tracking Workflow" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Project directory
$ProjectRoot = "C:\Users\Public\SC549-PA03-Player-Tracking"
Set-Location $ProjectRoot

# Step 0: Check prerequisites
Write-Host "[Step 0] Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check if videos exist
$VideoDir = Join-Path $ProjectRoot "data\raw_videos"
$Videos = Get-ChildItem -Path $VideoDir -Include *.mp4,*.avi,*.mov,*.mkv -Recurse

if ($Videos.Count -eq 0) {
    Write-Host "ERROR: No videos found in data/raw_videos/" -ForegroundColor Red
    Write-Host "Please download videos first (see VIDEO_SOURCES.md)" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($Videos.Count) video(s)" -ForegroundColor Green
foreach ($video in $Videos) {
    Write-Host "  - $($video.Name)" -ForegroundColor Gray
}
Write-Host ""

# Check Python environment
Write-Host "Checking Python environment..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 1: Install dependencies
Write-Host "[Step 1] Installing dependencies..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Would you like to install/update dependencies? (Y/N)" -ForegroundColor Cyan
$Install = Read-Host

if ($Install -eq "Y" -or $Install -eq "y") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Dependency installation failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "Skipping dependency installation" -ForegroundColor Gray
}
Write-Host ""

# Step 2: Extract frames
Write-Host "[Step 2] Extracting frames from videos..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Frame extraction rate (FPS): 5 (default)" -ForegroundColor Gray
Write-Host "Running: python src/01_frame_extraction.py" -ForegroundColor Gray
Write-Host ""

python src/01_frame_extraction.py --video_dir data/raw_videos --output_dir data/frames --fps 5

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Frame extraction failed" -ForegroundColor Red
    exit 1
}
Write-Host "Frame extraction complete" -ForegroundColor Green
Write-Host ""

# Step 3: Run detection
Write-Host "[Step 3] Running player detection..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Using pre-trained YOLOv8n model" -ForegroundColor Gray
Write-Host "Running: python src/03_inference_detection.py" -ForegroundColor Gray
Write-Host ""

python src/03_inference_detection.py --weights yolov8n.pt --source data/raw_videos --output outputs/detections --conf 0.25

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Detection inference failed" -ForegroundColor Red
    exit 1
}
Write-Host "Detection complete" -ForegroundColor Green
Write-Host ""

# Step 4: Run pose estimation
Write-Host "[Step 4] Running pose estimation..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Using pre-trained YOLOv8n-Pose model" -ForegroundColor Gray
Write-Host "Running: python src/04_pose_inference.py" -ForegroundColor Gray
Write-Host ""

python src/04_pose_inference.py --weights yolov8n-pose.pt --source data/raw_videos --output outputs/poses --conf 0.25 --frame-by-frame

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Pose estimation failed" -ForegroundColor Red
    exit 1
}
Write-Host "Pose estimation complete" -ForegroundColor Green
Write-Host ""

# Step 5: Evaluation
Write-Host "[Step 5] Generating evaluation metrics..." -ForegroundColor Yellow
Write-Host ""

# Find keypoint JSON files
$KeypointFiles = Get-ChildItem -Path "outputs/poses" -Filter "*_pose.json" -Recurse

if ($KeypointFiles.Count -eq 0) {
    Write-Host "WARNING: No keypoint JSON files found" -ForegroundColor Yellow
    Write-Host "Skipping evaluation" -ForegroundColor Yellow
} else {
    Write-Host "Found $($KeypointFiles.Count) keypoint file(s)" -ForegroundColor Gray
    
    # Run evaluation on first keypoint file
    $FirstKeypointFile = $KeypointFiles[0].FullName
    Write-Host "Evaluating: $($KeypointFiles[0].Name)" -ForegroundColor Gray
    Write-Host ""
    
    python src/05_evaluation.py --pose-keypoints $FirstKeypointFile --output outputs/metrics
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Evaluation completed with errors" -ForegroundColor Yellow
    } else {
        Write-Host "Evaluation complete" -ForegroundColor Green
    }
}
Write-Host ""

# Step 6: Summary
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Workflow Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Output Summary:" -ForegroundColor Cyan
Write-Host "  Detection results: outputs/detections/" -ForegroundColor Gray
Write-Host "  Pose results: outputs/poses/" -ForegroundColor Gray
Write-Host "  Metrics & plots: outputs/metrics/" -ForegroundColor Gray
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review outputs in outputs/ directories" -ForegroundColor Gray
Write-Host "2. Collect screenshots for report" -ForegroundColor Gray
Write-Host "3. Complete report in report/report.md" -ForegroundColor Gray
Write-Host "4. Update placeholders with actual results" -ForegroundColor Gray
Write-Host ""

Write-Host "Report Template: report/report.md" -ForegroundColor Cyan
Write-Host "Exploration Notebook: notebooks/exploration.ipynb" -ForegroundColor Cyan
Write-Host ""

# Open outputs folder
Write-Host "Would you like to open the outputs folder? (Y/N)" -ForegroundColor Cyan
$OpenFolder = Read-Host

if ($OpenFolder -eq "Y" -or $OpenFolder -eq "y") {
    explorer (Join-Path $ProjectRoot "outputs")
}

Write-Host ""
Write-Host "Done! Good luck with your assignment!" -ForegroundColor Green
