# Aryavarta - Linux & Raspberry Pi 5 Compatibility Guide

This guide covers running the Aryavarta Vedic Philosophy AI Assistant on Linux systems, with special focus on **Raspberry Pi 5 (64-bit Debian)**.

---

## System Requirements

### Minimum Specifications
- **OS**: Debian 12 / Ubuntu 22.04+ / Raspberry Pi OS (64-bit)
- **RAM**: 4GB (8GB recommended for comfortable operation)
- **Storage**: 10GB free (for models and dependencies)
- **Processor**: ARM64 (Raspberry Pi 5) or x86-64
- **Python**: 3.9 or higher

### Camera & Audio
- **Camera**: USB webcam OR Raspberry Pi CSI camera
- **Microphone**: USB microphone OR 3.5mm Jack + USB audio interface
- **Speaker**: 3.5mm Jack, USB, or Bluetooth

---

## Installation Steps

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt upgrade -y

# Core build tools
sudo apt install -y \
  python3-dev \
  python3-pip \
  python3-venv \
  build-essential \
  git

# Camera support
sudo apt install -y \
  libatlas-base-dev \
  libjasper-dev \
  libharfbuzz0b \
  libwebp6 \
  libtiff5 \
  libjasper1 \
  libopenjp2-7

# Audio support (for Pygame + edge-tts)
sudo apt install -y \
  alsa-utils \
  pulseaudio \
  libportaudio2 \
  portaudio19-dev

# Additional dependencies for Raspberry Pi
sudo apt install -y \
  libopenblas0 \
  liblapack3
```

### 2. Enable Camera (Raspberry Pi Only)

If using **Raspberry Pi CSI Camera**:

```bash
# 1. Enable camera in raspi-config
sudo raspi-config
# → Interface Options → Camera → Enable

# 2. Load camera module
sudo modprobe bcm2835-v4l2

# 3. Make it persistent
echo "bcm2835-v4l2" | sudo tee -a /etc/modules
```

Test camera:

```bash
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('✓ Camera OK' if cap.isOpened() else '✗ Camera FAILED')"
```

### 3. Configure Audio Devices

#### Find Available Devices

```bash
# List recording devices
arecord -l

# List playback devices
aplay -l

# Test recording
arecord -D plughw:1,0 -f cd test.wav
aplay test.wav
```

#### Configure ALSA (for Raspberry Pi)

Create/edit `~/.asoundrc`:

```bash
cat > ~/.asoundrc << 'EOF'
pcm.!default {
    type asym
    playback.pcm "speaker"
    capture.pcm "mic"
}

pcm.speaker {
    type plug
    slave.pcm "hw:0,0"
}

pcm.mic {
    type plug
    slave.pcm "hw:1,0"
}
EOF
```

#### Configure PulseAudio (Optional)

```bash
pulseaudio --start
pactl list sources
pactl list sinks
```

### 4. Install Python Dependencies

```bash
cd /path/to/aryavarta

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools
pip install -r requirements.txt

