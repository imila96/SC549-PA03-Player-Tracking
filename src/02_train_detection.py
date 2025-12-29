"""
SC549 - PA03: Player Tracking in Sports Videos
Script 02: Train YOLOv8 Detection Model

Fine-tunes YOLOv8 on custom sports player dataset.
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import torch


def train_detection_model(
    data_yaml,
    model_size="n",
    epochs=50,
    imgsz=640,
    batch=8,
    project="models/detection",
    name="player_detector",
    pretrained=True
):
    """
    Train YOLOv8 detection model.
    
    Args:
        data_yaml (str): Path to dataset YAML file
        model_size (str): Model size (n/s/m/l/x)
        epochs (int): Number of training epochs
        imgsz (int): Input image size
        batch (int): Batch size
        project (str): Project directory for saving results
        name (str): Experiment name
        pretrained (bool): Use pretrained weights
    """
    # Initialize model
    model_name = f"yolov8{model_size}.pt" if pretrained else f"yolov8{model_size}.yaml"
    print(f"\n🚀 Initializing YOLOv8 model: {model_name}")
    
    model = YOLO(model_name)
    
    # Display device info
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Device: {device.upper()}")
    
    if device == "cpu":
        print("⚠️  Warning: Training on CPU will be slow. Consider reducing epochs or using pretrained model.")
    
    # Training configuration
    print(f"\n⚙️  Training Configuration:")
    print(f"   Dataset: {data_yaml}")
    print(f"   Epochs: {epochs}")
    print(f"   Image size: {imgsz}")
    print(f"   Batch size: {batch}")
    print(f"   Device: {device}")
    
    # Train model
    print(f"\n🏋️  Starting training...\n")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        device=device,
        patience=10,  # Early stopping patience
        save=True,
        save_period=10,  # Save checkpoint every 10 epochs
        plots=True,  # Generate training plots
        verbose=True
    )
    
    print(f"\n✅ Training complete!")
    print(f"📊 Results saved to: {Path(project) / name}")
    print(f"🎯 Best model: {Path(project) / name / 'weights' / 'best.pt'}")
    
    return results


def validate_dataset(data_yaml):
    """
    Validate dataset YAML configuration.
    
    Args:
        data_yaml (str): Path to dataset YAML file
    
    Returns:
        bool: True if valid, False otherwise
    """
    import yaml
    
    data_path = Path(data_yaml)
    
    if not data_path.exists():
        print(f"❌ Error: Dataset YAML not found: {data_yaml}")
        print(f"\n📝 Expected format (data.yaml):")
        print("""
path: ../datasets/player_detection  # Dataset root
train: images/train  # Train images
val: images/val      # Validation images

names:
  0: player
        """)
        return False
    
    with open(data_path, 'r') as f:
        data_config = yaml.safe_load(f)
    
    required_keys = ['path', 'train', 'val', 'names']
    for key in required_keys:
        if key not in data_config:
            print(f"❌ Error: Missing required key '{key}' in {data_yaml}")
            return False
    
    print(f"✅ Dataset YAML validated")
    print(f"   Classes: {list(data_config['names'].values())}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Train YOLOv8 detection model for player tracking"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to dataset YAML file (e.g., data/datasets/data.yaml)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="n",
        choices=["n", "s", "m", "l", "x"],
        help="Model size (n=nano, s=small, m=medium, l=large, x=xlarge)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size"
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=8,
        help="Batch size (reduce if out of memory)"
    )
    parser.add_argument(
        "--project",
        type=str,
        default="models/detection",
        help="Project directory for saving results"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="player_detector",
        help="Experiment name"
    )
    parser.add_argument(
        "--no-pretrained",
        action="store_true",
        help="Train from scratch (not recommended)"
    )
    
    args = parser.parse_args()
    
    # Validate dataset
    if not validate_dataset(args.data):
        return
    
    # Train model
    train_detection_model(
        data_yaml=args.data,
        model_size=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
        pretrained=not args.no_pretrained
    )


if __name__ == "__main__":
    main()
