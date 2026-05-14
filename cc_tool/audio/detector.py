import numpy as np
import soundfile as sf
import tensorflow_hub as hub
import csv
import os
from cc_tool.audio.models import AudioEvent
from cc_tool.audio.utils import chunk_audio, normalize_waveform
from cc_tool.audio.mapping import get_canonical_label, _IGNORE_GROUPS

# AudioSet indices for speech - we ignore these
SPEECH_INDICES = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

class SoundEventDetector:
    def __init__(self, confidence_threshold=0.25): # Lowered threshold slightly for grouped detection
        self.confidence_threshold = confidence_threshold
        self._model = None
        self._class_names = []

    def _load_model(self):
        if self._model is None:
            self._model = hub.load("https://tfhub.dev/google/yamnet/1")
            class_map_path = self._model.class_map_path().numpy().decode()
            if os.path.exists(class_map_path):
                with open(class_map_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self._class_names = [row["display_name"] for row in reader]
            else:
                import urllib.request
                with urllib.request.urlopen(class_map_path) as f:
                    reader = csv.DictReader(line.decode("utf-8") for line in f)
                    self._class_names = [row["display_name"] for row in reader]

    def detect(self, wav_path):
        self._load_model()
        waveform, sr = sf.read(wav_path, dtype="float32")
        if waveform.ndim > 1: waveform = waveform.mean(axis=1)
        waveform = normalize_waveform(waveform)

        chunks = chunk_audio(waveform, sr)
        raw_events = []

        for start_sec, end_sec, chunk in chunks:
            scores, _, _ = self._model(chunk)
            mean_scores = scores.numpy().mean(axis=0)
            
            # Multi-label grouped scoring:
            # Sum scores for each canonical group across all 521 YAMNet classes.
            group_scores = {}
            for idx, score in enumerate(mean_scores):
                if idx in SPEECH_INDICES: continue
                canonical = get_canonical_label(self._class_names[idx])
                group_scores[canonical] = group_scores.get(canonical, 0) + score
            
            # Emit EVERY group that clears the threshold — not just the loudest one.
            # This is the key fix: co-occurring sounds (e.g., crowd + snake hiss)
            # were previously suppressed because only max() was kept per chunk.
            # Skip _ambient_ — it's the catch-all for unmapped background classes.
            for group, score in group_scores.items():
                if group in _IGNORE_GROUPS:
                    continue
                if score >= self.confidence_threshold:
                    raw_events.append(AudioEvent(
                        label=group,
                        confidence=float(score),
                        start_sec=start_sec,
                        end_sec=end_sec
                    ))

        return self._merge_events(raw_events)

    def _merge_events(self, events):
        if not events: return []
        events.sort(key=lambda x: x.start_sec)
        merged = [events[0]]
        for curr in events[1:]:
            prev = merged[-1]
            if curr.label == prev.label and curr.start_sec <= prev.end_sec:
                prev.end_sec = max(prev.end_sec, curr.end_sec)
                prev.confidence = max(prev.confidence, curr.confidence)
            else:
                merged.append(curr)
        return merged