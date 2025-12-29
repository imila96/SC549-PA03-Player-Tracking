"""
SC549 - PA03: Pose Estimation (Extract Keypoints Only - No Video)
Memory-efficient approach: Extract and save keypoint data without video rendering
"""

import cv2
import json
from pathlib import Path
from ultralytics import YOLO
import torch
from tqdm import tqdm
import numpy as np


def extract_pose_keypoints(video_path, output_json, max_frames=1000, model_weights="yolov8n-pose.pt"):
    """
    Extract pose keypoints from video frames without creating output video.
    Saves keypoint data to JSON for analysis.
    """
    print(f"\n🔍 Loading pose model: {model_weights}")
    model = YOLO(model_weights)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device.upper()}")
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"❌ Error opening video: {video_path}")
        return None
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames_to_process = min(max_frames, total_frames)
    
    print(f"\n📹 Video: {Path(video_path).name}")
    print(f"   Resolution: {width}x{height}, FPS: {fps}")
    print(f"   Processing: {frames_to_process}/{total_frames} frames (~{frames_to_process/fps:.1f} seconds)")
    
    # Process frames and collect keypoints
    results_data = {
        'video_name': Path(video_path).name,
        'resolution': [width, height],
        'fps': fps,
        'frames_processed': 0,
        'frames_with_detections': 0,
        'total_persons_detected': 0,
        'keypoints': []
    }
    
    print(f"\n🏃 Extracting pose keypoints...")
    pbar = tqdm(total=frames_to_process, desc="Processing")
    
    frame_count = 0
    while frame_count < frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run pose inference
        results = model.predict(frame, conf=0.25, imgsz=384, verbose=False)
        
        # Extract keypoint data
        if len(results) > 0 and results[0].keypoints is not None:
            keypoints = results[0].keypoints
            
            if keypoints.xy is not None and len(keypoints.xy) > 0:
                results_data['frames_with_detections'] += 1
                results_data['total_persons_detected'] += len(keypoints.xy)
                
                frame_data = {
                    'frame_num': frame_count,
                    'num_persons': len(keypoints.xy),
                    'persons': []
                }
                
                # Store each person's keypoints
                for person_idx in range(len(keypoints.xy)):
                    person_kpts = keypoints.xy[person_idx].cpu().numpy()
                    person_conf = keypoints.conf[person_idx].cpu().numpy() if keypoints.conf is not None else None
                    
                    person_data = {
                        'person_id': person_idx,
                        'keypoints_xy': person_kpts.tolist(),
                        'keypoints_conf': person_conf.tolist() if person_conf is not None else None,
                        'avg_confidence': float(person_conf.mean()) if person_conf is not None else 0.0
                    }
                    frame_data['persons'].append(person_data)
                
                results_data['keypoints'].append(frame_data)
        
        frame_count += 1
        pbar.update(1)
    
    pbar.close()
    cap.release()
    
    results_data['frames_processed'] = frame_count
    
    # Save to JSON
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\n✅ Pose keypoint extraction complete!")
    print(f"📊 Frames processed: {results_data['frames_processed']}")
    print(f"👥 Frames with detections: {results_data['frames_with_detections']}")
    print(f"🎯 Total persons detected: {results_data['total_persons_detected']}")
    if results_data['frames_with_detections'] > 0:
        avg_persons = results_data['total_persons_detected'] / results_data['frames_with_detections']
        print(f"📈 Average persons per frame: {avg_persons:.2f}")
    print(f"💾 Keypoint data saved to: {output_path}")
    
    return results_data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract pose keypoints from video")
    parser.add_argument("--source", required=True, help="Input video path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--max-frames", type=int, default=1000, help="Max frames (default: 1000)")
    parser.add_argument("--weights", default="yolov8n-pose.pt", help="Model weights")
    
    args = parser.parse_args()
    
    source = Path(args.source)
    if not source.exists():
        print(f"❌ Error: Source not found: {args.source}")
        return
    
    extract_pose_keypoints(
        video_path=source,
        output_json=args.output,
        max_frames=args.max_frames,
        model_weights=args.weights
    )


if __name__ == "__main__":
    main()
