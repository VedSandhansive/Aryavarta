import os
import sys

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================
# IMPORTS
# ==========================================

import queue
import tempfile
import wave
import sounddevice as sd
import webrtcvad

from faster_whisper import WhisperModel

# CHANGE THIS IF YOUR FILE IS NAMED DIFFERENTLY
from TTS.language import LANG_MAP
# OR:
# from TTS.language_map import LANG_MAP

# ==========================================
# SETTINGS
# ==========================================

MODEL_SIZE = "small"

SAMPLE_RATE = 16000
CHANNELS = 1

BLOCK_DURATION = 30
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION / 1000)

MAX_RECORD_SECONDS = 8
SILENCE_TO_STOP = 1.0

# ==========================================
# LANGUAGE
# ==========================================

print("\nSupported Languages:\n")

for lang in sorted(LANG_MAP.keys()):
    print(lang)

language = input("\nWhich language are you comfortable speaking?\n> ").lower().strip()

if language not in LANG_MAP:
    print("Language not found.")
    exit()

STT_LANGUAGE = LANG_MAP[language][0]

# Whisper doesn't officially support Sanskrit ("sa").
# Use Hindi as a fallback for Sanskrit chanting.
if STT_LANGUAGE == "sa":
    STT_LANGUAGE = "hi"

print(f"\nListening in {language.title()}...\n")

# ==========================================
# LOAD MODEL
# ==========================================

print("Loading Faster Whisper...")

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("Model Loaded.\n")

# ==========================================
# VAD
# ==========================================

vad = webrtcvad.Vad(2)

audio_queue = queue.Queue()

# ==========================================
# CALLBACK
# ==========================================

def callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(bytes(indata))

# ==========================================
# START MIC
# ==========================================

stream = sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    dtype="int16",
    channels=1,
    callback=callback
)

stream.start()

print("Aryavarta STT Started")
print("Speak...\n")

# ==========================================
# LOOP
# ==========================================

while True:

    frames = []
    silence = 0

    # Wait for speech

    while True:

        data = audio_queue.get()

        if vad.is_speech(data, SAMPLE_RATE):
            frames.append(data)
            break

    # Record speech

    while True:

        data = audio_queue.get()

        frames.append(data)

        if vad.is_speech(data, SAMPLE_RATE):
            silence = 0
        else:
            silence += BLOCK_DURATION / 1000

        duration = len(frames) * BLOCK_DURATION / 1000

        if silence >= SILENCE_TO_STOP:
            break

        if duration >= MAX_RECORD_SECONDS:
            break

    # Save temp wav

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp:

        filename = temp.name

    wf = wave.open(filename, "wb")

    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    for frame in frames:
        wf.writeframes(frame)

    wf.close()

    # Transcribe

    segments, info = model.transcribe(

        filename,

        language=STT_LANGUAGE,

        beam_size=10,

        best_of=10,

        temperature=0,

        vad_filter=True,

        vad_parameters=dict(
            min_silence_duration_ms=400
        ),

        condition_on_previous_text=True,

        word_timestamps=True,

        initial_prompt="""
        Bhagavad Gita
        Rigveda
        Yajurveda
        Samaveda
        Atharvaveda
        Sanskrit
        Krishna
        Arjuna
        Dharma
        Karma
        Moksha
        Indian names
        """
    )

    text = ""

    for segment in segments:
        text += segment.text + " "

    text = text.strip()

    if text:
        print("=" * 60)
        print("Language :", language.title())
        print("Text     :", text)
        print("=" * 60)

    os.remove(filename)