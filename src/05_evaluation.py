"""
SC549 - PA03: Player Tracking in Sports Videos
Script 05: Evaluation and Metrics

Evaluates detection and pose estimation performance.
Generates precision, recall, mAP metrics and visualization plots.
"""

import argparse
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ultralytics import YOLO
import pandas as pd


def evaluate_detection_model(model_path, data_yaml, output_dir):
    """
    Evaluate YOLOv8 detection model on validation set.
    
    Args:
        model_path (str): Path to trained model weights
        data_yaml (str): Path to dataset YAML
        output_dir (str): Directory to save evaluation results
    
    Returns:
        dict: Evaluation metrics
    """
    print(f"\n📊 Evaluating detection model: {model_path}")
    
    # Load model
    model = YOLO(model_path)
    
    # Run validation
    results = model.val(
        data=data_yaml,
        split='val',
        save_json=True,
        save_hybrid=True,
        plots=True,
        verbose=True
    )
    
    # Extract metrics
    metrics = {
        'precision': float(results.box.p),
        'recall': float(results.box.r),
        'mAP50': float(results.box.map50),
        'mAP50-95': float(results.box.map),
        'fitness': float(results.fitness)
    }
    
    print(f"\n✅ Detection Evaluation Results:")
    print(f"   Precision: {metrics['precision']:.4f}")
    print(f"   Recall: {metrics['recall']:.4f}")
    print(f"   mAP@0.5: {metrics['mAP50']:.4f}")
    print(f"   mAP@0.5:0.95: {metrics['mAP50-95']:.4f}")
    
    # Save metrics
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    metrics_file = output_path / 'detection_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"📂 Metrics saved to: {metrics_file}")
    
    return metrics


