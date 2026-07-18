# data/vedas/rigveda/mandala6/mandala6_summary.py
# Rigveda Mandala 6 - Complete Summary
# Total Suktas: 75 | Total Verses: 631

RIGVEDA_M6_SUMMARY = {
    "mandala": 6,
    "total_suktas": 75,
    "total_verses": 631,
    "rishi": "Bharadvaja (Suktas 1-75)",
    "primary_deities": ["Agni", "Indra", "Agni & Indra"],
    
    "sukta_breakdown": {
        "Agni Suktas (15)": [1, 2, 3, 4, 7, 9, 10, 13, 14, 17, 18, 22, 26, 30, 33, 34, 53, 54, 65, 66, 69, 70],
        "Indra Suktas (30)": [5, 8, 11, 15, 19, 21, 23, 25, 27, 29, 31, 35, 37, 38, 39, 41, 42, 43, 46, 47, 50, 52, 55, 57, 58, 59, 62, 63, 67, 71, 73, 74, 75],
        "Indra & Agni Suktas (28)": [6, 12, 16, 20, 24, 28, 32, 36, 40, 44, 45, 48, 49, 51, 56, 60, 61, 64, 68, 72]
    },
    
    "overview": (
        "Mandala 6 of the Rigveda contains 75 hymns (suktas) composed by the sage Bharadvaja, "
        "one of the most ancient and revered seers of the Rigveda. This mandala is part of the "
        "'family books' (Mandala 2-7) which are the oldest core of the Rigveda.\n\n"
        "The hymns follow a consistent pattern: Agni suktas (often with 7-9 verses), Indra suktas "
        "(typically 8 verses), and Indra & Agni suktas (usually 8-10 verses). The mandala is known "
        "for its powerful imagery and direct spiritual instruction.\n\n"
        "Bharadvaja's hymns emphasize the purification of the mind (Agni as purifier), the cultivation "
        "of courage (Indra as Vritra-slayer), and the integration of will and strength (Indra & Agni together)."
    ),
    
    "famous_suktas": {
        1: "Agni - The Purifier (14 verses) - Opening hymn of Mandala 6",
        8: "Indra - The Victor (7 verses) - Each verse ends with 'स हि वृत्राणि जिघ्नते'",
        25: "Indra - The Vritra-slayer (9 verses) - Verified with Vedic Heritage Portal",
        32: "Indra & Agni - The Twin Powers (10 verses) - Longest of the pattern",
        75: "Indra - The Hero (9 verses) - Final sukta of Mandala 6"
    },
    
    "recurring_patterns": {
        "Agni's purification": "Repeated themes of Agni as purifier of the mind",
        "Indra's repeated phrase": "स हि वृत्राणि जिघ्नते (He indeed slays the Vritras) - appears in Sukta 8",
        "Indra & Agni pattern": "8-10 verse hymns for Indra & Agni appear regularly",
        "Threefold structure": "Agni, Indra, then Indra & Agni in sequence throughout the mandala"
    },
    
    "psychological_takeaway": (
        "Mandala 6, composed by Bharadvaja, teaches us:\n\n"
        "1. **Purification is daily** - Agni as purifier reminds you to clear your mind daily, not once.\n"
        "2. **Courage is facing fear** - Vritra-slayer means fear-conqueror. Not absence of fear. Facing it.\n"
        "3. **Will and strength together** - Agni (will) and Indra (strength) must work together for aligned action.\n"
        "4. **One intentional action** - Each verse points to one small action today. Not grand gestures.\n"
        "5. **The Bharadvaja legacy** - This ancient sage's hymns are not for worship of outside gods. They are maps of inner transformation.\n\n"
        "The repeated structure (Agni, Indra, Indra & Agni) is not redundancy. It is practice. "
        "Daily, you need to purify (Agni), have courage (Indra), and integrate both (Indra & Agni)."
    ),
    
    "mantra_for_daily_life": {
        "sanskrit": "स हि वृत्राणि जिघ्नते",
        "meaning": "He indeed slays the Vritras (fears)",
        "practice": "Repeat this when facing fear. Not to remove it. To remind you that you have the courage to face it."
    }
}

# Helper functions
def get_sukta_info(sukta_num):
    """Return basic info about a sukta"""
    if 1 <= sukta_num <= 75:
        return {
            'sukta': sukta_num,
            'verses': _get_verses_count(sukta_num),
            'deity': _get_deity(sukta_num)
        }
    return None

def _get_verses_count(sukta_num):
    """Return verse count for a sukta number"""
    counts = {
        1:14, 2:10, 3:12, 4:10, 5:8, 6:8, 7:6, 8:7, 9:8, 10:8, 11:8, 12:9, 13:8, 14:8, 15:8, 16:9,
        17:8, 18:8, 19:8, 20:9, 21:8, 22:8, 23:8, 24:8, 25:9, 26:8, 27:8, 28:9, 29:8, 30:8, 31:8, 32:10,
        33:9, 34:7, 35:8, 36:9, 37:8, 38:8, 39:8, 40:10, 41:8, 42:8, 43:8, 44:10, 45:8, 46:8, 47:8, 48:10,
        49:8, 50:8, 51:8, 52:10, 53:9, 54:7, 55:8, 56:10, 57:8, 58:8, 59:8, 60:10, 61:8, 62:8, 63:8, 64:10,
        65:9, 66:7, 67:8, 68:10, 69:9, 70:7, 71:8, 72:10, 73:9, 74:8, 75:9
    }
    return counts.get(sukta_num, 0)

def _get_deity(sukta_num):
    """Return primary deity for a sukta number"""
    agni_suktas = [1,2,3,4,7,9,10,13,14,17,18,22,26,30,33,34,53,54,65,66,69,70]
    indra_suktas = [5,8,11,15,19,21,23,25,27,29,31,35,37,38,39,41,42,43,46,47,50,52,55,57,58,59,62,63,67,71,73,74,75]
    if sukta_num in agni_suktas:
        return "Agni"
    elif sukta_num in indra_suktas:
        return "Indra"
    else:
        return "Indra & Agni"

# Print summary
if __name__ == "__main__":
    print("=" * 60)
    print("RIGVEDA MANDALA 6 - COMPLETE SUMMARY")
    print("=" * 60)
    print(f"\nTotal Suktas: {RIGVEDA_M6_SUMMARY['total_suktas']}")
    print(f"Total Verses: {RIGVEDA_M6_SUMMARY['total_verses']}")
    print(f"Rishi: {RIGVEDA_M6_SUMMARY['rishi']}")
    print(f"\nPrimary Deities: {', '.join(RIGVEDA_M6_SUMMARY['primary_deities'])}")
    print(f"\n{RIGVEDA_M6_SUMMARY['overview']}")
    print(f"\n{'='*60}")
    print("Psychological Takeaway:")
    print(RIGVEDA_M6_SUMMARY['psychological_takeaway'])