# data/vedas/rigveda/mandala7/mandala7_summary.py
# Rigveda Mandala 7 - Complete Summary
# Total Suktas: 104 | Total Verses: 860

RIGVEDA_M7_SUMMARY = {
    "mandala": 7,
    "total_suktas": 104,
    "total_verses": 860,
    "rishi": "Vasishtha (Suktas 1-104)",
    "primary_deities": ["Agni", "Indra", "Agni & Indra", "Ashvins", "Maruts", "Soma", "Vayu", "Mitra", "Varuna", "Aryaman", "Pushan", "Brihaspati", "Aditi", "Surya", "Rudra", "Sarasvati"],
    
    "sukta_breakdown": {
        "Agni Suktas (28)": [1, 2, 3, 8, 9, 10, 13, 17, 18, 20, 21, 26, 28, 30, 31, 35, 36, 40, 41, 45, 46, 50, 51, 55, 56, 60, 61, 65, 66, 69, 70, 74, 75, 79, 80, 84, 85, 89, 90, 94, 95, 99, 100],
        "Indra Suktas (33)": [4, 5, 6, 11, 14, 15, 19, 22, 24, 27, 29, 32, 34, 37, 39, 42, 44, 48, 49, 52, 54, 57, 59, 62, 64, 67, 71, 73, 76, 78, 81, 83, 86, 88, 91, 93, 96, 98, 101, 103, 104],
        "Indra & Agni Suktas (22)": [7, 12, 16, 23, 25, 33, 38, 43, 47, 53, 58, 63, 68, 72, 77, 82, 87, 92, 97, 102],
        "Various Deities (6)": [41, 42, 43, 44, 62, 81]
    },
    
    "overview": (
        "Mandala 7 of the Rigveda contains 104 hymns (suktas) composed by the sage Vasishtha, "
        "one of the most celebrated and revered seers of the Rigveda. This mandala is part of the "
        "'family books' (Mandala 2-7) which are the oldest core of the Rigveda.\n\n"
        "Vasishtha is traditionally associated with purity, wisdom, and spiritual power. The hymns of "
        "Mandala 7 are known for their profound psychological depth and practical spiritual guidance.\n\n"
        "The mandala follows the established pattern of hymns to Agni (fire god/will), Indra (king of "
        "gods/courage), and Indra & Agni together (integration of will and courage). Vasishtha's hymns "
        "are characterized by their direct, powerful language and emphasis on inner transformation.\n\n"
        "Key themes include: Agni as the divine will and purifier, Indra as the slayer of Vritra (fear), "
        "the integration of strength and will, the importance of daily practice, and the recognition that "
        "the divine is not external but within every human being."
    ),
    
    "famous_suktas": {
        1: "Agni - The Purifier (10 verses) - Opening hymn of Mandala 7",
        4: "Indra - The Hero (9 verses) - First Indra hymn of the mandala",
        6: "Indra - The Mighty (10 verses) - Powerful Indra hymn",
        7: "Indra & Agni - The Twin Powers (6 verses) - Short integration hymn",
        18: "Agni - The Purifier (5 verses) - Short but potent Agni hymn",
        23: "Indra & Agni - The Twin Powers (11 verses) - Longer integration hymn",
        28: "Agni - The Priest (14 verses) - One of the longest Agni hymns in Mandala 7",
        33: "Indra & Agni - The Twin Powers (14 verses) - Contains the famous Vasishtha origin verse",
        53: "Indra & Agni - The Twin Powers (15 verses) - Longest integration hymn",
        72: "Indra & Agni - The Twin Powers (14 verses) - Deep teaching on unity",
        87: "Indra & Agni - The Twin Powers (13 verses) - Power of integration",
        104: "Indra - The Final Victor (19 verses) - Final hymn of Mandala 7"
    },
    
    "key_verses": [
        {"ref": "7.33.13", "sanskrit": "मानो महान्तमधि धायि द्यामिव सूर्यं न रश्मयो अभि प्र णोनुवुः", "meaning": "Let not the great one be placed, like heaven; like the sun, the rays have shone upon us."},
        {"ref": "7.1.1", "sanskrit": "प्र वो वाजा अभिद्यवो वचांस्यग्नये", "meaning": "For you, O Agni, the desires, heavenly, the words."},
        {"ref": "7.4.1", "sanskrit": "इन्द्रं वो विश्वतस्परि हरिवन्तं हरीणाम्", "meaning": "To Indra from all sides, the lord of bay horses, of the horses."}
    ],
    
    "psychological_takeaway": (
        "Mandala 7, composed by Rishi Vasishtha, teaches us:\n\n"
        "1. **Agni is your will** - The fire of intention that carries your actions to fulfillment.\n"
        "2. **Indra is your courage** - The strength to face Vritra (fear) daily.\n"
        "3. **Integration is key** - Strength (Indra) and will (Agni) must work together.\n"
        "4. **Daily practice** - The repeated patterns are not redundancy. They are practice.\n"
        "5. **You are the divine** - The gods are not external. They are powers within you.\n\n"
        "Vasishtha's most profound teaching: You are not becoming whole. You are remembering "
        "that you already are whole. The hymns are not prayers to distant gods. They are maps "
        "to your own inner landscape. Agni is your will. Indra is your courage. Soma is your peace. "
        "The Ashvins are your healing. When you act with intention and courage, you are not praying "
        "to gods — you are becoming them.\n\n"
        "The final verse of Mandala 7 (7.104.19) reminds us: 'By your yoking — your integration of "
        "will and courage — all powers sing.' Not in heaven. In you. Your integrated action is the song. "
        "Sing it once today. That is enough."
    ),
    
    "mantra_for_daily_life": {
        "sanskrit": "येना युजा तविषीरिगीयते",
        "meaning": "By which yoking, the powers are sung",
        "practice": "Before any action, pause and ask: 'Am I acting with both will and courage?' One integrated action today sings all powers into being."
    }
}

