"""
config.py — Central configuration for Aryavarta's Ollama-powered verse engine.

Everything in this file runs 100% locally through Ollama.
No API keys, no cloud calls, no internet required once models are pulled.

Optimized for Raspberry Pi 5 (64-bit Debian).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Ollama models
# ---------------------------------------------------------------------------
# For Raspberry Pi, use lighter models to conserve memory:
#   ollama pull nomic-embed-text
#   ollama pull phi3:mini        (smaller LLM, ~2.2GB)
#
# Default is qwen2.5:7b. If memory is tight, try:
#   - phi3:mini (2.2B, very fast)
#   - gemma2:2b (2B, lightweight)
#   - mistral:7b (7B, balanced)
OLLAMA_EMBED_MODEL = "nomic-embed-text"
OLLAMA_LLM_MODEL = "phi3:mini"  # Changed from qwen2.5:7b for Pi compatibility

# Default local Ollama server address (started by `ollama serve`,
# or automatically by the Ollama desktop app). Never leaves your machine.
OLLAMA_HOST = "http://localhost:11434"

# ---------------------------------------------------------------------------
# Vector store (Chroma, persisted to disk — also fully local)
# ---------------------------------------------------------------------------
VECTOR_DB_PATH = str(BASE_DIR / "verse_db")
GITA_COLLECTION = "gita_verses"
VEDAS_COLLECTION = "vedas_verses"

# ---------------------------------------------------------------------------
# Data locations (matches the existing data/ folder structure)
# ---------------------------------------------------------------------------
GITA_DATA_PATH = str(BASE_DIR.parent / "data" / "gita")
VEDAS_DATA_PATH = str(BASE_DIR.parent / "data" / "vedas")

# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------
TOP_K_PER_SOURCE = 3          # how many verses to pull from Gita and from Vedas each
EMBED_BATCH_LOG_EVERY = 250   # progress log frequency during indexing
