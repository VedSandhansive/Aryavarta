import os
import sys
import json
import tempfile

import sounddevice as sd
import soundfile as sf

from deep_translator import GoogleTranslator
from faster_whisper import WhisperModel

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )

# ==========================================================
# IMPORTS
# ==========================================================

from TTS.speaker import speak
from TTS.language import LANG_MAP
from STT.transcribe import transcribe_audio
from STT.sarvam_stt import sarvam_transcribe

# ==========================================================
# LANGUAGE DETECTOR
# ==========================================================

language_detector = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# ==========================================================
# LANGUAGE ALIASES
# ==========================================================

LANGUAGE_ALIASES = {

    "हिंदी": "hindi",
    "हिन्दी": "hindi",
    "ગુજરાતી": "gujarati",
    "বাংলা": "bengali",
    "தமிழ்": "tamil",
    "తెలుగు": "telugu",
    "मराठी": "marathi",
    "ಕನ್ನಡ": "kannada",
    "മലയാളം": "malayalam",
    "ਪੰਜਾਬੀ": "punjabi",
    "اردو": "urdu",
    "中文": "chinese simplified",
    "繁體中文": "chinese traditional",
    "日本語": "japanese",
    "한국어": "korean",
    "العربية": "arabic",
    "русский": "russian",
    "français": "french",
    "español": "spanish",
    "Deutsch": "german"

}

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LANGUAGE_FILE = os.path.join(
    BASE_DIR,
    "language.json"
)

REASON_FILE = os.path.join(
    BASE_DIR,
    "reason.json"
)

# ==========================================================
# AUDIO SETTINGS
# ==========================================================

SAMPLE_RATE = 16000

CHANNELS = 1

# Reduced from 5 to 3 seconds for faster interaction on Pi
# Can be overridden dynamically if silence is detected
RECORD_SECONDS = 3

# Early termination if silence detected for SILENCE_THRESHOLD seconds
SILENCE_THRESHOLD = 1.5
SILENCE_DB_THRESHOLD = -40  # dB threshold for silence detection

# ==========================================================
# MICROPHONE
# Change this number if you want another microphone.
# ==========================================================

MIC_INDEX = 1

# ==========================================================
# SHOW MICROPHONES
# ==========================================================

def _find_default_input_index(devices):
    for index, device in enumerate(devices):
        if device["max_input_channels"] > 0:
            return index
    return None


def list_microphones():

    print("\nAvailable Input Devices:\n")

    devices = sd.query_devices()

    for index, device in enumerate(devices):

        if device["max_input_channels"] > 0:

            print(

                f"{index} -> {device['name']}"

            )

    print()

    global MIC_INDEX

    if MIC_INDEX is None or MIC_INDEX >= len(devices) or devices[MIC_INDEX]["max_input_channels"] == 0:
        fallback = _find_default_input_index(devices)
        if fallback is not None:
            MIC_INDEX = fallback
            print(f"Falling back to microphone index: {MIC_INDEX}")
        else:
            print("No valid microphone found.")
            return

    try:

        print(

            f"Using Microphone Index: {MIC_INDEX}"

        )

        print(

            devices[MIC_INDEX]["name"]

        )

    except Exception:

        print(

            "Invalid microphone index."

        )
# ==========================================================
# LANGUAGE FILE
# ==========================================================

