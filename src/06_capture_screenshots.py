"""
06_capture_screenshots.py
Capture representative screenshots from detection videos for the report
"""

import cv2
import os
from pathlib import Path
import random

def capture_screenshots(detection_dir, output_dir, num_screenshots=3):
    """
    Capture random frames from each detection video as screenshots
    
    Args:
        detection_dir: Directory containing detection videos
        output_dir: Directory to save screenshots
        num_screenshots: Number of screenshots per video
    """
    detection_dir = Path(detection_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📸 Capturing screenshots from detection videos...")
    print(f"Source: {detection_dir}")
    print(f"Output: {output_dir}\n")
    
    # Find all detection videos (only files, not directories)
    video_files = [f for f in detection_dir.glob("*.avi") if f.is_file()]
    video_files += [f for f in detection_dir.glob("*.mp4") if f.is_file()]
    
    if not video_files:
        print("❌ No video files found!")
        return
    
    print(f"Found {len(video_files)} videos:\n")
    
    total_screenshots = 0
    
    for video_file in sorted(video_files):
        print(f"Processing: {video_file.name}")
        
        # Open video
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"  ❌ Failed to open video")
            continue
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"  Frames: {total_frames}, FPS: {fps}, Duration: {duration:.1f}s")
        
        # Select random frames (avoiding first/last 10% which might be blank)
        start_frame = int(total_frames * 0.1)
        end_frame = int(total_frames * 0.9)
        
        if end_frame - start_frame < num_screenshots:
            # If video too short, just take evenly spaced frames
            frame_indices = [int(i * total_frames / num_screenshots) for i in range(num_screenshots)]
        else:
            # Random sampling from middle 80% of video
            frame_indices = sorted(random.sample(range(start_frame, end_frame), num_screenshots))
        
        print(f"  Capturing frames: {frame_indices}")
        
        # Capture screenshots
        screenshots_saved = 0
        for idx, frame_number in enumerate(frame_indices):
            # Seek to frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if not ret:
                print(f"    ⚠️  Failed to read frame {frame_number}")
                continue
            
            # Generate output filename
            video_name = video_file.stem
            screenshot_name = f"{video_name}_screenshot_{idx+1}_frame{frame_number}.jpg"
            screenshot_path = output_dir / screenshot_name
            
            # Save screenshot
            cv2.imwrite(str(screenshot_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            # Get file size
            file_size = os.path.getsize(screenshot_path) / 1024  # KB
            
            print(f"    ✅ Saved: {screenshot_name} ({file_size:.1f} KB)")
            screenshots_saved += 1
            total_screenshots += 1
        
        cap.release()
        print(f"  ✅ {screenshots_saved}/{num_screenshots} screenshots captured\n")
    
    print(f"\n{'='*60}")
    print(f"✅ Screenshot Capture Complete!")
    print(f"Total screenshots: {total_screenshots}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}")

def capture_single_best_frame(detection_dir, output_dir):
    """
    Capture one representative frame from each video (from middle)
    
    Args:
        detection_dir: Directory containing detection videos
        output_dir: Directory to save screenshots
    """
    detection_dir = Path(detection_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📸 Capturing single best frame from each detection video...\n")
    
    # Find all detection videos (only files, not directories)
    video_files = [f for f in detection_dir.glob("*.avi") if f.is_file()]
    video_files += [f for f in detection_dir.glob("*.mp4") if f.is_file()]
    
    for video_file in sorted(video_files):
        print(f"Processing: {video_file.name}")
        
        # Open video
        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"  ❌ Failed to open video")
            continue
        
        # Get middle frame
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        middle_frame = total_frames // 2
        
        # Seek and capture
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
        ret, frame = cap.read()
        
        if ret:
            # Save screenshot
            video_name = video_file.stem
            screenshot_name = f"{video_name}_detection.jpg"
            screenshot_path = output_dir / screenshot_name
            
            cv2.imwrite(str(screenshot_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            file_size = os.path.getsize(screenshot_path) / 1024
            print(f"  ✅ Saved: {screenshot_name} ({file_size:.1f} KB)")
        else:
            print(f"  ❌ Failed to capture frame")
        
        cap.release()
        print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Capture screenshots from detection videos")
    parser.add_argument("--detection-dir", type=str, 
                        default="../outputs/detections",
                        help="Directory containing detection videos")
    parser.add_argument("--output-dir", type=str,
                        default="../outputs/screenshots",
                        help="Directory to save screenshots")
    parser.add_argument("--num-screenshots", type=int, default=3,
                        help="Number of screenshots per video (default: 3)")
    parser.add_argument("--single", action="store_true",
                        help="Capture only one frame per video (middle frame)")
    
    args = parser.parse_args()
    
    print("="*60)
    print("SC549-PA03: Screenshot Capture Tool")
    print("="*60)
    print()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    if args.single:
        capture_single_best_frame(args.detection_dir, args.output_dir)
    else:
        capture_screenshots(args.detection_dir, args.output_dir, args.num_screenshots)
