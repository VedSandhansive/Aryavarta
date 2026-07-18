# Aryavarta - Raspberry Pi 5 Setup Guide

## System Requirements
- Raspberry Pi 5 (64-bit Debian)
- 4GB+ RAM (8GB recommended for ML models)
- USB microphone or built-in audio
- USB camera or CSI camera ribbon

## Installation Steps

### 1. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    libopenblas-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libjasper-dev \
    libtiff5 \
    libjasper1 \
    libharfbuzz0b \
    libwebp6 \
    libtiff5 \
    libjasper1 \
    libatlas-base-dev \
    alsa-utils \
    portaudio19-dev
```

### 2. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Audio Device
Check connected audio devices:
```bash
arecord -l
```

Update `STT/main_stt.py` with correct microphone index if needed (line 109).

### 4. Test Camera
```bash
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Failed')"
```

### 5. Run the Application
```bash
cd /path/to/Aryavarta-main-lin
python3 interaction/main.py
```

## Troubleshooting

### Camera Issues
- Try: `sudo modprobe bcm2835-v4l2` (for CSI cameras)
- Check: `ls /dev/video*`

### Audio Issues
- List devices: `arecord -l`
- Test recording: `arecord -d 5 test.wav`
- Test playback: `aplay test.wav`

### Memory Issues
- Disable GUI: `sudo systemctl set-default multi-user.target`
- Check memory: `free -h`

### TensorFlow/Keras
- Uses `tensorflow-aarch64==2.14.1` for ARM64
- First run may take time loading models

## Performance Notes
- Emotion detection uses smaller Keras model (48x48 grayscale)
- Gender detection uses lightweight OpenCV DNN
- Whisper speech-to-text uses "tiny" model for speed
- Sarvam API for Indian language detection
