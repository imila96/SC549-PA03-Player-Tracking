"""
SC549 - PA03: Player Tracking in Sports Videos
Script 03: Detection Inference

Runs YOLOv8 detection on videos/images and saves annotated outputs.
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import cv2
import torch
from tqdm import tqdm


def run_detection_inference(
    weights,
    source,
    output_dir,
    conf=0.25,
    iou=0.45,
    imgsz=640,
    save_txt=True,
    save_conf=True
):
    """
    Run YOLOv8 detection inference on videos or images.
    
    Args:
        weights (str): Path to model weights
        source (str): Path to input video/image/directory
        output_dir (str): Directory to save results
        conf (float): Confidence threshold
        iou (float): IoU threshold for NMS
        imgsz (int): Inference image size
        save_txt (bool): Save detection results as txt
        save_conf (bool): Save confidence scores
    """
    # Load model
    print(f"\n🔍 Loading detection model: {weights}")
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
    print(f"\n🚀 Running detection inference...\n")
    
    results = model.predict(
        source=source,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        device=device,
        save=True,
        save_txt=save_txt,
        save_conf=save_conf,
        project=str(output_path.parent),
        name=output_path.name,
        exist_ok=True,
        verbose=True
    )
    
    # Print summary
    print(f"\n✅ Detection complete!")
    print(f"📊 Processed {len(results)} frame(s)")
    print(f"📂 Results saved to: {output_path}")
    
    return results


def run_detection_on_video(
    weights,
    video_path,
    output_path,
    conf=0.25,
    iou=0.45,
    imgsz=640
):
    """
    Run detection on a single video with frame-by-frame control.
    
    Args:
        weights (str): Path to model weights
        video_path (str): Path to input video
        output_path (str): Path to save output video
        conf (float): Confidence threshold
        iou (float): IoU threshold
        imgsz (int): Inference image size
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
    
    print(f"📹 Processing video: {Path(video_path).name}")
    print(f"   Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")
    
    frame_count = 0
    total_detections = 0
    
    pbar = tqdm(total=total_frames, desc="Processing frames", unit="frame")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run detection
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
        
        # Count detections
        num_detections = len(results[0].boxes)
        total_detections += num_detections
        
        # Write frame
        out.write(annotated_frame)
        
        frame_count += 1
        pbar.update(1)
    
    pbar.close()
    cap.release()
    out.release()
    
    avg_detections = total_detections / frame_count if frame_count > 0 else 0
    print(f"✅ Complete! Avg detections per frame: {avg_detections:.2f}")
    print(f"📂 Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 detection inference on sports videos"
    )
    parser.add_argument(
        "--weights",
        type=str,
        default="yolov8n.pt",
        help="Path to model weights (or model name for pretrained)"
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
        default="outputs/detections",
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
        help="Don't save detection results as txt"
    )
    parser.add_argument(
        "--no-save-conf",
        action="store_true",
        help="Don't save confidence scores"
    )
    parser.add_argument(
        "--frame-by-frame",
        action="store_true",
        help="Process video frame-by-frame (slower but more control)"
    )
    
    args = parser.parse_args()
    
    # Check if source exists
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"❌ Error: Source not found: {args.source}")
        return
    
    # Run inference
    if args.frame_by_frame and source_path.is_file() and source_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        output_video = Path(args.output) / f"{source_path.stem}_detected.mp4"
        output_video.parent.mkdir(parents=True, exist_ok=True)
        
        run_detection_on_video(
            weights=args.weights,
            video_path=str(source_path),
            output_path=str(output_video),
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz
        )
    else:
        run_detection_inference(
            weights=args.weights,
            source=args.source,
            output_dir=args.output,
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz,
            save_txt=not args.no_save_txt,
            save_conf=not args.no_save_conf
        )


if __name__ == "__main__":
    main()
