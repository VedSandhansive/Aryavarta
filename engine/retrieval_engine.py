"""
retrieval_engine.py — Given a user's problem + detected emotion, retrieve
the most relevant Gita verses and Vedic verses (as two SEPARATE result
sets) and have the local Ollama LLM explain why they fit.

Everything below runs through the local Ollama server only.
"""

import re
import chromadb
from .config import (
    VECTOR_DB_PATH, GITA_COLLECTION, VEDAS_COLLECTION, TOP_K_PER_SOURCE,
)
from .ollama_engine import embed_text, generate_response

_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)


INTENT_KEYWORDS = {
    "medicine": [
        "medicine", "medical", "doctor", "healing", "heal", "illness", "disease",
        "health", "herb", "remedy", "cure", "sickness", "fever", "pain", "ailment",
        "memory", "brain", "sleep", "digest", "digestion", "stress", "well-being",
    ],
    "mantra": [
        "mantra", "chant", "song", "music", "melody", "devotion", "worship", "prayer",
        "peace", "calm", "serenity", "meditation", "chanting", "sing", "quiet",
    ],
    "ritual": [
        "ritual", "yajna", "yajna", "agnihotra", "havan", "fire", "ceremony", "sacrifice",
        "offering", "procedure", "puja", "priest", "rituals", "rites",
    ],
    "hymn": [
        "hymn", "courage", "bravery", "protection", "shield", "hero", "strength",
        "warrior", "song for", "hymn for", "gods", "praise",
    ],
    "life_guidance": [
        "sad", "depressed", "hopeless", "lost", "alone", "anxious", "worry", "fear",
        "confused", "decision", "relationship", "career", "stress", "help", "future",
        "who am i", "purpose", "duty", "responsibility", "anger", "frustrated",
    ],
}

VEDA_BRANCH_KEYWORDS = {
    "rigveda": ["hymn", "courage", "bravery", "protection", "shield", "hero", "strength"],
    "atharvaveda": [
        "medicine", "healing", "health", "doctor", "herb", "remedy", "cure", "illness",
        "disease", "pain", "sickness", "fever", "memory", "sleep", "well-being",
    ],
    "samaveda": [
        "mantra", "chant", "song", "music", "prayer", "peace", "calm", "devotion",
        "worship", "meditation", "chanting",
    ],
    "yajurveda": [
        "ritual", "yajna", "agnihotra", "havan", "fire", "ceremony", "sacrifice",
        "offering", "procedure", "puja", "priest", "rites",
    ],
}


def _keyword_match(text: str, keywords: list[str]) -> bool:
    return any(word in text for word in keywords)


def _classify_request(user_text: str) -> dict:
    text = (user_text or "").lower()

    if _keyword_match(text, INTENT_KEYWORDS["medicine"]):
        return {
            "intent": "medicine",
            "source": "vedas",
            "selected_veda_branch": "atharvaveda",
        }

    if _keyword_match(text, INTENT_KEYWORDS["mantra"]):
        return {
            "intent": "mantra",
            "source": "vedas",
            "selected_veda_branch": "samaveda",
        }

    if _keyword_match(text, INTENT_KEYWORDS["ritual"]):
        return {
            "intent": "ritual",
            "source": "vedas",
            "selected_veda_branch": "yajurveda",
        }

    if _keyword_match(text, INTENT_KEYWORDS["hymn"]):
        return {
            "intent": "hymn",
            "source": "vedas",
            "selected_veda_branch": "rigveda",
        }

    if _keyword_match(text, INTENT_KEYWORDS["life_guidance"]):
        return {
            "intent": "life_guidance",
            "source": "gita",
            "selected_veda_branch": None,
        }

    # Fallbacks for common Veda topics
    if _keyword_match(text, VEDA_BRANCH_KEYWORDS["atharvaveda"]):
        return {
            "intent": "medicine",
            "source": "vedas",
            "selected_veda_branch": "atharvaveda",
        }
    if _keyword_match(text, VEDA_BRANCH_KEYWORDS["samaveda"]):
        return {
            "intent": "mantra",
            "source": "vedas",
            "selected_veda_branch": "samaveda",
        }
    if _keyword_match(text, VEDA_BRANCH_KEYWORDS["yajurveda"]):
        return {
            "intent": "ritual",
            "source": "vedas",
            "selected_veda_branch": "yajurveda",
        }
    if _keyword_match(text, VEDA_BRANCH_KEYWORDS["rigveda"]):
        return {
            "intent": "hymn",
            "source": "vedas",
            "selected_veda_branch": "rigveda",
        }

    return {
        "intent": "life_guidance",
        "source": "gita",
        "selected_veda_branch": None,
    }


