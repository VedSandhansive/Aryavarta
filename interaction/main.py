import json
import os
import sys
from pathlib import Path
from threading import Thread, Event
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==================== LAZY IMPORTS ====================
# Only import what we need when we need it
# This speeds up startup time significantly

def lazy_import():
    """Import heavy modules lazily to speed up startup"""
    global run_vision, ask_language, process_voice
    global ask_user_based_on_emotion, run_pipeline, save_metadata_output, speak_selected_verse

    from emotion_detection.main_vision import main as run_vision
    from STT.main_stt import ask_language, process_voice
    from TTS.emotion_prompt import ask_user_based_on_emotion
    from engine.retrieval_engine import run_pipeline, save_metadata_output
    from TTS.verse_speaker import speak_selected_verse

OUTPUT_FILE = PROJECT_ROOT / "output.json"
EMOTION_FILES = [PROJECT_ROOT / "emotion.json", PROJECT_ROOT / "emotion_state.json"]


def load_emotion_state():
    """Load previously detected emotion from file"""
    for path in EMOTION_FILES:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue

    return {"emotion": "neutral", "confidence": 0.0, "gender": "Unknown"}


def run_step_with_timeout(step_name, func, timeout=None, *args, **kwargs):

    """
    Run a step with optional timeout for Raspberry Pi
    """
    print(f"\n[{step_name}]", flush=True)
    
    if timeout is None:
        return func(*args, **kwargs)
    
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    
    thread = Thread(target=target, daemon=False)
    thread.start()
    thread.join(timeout=timeout)
    
    if thread.is_alive():
        print(f"[⏱️ TIMEOUT] {step_name} exceeded {timeout}s - using default")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]


def main(skip_vision=False, skip_tts=False, fast_mode=False):
    """
    Main interaction loop with optimization options
    
    Parameters:
    -----------
    skip_vision : bool - Skip emotion detection (use previous or neutral)
    skip_tts : bool - Skip speaking verse (only output text)
    fast_mode : bool - Aggressive optimization (fewer verses, faster models)
    """
    
    # Import only when main() is called
    lazy_import()
    
    start_time = time.time()
    
    # ==================== STEP 1: EMOTION DETECTION ====================
    emotion = "neutral"
    gender = "Unknown"
    
    if not skip_vision:
        print("\n" + "="*60)
        print("Step 1/6: Detecting emotion from camera...")
        print("="*60)
        
        try:
            # Run with 15s timeout on Raspberry Pi for faster operation
            run_vision(auto_exit=True, max_seconds=15)
            emotion_state = load_emotion_state()
            emotion = emotion_state.get("emotion", "neutral")
            gender = emotion_state.get("gender", "Unknown")
            print(f"✓ Emotion: {emotion} | Gender: {gender}")
        except Exception as e:
            print(f"⚠️  Emotion detection failed: {e}")
            print(f"   Using default: neutral")
    else:
        emotion_state = load_emotion_state()
        emotion = emotion_state.get("emotion", "neutral")
        print(f"✓ Using cached emotion: {emotion}")
    
    step1_time = time.time() - start_time
    print(f"   Time: {step1_time:.1f}s")
    
    # ==================== STEP 2: LANGUAGE SELECTION ====================
    print("\n" + "="*60)
    print("Step 2/6: Selecting language...")
    print("="*60)
    
    step2_start = time.time()
    selected_language = ask_language()
    step2_time = time.time() - step2_start
    print(f"✓ Language: {selected_language}")
    print(f"   Time: {step2_time:.1f}s")
    
    # ==================== STEP 3: EMOTION-BASED PROMPT ====================
    print("\n" + "="*60)
    print("Step 3/6: Asking emotion-based question...")
    print("="*60)
    
    step3_start = time.time()
    try:
        user_emotion = ask_user_based_on_emotion(selected_language)
        if user_emotion:
            emotion = user_emotion
    except Exception as e:
        print(f"⚠️  Emotion prompt failed: {e}")
    step3_time = time.time() - step3_start
    print(f"   Time: {step3_time:.1f}s")
    
    # ==================== STEP 4: PROBLEM TRANSCRIPTION ====================
    print("\n" + "="*60)
    print("Step 4/6: Recording your problem...")
    print("="*60)
    
    step4_start = time.time()
    problem_text = None
    retry_count = 0
    max_retries = 2
    
    while problem_text is None and retry_count < max_retries:
        try:
            problem_text = process_voice()
            if problem_text is None:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"⚠️  No speech captured. Retrying ({retry_count}/{max_retries})...")
        except Exception as e:
            print(f"⚠️  Recording failed: {e}")
            retry_count += 1
    
    if problem_text is None:
        problem_text = "I need guidance and help"
        print(f"⚠️  Using default problem: '{problem_text}'")
    
    step4_time = time.time() - step4_start
    print(f"✓ Problem: {problem_text[:50]}...")
    print(f"   Time: {step4_time:.1f}s")
    
    # ==================== STEP 5: VERSE RETRIEVAL ====================
    print("\n" + "="*60)
    print("Step 5/6: Retrieving relevant verses...")
    print("="*60)
    
    step5_start = time.time()
    try:
        result = run_pipeline(problem_text, emotion)
        save_metadata_output(result, str(OUTPUT_FILE))
        print(f"✓ Found verses for: {result.get('selected_scripture', 'unknown')}")
    except Exception as e:
        print(f"⚠️  Verse retrieval failed: {e}")
        result = {
            "problem": problem_text,
            "emotion": emotion,
            "selected_scripture": "gita",
            "gita": [{"chapter": 2, "verse": 47}],
            "vedas": [],
            "intro": "Bhagavad Gita offers guidance.",
            "response": ""
        }
    step5_time = time.time() - step5_start
    print(f"   Time: {step5_time:.1f}s")
    
    # ==================== STEP 6: VERSE SPEAKING ====================
    if not skip_tts:
        print("\n" + "="*60)
        print("Step 6/6: Speaking verse guidance...")
        print("="*60)
        
        step6_start = time.time()
        try:
            speak_selected_verse(result)
        except Exception as e:
            print(f"⚠️  TTS failed: {e}")
        step6_time = time.time() - step6_start
        print(f"   Time: {step6_time:.1f}s")
    else:
        step6_time = 0
        print("\n[Skipping TTS]")
    
    # ==================== SUMMARY ====================
    total_time = time.time() - start_time
    
    print("\n" + "="*60)
    print("✅ INTERACTION COMPLETE")
    print("="*60)
    print(f"Step 1 (Emotion Detection):     {step1_time:6.1f}s")
    print(f"Step 2 (Language Selection):    {step2_time:6.1f}s")
    print(f"Step 3 (Emotion Prompt):        {step3_time:6.1f}s")
    print(f"Step 4 (Problem Recording):     {step4_time:6.1f}s")
    print(f"Step 5 (Verse Retrieval):       {step5_time:6.1f}s")
    print(f"Step 6 (TTS/Speaking):          {step6_time:6.1f}s")
    print("-" * 60)
    print(f"TOTAL TIME:                    {total_time:6.1f}s")
    print("="*60)
    
    
    print(f"\n✓ Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Aryavarta Vedic AI Assistant")
    parser.add_argument("--skip-vision", action="store_true", help="Skip emotion detection")
    parser.add_argument("--skip-tts", action="store_true", help="Skip text-to-speech")
    parser.add_argument("--fast", action="store_true", help="Aggressive optimization mode")
    
    args = parser.parse_args()
    
    main(
        skip_vision=args.skip_vision,
        skip_tts=args.skip_tts,
        fast_mode=args.fast
    )

