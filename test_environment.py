"""
SC549 - PA03: Quick Test Script
Tests the environment and runs a simple detection on a sample image.
"""

import sys
from pathlib import Path

def test_environment():
    """Test if all required packages are installed."""
    print("🔍 Testing environment setup...\n")
    
    required_packages = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'ultralytics': 'Ultralytics YOLOv8',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'pandas': 'Pandas'
    }
    
    missing = []
    installed = []
    
    for package, name in required_packages.items():
        try:
            if package == 'cv2':
                import cv2
            else:
                __import__(package)
            installed.append(name)
            print(f"✅ {name}")
        except ImportError:
            missing.append(name)
            print(f"❌ {name} - NOT INSTALLED")
    
    print(f"\n📊 Status: {len(installed)}/{len(required_packages)} packages installed")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Run: pip install -r requirements.txt")
        return False
    
    # Test PyTorch
    import torch
    print(f"\n🖥️  PyTorch version: {torch.__version__}")
    print(f"   Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    return True


def test_yolo_download():
    """Test YOLOv8 model download."""
    print("\n🔍 Testing YOLOv8 model download...\n")
    
    try:
        from ultralytics import YOLO
        
        print("Downloading YOLOv8n (detection model)...")
        model_det = YOLO('yolov8n.pt')
        print(f"✅ Detection model ready: yolov8n.pt")
        
        print("\nDownloading YOLOv8n-Pose (pose model)...")
        model_pose = YOLO('yolov8n-pose.pt')
        print(f"✅ Pose model ready: yolov8n-pose.pt")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_on_sample_image():
    """Run detection on a sample image if available."""
    print("\n🔍 Looking for sample images to test...\n")
    
    try:
        from ultralytics import YOLO
        import cv2
        import numpy as np
        
        # Check if there are any frames extracted
        frames_dir = Path("data/frames")
        sample_image = None
        
        if frames_dir.exists():
            images = list(frames_dir.rglob("*.jpg")) + list(frames_dir.rglob("*.png"))
            if images:
                sample_image = str(images[0])
        
        if not sample_image:
            print("⚠️  No sample images found in data/frames/")
            print("   Run frame extraction first or place test image manually")
            return True
        
        print(f"📸 Testing on: {Path(sample_image).name}")
        
        # Test detection
        print("\n1️⃣  Running detection...")
        model_det = YOLO('yolov8n.pt')
        results_det = model_det.predict(sample_image, conf=0.25, verbose=False)
        num_detections = len(results_det[0].boxes)
        print(f"   ✅ Detected {num_detections} object(s)")
        
        # Test pose
        print("\n2️⃣  Running pose estimation...")
        model_pose = YOLO('yolov8n-pose.pt')
        results_pose = model_pose.predict(sample_image, conf=0.25, verbose=False)
        num_persons = len(results_pose[0].keypoints) if hasattr(results_pose[0], 'keypoints') else 0
        print(f"   ✅ Detected {num_persons} person(s) with keypoints")
        
        # Save test output
        output_dir = Path("outputs/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        det_output = output_dir / "test_detection.jpg"
        pose_output = output_dir / "test_pose.jpg"
        
        cv2.imwrite(str(det_output), results_det[0].plot())
        cv2.imwrite(str(pose_output), results_pose[0].plot())
        
        print(f"\n📂 Test outputs saved:")
        print(f"   Detection: {det_output}")
        print(f"   Pose: {pose_output}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_project_structure():
    """Verify project directory structure."""
    print("\n🔍 Checking project structure...\n")
    
    required_dirs = [
        "data/raw_videos",
        "data/frames",
        "models/detection",
        "models/pose",
        "src",
        "outputs/detections",
        "outputs/poses",
        "outputs/metrics",
        "report"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - MISSING")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 60)
    print("SC549-PA03: Environment Test Script")
    print("=" * 60)
    
    # Test 1: Project structure
    if not check_project_structure():
        print("\n⚠️  Some directories are missing. This should not happen.")
        print("   The setup script should have created all directories.")
    
    # Test 2: Python packages
    if not test_environment():
        print("\n❌ Environment test failed!")
        print("   Please install required packages: pip install -r requirements.txt")
        sys.exit(1)
    
    # Test 3: YOLO models
    if not test_yolo_download():
        print("\n❌ YOLO model download failed!")
        print("   Check your internet connection")
        sys.exit(1)
    
    # Test 4: Sample inference (if data available)
    test_on_sample_image()
    
    print("\n" + "=" * 60)
    print("✅ Environment test complete!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Download videos to data/raw_videos/ (see VIDEO_SOURCES.md)")
    print("2. Extract frames: python src/01_frame_extraction.py")
    print("3. Run detection: python src/03_inference_detection.py --source data/raw_videos")
    print("4. Run pose: python src/04_pose_inference.py --source data/raw_videos")


if __name__ == "__main__":
    main()
