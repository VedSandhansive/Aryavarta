"""
data/build_index.py — Run this ONCE (and again any time verse files change)
to embed every verse with Ollama and store the vectors in a local Chroma DB.

    python data/build_index.py

This is the slow, one-time step: ~700 Gita verses + ~16,800 Vedic verses
means ~17,500 embedding calls to your local Ollama server. On a normal
laptop CPU that can take a while (roughly 1-3 hours depending on hardware),
so this script is RESUMABLE — if you stop it (Ctrl+C, crash, laptop sleep)
and rerun, it skips verses that are already indexed instead of starting over.

Everything here runs locally through Ollama — no internet needed.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from engine.config import (
    VECTOR_DB_PATH, GITA_COLLECTION, VEDAS_COLLECTION,
    GITA_DATA_PATH, VEDAS_DATA_PATH, EMBED_BATCH_LOG_EVERY,
)
from data.loaders import load_gita_records, load_vedas_records
from engine.ollama_engine import embed_text, check_ollama_ready


def index_records(records, collection, label):
    existing_ids = set(collection.get(include=[])["ids"])
    to_index = [r for r in records if r["id"] not in existing_ids]

    print(f"[{label}] {len(records)} total, {len(existing_ids)} already indexed, "
          f"{len(to_index)} remaining.")

    start = time.time()
    for i, r in enumerate(to_index, 1):
        # Embed meaning + example (not raw Sanskrit) — this is the text
        # that best captures the emotional/thematic content for retrieval.
        embed_source = f"{r['meaning']} {r['example']}".strip()
        vector = embed_text(embed_source)

        collection.add(
            ids=[r["id"]],
            embeddings=[vector],
            documents=[embed_source],
            metadatas=[{
                "source": r["source"],
                "collection_name": r["collection_name"],
                "verse_number": r["verse_number"],
                "sanskrit": r["sanskrit"],
                "meaning": r["meaning"],
                "example": r["example"],
                "file_path": r["file_path"],
            }],
        )

        if i % EMBED_BATCH_LOG_EVERY == 0 or i == len(to_index):
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(to_index) - i) / rate if rate > 0 else float("inf")
            print(f"  [{label}] {i}/{len(to_index)} embedded "
                  f"({rate:.1f}/sec, ~{remaining/60:.1f} min remaining)")

    print(f"[{label}] Done. Collection now has {collection.count()} verses.")


def main():
    check_ollama_ready()

    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    gita_col = client.get_or_create_collection(GITA_COLLECTION)
    vedas_col = client.get_or_create_collection(VEDAS_COLLECTION)

    print("Loading verse files from disk...")
    gita_records = load_gita_records(GITA_DATA_PATH)
    vedas_records = load_vedas_records(VEDAS_DATA_PATH)

    index_records(gita_records, gita_col, "gita")
    index_records(vedas_records, vedas_col, "vedas")

    print("\nIndex build complete. Vector DB saved to:", VECTOR_DB_PATH)


if __name__ == "__main__":
    main()