# For Raspberry Pi, if tensorflow fails, use pre-built wheels:
pip install tensorflow-aarch64==2.14.1
```

---

## Configuration Files

### STT/language.json

Store your selected language:

```json
{
    "language": "hindi"
}
```

Supported languages: `english`, `hindi`, `tamil`, `telugu`, `kannada`, `malayalam`, `bengali`, `marathi`, `gujarati`, `punjabi`, `urdu`

### emotion_detection/camera_properties.py

Default configuration:

```python
CAMERA_INDEX = 0          # Camera device ID
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30
BRIGHTNESS = 0
CONTRAST = 0
SATURATION = 0
```

For **Raspberry Pi CSI Camera**:

```python
# Already uses YUYV format and handles CSI properly
# No changes needed if you've run: sudo modprobe bcm2835-v4l2
```

---

## Running the Application

### Quick Start

```bash
cd /path/to/aryavarta
python3 interaction/main.py
```

### Step-by-Step Interaction Flow

1. **Emotion Detection** (25 seconds max)
   - Camera captures face
   - Auto-exits when emotion is stable or timeout reaches

2. **Language Selection**
   - Listens for language choice
   - Uses **Sarvam STT** for Indian languages (requires internet)
   - Falls back to local Whisper if Sarvam unavailable

3. **Problem Description**
   - Records your problem (5 seconds)
   - Transcribes speech to text
   - Uses local Whisper model (no internet needed)

4. **Verse Retrieval**
   - Sends problem + detected emotion to Ollama
   - Retrieves relevant Bhagavad Gita/Vedas verses
   - Uses embeddings from local ChromaDB

5. **Response & Guidance**
   - Speaks verse guidance using edge-tts
   - Translates to selected language using deep-translator
   - Outputs JSON metadata to `output.json`

---

## Performance Optimization for Raspberry Pi

### Model Selection

The project uses **lightweight models** for Pi compatibility:

| Component | Model | Size | Speed |
|-----------|-------|------|-------|
| Whisper (Speech-to-Text) | `tiny` | 39MB | ~2s per 5s audio |
| LLM (Verse guidance) | `phi3:mini` | 2.2GB | ~3s per response |
| Embeddings | `nomic-embed-text` | 274MB | ~100ms per text |
| Gender/Emotion Detection | OpenCV DNN | ~50MB | ~50ms per frame |

### Reducing Memory Usage

If you hit memory limits (< 2GB free):

1. **Reduce Whisper model size**:
   ```python
   # STT/transcribe.py line 10
   self.model = WhisperModel("tiny", device="cpu", compute_type="int8")
   ```

2. **Use lighter LLM**:
   ```python
   # engine/config.py line 22
   OLLAMA_LLM_MODEL = "gemma2:2b"  # Instead of phi3:mini
   ```

3. **Disable emotion/gender detection** if camera is unreliable:
   ```python
   # interaction/main.py line 36
   # Skip run_vision() and set emotion="neutral" manually
   emotion_state = {"emotion": "neutral", "confidence": 0.0}
   ```

### Monitoring Performance

```bash
# Watch CPU/Memory during runtime
watch -n 1 'ps aux | grep python | grep -v grep'

# Monitor Ollama model loading
tail -f /var/log/ollama/ollama.log  # If installed as service
```

---

## Troubleshooting

### Audio Issues

**Problem**: "No microphone detected" or "Audio device busy"

**Solution**:
```bash
# Find available device
arecord -l

# Kill PulseAudio if it's blocking ALSA
pulseaudio -k

# Or configure PulseAudio to use specific device
pactl set-default-source alsa_input.usb-...
```

**For USB Audio Interface**:
```bash
# Install USB audio drivers
sudo apt install alsa-utils pulseaudio

# Reload sound modules
sudo alsa force-reload
```

### Camera Issues

**Problem**: "Camera failed to initialize"

**Solution**:
```bash
# Verify camera device exists
ls -la /dev/video0

# Check CSI camera (Raspberry Pi)
vcgencmd get_camera

# Try different camera index
python3 -c "
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f'✓ Camera {i} works')
        cap.release()
"
```

**For CSI Camera**:
```bash
# Enable in raspi-config
sudo raspi-config

# Load driver
sudo modprobe bcm2835-v4l2

# Verify
ls -la /dev/video0
```

### TTS (Text-to-Speech) Issues

**Problem**: "Pygame audio playback failed"

**Solution**:
```bash
# Ensure ALSA is properly configured
speaker-test -c 2 -t wav

# If using Bluetooth speaker, pair first
sudo bluetoothctl
> pair <MAC>
> connect <MAC>

# Test pygame mixer
python3 -c "
import pygame
pygame.mixer.init()
print('✓ Pygame mixer initialized')
"
```

### Model Loading Issues

**Problem**: "Cannot load tensorflow" or "Model file not found"

**Solution**:
```bash
# For Raspberry Pi ARM64
pip install tensorflow-aarch64==2.14.1 --no-cache-dir

# Verify model paths
python3 -c "
from pathlib import Path
model_dir = Path('emotion_detection/models')
print('Gender models:', list(model_dir.glob('gender*')))
"
```

### Out of Memory (OOM)

**Problem**: Application crashes with "Memory limit exceeded"

**Solution**:
```bash
# Increase swap space (temporary, until reboot)
sudo dphys-swapfile swapon

# Permanent increase:
sudo nano /etc/dphys-swapfile
# Change: CONF_SWAPSIZE=2048

# Reduce model sizes (see Optimization section above)
```

---

## Network & Internet

### Sarvam STT (Optional, requires internet)

The app automatically uses **Sarvam STT** for better Indian language detection:

```python
# Works if you have API key
export SARVAM_API_KEY="your_key_here"

