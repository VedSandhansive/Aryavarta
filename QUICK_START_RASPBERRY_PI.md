# Raspberry Pi 5 - Quick Start Guide

**Expected time to setup**: 30-45 minutes (excluding model downloads: 10-15 min more)

---

## Pre-Flight Checklist

- [ ] Raspberry Pi 5 with 4GB+ RAM
- [ ] 64-bit Debian OS installed
- [ ] USB microphone (or CSI camera microphone)
- [ ] USB webcam or Raspberry Pi CSI camera
- [ ] HDMI monitor + keyboard (or SSH access)
- [ ] Stable WiFi connection
- [ ] ~10GB free disk space

---

## Installation (Copy-Paste Ready)

### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-dev python3-pip build-essential alsa-utils
```

### Step 2: Clone/Download Aryavarta
```bash
cd ~
# Clone or copy your Aryavarta project here
cd Aryavarta-main-lin
```

### Step 3: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
# This takes ~5-10 minutes
```

### Step 5: Setup Camera (if using CSI)
```bash
sudo raspi-config
# → Interface Options → Camera → Enable
# → Exit and reboot when prompted
sudo modprobe bcm2835-v4l2
```

### Step 6: Test Hardware
```bash
# Test Camera
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('✓ Camera OK' if cap.isOpened() else '✗ Camera FAILED')"

# List Audio Devices
arecord -l
# Note your USB microphone device (usually plughw:1,0)

# Test Microphone (15 seconds)
arecord -D plughw:1,0 -d 5 test.wav && aplay test.wav
```

### Step 7: Setup Ollama (Local AI Models)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama in background
ollama serve &

# Wait for "listening on..." message, then pull models:
ollama pull nomic-embed-text    # ~400MB (2-3 min)
ollama pull phi3:mini           # ~2GB (5-10 min)
```

### Step 8: Configure Language (Optional)
```bash
# Set your preferred language
# Options: english, hindi, tamil, telugu, kannada, malayalam, bengali, marathi, gujarati, punjabi, urdu
echo '{"language": "hindi"}' > STT/language.json
```

### Step 9: Run Application
```bash
python3 interaction/main.py
```

---

## Typical Interaction Flow

1. **Emotion Detection** (5-25 seconds)
   - Camera will show detection window
   - Auto-exits when emotion is stable or timeout reached
   - Press `q` to quit if needed

2. **Language Selection** (3-8 seconds)
   - Speak "English", "Hindi", "Tamil", etc.
   - Listens for ~5 seconds

3. **Problem Description** (5 seconds)
   - Speak your question/problem
   - Records for exactly 5 seconds

4. **Processing** (10-20 seconds)
   - Ollama processes your problem with AI model
   - Retrieves relevant verses

5. **Output** (5-10 seconds)
   - AI reads verse guidance in your selected language
   - Saves result to `output.json`

**Total Time: 30-60 seconds**

---

## Troubleshooting Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Camera failed" | `sudo modprobe bcm2835-v4l2` or use USB webcam |
| "Microphone not found" | Run `arecord -l`, update `STT/main_stt.py` MIC_INDEX |
| "Ollama connection error" | Restart Ollama: `pkill ollama; ollama serve &` |
| "Out of memory" | Close other apps, increase swap (see LINUX_RASPBERRY_PI_GUIDE.md) |
| "Audio playback failed" | Run `speaker-test -c 2 -t wav` to verify ALSA |

---

## Environment Variables (Optional)

```bash
# Use lighter model if low on RAM
export OLLAMA_LLM_MODEL="gemma2:2b"

# Use Sarvam API for better Indian language support (optional)
export SARVAM_API_KEY="your_api_key_here"

# Set default microphone (replace with your device from arecord -l)
export ALSA_DEVICE="plughw:1,0"
```

---

## Monitor Performance

```bash
# Watch CPU/Memory usage during run
watch -n 1 'free -h && ps aux | grep python | grep -v grep'

# Check Ollama model size
du -sh ~/.ollama/models/

# Monitor real-time logs
tail -f ~/.ollama/ollama.log
```

---

## Stop/Restart Services

```bash
# Stop Ollama
pkill ollama

