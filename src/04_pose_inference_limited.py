"""
SC549 - PA03: Player Tracking in Sports Videos
Script: Pose Estimation on Limited Frames (Memory-Efficient)

Processes first N frames of each video for pose estimation to avoid memory issues.
"""

import cv2
from pathlib import Path
from ultralytics import YOLO
import torch
from tqdm import tqdm

def process_video_limited_frames(video_path, output_path, max_frames=1000, model_weights="yolov8n-pose.pt"):
    """
    Process first N frames of a video with pose estimation.
    
    Args:
        video_path: Path to input video
        output_path: Path to save output video
        max_frames: Maximum number of frames to process
        model_weights: YOLOv8-Pose model weights
    """
    # Load model
    print(f"\n🔍 Loading pose model: {model_weights}")
    model = YOLO(model_weights)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device.upper()}")
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"❌ Error opening video: {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames_to_process = min(max_frames, total_frames)
    
    print(f"\n📹 Video: {Path(video_path).name}")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Total frames: {total_frames}")
    print(f"   Processing: {frames_to_process} frames (~{frames_to_process/fps:.1f} seconds)")
    
    # Setup output video
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    # Process frames
    frame_count = 0
    keypoint_data = []
    
    print(f"\n🏃 Processing frames with pose estimation...")
    pbar = tqdm(total=frames_to_process, desc="Processing")
    
    while frame_count < frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run pose inference
        results = model.predict(frame, conf=0.25, verbose=False)
        
        # Draw keypoints on frame
        if len(results) > 0 and results[0].keypoints is not None:
            annotated_frame = results[0].plot()
            
            # Store keypoint data
            keypoints = results[0].keypoints
            if keypoints.xy is not None and len(keypoints.xy) > 0:
                keypoint_data.append({
                    'frame': frame_count,
                    'num_persons': len(keypoints.xy),
                    'confidence': keypoints.conf.mean().item() if keypoints.conf is not None else 0
                })
        else:
            annotated_frame = frame
        
        out.write(annotated_frame)
        frame_count += 1
        pbar.update(1)
    
    pbar.close()
    cap.release()
    out.release()
    
    print(f"\n✅ Pose estimation complete!")
    print(f"📊 Processed: {frame_count} frames")
    print(f"👥 Detected persons in: {len(keypoint_data)} frames")
    if keypoint_data:
        avg_conf = sum(d['confidence'] for d in keypoint_data) / len(keypoint_data)
        print(f"📈 Average confidence: {avg_conf:.3f}")
    print(f"💾 Saved to: {output_path}")
    
    return keypoint_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Pose estimation on limited frames")
    parser.add_argument("--source", required=True, help="Input video path")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--max-frames", type=int, default=1000, help="Max frames to process (default: 1000)")
    parser.add_argument("--weights", default="yolov8n-pose.pt", help="Model weights")
    
    args = parser.parse_args()
    
    source = Path(args.source)
    if not source.exists():
        print(f"❌ Error: Source not found: {args.source}")
        return
    
    process_video_limited_frames(
        video_path=source,
        output_path=args.output,
        max_frames=args.max_frames,
        model_weights=args.weights
    )


if __name__ == "__main__":
    main()
