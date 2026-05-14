import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
from cc_tool.vision.models import ReactionResult

class ReactionDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh
        
        self.pose = self.mp_pose.Pose(static_image_mode=True, model_complexity=1)
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pose.close()
        self.face_mesh.close()

    def _get_baseline_landmarks(self, frame_path) -> Optional[np.ndarray]:
        """
        Hybrid detector: Tries Pose first, falls back to FaceMesh for head/shoulders.
        """
        image = cv2.imread(frame_path)
        if image is None: return None
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 1. Try Pose (Full/Half body)
        pose_res = self.pose.process(rgb)
        if pose_res.pose_landmarks:
            lm = pose_res.pose_landmarks.landmark
            # Track Shoulders and Hips
            return np.array([[lm[i].x, lm[i].y] for i in [11, 12, 23, 24]])
        
        # 2. Fallback to FaceMesh (Head only)
        face_res = self.face_mesh.process(rgb)
        if face_res.multi_face_landmarks:
            lm = face_res.multi_face_landmarks[0].landmark
            # Track Nose and Eyes
            return np.array([[lm[i].x, lm[i].y] for i in [1, 33, 263]])
            
        return None

    def analyze_frames(self, event_idx: int, frame_paths: List[str]) -> ReactionResult:
        """
        BUG FIX: 
        - Compares all frames to pre-event baseline (Frame 0).
        - Lower sensitivity thresholds (3-8% body height).
        """
        if len(frame_paths) < 2:
            return ReactionResult(event_idx, "none", 0.0, None)

        # Baseline: The state of the person BEFORE/AT the sound starts
        baseline = self._get_baseline_landmarks(frame_paths[0])
        if baseline is None:
            return ReactionResult(event_idx, "none", 0.0, None)

        max_movement = 0.0
        for path in frame_paths[1:]:
            current = self._get_baseline_landmarks(path)
            if current is not None and current.shape == baseline.shape:
                # Calculate movement relative to the baseline
                dist = np.linalg.norm(current - baseline, axis=1)
                max_movement = max(max_movement, np.mean(dist))

        # BUG FIX: Lowered thresholds for "startle" detection
        # 0.015 - 0.03 (1.5% - 3%) = Posture shift / Startle
        # > 0.08 (8%) = Significant movement
        confidence = min(1.0, max_movement * 15)
        
        reaction_type = "none"
        if max_movement > 0.06:
            reaction_type = "significant_movement"
        elif max_movement > 0.015:
            reaction_type = "reaction/startle"

        return ReactionResult(
            event_index=event_idx,
            reaction_type=reaction_type,
            confidence=confidence,
            frame_path=frame_paths[len(frame_paths)//2]
        )
