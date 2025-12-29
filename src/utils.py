"""
SC549 - PA03: Player Tracking in Sports Videos
Utility Functions

Helper functions for video processing, visualization, and data handling.
"""

import cv2
import numpy as np
from pathlib import Path
import json


def load_video_info(video_path):
    """
    Load basic information about a video file.
    
    Args:
        video_path (str): Path to video file
    
    Returns:
        dict: Video information (fps, resolution, frame count, duration)
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return None
    
    info = {
        'path': str(video_path),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    }
    
    cap.release()
    return info


def draw_bounding_boxes(image, boxes, labels=None, confidences=None, color=(0, 255, 0)):
    """
    Draw bounding boxes on an image.
    
    Args:
        image (np.ndarray): Input image
        boxes (list): List of bounding boxes [x1, y1, x2, y2]
        labels (list): Optional class labels
        confidences (list): Optional confidence scores
        color (tuple): Box color in BGR
    
    Returns:
        np.ndarray: Annotated image
    """
    img = image.copy()
    
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        
        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        if labels or confidences:
            label_text = ""
            if labels:
                label_text += f"{labels[i]}"
            if confidences:
                label_text += f" {confidences[i]:.2f}"
            
            # Draw background for text
            (text_width, text_height), _ = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            cv2.rectangle(
                img,
                (x1, y1 - text_height - 5),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Draw text
            cv2.putText(
                img,
                label_text,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
    
    return img


def draw_keypoints(image, keypoints, confidences=None, threshold=0.5):
    """
    Draw pose keypoints on an image (COCO format).
    
    Args:
        image (np.ndarray): Input image
        keypoints (np.ndarray): Keypoint coordinates (17x2 or Nx17x2)
        confidences (np.ndarray): Keypoint confidences (17 or Nx17)
        threshold (float): Confidence threshold for drawing
    
    Returns:
        np.ndarray: Annotated image
    """
    img = image.copy()
    
    # COCO skeleton connections
    skeleton = [
        [16, 14], [14, 12], [17, 15], [15, 13], [12, 13],  # Legs
        [6, 8], [8, 10], [7, 9], [9, 11],  # Arms
        [6, 12], [7, 13],  # Torso
        [6, 7],  # Shoulders
        [0, 1], [0, 2], [1, 3], [2, 4], [0, 5], [0, 6]  # Face to body
    ]
    
    # Colors for different body parts
    colors = {
        'face': (255, 200, 100),
        'upper_body': (100, 255, 100),
        'lower_body': (100, 100, 255)
    }
    
    # Handle single or multiple persons
    if keypoints.ndim == 2:
        keypoints = keypoints[np.newaxis, :]
        if confidences is not None:
            confidences = confidences[np.newaxis, :]
    
    for person_idx in range(len(keypoints)):
        kpts = keypoints[person_idx]
        confs = confidences[person_idx] if confidences is not None else np.ones(len(kpts))
        
        # Draw skeleton connections
        for connection in skeleton:
            pt1_idx, pt2_idx = connection
            if pt1_idx >= len(kpts) or pt2_idx >= len(kpts):
                continue
            
            if confs[pt1_idx] > threshold and confs[pt2_idx] > threshold:
                pt1 = tuple(map(int, kpts[pt1_idx]))
                pt2 = tuple(map(int, kpts[pt2_idx]))
                
                # Choose color based on body part
                if max(pt1_idx, pt2_idx) <= 4:
                    color = colors['face']
                elif max(pt1_idx, pt2_idx) <= 11:
                    color = colors['upper_body']
                else:
                    color = colors['lower_body']
                
                cv2.line(img, pt1, pt2, color, 2)
        
        # Draw keypoints
        for idx, (kpt, conf) in enumerate(zip(kpts, confs)):
            if conf > threshold:
                x, y = map(int, kpt)
                cv2.circle(img, (x, y), 4, (0, 255, 255), -1)
                cv2.circle(img, (x, y), 4, (0, 0, 0), 1)
    
    return img


def create_dataset_yaml(dataset_path, class_names, output_file="data.yaml"):
    """
    Create YOLO dataset YAML configuration file.
    
    Args:
        dataset_path (str): Path to dataset root directory
        class_names (list): List of class names
        output_file (str): Output YAML filename
    
    Returns:
        str: Path to created YAML file
    """
    import yaml
    
    dataset_path = Path(dataset_path)
    
    config = {
        'path': str(dataset_path.resolve()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {i: name for i, name in enumerate(class_names)}
    }
    
    yaml_path = dataset_path / output_file
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(yaml_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Dataset YAML created: {yaml_path}")
    return str(yaml_path)


def split_dataset(image_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1, seed=42):
    """
    Split dataset into train/val/test sets.
    
    Args:
        image_dir (str): Directory containing images
        train_ratio (float): Training set ratio
        val_ratio (float): Validation set ratio
        test_ratio (float): Test set ratio
        seed (int): Random seed for reproducibility
    
    Returns:
        dict: Split information
    """
    import random
    import shutil
    
    image_dir = Path(image_dir)
    images = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
    
    # Shuffle with seed
    random.seed(seed)
    random.shuffle(images)
    
    # Calculate splits
    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]
    
    # Create directories
    splits = {
        'train': train_images,
        'val': val_images,
        'test': test_images
    }
    
    dataset_root = image_dir.parent
    
    for split_name, split_images in splits.items():
        img_dir = dataset_root / 'images' / split_name
        label_dir = dataset_root / 'labels' / split_name
        
        img_dir.mkdir(parents=True, exist_ok=True)
        label_dir.mkdir(parents=True, exist_ok=True)
        
        for img_path in split_images:
            # Copy image
            shutil.copy(img_path, img_dir / img_path.name)
            
            # Copy corresponding label if exists
            label_path = img_path.parent.parent / 'labels' / img_path.with_suffix('.txt').name
            if label_path.exists():
                shutil.copy(label_path, label_dir / label_path.name)
    
    split_info = {
        'train': len(train_images),
        'val': len(val_images),
        'test': len(test_images),
        'total': total
    }
    
    print(f"✅ Dataset split complete:")
    print(f"   Train: {split_info['train']} ({train_ratio*100:.0f}%)")
    print(f"   Val: {split_info['val']} ({val_ratio*100:.0f}%)")
    print(f"   Test: {split_info['test']} ({test_ratio*100:.0f}%)")
    
    return split_info


def save_detection_results(results, output_file):
    """
    Save detection results to JSON file.
    
    Args:
        results (list): Detection results from YOLO
        output_file (str): Output JSON file path
    """
    output_data = []
    
    for result in results:
        frame_data = {
            'image_path': result.path,
            'detections': []
        }
        
        for box in result.boxes:
            detection = {
                'class': int(box.cls[0]),
                'confidence': float(box.conf[0]),
                'bbox': box.xyxy[0].tolist()
            }
            frame_data['detections'].append(detection)
        
        output_data.append(frame_data)
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Detection results saved: {output_file}")


def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two bounding boxes.
    
    Args:
        box1 (list): [x1, y1, x2, y2]
        box2 (list): [x1, y1, x2, y2]
    
    Returns:
        float: IoU score
    """
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])
    y2_inter = min(box1[3], box2[3])
    
    inter_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
    
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0


if __name__ == "__main__":
    print("Utility functions for SC549-PA03 Player Tracking")
    print("Import this module to use the helper functions.")
