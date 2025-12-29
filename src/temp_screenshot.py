"""Quick script to capture remaining screenshots"""
import cv2
from pathlib import Path
import os

output_dir = Path('../outputs/screenshots')
output_dir.mkdir(exist_ok=True)

videos = [
    (Path(r'C:\Users\Public\SC549-PA03-Player-Tracking\outputs\detections\Badminton.avi') / '🇮🇳 India vs Indonesia 🇮🇩 _ Men\'s Badminton doubles _ Paris 2024 Highlights.avi', 'Badminton'),
    (Path(r'C:\Users\Public\SC549-PA03-Player-Tracking\outputs\detections\Hockey.avi') / '🇦🇺 Australia vs. India 🇮🇳 _ Men\'s Hockey _ #Paris2024 Highlights.avi', 'Hockey'),
    (Path(r'C:\Users\Public\SC549-PA03-Player-Tracking\outputs\detections\Rugby Haka.avi') / 'The Greatest haka EVER_.avi', 'Rugby Haka')
]

for v, name in videos:
    if not v.is_file():
        print(f"❌ Not a file: {v}")
        continue
        
    print(f"Processing: {name}")
    cap = cv2.VideoCapture(str(v))
    
    if not cap.isOpened():
        print(f"  ❌ Failed to open")
        continue
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mid = total_frames // 2
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    
    if ret:
        out_path = output_dir / f'{name}_detection.jpg'
        cv2.imwrite(str(out_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        size = os.path.getsize(out_path) / 1024
        print(f"  ✅ Saved: {out_path.name} ({size:.1f} KB)")
    else:
        print(f"  ❌ Failed to read frame")
    
    cap.release()

print("\n✅ Done!")
