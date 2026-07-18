from faster_whisper import WhisperModel
from TTS.language import LANG_MAP

whisper = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(filename, language):
    language = language.lower().strip()
    code = LANG_MAP.get(language, ("en",))[0]

    print("Using local Whisper transcription...")

    segments, info = whisper.transcribe(
        filename,
        language=code,
        beam_size=1,
    )

    text = " ".join(segment.text.strip() for segment in segments)
    return text