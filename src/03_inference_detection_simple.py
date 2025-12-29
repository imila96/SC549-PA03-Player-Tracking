"""
Simple YOLOv8 Detection Inference (Memory-Efficient)
Process videos one at a time without visualization to avoid memory errors
"""
import argparse
from pathlib import Path
from ultralytics import YOLO
import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default="yolov8n.pt")
    parser.add_argument("--source", type=str, required=True)
    parser.add_argument("--output", type=str, default="outputs/detections")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--imgsz", type=int, default=640)
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load model
    print(f"🚀 Loading YOLOv8 model: {args.weights}")
    model = YOLO(args.weights)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device}")
    
    # Get video files
    source_path = Path(args.source)
    if source_path.is_dir():
        video_files = (list(source_path.glob("*.mp4")) + 
                      list(source_path.glob("*.avi")) + 
                      list(source_path.glob("*.mov")))
        print(f"\n📂 Found {len(video_files)} videos\n")
    else:
        video_files = [source_path]
    
    # Process each video separately
    for idx, video_file in enumerate(video_files, 1):
        print(f"{'='*60}")
        print(f"🎬 Video {idx}/{len(video_files)}: {video_file.name}")
        print(f"{'='*60}")
        
        video_output = output_path / video_file.stem
        video_output.mkdir(exist_ok=True)
        
        try:
            # Run inference - NO visualization to save memory
            results = model.predict(
                source=str(video_file),
                conf=args.conf,
                imgsz=args.imgsz,
                device=device,
                save=False,  # Don't save images
                save_txt=True,  # Save text detections
                save_conf=True,
                project=str(video_output.parent),
                name=video_output.name,
                exist_ok=True,
                stream=True,  # Stream mode for lower memory
                verbose=False  # Less verbose output
            )
            
            # Count detections
            frame_count = 0
            total_detections = 0
            for result in results:
                frame_count += 1
                if hasattr(result, 'boxes') and result.boxes is not None:
                    total_detections += len(result.boxes)
                if frame_count % 500 == 0:
                    print(f"   ✓ Processed {frame_count} frames...")
            
            print(f"✅ Complete: {frame_count} frames, {total_detections} total detections")
            print(f"📁 Results saved to: {video_output}\n")
            
        except Exception as e:
            print(f"❌ Error processing {video_file.name}: {e}\n")
            continue
    
    print(f"\n{'='*60}")
    print(f"🎉 All videos processed!")
    print(f"📂 Results in: {output_path}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
