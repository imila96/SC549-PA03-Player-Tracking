"""
SC549 - PA03: Player Tracking in Sports Videos
Script 04: Pose Estimation Inference

Runs YOLOv8-Pose on videos/images to detect player keypoints.
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import cv2
import torch
from tqdm import tqdm
import numpy as np


def run_pose_inference(
    weights,
    source,
    output_dir,
    conf=0.25,
    iou=0.45,
    imgsz=640,
    save_txt=True
):
    """
    Run YOLOv8-Pose inference on videos or images.
    
    Args:
        weights (str): Path to pose model weights
        source (str): Path to input video/image/directory
        output_dir (str): Directory to save results
        conf (float): Confidence threshold
        iou (float): IoU threshold for NMS
        imgsz (int): Inference image size
        save_txt (bool): Save keypoint results as txt
    """
    # Load model
    print(f"\n🔍 Loading pose estimation model: {weights}")
    model = YOLO(weights)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device.upper()}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n⚙️  Inference Configuration:")
    print(f"   Source: {source}")
    print(f"   Confidence: {conf}")
    print(f"   IoU threshold: {iou}")
    print(f"   Image size: {imgsz}")
    print(f"   Output: {output_path}")
    
    # Run inference
    print(f"\n🚀 Running pose estimation...\n")
    
    results = model.predict(
        source=source,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        device=device,
        save=True,
        save_txt=save_txt,
        project=str(output_path.parent),
        name=output_path.name,
        exist_ok=True,
        verbose=True
    )
    
    # Print summary
    print(f"\n✅ Pose estimation complete!")
    print(f"📊 Processed {len(results)} frame(s)")
    print(f"📂 Results saved to: {output_path}")
    
    # Print keypoint information
    if len(results) > 0 and hasattr(results[0], 'keypoints'):
        print(f"\n🎯 Keypoint Detection:")
        print(f"   Total persons detected: {len(results[0].keypoints)}")
        print(f"   Keypoints per person: {results[0].keypoints.shape[-2] if len(results[0].keypoints) > 0 else 0}")
        print(f"\n📝 COCO Keypoint Format (17 points):")
        print("""
   0: Nose           6: Left Shoulder    12: Left Hip
   1: Left Eye       7: Right Shoulder   13: Right Hip
   2: Right Eye      8: Left Elbow       14: Left Knee
   3: Left Ear       9: Right Elbow      15: Right Knee
   4: Right Ear     10: Left Wrist       16: Left Ankle
   5: Neck          11: Right Wrist      17: Right Ankle
        """)
    
    return results


def run_pose_on_video(
    weights,
    video_path,
    output_path,
    conf=0.25,
    iou=0.45,
    imgsz=640,
    save_keypoints=True
):
    """
    Run pose estimation on a single video with frame-by-frame control.
    
    Args:
        weights (str): Path to pose model weights
        video_path (str): Path to input video
        output_path (str): Path to save output video
        conf (float): Confidence threshold
        iou (float): IoU threshold
        imgsz (int): Inference image size
        save_keypoints (bool): Save keypoint coordinates to txt file
    """
    # Load model
    model = YOLO(weights)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Prepare keypoint output file
    keypoint_data = []
    
    print(f"📹 Processing video: {Path(video_path).name}")
    print(f"   Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
    
    frame_count = 0
    total_persons = 0
    
    pbar = tqdm(total=total_frames, desc="Processing frames", unit="frame")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run pose estimation
        results = model.predict(
            frame,
            conf=conf,
            iou=iou,
            imgsz=imgsz,
            device=device,
            verbose=False
        )
        
        # Get annotated frame
        annotated_frame = results[0].plot()
        
        # Extract keypoint data
        if hasattr(results[0], 'keypoints') and results[0].keypoints is not None:
            num_persons = len(results[0].keypoints)
            total_persons += num_persons
            
            if save_keypoints and num_persons > 0:
                keypoints_xy = results[0].keypoints.xy.cpu().numpy()
                keypoints_conf = results[0].keypoints.conf.cpu().numpy()
                
                for person_id in range(num_persons):
                    kpts = keypoints_xy[person_id]
                    confs = keypoints_conf[person_id]
                    
                    keypoint_data.append({
                        'frame': frame_count,
                        'person_id': person_id,
                        'keypoints': kpts.tolist(),
                        'confidences': confs.tolist()
                    })
        
        # Write frame
        out.write(annotated_frame)
        
        frame_count += 1
        pbar.update(1)
    
    pbar.close()
    cap.release()
    out.release()
    
    avg_persons = total_persons / frame_count if frame_count > 0 else 0
    print(f"✅ Complete! Avg persons per frame: {avg_persons:.2f}")
    print(f"📂 Output video: {output_path}")
    
    # Save keypoint data
    if save_keypoints and keypoint_data:
        import json
        keypoint_file = Path(output_path).with_suffix('.json')
        with open(keypoint_file, 'w') as f:
            json.dump(keypoint_data, f, indent=2)
        print(f"📊 Keypoint data saved: {keypoint_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run YOLOv8-Pose estimation on sports videos"
    )
    parser.add_argument(
        "--weights",
        type=str,
        default="yolov8n-pose.pt",
        help="Path to pose model weights (or model name for pretrained)"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to video file, image, or directory"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/poses",
        help="Output directory for results"
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold (0-1)"
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="IoU threshold for NMS"
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Inference image size"
    )
    parser.add_argument(
        "--no-save-txt",
        action="store_true",
        help="Don't save keypoint results as txt"
    )
    parser.add_argument(
        "--frame-by-frame",
        action="store_true",
        help="Process video frame-by-frame with keypoint extraction"
    )
    
    args = parser.parse_args()
    
    # Check if source exists
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"❌ Error: Source not found: {args.source}")
        return
    
    # Run inference
    if args.frame_by_frame and source_path.is_file() and source_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        output_video = Path(args.output) / f"{source_path.stem}_pose.mp4"
        output_video.parent.mkdir(parents=True, exist_ok=True)
        
        run_pose_on_video(
            weights=args.weights,
            video_path=str(source_path),
            output_path=str(output_video),
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz,
            save_keypoints=not args.no_save_txt
        )
    else:
        run_pose_inference(
            weights=args.weights,
            source=args.source,
            output_dir=args.output,
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz,
            save_txt=not args.no_save_txt
        )


if __name__ == "__main__":
    main()
