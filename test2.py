import json
from TTS.verse_speaker import speak_selected_verse

with open("sample_output.json", "r", encoding="utf-8") as f:
    result = json.load(f)

speak_selected_verse(result)