def analyze_training_logs(log_file, output_dir):
    """
    Analyze training logs and generate loss curves.
    
    Args:
        log_file (str): Path to training log file (results.csv)
        output_dir (str): Directory to save plots
    """
    print(f"\n📈 Analyzing training logs: {log_file}")
    
    # Read training results
    try:
        df = pd.read_csv(log_file)
        df.columns = df.columns.str.strip()  # Remove whitespace from column names
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Plot training curves
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Training Progress', fontsize=16, fontweight='bold')
    
    # Loss curves
    loss_cols = [col for col in df.columns if 'loss' in col.lower()]
    if loss_cols:
        ax = axes[0, 0]
        for col in loss_cols:
            ax.plot(df['epoch'], df[col], label=col, marker='o', markersize=3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # mAP curves
    map_cols = [col for col in df.columns if 'map' in col.lower()]
    if map_cols:
        ax = axes[0, 1]
        for col in map_cols:
            ax.plot(df['epoch'], df[col], label=col, marker='o', markersize=3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('mAP')
        ax.set_title('Mean Average Precision')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Precision/Recall
    if 'precision' in df.columns and 'recall' in df.columns:
        ax = axes[1, 0]
        ax.plot(df['epoch'], df['precision'], label='Precision', marker='o', markersize=3)
        ax.plot(df['epoch'], df['recall'], label='Recall', marker='o', markersize=3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Score')
        ax.set_title('Precision & Recall')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Learning rate (if available)
    lr_cols = [col for col in df.columns if 'lr' in col.lower()]
    if lr_cols:
        ax = axes[1, 1]
        for col in lr_cols:
            ax.plot(df['epoch'], df[col], label=col, marker='o', markersize=3)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Learning Rate')
        ax.set_title('Learning Rate Schedule')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_file = output_path / 'training_curves.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"📊 Training curves saved to: {plot_file}")
    plt.close()


def analyze_pose_results(keypoint_file, output_dir):
    """
    Analyze pose estimation results and generate statistics.
    
    Args:
        keypoint_file (str): Path to keypoint JSON file
        output_dir (str): Directory to save analysis
    """
    print(f"\n🎯 Analyzing pose estimation results: {keypoint_file}")
    
    # Load keypoint data
    try:
        with open(keypoint_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading keypoint file: {e}")
        return
    
    if not data:
        print("⚠️  No keypoint data found")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Extract statistics
    num_frames = len(set(d['frame'] for d in data))
    num_detections = len(data)
    avg_persons_per_frame = num_detections / num_frames if num_frames > 0 else 0
    
    # Analyze keypoint confidences
    all_confidences = []
    for detection in data:
        all_confidences.extend(detection['confidences'])
    
    avg_confidence = np.mean(all_confidences)
    
    print(f"\n✅ Pose Estimation Statistics:")
    print(f"   Total frames: {num_frames}")
    print(f"   Total persons detected: {num_detections}")
    print(f"   Avg persons per frame: {avg_persons_per_frame:.2f}")
    print(f"   Avg keypoint confidence: {avg_confidence:.4f}")
    
    # Visualize keypoint confidence distribution
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle('Pose Estimation Analysis', fontsize=16, fontweight='bold')
    
    # Confidence histogram
    ax = axes[0]
    ax.hist(all_confidences, bins=50, edgecolor='black', alpha=0.7)
    ax.axvline(avg_confidence, color='red', linestyle='--', label=f'Mean: {avg_confidence:.3f}')
    ax.set_xlabel('Confidence Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Keypoint Confidence Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Persons per frame
    frames = [d['frame'] for d in data]
    ax = axes[1]
    frame_counts = pd.Series(frames).value_counts().sort_index()
    ax.plot(frame_counts.index, frame_counts.values, marker='o', markersize=3)
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('Number of Persons Detected')
    ax.set_title('Persons Detected Per Frame')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_file = output_path / 'pose_analysis.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"📊 Pose analysis saved to: {plot_file}")
    plt.close()
    
    # Save statistics
    stats = {
        'num_frames': num_frames,
        'num_detections': num_detections,
        'avg_persons_per_frame': avg_persons_per_frame,
        'avg_keypoint_confidence': avg_confidence
    }
    
    stats_file = output_path / 'pose_statistics.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"📂 Statistics saved to: {stats_file}")


def generate_comparison_report(detection_metrics, pose_stats, output_dir):
    """
    Generate comparative analysis report.
    
    Args:
        detection_metrics (dict): Detection evaluation metrics
        pose_stats (dict): Pose estimation statistics
        output_dir (str): Directory to save report
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create comparison visualization
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle('Performance Comparison', fontsize=16, fontweight='bold')
    
    # Detection metrics
    if detection_metrics:
        ax = axes[0]
        metrics = ['precision', 'recall', 'mAP50', 'mAP50-95']
        values = [detection_metrics.get(m, 0) for m in metrics]
        bars = ax.bar(metrics, values, color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'])
        ax.set_ylabel('Score')
        ax.set_title('Detection Performance')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontweight='bold')
    
    # Pose statistics
    if pose_stats:
        ax = axes[1]
        labels = ['Avg Persons\nPer Frame', 'Avg Keypoint\nConfidence']
        values = [
            pose_stats.get('avg_persons_per_frame', 0),
            pose_stats.get('avg_keypoint_confidence', 0)
        ]
        
        # Normalize for visualization
        normalized_values = [
            min(values[0] / 5, 1),  # Normalize to max 5 persons
            values[1]  # Confidence already 0-1
        ]
        
        bars = ax.bar(labels, normalized_values, color=['#9b59b6', '#1abc9c'])
        ax.set_ylabel('Normalized Score')
        ax.set_title('Pose Estimation Performance')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add actual values as text
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{values[i]:.3f}',
                   ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    plot_file = output_path / 'performance_comparison.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"\n📊 Comparison report saved to: {plot_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate detection and pose estimation performance"
    )
    parser.add_argument(
        "--detection-model",
        type=str,
        help="Path to trained detection model weights"
    )
    parser.add_argument(
        "--data-yaml",
        type=str,
        help="Path to dataset YAML for detection evaluation"
    )
    parser.add_argument(
        "--training-log",
        type=str,
        help="Path to training log file (results.csv)"
    )
    parser.add_argument(
        "--pose-keypoints",
        type=str,
        help="Path to pose keypoints JSON file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/metrics",
        help="Output directory for evaluation results"
    )
    
    args = parser.parse_args()
    
    detection_metrics = None
    pose_stats = None
    
    # Evaluate detection model
    if args.detection_model and args.data_yaml:
        if Path(args.detection_model).exists() and Path(args.data_yaml).exists():
            detection_metrics = evaluate_detection_model(
                args.detection_model,
                args.data_yaml,
                args.output
            )
        else:
            print(f"⚠️  Warning: Detection model or data YAML not found")
    
    # Analyze training logs
    if args.training_log:
        if Path(args.training_log).exists():
            analyze_training_logs(args.training_log, args.output)
        else:
            print(f"⚠️  Warning: Training log not found: {args.training_log}")
    
    # Analyze pose results
    if args.pose_keypoints:
        if Path(args.pose_keypoints).exists():
            analyze_pose_results(args.pose_keypoints, args.output)
            
            # Load stats for comparison
            stats_file = Path(args.output) / 'pose_statistics.json'
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    pose_stats = json.load(f)
        else:
            print(f"⚠️  Warning: Pose keypoints file not found: {args.pose_keypoints}")
    
    # Generate comparison report
    if detection_metrics or pose_stats:
        generate_comparison_report(detection_metrics, pose_stats, args.output)
    
    print(f"\n✅ Evaluation complete!")
    print(f"📂 All results saved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
