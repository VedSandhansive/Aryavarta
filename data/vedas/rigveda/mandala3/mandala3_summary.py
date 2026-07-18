# data/vedas/rigveda/mandala3/mandala3_summary.py
# Rigveda Mandala 3 - Complete Summary
# Total Suktas: 62 | Total Verses: 384

RIGVEDA_M3_SUMMARY = {
    "mandala": 3,
    "total_suktas": 62,
    "total_verses": 384,
    "rishi": "Vishvamitra",
    "primary_deities": ["Agni", "Indra", "Agni & Indra", "Ashvins", "Maruts", "Soma", "Vayu", "Pushan", "Brihaspati", "Aditi", "Varuna", "Mitra"],
    
    "sukta_breakdown": {
    "Agni Suktas (37)": [1, 2, 4, 5, 7, 8, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 29, 30, 31, 34, 36, 37, 38, 41, 42, 43, 54, 57, 58, 61, 62],
    "Indra Suktas (14)": [3, 6, 11, 15, 24, 28, 32, 33, 40, 45, 46, 51, 55, 59],
    "Indra & Agni Suktas (11)": [9, 19, 35, 47, 48, 49, 50, 52, 53, 56, 60],
    "Ashvin Suktas (1)": [44],
    "Marut Suktas (1)": [39],
    "Total Suktas": 62
},
    
    "overview": (
        "Mandala 3 of the Rigveda contains 62 hymns (suktas) composed by the sage Vishvamitra, "
        "one of the most celebrated seers of ancient India. This mandala is primarily dedicated "
        "to Agni (fire god) and Indra (king of gods), with many hymns to Indra and Agni together.\n\n"
        "Vishvamitra is unique among the Vedic seers as he was originally a king (Kshatriya) who "
        "became a Brahmin through intense spiritual practice. His hymns reflect both warrior strength "
        "and priestly wisdom.\n\n"
        "The most famous hymn in this mandala is the Gayatri Mantra (Sukta 62, Verse 10), "
        "though it appears in Mandala 3.62.10 and is the most well-known Vedic mantra worldwide.\n\n"
        "Key themes include: Agni as the divine messenger, Indra's heroic deeds, the importance of "
        "sacrifice (yajna), and the pursuit of spiritual wealth (rayi)."
    ),
    
    "famous_suktas": {
        1: "Agni - The Purifier (12 verses) - Opening hymn of Mandala 3",
        3: "Indra - The Hero (10 verses)",
        7: "Agni - The Priest (6 verses) - Repetitive 'serve' verses",
        10: "Agni - The Priest (7 verses) - All verses identical",
        11: "Indra - The Hero (8 verses) - Each verse ends with 'अस्माकमिद्धि ते सखा'",
        12: "Agni - The All-Knowing (6 verses) - Repetitive structure",
        29: "Agni - The Purifier (6 verses) - Powerful purification hymn",
        62: "Agni - The Priest (8 verses) - Final hymn, contains Gayatri Mantra"
    },
    
    "key_themes": [
        "Agni as divine messenger and priest",
        "Indra as Vritra-slayer (fear-conqueror)",
        "The power of yajna (sacrifice/intentional action)",
        "Soma as divine nectar (peace/devotion)",
        "The twin powers of Indra (strength) and Agni (will)",
        "The Gayatri Mantra (3.62.10) - meditation on the sun",
        "Vishvamitra's unique perspective as king-turned-sage"
    ],
    
    "famous_verses": [
        {"ref": "3.1.1", "sanskrit": "अग्निं दूतं पुरो दधे हव्यवाहं उप ब्रुवे", "meaning": "I place Agni as the messenger in front; I call the carrier of offerings."},
        {"ref": "3.10.1-7", "sanskrit": "विश्वे देवा अग्निं नेमं यज्ञियं", "meaning": "All gods, this Agni, worshipful."},
        {"ref": "3.11.1-8", "sanskrit": "यच्चिद्धि त्वा जना इन्द्र जग्मुर्वृत्रतूर्ये", "meaning": "Whatever peoples have come to you, O Indra, in Vritra-overcoming."},
        {"ref": "3.62.10", "sanskrit": "तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि", "meaning": "We meditate on the desirable light of the divine Savitar."}
    ],
    
    "gayatri_mantra": {
        "verse": "3.62.10",
        "sanskrit": "तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि | धियो यो नः प्रचोदयात् ||",
        "transliteration": "Tat savitur varenyam bhargo devasya dhimahi | dhiyo yo nah prachodayat ||",
        "meaning": "We meditate on the desirable light of the divine Savitar (the sun/awakened consciousness). May he stimulate our intellects.",
        "psychological_meaning": "This is not a prayer to an external sun. It is an affirmation: 'I meditate on my own inner light, the awareness that awakens me. May that awareness guide my thoughts toward truth.'"
    },
    
    "psychological_takeaway": (
        "Mandala 3, composed by Vishvamitra (the king who became a sage), teaches us:\n\n"
        "1. **Transformation is possible** - A king became a seer. Your past does not define your future.\n"
        "2. **Agni is your will** - The fire of intention that carries your actions.\n"
        "3. **Indra is your courage** - The strength to face Vritra (fear).\n"
        "4. **The Gayatri Mantra** - The sun (awareness) is within you. Meditate on it.\n"
        "5. **Sacrifice (yajna)** is not about offerings to gods outside. It is about intentional action offered to your highest self.\n\n"
        "Vishvamitra's journey from warrior to sage mirrors your own journey from outer achievement to inner peace."
    ),
    
    "mantra_for_daily_life": {
        "sanskrit": "तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि | धियो यो नः प्रचोदयात् ||",
        "meaning": "I meditate on my own inner light. May it guide my thoughts.",
        "practice": "Repeat this once slowly before starting any important task. It aligns your awareness with your intention."
    }
}

