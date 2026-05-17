# data/vedas/rigveda/mandala4/mandala4_summary.py
# Rigveda Mandala 4 - Complete Summary
# Total Suktas: 58 | Total Verses: 582

RIGVEDA_M4_SUMMARY = {
    "mandala": 4,
    "total_suktas": 58,
    "total_verses": 582,
    "rishi": "Vamadeva Gautama (Suktas 1-58)",
    "primary_deities": ["Agni", "Indra", "Agni & Indra", "Ashvins", "Maruts", "Soma", "Vayu", "Mitra", "Varuna", "Aryaman", "Pushan", "Brihaspati", "Aditi", "Surya", "Rudra"],
    
    "sukta_breakdown": {
        "Agni Suktas (23)": [1, 2, 3, 8, 10, 11, 12, 13, 14, 18, 19, 20, 22, 23, 24, 27, 28, 31, 32, 35, 36, 39, 40, 43, 44, 47, 48, 51, 52, 55, 56],
        "Indra Suktas (13)": [4, 5, 6, 7, 15, 17, 21, 25, 26, 29, 33, 37, 41, 45, 49, 53, 57],
        "Indra & Agni Suktas (12)": [9, 16, 30, 34, 38, 42, 46, 50, 54, 58],
        "Total": 58
    },
    
    "overview": (
        "Mandala 4 of the Rigveda contains 58 hymns (suktas) composed by the sage Vamadeva Gautama. "
        "This mandala is notable for its beautiful hymns to Agni (the fire god) and Indra (the king of gods), "
        "with a significant number of hymns addressed to Indra and Agni together.\n\n"
        "Vamadeva is one of the most celebrated seers of the Rigveda, and his hymns are known for their "
        "spiritual depth and poetic beauty. Mandala 4 continues the tradition of the earlier mandalas "
        "with its focus on sacrifice (yajna), the Soma ritual, and the praise of deities.\n\n"
        "Key themes include: Agni as the divine messenger and priest, Indra's heroic deeds as Vritra-slayer, "
        "the importance of yajna (sacrifice/intentional action), and the twin powers of Indra (strength) "
        "and Agni (will). The repeated phrase 'स हि वृत्राणि जिघ्नते' (He indeed slays the Vritras) "
        "appears throughout many Indra hymns."
    ),
    
    "key_suktas": {
        1: "Agni - The Purifier (13 verses) - Opening hymn of Mandala 4",
        4: "Indra - The Hero (8 verses) - First Indra hymn of the mandala",
        6: "Indra - The Victor (11 verses) - Each verse ends with 'स हि वृत्राणि जिघ्नते'",
        7: "Indra - The Generous (12 verses) - Varied structure",
        8: "Agni - The Purifier (12 verses) - Contains repetitive invocations",
        13: "Agni - The All-Knowing (13 verses) - Longest Agni hymn in this mandala",
        17: "Indra - The Victor (11 verses) - Second set of 'He indeed slays the Vritras'",
        31: "Agni - The Purifier (12 verses) - Later Agni hymn",
        58: "Indra & Agni - The Twin Powers (9 verses) - Final sukta of Mandala 4"
    },
    
    "recurring_patterns": {
        "Indra's repeated phrase": "स हि वृत्राणि जिघ्नते (He indeed slays the Vritras) - appears in Suktas 6, 17",
        "Agni's repetitive invocations": "प्राग्नये वाचमीरय (Raise your voice for Agni) - appears in Suktas 8, 19, etc.",
        "Twin deity hymns": "Indra & Agni together in Suktas 9, 16, 30, 34, 38, 42, 46, 50, 54, 58"
    },
    
    "famous_verses": [
        {"ref": "4.1.1", "sanskrit": "त्वमग्ने प्रथमो अङ्गिरा ऋषिर्देवो देवानामभवः शिवः सखा", "meaning": "Thou, Agni, wast the earliest Angiras, a Seer, a God, a gracious Friend of other Gods."},
        {"ref": "4.4.1", "sanskrit": "इन्द्रं वो विश्वतस्परि हरिवन्तं हरीणाम्", "meaning": "To Indra from all sides, the lord of bay horses, of the horses."},
        {"ref": "4.6.3", "sanskrit": "स हि शूरः स हि क्षयः स हि ददे विश्वे वसु | स हि वृत्राणि जिघ्नते ||", "meaning": "He indeed is hero, he indeed is abode, he indeed gives all goods; he indeed slays the Vritras."},
        {"ref": "4.8.1", "sanskrit": "प्राग्नये वाचमीरय यज्ञाय वाचमीरय | प्र सोमाय वाचमीरय ||", "meaning": "Raise your voice for Agni, raise your voice for the sacrifice, raise your voice for Soma."}
    ],
    
    "psychological_takeaway": (
        "Mandala 4, composed by Vamadeva Gautama, teaches us:\n\n"
        "1. **Agni is your will** - The fire of intention that carries your actions to fulfillment.\n"
        "2. **Indra is your courage** - The strength to face Vritra (fear) daily.\n"
        "3. **The twin powers** - Strength (Indra) and will (Agni) must work together for aligned action.\n"
        "4. **Repetition as practice** - The repeated phrases are not errors but mantras for daily reinforcement.\n"
        "5. **Yajna (sacrifice) is intentional action** - Not offerings to gods outside, but actions offered to your highest self.\n\n"
        "Vamadeva's hymns remind us that the divine is not separate from us. Agni is within as will. "
        "Indra is within as courage. The Soma is within as peace. When you act with will and courage, "
        "you are not praying to gods — you are becoming them."
    ),
    
    "mantra_for_daily_life": {
        "sanskrit": "प्राग्नये वाचमीरय यज्ञाय वाचमीरय | प्र सोमाय वाचमीरय ||",
        "meaning": "Raise your voice for Agni (will), raise your voice for the sacrifice (action), raise your voice for Soma (peace).",
        "practice": "Repeat this before any important task. It aligns your intention with your action."
    }
}

