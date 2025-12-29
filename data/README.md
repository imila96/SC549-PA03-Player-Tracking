# Dataset Instructions

## Option A: Using Pre-trained Models (No Annotation Required)

If you want to use pre-trained YOLOv8 models without fine-tuning:

1. Place your video clips in `data/raw_videos/`
2. Skip annotation steps
3. Run inference directly with `yolov8n.pt` (pre-trained)

## Option B: Fine-tuning with Custom Dataset

If you want to fine-tune the model on your specific sports dataset:

### Step 1: Extract Frames
```bash
python src/01_frame_extraction.py --video_dir data/raw_videos --fps 5
```

### Step 2: Annotate Frames

**Recommended Tools:**
- **Roboflow** (https://roboflow.com/) - Web-based, free tier, YOLO export
- **CVAT** (https://www.cvat.ai/) - Open-source, powerful
- **LabelImg** (https://github.com/heartexlabs/labelImg) - Desktop tool

**Annotation Steps:**
1. Upload frames from `data/frames/`
2. Draw bounding boxes around players
3. Label all boxes as "player"
4. Export in **YOLO format** (txt files with normalized coordinates)

### Step 3: Organize Dataset

Create the following structure:
```
data/datasets/player_detection/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### Step 4: Create data.yaml

Copy `data.yaml.example` to `data.yaml` and update paths if needed.

### Step 5: Train

```bash
python src/02_train_detection.py --data data/datasets/data.yaml --epochs 50
```

## Dataset Recommendations

**Minimum Requirements:**
- 5-10 video clips
- 5-10 seconds each
- At least 100 annotated frames for training

**Optimal:**
- 10+ video clips
- Diverse sports and camera angles
- 300+ annotated frames
