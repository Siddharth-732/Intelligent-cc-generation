from cc_tool.audio.detector import SoundEventDetector
from cc_tool.vision.frame_extractor import extract_frames_at
from cc_tool.vision.reaction_detector import ReactionDetector
import sys
import os

def test_goal_2(video_path):
    print(f"--- Starting Goal 2 Analysis ---")
    print(f"Video: {video_path}")
    
    # 1. Detect Audio Events (Goal 1)
    # We use the existing wav if available
    wav_path = f"outputs/audio/{os.path.basename(video_path).split('.')[0]}.wav"
    if not os.path.exists(wav_path):
        from cc_tool.audio.extractor import extract_audio
        wav_path = extract_audio(video_path)
    
    detector = SoundEventDetector(confidence_threshold=0.3)
    audio_events = detector.detect(wav_path)
    
    if not audio_events:
        print("No audio events found to analyze.")
        return

    # 2. Extract Frames around those events
    print(f"Found {len(audio_events)} audio events. Extracting frames...")
    timestamps = [e.start_sec for e in audio_events]
    frames_map = extract_frames_at(video_path, timestamps)
    
    # 3. Analyze Reactions
    print("Analyzing visual reactions...")
    results = []
    with ReactionDetector() as reaction_detector:
        for idx, event in enumerate(audio_events):
            frame_paths = frames_map.get(event.start_sec, [])
            reaction = reaction_detector.analyze_frames(idx, frame_paths)
            results.append((event, reaction))
            
            print(f"\n[{event.start_sec:0.2f}s] Sound: {event.label}")
            print(f"       Visual Reaction: {reaction.reaction_type} (Conf: {reaction.confidence:0.2f})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_goal_2.py <path_to_video>")
    else:
        test_goal_2(sys.argv[1])