# Helper functions
def get_sukta_info(sukta_num):
    """Return basic info about a sukta"""
    if 1 <= sukta_num <= 58:
        return {
            'sukta': sukta_num,
            'verses': _get_verses_count(sukta_num),
            'deity': _get_deity(sukta_num)
        }
    return None

def _get_verses_count(sukta_num):
    """Return verse count for a sukta number"""
    counts = {
        1:13, 2:9, 3:9, 4:8, 5:11, 6:11, 7:12, 8:12, 9:6, 10:7,
        11:9, 12:9, 13:13, 14:13, 15:12, 16:9, 17:11, 18:8, 19:9, 20:9,
        21:8, 22:7, 23:10, 24:10, 25:9, 26:9, 27:10, 28:10, 29:10, 30:10,
        31:12, 32:11, 33:10, 34:9, 35:11, 36:11, 37:12, 38:10, 39:11, 40:11,
        41:10, 42:9, 43:11, 44:11, 45:10, 46:8, 47:10, 48:10, 49:10, 50:9,
        51:10, 52:10, 53:10, 54:9, 55:10, 56:10, 57:10, 58:9
    }
    return counts.get(sukta_num, 0)

def _get_deity(sukta_num):
    """Return primary deity for a sukta number"""
    if sukta_num in [1,2,3,8,10,11,12,13,14,18,19,20,22,23,24,27,28,31,32,35,36,39,40,43,44,47,48,51,52,55,56]:
        return "Agni"
    elif sukta_num in [4,5,6,7,15,17,21,25,26,29,33,37,41,45,49,53,57]:
        return "Indra"
    elif sukta_num in [9,16,30,34,38,42,46,50,54,58]:
        return "Indra & Agni"
    else:
        return "Various"

# Print summary
if __name__ == "__main__":
    print("=" * 60)
    print("RIGVEDA MANDALA 4 - COMPLETE SUMMARY")
    print("=" * 60)
    print(f"\nTotal Suktas: {RIGVEDA_M4_SUMMARY['total_suktas']}")
    print(f"Total Verses: {RIGVEDA_M4_SUMMARY['total_verses']}")
    print(f"Rishi: {RIGVEDA_M4_SUMMARY['rishi']}")
    print(f"\nPrimary Deities: {', '.join(RIGVEDA_M4_SUMMARY['primary_deities'][:8])}...")
    print(f"\n{RIGVEDA_M4_SUMMARY['overview']}")
    print(f"\n{'='*60}")
    print("Recurring Pattern:")
    print(RIGVEDA_M4_SUMMARY['recurring_patterns']['Indra\'s repeated phrase'])
    print(f"\nPsychological Takeaway:")
    print(RIGVEDA_M4_SUMMARY['psychological_takeaway'])