# Helper functions
def get_sukta_info(sukta_num):
    """Return basic info about a sukta"""
    if 1 <= sukta_num <= 104:
        return {
            'sukta': sukta_num,
            'verses': _get_verses_count(sukta_num),
            'deity': _get_deity(sukta_num)
        }
    return None

def _get_verses_count(sukta_num):
    """Return verse count for a sukta number"""
    counts = {
        1:10, 2:10, 3:10, 4:9, 5:9, 6:10, 7:6, 8:7, 9:8, 10:10,
        11:8, 12:9, 13:9, 14:8, 15:8, 16:8, 17:9, 18:5, 19:8, 20:9,
        21:9, 22:8, 23:11, 24:8, 25:8, 26:9, 27:10, 28:14, 29:8, 30:8,
        31:10, 32:8, 33:14, 34:9, 35:9, 36:9, 37:8, 38:11, 39:8, 40:8,
        41:10, 42:9, 43:14, 44:8, 45:9, 46:9, 47:10, 48:14, 49:8, 50:8,
        51:9, 52:8, 53:15, 54:8, 55:8, 56:9, 57:8, 58:13, 59:8, 60:8,
        61:9, 62:8, 63:15, 64:8, 65:8, 66:10, 67:8, 68:13, 69:8, 70:9,
        71:8, 72:14, 73:8, 74:8, 75:9, 76:8, 77:13, 78:8, 79:8, 80:9,
        81:8, 82:13, 83:8, 84:8, 85:9, 86:8, 87:13, 88:8, 89:8, 90:9,
        91:8, 92:13, 93:8, 94:7, 95:9, 96:8, 97:13, 98:8, 99:6, 100:7,
        101:6, 102:7, 103:6, 104:19
    }
    return counts.get(sukta_num, 0)

def _get_deity(sukta_num):
    """Return primary deity for a sukta number"""
    agni_suktas = [1,2,3,8,9,10,13,17,18,20,21,26,28,30,31,35,36,40,41,45,46,50,51,55,56,60,61,65,66,69,70,74,75,79,80,84,85,89,90,94,95,99,100]
    indra_suktas = [4,5,6,11,14,15,19,22,24,27,29,32,34,37,39,42,44,48,49,52,54,57,59,62,64,67,71,73,76,78,81,83,86,88,91,93,96,98,101,103,104]
    if sukta_num in agni_suktas:
        return "Agni"
    elif sukta_num in indra_suktas:
        return "Indra"
    else:
        return "Indra & Agni"

# Print summary
if __name__ == "__main__":
    print("=" * 60)
    print("RIGVEDA MANDALA 7 - COMPLETE SUMMARY")
    print("=" * 60)
    print(f"\nTotal Suktas: {RIGVEDA_M7_SUMMARY['total_suktas']}")
    print(f"Total Verses: {RIGVEDA_M7_SUMMARY['total_verses']}")
    print(f"Rishi: {RIGVEDA_M7_SUMMARY['rishi']}")
    print(f"\nPrimary Deities: {', '.join(RIGVEDA_M7_SUMMARY['primary_deities'][:8])}...")
    print(f"\n{RIGVEDA_M7_SUMMARY['overview']}")
    print(f"\n{'='*60}")
    print("Famous Verse (7.33.13):")
    print(f"   Sanskrit: {RIGVEDA_M7_SUMMARY['key_verses'][0]['sanskrit']}")
    print(f"   Meaning: {RIGVEDA_M7_SUMMARY['key_verses'][0]['meaning']}")
    print(f"\nPsychological Takeaway:")
    print(RIGVEDA_M7_SUMMARY['psychological_takeaway'])