# Falls back to local Whisper if:
# - No internet
# - No API key set
# - API call fails
```

### Ollama (Local, no internet required)

Ollama runs 100% locally on your Raspberry Pi. First-time setup:

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull required models
ollama pull nomic-embed-text
ollama pull phi3:mini

# Start Ollama service
ollama serve &
```

---

## Testing Individual Components

```bash
# 1. Test Camera
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(f'✓ Camera works: {frame.shape}' if ret else '✗ Camera failed')
cap.release()
"

# 2. Test Microphone
python3 -c "
import sounddevice as sd
import soundfile as sf
print('Recording 3 seconds...')
audio = sd.rec(int(3 * 44100), samplerate=44100, channels=2)
sd.wait()
sf.write('test.wav', audio, 44100)
print('✓ Microphone works')
"

# 3. Test Speaker
python3 -c "
import pygame
pygame.mixer.init()
# Play system sound or test file
pygame.mixer.music.load('test.wav')
pygame.mixer.music.play()
import time; time.sleep(5)
print('✓ Speaker works')
"

# 4. Test STT (Speech-to-Text)
python3 -c "
from STT.main_stt import process_voice
text = process_voice()
print(f'✓ STT works: {text}')
"

# 5. Test TTS (Text-to-Speech)
python3 -c "
from TTS.speaker import speak
speak('Hello, this is a test', 'english')
print('✓ TTS works')
"

# 6. Test Ollama
python3 -c "
import requests
response = requests.post(
    'http://localhost:11434/api/generate',
    json={'model': 'phi3:mini', 'prompt': 'test'}
)
print('✓ Ollama works' if response.status_code == 200 else '✗ Ollama failed')
"
```

---

## Cross-Platform Compatibility Notes

### Path Handling

All code uses **pathlib.Path** for cross-platform compatibility:

```python
from pathlib import Path

# Works on both Windows and Linux
config_path = Path("config") / "settings.json"
```

### File I/O

All file operations use UTF-8 encoding:

```python
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
```

### Process Management

Async operations are compatible with asyncio on Linux:

```python
import asyncio

# Works on Linux/Pi with proper event loop
asyncio.run(async_function())
```

---

## Performance Benchmarks (Raspberry Pi 5)

Expected timing per interaction cycle:

| Step | Time |
|------|------|
| Emotion Detection | 5-25s (auto-exits early if stable) |
| Language Selection | 3-8s |
| Problem Recording | 5s (fixed) |
| STT Transcription | 2-4s |
| Verse Retrieval | 3-5s |
| TTS Generation | 2-5s per verse |
| **Total** | **20-52s** |

---

## Advanced Configuration

### Custom Camera Settings

Edit `emotion_detection/camera_properties.py`:

```python
CAMERA_INDEX = 0          # Change if using multiple cameras
FRAME_WIDTH = 320         # Lower for faster processing
FRAME_HEIGHT = 240
FPS = 15                  # Lower reduces CPU usage
BRIGHTNESS = 10
CONTRAST = 10
SATURATION = 10
```

### Custom Audio Settings

Edit `STT/main_stt.py`:

```python
SAMPLE_RATE = 44100       # Audio sample rate
RECORD_SECONDS = 5        # Recording duration
CHANNELS = 2
MIC_INDEX = 1             # Change based on arecord -l output
```

### Custom Model Settings

Edit `engine/config.py`:

```python
OLLAMA_LLM_MODEL = "gemma2:2b"  # Lighter model
OLLAMA_EMBED_MODEL = "nomic-embed-text"
TOP_K_PER_SOURCE = 2      # Fewer verses (faster)
```

---

## Support & Resources

- **Raspberry Pi Setup**: https://www.raspberrypi.com/documentation/computers/getting-started.html
- **Audio Setup**: https://www.alsa-project.org/
- **Ollama Documentation**: https://github.com/ollama/ollama
- **OpenCV on Pi**: https://raspberrypi-guide.github.io/programming/using-opencv

---

## License & Attribution

Aryavarta - Vedic Philosophy AI Assistant
Optimized for Raspberry Pi 5 and Linux systems

---

**Last Updated**: January 2025
**Tested On**: Raspberry Pi 5 (Debian 12), Ubuntu 22.04 LTS