def save_language(language):

    code = LANG_MAP[language][0]

    data = {

        "language": language,

        "language_code": code

    }

    with open(
        LANGUAGE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_language():

    with open(
        LANGUAGE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    return data["language"]

# ==========================================================
# SAVE REASON
# ==========================================================

def save_reason(text):

    with open(
        REASON_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(

            {

                "reason": text

            },

            f,

            indent=4,

            ensure_ascii=False

        )
# ==========================================================
# SHOW LANGUAGES
# ==========================================================

def show_languages():

    print("\n================== SUPPORTED LANGUAGES ==================\n")

    for language in sorted(LANG_MAP.keys()):
        print(language.title())

    print()


# ==========================================================
# TRANSLATE READY MESSAGE
# ==========================================================

def _translate_ready_message(text, language):

    code = LANG_MAP.get(language, ("en",))[0]

    if code == "sa":
        code = "hi"

    try:

        return GoogleTranslator(

            source="en",

            target=code

        ).translate(text)

    except Exception:

        return text


# ==========================================================
# NORMALIZE TEXT
# ==========================================================

def _normalize_text(text):

    text = text.lower()

    for ch in ".,!?;:\"'()[]{}<>/\n\r\t":

        text = text.replace(ch, " ")

    return " ".join(text.split())


# ==========================================================
# RECORD AUDIO
# ==========================================================

def record_audio():
    """
    Records audio from the selected microphone.

    Features:
    - 16kHz mono recording
    - Early stop after prolonged silence
    - Correct RMS calculation
    - Debug information
    """

    global MIC_INDEX

    import numpy as np

    print("\nSpeak now...")

    chunk_duration = 0.5
    chunk_size = int(SAMPLE_RATE * chunk_duration)
    max_chunks = int(RECORD_SECONDS / chunk_duration)

    audio_chunks = []
    silence_frames = 0

    try:

        for chunk_idx in range(max_chunks):

            chunk = sd.rec(
                frames=chunk_size,
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16",
                device=MIC_INDEX
            )

            sd.wait()

            audio_chunks.append(chunk)

            # Convert to float to avoid int16 overflow
            audio_float = chunk.astype(np.float32) / 32768.0

            rms = np.sqrt(np.mean(audio_float ** 2))

            db = 20 * np.log10(max(rms, 1e-10))

            print(f"Chunk {chunk_idx+1}: RMS={rms:.5f}  dB={db:.2f}")

            if db < SILENCE_DB_THRESHOLD:
                silence_frames += 1
            else:
                silence_frames = 0

            if (
                silence_frames * chunk_duration >= SILENCE_THRESHOLD
                and chunk_idx >= 2
            ):
                print(
                    f"[INFO] Silence detected. Recording stopped after {(chunk_idx+1)*chunk_duration:.1f} seconds."
                )
                break

    except Exception as e:

        print(f"[ERROR] Recording failed: {e}")

        print("[INFO] Trying default microphone...")

        try:

            audio = sd.rec(
                frames=int(RECORD_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16"
            )

            sd.wait()

            audio_chunks = [audio]

        except Exception as e2:

            print(f"[ERROR] Fallback failed: {e2}")

            return None

    if len(audio_chunks) == 0:

        print("[ERROR] No audio captured.")

        return None

    audio = np.vstack(audio_chunks)

    peak = np.max(np.abs(audio))
    mean = np.mean(np.abs(audio))

    print("\n========== AUDIO DEBUG ==========")
    print(f"Peak amplitude : {peak}")
    print(f"Mean amplitude : {mean}")
    print(f"Duration       : {len(audio)/SAMPLE_RATE:.2f} sec")
    print("================================")

    if peak < 500:
        print("[WARNING] Audio level is extremely low.")
        print("Possible causes:")
        print("- Wrong microphone selected")
        print("- Microphone muted")
        print("- USB webcam mic not detected")

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    filename = temp.name
    temp.close()

    try:

        sf.write(
            filename,
            audio,
            SAMPLE_RATE,
            subtype="PCM_16"
        )

        print(f"[INFO] Audio saved: {filename}")

    except Exception as e:

        print(f"[ERROR] Failed to save WAV: {e}")

        return None

    return filename

# ==========================================================
# DETECT LANGUAGE WORD
# ==========================================================

def detect_language_word(filename):
    try:
        print("\nDetecting language using Sarvam STT...")
        detected = sarvam_transcribe(filename, "english")
        detected = _normalize_text(detected or "")
        if detected:
            print("\nDetected Speech (Sarvam):", detected)
            return detected
    except Exception as e:
        print("[WARN] Sarvam language detection failed:", e)

    print("\nFalling back to local Whisper language detection...")
    segments, info = language_detector.transcribe(
        filename,
        beam_size=1
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    text = _normalize_text(text)

    print("\nDetected Speech (Whisper):", text)

    return text
# ==========================================================
# ASK LANGUAGE
# ==========================================================

def ask_language():

    show_languages()

    speak(
        "Which language are you comfortable speaking?",
        "english"
    )

    print("\nWaiting for language...\n")

    while True:

        filename = record_audio()

        if filename is None:
            continue

        detected = detect_language_word(filename)

        selected = None

        # ---------------------------------------------
        # Check aliases first
        # ---------------------------------------------

        for alias, lang in LANGUAGE_ALIASES.items():

            if alias.lower() in detected:

                selected = lang

                break

        # ---------------------------------------------
        # Check actual language names
        # ---------------------------------------------

        if selected is None:

            detected_words = set(detected.split())

            for lang in LANG_MAP.keys():

                normalized = _normalize_text(lang)

                words = normalized.split()

                if all(word in detected_words for word in words):

                    selected = lang

                    break

                if normalized == detected:

                    selected = lang

                    break

        # ---------------------------------------------
        # Partial match
        # ---------------------------------------------

        if selected is None:

            for lang in LANG_MAP.keys():

                normalized = _normalize_text(lang)

                if normalized in detected:

                    selected = lang

                    break

        # ---------------------------------------------
        # Success
        # ---------------------------------------------

        if selected is not None:

            save_language(selected)

            print("\nSelected Language :", selected)

            speak(

                f"{selected} language selected.",

                selected

            )

            try:
                os.remove(filename)
            except:
                pass

            ready = _translate_ready_message(

                "Aryavarta is ready. Tell your problem.",

                selected

            )

            speak(
                ready,
                selected
            )

            return selected

        # ---------------------------------------------
        # Failed
        # ---------------------------------------------

        try:
            os.remove(filename)
        except:
            pass

        print("Language not recognized.")

        speak(

            "I could not understand. Please say your language again.",

            "english"

        )
# ==========================================================
# PROCESS USER VOICE
# ==========================================================

def process_voice():

    language = load_language()

    print("\nUsing Language:", language)

    filename = record_audio()

    if filename is None:
        return None

    print("\nTranscribing...")

    text = transcribe_audio(
        filename,
        language
    )

    try:
        os.remove(filename)
    except Exception:
        pass

    if text is None:
        return None

    text = text.strip()

    if text == "":
        print("No speech detected.")
        return None

    print("\n===================================")
    print("USER SAID")
    print("===================================")
    print(text)

    save_reason(text)

    print("\nSaved reason.json")

    return text


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("          ARYAVARTA SPEECH ENGINE")
    print("=" * 60)

    list_microphones()

    print("\nSelecting language...\n")

    language = ask_language()

    print("\nLanguage Selected:", language)

    while True:

        print("\n--------------------------------------")
        print("Tell your problem")
        print("--------------------------------------")

        text = process_voice()

        if text is None:

            speak(
                "I could not understand. Please speak again.",
                language
            )

            continue

        print("\nCaptured Successfully.")

        return text


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nStopped.")

    except Exception as e:

        print("\nError:", e)