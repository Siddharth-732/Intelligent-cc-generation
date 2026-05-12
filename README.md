# Intelligent CC Suggestion Tool — Goal 1

## Sound Event Detection Module
This module automatically detects and classifies non-speech audio events (like honking, laughter, music) from a video file.

---

## 🛠 Setup Instructions

### 1. Prerequisites
- **Python 3.10+**
- **FFmpeg**: Must be installed and available in your system's PATH.
  - *Windows*: `winget install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```bash
# Clone the repository
git clone https://github.com/Siddharth-732/Intelligent-cc-generation.git
cd Intelligent-cc-generation

# Create a virtual environment
python -m venv .venv

# Activate the environment
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage
Verify the installation by running the test script on a video file:

```bash
python test_goal_1.py "path/to/your/video.mp4"
```

---

## 💻 Programmatic Usage
```python
from cc_tool.audio import extract_audio, SoundEventDetector

# 1. Extract audio from video
wav_path = extract_audio("video.mp4")

# 2. Initialize detector
detector = SoundEventDetector(confidence_threshold=0.3)

# 3. Detect non-speech events
events = detector.detect(wav_path)

for e in events:
    print(f"[{e.start_sec}s - {e.end_sec}s] {e.label} ({e.confidence})")
```

---

## 📁 Project Structure
- `cc_tool/audio/extractor.py`: Audio extraction logic.
- `cc_tool/audio/detector.py`: YAMNet model implementation.
- `cc_tool/audio/models.py`: Data models.
- `cc_tool/audio/utils.py`: Audio processing utilities.