# Restart Ollama (if stuck)
pkill -9 ollama
sleep 2
ollama serve &

# Exit virtual environment
deactivate
```

---

## Common Model Sizes (for storage planning)

| Component | Size | Speed on Pi 5 |
|-----------|------|--------------|
| nomic-embed-text | 400MB | ~50ms |
| phi3:mini (LLM) | 2.2GB | ~3s per response |
| gemma2:2b (lighter LLM) | 1.6GB | ~2s per response |
| Whisper (tiny) | 39MB | ~2s per 5s audio |
| edge-tts cache | ~100MB | Instant (cached) |

---

## Performance Expectations

**First Run**:
- Model download: 10-20 minutes
- Model loading: 30-60 seconds

**Subsequent Runs**:
- Cold start (fresh boot): ~15-20 seconds
- Warm start (models cached): ~5-10 seconds
- Per interaction: 30-60 seconds total

---

## Testing Each Component

```bash
# Copy-paste one by one:

# 1. Camera
python3 -c "import cv2; c=cv2.VideoCapture(0); print('✓' if c.isOpened() else '✗')"

# 2. Microphone
python3 -c "import sounddevice as sd; a=sd.rec(1000); print('✓')"

# 3. Speaker
python3 -c "import pygame; pygame.mixer.init(); print('✓')"

# 4. Edge-TTS
python3 -c "import edge_tts; print('✓')"

# 5. Ollama
curl http://localhost:11434/api/tags | grep "name" && echo "✓"

# 6. Full app test
python3 interaction/main.py --test
```

---

## SSH Remote Access (Optional)

If you're running Pi headless:

```bash
# On your laptop/PC, SSH into Pi
ssh pi@192.168.1.XXX

# Or use VNC for GUI
vncserver :1 -geometry 1920x1080 -depth 24

# Monitor from another terminal
tail -f nohup.out
```

---

## Useful Commands

```bash
# See Pi system info
cat /proc/meminfo | grep MemTotal
cat /proc/cpuinfo | grep processor | wc -l

# Check WiFi signal
iwconfig wlan0

# Clear temp files
rm -rf ~/.ollama/blobs
rm -rf ~/.cache/pip

# Find large files taking space
du -sh ~/* | sort -h

# Monitor bandwidth
iftop -i wlan0
```

---

## What's Different from Windows?

| Aspect | Windows | Raspberry Pi |
|--------|---------|--------------|
| Paths | `data\gita\ch2.py` | `data/gita/ch2.py` |
| Audio | Direct WASAPI | ALSA/PulseAudio |
| GPU | CUDA capable | CPU only |
| Model Cache | `~\AppData\...` | `~/.ollama/` |
| Models Size | Larger (int32) | Smaller (int8) |
| Temp Files | `C:\Temp` | `/tmp` |

---

## Restore Defaults

If something breaks:

```bash
# Reset to clean installation
source venv/bin/activate
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Clear Ollama cache (warning: re-downloads models)
rm -rf ~/.ollama/
ollama pull phi3:mini

# Reset emotion detection
rm emotion.json emotion_state.json

# Reset language
rm STT/language.json
```

---

## Next Steps After Installation

1. ✅ Read `LINUX_RASPBERRY_PI_GUIDE.md` for advanced configuration
2. ✅ Check `RASPBERRY_PI_CHANGES_SUMMARY.md` to understand code changes
3. ✅ Test each component (see Testing section above)
4. ✅ Adjust model selection if needed (see performance expectations)
5. ✅ Set up scheduled tasks (cron) if running 24/7

---

## Support Resources

- **Raspberry Pi Docs**: https://www.raspberrypi.com/documentation/
- **Ollama GitHub**: https://github.com/ollama/ollama
- **OpenCV on Pi**: https://docs.opencv.org/4.9.0/d6/d00/tutorial_py_table_of_contents.html
- **ALSA Sound Setup**: https://wiki.debian.org/ALSA

---

**Setup Version**: 1.0  
**Last Updated**: January 2025  
**Estimated Time to Deploy**: 45 minutes (+ 15 min model downloads)
