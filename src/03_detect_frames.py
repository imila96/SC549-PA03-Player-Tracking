"""
YOLOv8 Detection on Extracted Frames (Ultra Memory-Efficient)
Process individual frames with aggressive memory management
"""
import argparse
from pathlib import Path
from ultralytics import YOLO
import torch
import gc
import json

def process_frames_batch(model, frame_paths, conf, output_file, batch_size=10):
    """Process frames in small batches"""
    detections = []
    
    for i in range(0, len(frame_paths), batch_size):
        batch = frame_paths[i:i+batch_size]
        
        try:
            results = model(batch, conf=conf, verbose=False)
            
            for frame_path, result in zip(batch, results):
                frame_data = {
                    "frame": frame_path.name,
                    "detections": []
                }
                
                if hasattr(result, 'boxes') and result.boxes is not None:
                    for box in result.boxes:
                        detection = {
                            "class": int(box.cls[0]),
                            "confidence": float(box.conf[0]),
                            "bbox": box.xyxy[0].tolist()
                        }
                        frame_data["detections"].append(detection)
                
                detections.append(frame_data)
            
            # Clear memory aggressively
            del results
            gc.collect()
            
            if (i // batch_size) % 10 == 0:
                print(f"   ✓ Processed {i + len(batch)}/{len(frame_paths)} frames...")
                
        except Exception as e:
            print(f"   ⚠️ Error in batch {i}: {e}")
            continue
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(detections, f, indent=2)
    
    return len(detections)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default="yolov8n.pt")
    parser.add_argument("--frames", type=str, default="data/frames")
    parser.add_argument("--output", type=str, default="outputs/detections")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--batch", type=int, default=5)
    args = parser.parse_args()
    
    # Setup
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    frames_path = Path(args.frames)
    
    print(f"🚀 Loading YOLOv8n (tiny model for low memory)")
    model = YOLO(args.weights)
    model.fuse()  # Optimize model
    device = "cpu"
    print(f"🖥️  Device: {device}")
    print(f"📦 Batch size: {args.batch}")
    
    # Get video folders
    video_dirs = [d for d in frames_path.iterdir() if d.is_dir()]
    print(f"\n📂 Found {len(video_dirs)} video folders\n")
    
    # Process each video's frames
    for idx, video_dir in enumerate(video_dirs, 1):
        print(f"{'='*50}")
        print(f"🎬 Video {idx}/{len(video_dirs)}: {video_dir.name}")
        print(f"{'='*50}")
        
        # Get frame files
        frames = sorted(list(video_dir.glob("*.jpg")) + list(video_dir.glob("*.png")))
        
        if not frames:
            print(f"   ⚠️ No frames found\n")
            continue
        
        print(f"   📊 {len(frames)} frames to process")
        
        # Process
        output_json = output_path / f"{video_dir.name}_detections.json"
        
        try:
            processed = process_frames_batch(
                model, frames, args.conf, output_json, args.batch
            )
            print(f"✅ Complete: {processed} frames")
            print(f"📁 Saved: {output_json.name}\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
            continue
        
        # Clear memory between videos
        gc.collect()
    
    print(f"\n{'='*50}")
    print(f"🎉 All videos processed!")
    print(f"📂 Results in: {output_path}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
