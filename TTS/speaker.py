import asyncio
import edge_tts
import pygame
import uuid
import os
import time
import tempfile
import platform
from pathlib import Path

from .language import LANG_MAP


async def _speak(text, voice):
    """
    Generate and play speech using edge-tts and pygame.
    Supports Windows and Linux (Raspberry Pi) platforms.
    """

    # Use system temp directory for cross-platform compatibility
    temp_dir = Path(tempfile.gettempdir())
    filename = str(temp_dir / f"audio_{uuid.uuid4().hex}.mp3")

    try:
        # Generate speech with edge-tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    except Exception as e:
        print(f"[ERROR] Failed to generate speech: {e}")
        return

    # Initialize and play audio
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

        pygame.mixer.quit()

    except Exception as e:
        print(f"[ERROR] Pygame playback failed: {e}")
        print("[INFO] Ensure ALSA/PulseAudio is configured on Raspberry Pi")

    finally:
        # Clean up temp file
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"[WARN] Could not remove temp file {filename}: {e}")


def speak(text, language="english"):
    """
    Speak text in any supported language.
    
    Supported on:
    - Windows 10/11
    - Linux (with ALSA/PulseAudio)
    - Raspberry Pi 5 (64-bit Debian)
    """

    language = language.lower().strip()

    if language not in LANG_MAP:
        language = "english"

    _, voice = LANG_MAP[language]

    try:
        asyncio.run(_speak(text, voice))
    except Exception as e:
        print(f"[ERROR] Speech synthesis failed: {e}")