# Helper functions
def get_sukta_info(sukta_num):
    """Return basic info about a sukta"""
    if 1 <= sukta_num <= 62:
        return {
            'sukta': sukta_num,
            'verses': _get_verses_count(sukta_num),
            'deity': _get_deity(sukta_num)
        }
    return None

def _get_verses_count(sukta_num):
    """Return verse count for a sukta number"""
    counts = {
        1:12, 2:10, 3:10, 4:10, 5:12, 6:10, 7:6, 8:8,
        9:8, 10:7, 11:8, 12:6, 13:6, 14:4, 15:4, 16:4,
        17:6, 18:4, 19:6, 20:4, 21:6, 22:4, 23:6, 24:4,
        25:6, 26:4, 27:6, 28:4, 29:6, 30:4, 31:6, 32:4,
        33:6, 34:6, 35:6, 36:4, 37:6, 38:6, 39:6, 40:6,
        41:6, 42:6, 43:6, 44:6, 45:6, 46:6, 47:8, 48:8,
        49:6, 50:6, 51:8, 52:8, 53:6, 54:6, 55:8, 56:8,
        57:6, 58:6, 59:8, 60:8, 61:6, 62:8
    }
    return counts.get(sukta_num, 0)

def _get_deity(sukta_num):
    """Return primary deity for a sukta number"""
    if sukta_num in [1,2,4,5,7,8,10,12,13,14,16,17,18,20,21,22,23,25,26,27,29,30,31,34,36,37,38,39,41,42,43,44,54,57,58,61,62]:
        return "Agni"
    elif sukta_num in [3,6,11,15,24,28,32,33,40,45,46,51,55,59]:
        return "Indra"
    elif sukta_num in [9,19,35,47,48,49,50,52,53,56,60]:
        return "Indra & Agni"
    else:
        return "Various"

# Print summary
if __name__ == "__main__":
    print("=" * 60)
    print("RIGVEDA MANDALA 3 - COMPLETE SUMMARY")
    print("=" * 60)
    print(f"\nTotal Suktas: {RIGVEDA_M3_SUMMARY['total_suktas']}")
    print(f"Total Verses: {RIGVEDA_M3_SUMMARY['total_verses']}")
    print(f"Rishi: {RIGVEDA_M3_SUMMARY['rishi']}")
    print(f"\nPrimary Deities: {', '.join(RIGVEDA_M3_SUMMARY['primary_deities'][:10])}...")
    print(f"\n{RIGVEDA_M3_SUMMARY['overview']}")
    print(f"\n{'='*60}")
    print("Gayatri Mantra (3.62.10):")
    print(f"   Sanskrit: {RIGVEDA_M3_SUMMARY['gayatri_mantra']['sanskrit']}")
    print(f"   Meaning: {RIGVEDA_M3_SUMMARY['gayatri_mantra']['meaning']}")
    print(f"\nPsychological Takeaway:")
    print(RIGVEDA_M3_SUMMARY['psychological_takeaway'])