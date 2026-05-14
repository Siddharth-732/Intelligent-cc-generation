import cv2
import os
from pathlib import Path
from typing import List, Dict

def extract_frames_at(video_path: str, timestamps: List[float], output_dir: str = "outputs/frames") -> Dict[float, List[str]]:
    """
    Extracts frames in a wider window around the timestamp to catch late reactions.
    """
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    
    results = {}
    video_name = Path(video_path).stem

    for ts in timestamps:
        # We now look from -0.1s to +1.0s after the sound
        # (People often take 0.5s to react)
        offsets = [-0.1, 0.2, 0.5, 0.8, 1.2] 
        frame_paths = []
        
        for offset in offsets:
            target_ts = max(0, ts + offset)
            cap.set(cv2.CAP_PROP_POS_MSEC, target_ts * 1000)
            success, frame = cap.read()
            
            if success:
                filename = f"{video_name}_{ts:0.2f}_offset_{offset:0.1f}.jpg"
                path = os.path.join(output_dir, filename)
                cv2.imwrite(path, frame)
                frame_paths.append(path)
        
        results[ts] = frame_paths

    cap.release()
    return results
