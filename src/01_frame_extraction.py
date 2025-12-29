"""
SC549 - PA03: Player Tracking in Sports Videos
Script 01: Frame Extraction from Video Clips

Extracts frames from sports video clips at specified FPS for annotation and training.
"""

import os
import cv2
import argparse
from pathlib import Path
from tqdm import tqdm


def extract_frames(video_path, output_dir, fps=5, max_frames=None):
    """
    Extract frames from a video file at specified FPS.
    
    Args:
        video_path (str): Path to input video
        output_dir (str): Directory to save extracted frames
        fps (int): Frame extraction rate (frames per second)
        max_frames (int): Maximum number of frames to extract (None = all)
    
    Returns:
        int: Number of frames extracted
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video {video_path}")
        return 0
    
    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_name = Path(video_path).stem
    
    print(f"\n📹 Processing: {video_name}")
    print(f"   Original FPS: {video_fps:.2f}")
    print(f"   Total frames: {total_frames}")
    
    # Calculate frame interval
    frame_interval = int(video_fps / fps) if fps < video_fps else 1
    
    # Create output directory
    video_output_dir = Path(output_dir) / video_name
    video_output_dir.mkdir(parents=True, exist_ok=True)
    
    frame_count = 0
    saved_count = 0
    
    pbar = tqdm(total=total_frames, desc=f"Extracting from {video_name}", unit="frame")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Extract frame at specified interval
        if frame_count % frame_interval == 0:
            frame_filename = video_output_dir / f"frame_{saved_count:04d}.jpg"
            cv2.imwrite(str(frame_filename), frame)
            saved_count += 1
            
            if max_frames and saved_count >= max_frames:
                break
        
        frame_count += 1
        pbar.update(1)
    
    pbar.close()
    cap.release()
    
    print(f"✅ Extracted {saved_count} frames → {video_output_dir}")
    return saved_count


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames from sports video clips"
    )
    parser.add_argument(
        "--video_dir",
        type=str,
        default="data/raw_videos",
        help="Directory containing video files"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data/frames",
        help="Directory to save extracted frames"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=5,
        help="Frame extraction rate (frames per second)"
    )
    parser.add_argument(
        "--max_frames",
        type=int,
        default=None,
        help="Maximum frames per video (None = all)"
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=["mp4", "avi", "mov", "mkv"],
        help="Video file extensions to process"
    )
    
    args = parser.parse_args()
    
    # Find all video files
    video_dir = Path(args.video_dir)
    if not video_dir.exists():
        print(f"❌ Error: Video directory not found: {video_dir}")
        print(f"   Please create the directory and add video files.")
        return
    
    video_files = []
    for ext in args.extensions:
        video_files.extend(video_dir.glob(f"*.{ext}"))
        video_files.extend(video_dir.glob(f"*.{ext.upper()}"))
    
    if not video_files:
        print(f"❌ No video files found in {video_dir}")
        print(f"   Supported extensions: {args.extensions}")
        return
    
    print(f"🎬 Found {len(video_files)} video file(s)")
    print(f"⚙️  Extraction settings: {args.fps} FPS, Max frames: {args.max_frames or 'All'}")
    
    # Extract frames from each video
    total_frames = 0
    for video_file in video_files:
        frames_extracted = extract_frames(
            str(video_file),
            args.output_dir,
            fps=args.fps,
            max_frames=args.max_frames
        )
        total_frames += frames_extracted
    
    print(f"\n✅ Complete! Total frames extracted: {total_frames}")
    print(f"📂 Output directory: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