def _distance_to_score(distance):
    try:
        if distance is None:
            return None
        distance = float(distance)
        if distance < 0:
            return 1.0
        return 1.0 / (1.0 + distance)
    except Exception:
        return None
_gita_col = _client.get_or_create_collection(GITA_COLLECTION)
_vedas_col = _client.get_or_create_collection(VEDAS_COLLECTION)


def _query_collection(query_text, collection, top_k):
    query_vector = embed_text(query_text)
    results = collection.query(query_embeddings=[query_vector], n_results=top_k)
    metadatas = results.get("metadatas", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []
    matches = []
    for metadata, distance in zip(metadatas, distances):
        record = dict(metadata)
        record["distance"] = distance
        record["score"] = _distance_to_score(distance)
        matches.append(record)
    return matches


def retrieve_verses(user_text: str, emotion: str, top_k: int = TOP_K_PER_SOURCE):
    """Returns (gita_matches, vedas_matches, selected_scripture, selected_veda_branch, intent)."""
    query = f"A person feeling {emotion} shares this problem: {user_text}"
    classification = _classify_request(user_text)
    selected_scripture = classification["source"]
    selected_veda_branch = classification.get("selected_veda_branch")
    intent = classification.get("intent", "life_guidance")

    if selected_scripture == "gita":
        return _query_collection(query, _gita_col, top_k), [], "gita", None, intent

    return [], _query_veda_collection(query, selected_veda_branch, top_k), "vedas", selected_veda_branch, intent


def _format_matches(matches):
    lines = []
    for m in matches:
        lines.append(
            f"- {m['collection_name']} verse {m['verse_number']}: "
            f"{m['meaning']} | Guidance: {m['example']}"
        )
    return "\n".join(lines) if lines else "(none found)"


def _build_intro(emotion: str, selected_scripture: str | None = None) -> str:
    emotion = (emotion or "").strip().lower()
    scripture_phrase = "the Vedas" if selected_scripture == "vedas" else "the Bhagavad Gita"
    if emotion in {"sad", "depressed", "hopeless", "lost", "alone"}:
        verb = "offer" if scripture_phrase == "the Vedas" else "offers"
        return (
            "I understand how overwhelming this situation feels. "
            f"You are not alone, and {scripture_phrase} {verb} guidance for moments like these."
        )
    if emotion in {"anxious", "anxiety", "worried", "fearful", "afraid", "overwhelmed"}:
        verb = "offer" if scripture_phrase == "the Vedas" else "has"
        return (
            "I can feel your worry, and this is a gentle moment to pause. "
            f"{scripture_phrase.title()} {verb} teachings that can help steady your mind and bring clarity."
        )
    if emotion in {"angry", "frustrated", "resentful", "upset"}:
        verb = "offer" if scripture_phrase == "the Vedas" else "offers"
        return (
            "I hear how strong this feels for you. "
            f"{scripture_phrase.title()} {verb} guidance on how to respond with calm strength instead of reaction."
        )
    verb = "offer" if scripture_phrase == "the Vedas" else "offers"
    return (
        "I understand how heavy this feels right now. "
        f"You are not alone, and {scripture_phrase} {verb} guidance for moments like these."
    )


def _score_text(text: str, keywords: list[str]) -> int:
    text = (text or "").lower()
    return sum(1 for kw in keywords if kw in text)


def _select_veda_branch(user_text: str) -> str:
    text = (user_text or "").lower()
    if any(word in text for word in [
        "medicine", "medical", "doctor", "healing", "heal", "illness", "disease", "health",
        "herb", "remedy", "cure", "sickness", "fever", "pain", "ailment", "potion",
    ]):
        return "atharvaveda"
    if any(word in text for word in [
        "meditation", "meditate", "mindfulness", "yoga", "chant", "song", "music", "melody",
        "devotion", "devote", "calm", "peace", "mantra", "prayer", "worship", "sacred song",
    ]):
        return "samaveda"
    if any(word in text for word in [
        "ritual", "sacrifice", "yajna", "offering", "ceremony", "priest", "fire", "havan",
        "puja", "practice", "procedure", "sacred", "rite", "yajur", "mantra for ritual",
    ]):
        return "yajurveda"
    if any(word in text for word in [
        "knowledge", "wisdom", "learn", "study", "truth", "cosmic", "creation", "nature",
        "hymn", "pray", "light", "god", "gods", "mantra", "sanskrit", "verse",
    ]):
        return "rigveda"
    return "either"


def _select_scripture(user_text: str) -> str:
    text = (user_text or "").lower()
    gita_keywords = [
        "exam", "failed", "failure", "parents", "teacher", "fear", "scared", "confused",
        "lost", "decision", "duty", "responsibility", "career", "relationship", "angry",
        "stress", "anxiety", "worry", "depressed", "sad", "alone", "future", "help",
        "choose", "path", "problem", "direction", "courage", "action", "difficult", "hurt",
    ]
    veda_keywords = [
        "medicine", "healing", "health", "ritual", "sacrifice", "worship", "prayer",
        "mantra", "chant", "song", "music", "devotion", "meditation", "yoga", "knowledge",
        "wisdom", "hymn", "cosmic", "creation", "nature", "ceremony",
    ]
    score_gita = _score_text(text, gita_keywords)
    score_veda = _score_text(text, veda_keywords)
    veda_branch = _select_veda_branch(user_text)
    if veda_branch != "either":
        score_veda += 2
    if score_veda > score_gita:
        return "vedas"
    return "gita"


def _filter_veda_matches_by_branch(matches, branch: str, top_k: int):
    filtered = []
    for m in matches:
        normalized = _normalize_veda_metadata(m)
        if normalized.get("type") == branch:
            filtered.append(m)
    if len(filtered) >= top_k:
        return filtered[:top_k]
    if branch == "yajurveda":
        # if Yajurveda branch is requested, allow either branch if strict results are low
        return filtered[:top_k]
    return filtered[:top_k]


def _query_veda_collection(query_text, branch: str, top_k: int):
    n_results = max(top_k * 5, 15)
    results = _vedas_col.query(query_embeddings=[embed_text(query_text)], n_results=n_results)
    metadatas = results.get("metadatas", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []
    matches = []
    for metadata, distance in zip(metadatas, distances):
        record = dict(metadata)
        record["distance"] = distance
        record["score"] = _distance_to_score(distance)
        matches.append(record)

    if branch == "either" or branch is None:
        return matches[:top_k]

    filtered = _filter_veda_matches_by_branch(matches, branch, top_k)
    if len(filtered) < top_k:
        return matches[:top_k]
    return filtered[:top_k]


def _normalize_gita_metadata(match):
    collection_name = match.get("collection_name", "")
    verse_number = int(match.get("verse_number", 0))
    chapter_match = re.search(r"BHAGAVAD_GITA_CH(\d+)", collection_name)
    chapter = int(chapter_match.group(1)) if chapter_match else None
    return {"chapter": chapter, "verse": verse_number, "score": match.get("score")}


def _normalize_veda_metadata(match):
    collection_name = match.get("collection_name", "")
    verse_number = int(match.get("verse_number", 0))
    file_path = match.get("file_path", "").replace("\\", "/").lower()

    if collection_name.startswith("RIGVEDA_") or "/rigveda/" in file_path:
        m = re.match(r"RIGVEDA_M(\d+)_S(\d+)", collection_name)
        if m:
            return {
                "type": "rigveda",
                "mandala": int(m.group(1)),
                "sukta": int(m.group(2)),
                "verse": verse_number,
            }
        m = re.search(r"mandala(\d+)/sukta(\d+)\.py", file_path)
        if m:
            return {
                "type": "rigveda",
                "mandala": int(m.group(1)),
                "sukta": int(m.group(2)),
                "verse": verse_number,
            }

    if collection_name.startswith("ATHARVAVEDA_") or "/atharvaveda/" in file_path:
        m = re.match(r"ATHARVAVEDA_K(\d+)_S(\d+)", collection_name)
        if m:
            return {
                "type": "atharvaveda",
                "kanda": int(m.group(1)),
                "sukta": int(m.group(2)),
                "verse": verse_number,
                "score": match.get("score"),
            }
        m = re.search(r"kanda(\d+)/sukta(\d+)\.py", file_path)
        if m:
            return {
                "type": "atharvaveda",
                "kanda": int(m.group(1)),
                "sukta": int(m.group(2)),
                "verse": verse_number,
                "score": match.get("score"),
            }

    if collection_name.startswith("KRISHNA_YAJURVEDA_") or "/krishna_yajurveda/" in file_path:
        m = re.match(r"KRISHNA_YAJURVEDA_K(\d+)_P(\d+)", collection_name)
        if m:
            return {
                "type": "yajurveda",
                "branch": "krishna",
                "kanda": int(m.group(1)),
                "prapathaka": int(m.group(2)),
                "verse": verse_number,
                "score": match.get("score"),
            }
        m = re.search(r"kanda(\d+)\.py", file_path)
        if m:
            return {
                "type": "yajurveda",
                "branch": "krishna",
                "kanda": int(m.group(1)),
                "verse": verse_number,
                "score": match.get("score"),
            }

    if collection_name.startswith("SHUKLA_YAJURVEDA_") or "/shukla_yajurveda/" in file_path:
        m = re.match(r"SHUKLA_YAJURVEDA_ADHYAYA_(\d+)", collection_name)
        if m:
            return {
                "type": "yajurveda",
                "branch": "shukla",
                "adhyaya": int(m.group(1)),
                "verse": verse_number,
                "score": match.get("score"),
            }
        m = re.search(r"adhyaya(\d+)\.py", file_path)
        if m:
            return {
                "type": "yajurveda",
                "branch": "shukla",
                "adhyaya": int(m.group(1)),
                "verse": verse_number,
                "score": match.get("score"),
            }

    if collection_name.startswith("SAMAVEDA_") or "/samaveda/" in file_path:
        parts = collection_name.split("_")
        archika = None
        section_title = None
        if len(parts) >= 2:
            archika_raw = parts[1]
            archika = archika_raw.replace("_", " ").title()
        if len(parts) == 3:
            section = parts[2]
            section_title = section.replace("_", " ").title()
        if not archika and "/samaveda/" in file_path:
            path_parts = file_path.split("/")
            for item in path_parts:
                if item in {"purvarcika_agneya", "purvarcika_aindra", "purvarcika_pavamana", "purvarcika_aranya", "uttararcika", "mahanamni_mantras"}:
                    archika = item.replace("_", " ").title()
                    break
        normalized = {
            "type": "samaveda",
            "verse": verse_number,
            "score": match.get("score"),
        }
        if archika:
            normalized["archika"] = archika
        if section_title:
            normalized["section"] = section_title
            section_order = {
                "Aindra": 1,
                "Agneya": 2,
                "Pavamana": 3,
                "Aranya": 4,
            }
            if section_title in section_order:
                normalized["chapter"] = section_order[section_title]
        elif archika:
            normalized["chapter"] = 1
        return normalized

    return {"type": "vedas", "collection_name": collection_name, "verse": verse_number, "score": match.get("score")}


def _format_short_metadata(selected_scripture: str, selected_veda_branch: str | None, gita_matches, vedas_matches) -> str:
    if selected_scripture == "gita":
        verses = [ _normalize_gita_metadata(m) for m in gita_matches ]
        verse_texts = [f"Ch {v['chapter']} V {v['verse']}" for v in verses if v['chapter'] is not None]
        if verse_texts:
            return f"Selected scripture: Bhagavad Gita. Verses: {', '.join(verse_texts)}."
        return "Selected scripture: Bhagavad Gita."

    if selected_scripture == "vedas":
        normalized = [_normalize_veda_metadata(m) for m in vedas_matches]
        entries = []
        for v in normalized:
            if v["type"] == "rigveda":
                entries.append(f"Rigveda Mandala {v['mandala']} Sukta {v['sukta']} Verse {v['verse']}")
            elif v["type"] == "atharvaveda":
                entries.append(f"Atharvaveda Kanda {v['kanda']} Sukta {v['sukta']} Verse {v['verse']}")
            elif v["type"] == "yajurveda":
                if v.get("branch") == "krishna":
                    entries.append(f"Krishna Yajurveda Kanda {v['kanda']} Prapathaka {v['prapathaka']} Verse {v['verse']}")
                elif v.get("branch") == "shukla":
                    entries.append(f"Shukla Yajurveda Adhyaya {v['adhyaya']} Verse {v['verse']}")
                else:
                    entries.append(f"Yajurveda Verse {v['verse']}")
            elif v["type"] == "samaveda":
                archika = v.get("archika", "Samaveda")
                section = v.get("section")
                if section:
                    entries.append(f"Samaveda {archika} {section} Verse {v['verse']}")
                else:
                    entries.append(f"Samaveda {archika} Verse {v['verse']}")
            else:
                entries.append(f"{v['type'].title()} Verse {v['verse']}")
        title = selected_veda_branch.replace("_", " ").title() if selected_veda_branch and selected_veda_branch != "either" else "Vedas"
        if entries:
            return f"Selected scripture: {title}. Verse(s): {', '.join(entries)}."
        return f"Selected scripture: {title}."

    return "Selected scripture could not be determined."


def _build_short_response(selected_scripture: str, selected_veda_branch: str | None, gita_matches, vedas_matches) -> str:
    if selected_scripture == "gita":
        verses = [
            f"Chapter {v['chapter']} Verse {v['verse']}"
            for v in (_normalize_gita_metadata(m) for m in gita_matches)
            if v["chapter"] is not None
        ]
        if verses:
            return (
                "Yes, I can feel that. For you, the Bhagavad Gita says "
                + "; ".join(verses) + "."
            )
        return "Yes, I can feel that. For you, the Bhagavad Gita has guidance that can help."

    if selected_scripture == "vedas":
        normalized = [_normalize_veda_metadata(m) for m in vedas_matches]
        entries = []
        for v in normalized:
            if v["type"] == "rigveda":
                entries.append(f"Rigveda Mandala {v['mandala']} Sukta {v['sukta']} Verse {v['verse']}")
            elif v["type"] == "atharvaveda":
                entries.append(f"Atharvaveda Kanda {v['kanda']} Sukta {v['sukta']} Verse {v['verse']}")
            elif v["type"] == "yajurveda":
                if v.get("branch") == "krishna":
                    entries.append(f"Krishna Yajurveda Kanda {v['kanda']} Prapathaka {v['prapathaka']} Verse {v['verse']}")
                elif v.get("branch") == "shukla":
                    entries.append(f"Shukla Yajurveda Adhyaya {v['adhyaya']} Verse {v['verse']}")
                else:
                    entries.append(f"Yajurveda Verse {v['verse']}")
            elif v["type"] == "samaveda":
                archika = v.get("archika", "Samaveda")
                section = v.get("section")
                if section:
                    entries.append(f"Samaveda {archika} {section} Verse {v['verse']}")
                else:
                    entries.append(f"Samaveda {archika} Verse {v['verse']}")
            else:
                entries.append(f"{v['type'].title()} Verse {v['verse']}")

        branch_name = selected_veda_branch.replace("_", " ").title() if selected_veda_branch else "the Vedas"
        if entries:
            return (
                "Yes, I can feel that. For you, "
                + branch_name + " says "
                + "; ".join(entries) + "."
            )
        return "Yes, I can feel that. For you, the Vedas have guidance that can help."

    return "Yes, I can feel that. I am here to help you find the right guidance."


def synthesize_response(
    user_text: str,
    emotion: str,
    selected_scripture: str,
    selected_veda_branch: str,
    gita_matches,
    vedas_matches,
) -> str:
    """Ask the local LLM to explain the retrieved verses, grounded strictly
    in what was retrieved — the prompt explicitly forbids inventing verses."""
    scripture_phrase = "Bhagavad Gita" if selected_scripture == "gita" else "Vedas"
    section_heading = (
        "=== BHAGAVAD GITA VERSES ===\n" + _format_matches(gita_matches)
        if selected_scripture == "gita"
        else "=== VEDIC VERSES ===\n" + _format_matches(vedas_matches)
    )
    branch_note = ""
    if selected_scripture == "vedas" and selected_veda_branch:
        branch_note = f"The selected Veda branch is {selected_veda_branch}.\n\n"

    prompt = f"""You are a calm, compassionate guide helping someone with a personal problem. Do not invent or reference any verse that is not listed here.

The person feels: {emotion}
They said: "{user_text}"

{branch_note}{section_heading}

Only respond with a very short message: one consoling sentence followed by a single brief line naming the selected scripture and the exact verse references. Do not write a longer explanation.
Use only the selected scripture above ({scripture_phrase}). Do not mention the other scripture.
"""

    return generate_response(prompt)


def save_pipeline_result(result: dict, path: str = "output.json") -> None:
    import json

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def build_metadata_list(result: dict) -> list[dict]:
    metadata = []
    for item in result.get("gita", []):
        metadata.append({
            "collection": "gita",
            "chapter": item["chapter"],
            "verse": item["verse"],
            "score": item.get("score") if item.get("score") is not None else None,
        })
    for item in result.get("vedas", []):
        entry = {
            "collection": "vedas",
            "type": item["type"],
            "score": item.get("score") if item.get("score") is not None else None,
        }
        entry.update({k: v for k, v in item.items() if k not in {"type", "score"}})
        metadata.append(entry)
    return metadata


def save_metadata_output(result: dict, path: str = "output.json") -> None:
    import json
    metadata = build_metadata_list(result)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def run_pipeline_metadata(user_text: str, emotion: str = "neutral") -> list[dict]:
    result = run_pipeline(user_text, emotion)
    return build_metadata_list(result)


def run_pipeline(user_text: str, emotion: str = "neutral"):
    gita_matches, vedas_matches, selected_scripture, selected_veda_branch, intent = retrieve_verses(user_text, emotion)
    response = _build_short_response(selected_scripture, selected_veda_branch, gita_matches, vedas_matches)
    return {
        "intro": _build_intro(emotion, selected_scripture),
        "response": response,
        "selected_scripture": selected_scripture,
        "selected_veda_branch": selected_veda_branch,
        "intent": intent,
        "gita": [_normalize_gita_metadata(m) for m in gita_matches],
        "vedas": [_normalize_veda_metadata(m) for m in vedas_matches],
        "emotion": emotion,
    }


def run_pipeline_with_explanation(user_text: str, emotion: str = "neutral"):
    gita_matches, vedas_matches, selected_scripture, selected_veda_branch, intent = retrieve_verses(user_text, emotion)
    response = synthesize_response(
        user_text,
        emotion,
        selected_scripture,
        selected_veda_branch,
        gita_matches,
        vedas_matches,
    )
    return {
        "intro": _build_intro(emotion, selected_scripture),
        "response": response,
        "selected_scripture": selected_scripture,
        "selected_veda_branch": selected_veda_branch,
        "intent": intent,
        "gita": [_normalize_gita_metadata(m) for m in gita_matches],
        "vedas": [_normalize_veda_metadata(m) for m in vedas_matches],
        "emotion": emotion,
    }


if __name__ == "__main__":
    # Quick CLI test:
    #   python retrieval_engine.py "I feel anxious about my exam results" anxious output.json
    import sys
    import json

    text = sys.argv[1] if len(sys.argv) > 1 else "I feel lost and don't know what to do with my life"
    emo = sys.argv[2] if len(sys.argv) > 2 else "confused"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "output.json"

    result = run_pipeline(text, emo)
    save_pipeline_result(result, output_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"Saved result to {output_file}")
