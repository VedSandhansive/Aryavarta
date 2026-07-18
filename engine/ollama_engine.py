"""
ollama_engine.py — All calls to the local Ollama server live here.

Every function in this file talks to OLLAMA_HOST (default:
http://localhost:11434), which is Ollama running on your own machine.
Nothing here reaches the internet.
"""

import ollama
from .config import OLLAMA_EMBED_MODEL, OLLAMA_LLM_MODEL, OLLAMA_HOST

_client = ollama.Client(host=OLLAMA_HOST)


def embed_text(text: str) -> list[float]:
    """Turn a string into a vector using the local embedding model."""
    response = _client.embeddings(model=OLLAMA_EMBED_MODEL, prompt=text)
    return response["embedding"]


def generate_response(prompt: str) -> str:
    """Send a prompt to the local LLM and return its text response."""
    response = _client.generate(model=OLLAMA_LLM_MODEL, prompt=prompt)
    return response["response"].strip()


def _extract_model_names(list_response):
    """
    The `ollama` Python package has changed the shape of client.list()
    across versions:
      - older versions: dict-like, model name under "name"
      - newer versions (0.4+): pydantic-style objects, model name under
        the `.model` attribute (e.g. "llama3.1:8b"), accessed via
        response.models rather than response["models"]

    This handles both so the check doesn't break on a client upgrade.
    """
    models = getattr(list_response, "models", None)
    if models is None and isinstance(list_response, dict):
        models = list_response.get("models", [])
    models = models or []

    names = []
    for m in models:
        name = getattr(m, "model", None)
        if name is None and isinstance(m, dict):
            name = m.get("model") or m.get("name")
        if name:
            names.append(name)
    return names


def check_ollama_ready():
    """
    Verifies the Ollama server is running and both required models are
    pulled. Call this once at startup so failures surface early with a
    clear message instead of a confusing stack trace mid-pipeline.
    """
    try:
        models = _extract_model_names(_client.list())
    except Exception as e:
        raise RuntimeError(
            "Could not reach the local Ollama server. "
            "Is it running? Start it with: ollama serve\n"
            f"Underlying error: {e}"
        )

    missing = []
    for required in (OLLAMA_EMBED_MODEL, OLLAMA_LLM_MODEL):
        if not any(m.startswith(required) for m in models):
            missing.append(required)

    if missing:
        raise RuntimeError(
            f"Missing Ollama model(s): {missing}. Pull them with:\n"
            + "\n".join(f"  ollama pull {m}" for m in missing)
        )

    print("[ollama_engine] Ollama server reachable, required models present.")


if __name__ == "__main__":
    check_ollama_ready()
    vec = embed_text("test sentence for offline embedding")
    print(f"Embedding length: {len(vec)}")