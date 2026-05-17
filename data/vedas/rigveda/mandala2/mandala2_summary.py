# data/vedas/rigveda/mandala2/mandala2_summary.py
# Rigveda Mandala 2 - Complete Summary
# Total Suktas: 43 | Total Verses: 416

RIGVEDA_M2_SUMMARY = {
    "mandala": 2,
    "total_suktas": 43,
    "total_verses": 416,
    "rishi": "Grtsamada Shaunahotra",
    "primary_deities": ["Agni", "Indra", "Agni & Indra", "Maruts", "Ashvins", "Rudra", "Mitra", "Varuna", "Soma", "Vayu", "Pushan", "Brihaspati", "Aditi", "Prajapati"],
    
    "sukta_breakdown": {
        "Agni Suktas": [1, 2, 3, 4, 5, 6, 9, 10, 19, 32, 33, 41, 42, 43],
        "Indra Suktas": [11, 14, 15, 16, 17, 18, 20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 34, 35, 36, 38, 39],
        "Indra & Agni Suktas": [7, 8, 12, 13, 23, 24, 37, 40],
        "Marut Suktas": [39],
        "Various": [33]
    },
    
    "overview": (
        "Mandala 2 of the Rigveda contains 43 hymns (suktas) composed by the sage Grtsamada Shaunahotra. "
        "This mandala is primarily dedicated to Agni (fire god) and Indra (king of gods), with significant "
        "hymns to the Maruts (storm gods), Ashvins (divine healers), and other deities.\n\n"
        "The hymns of Mandala 2 are known for their vivid imagery and philosophical depth. "
        "Sukta 1 is a famous 16-verse hymn to Agni, establishing him as the supreme priest. "
        "Sukta 12 celebrates the twin powers of Indra and Agni. "
        "Sukta 19 is a long 18-verse hymn to Agni as the purifier.\n\n"
        "Key themes include: the sacred fire (Agni) as messenger between humans and gods, "
        "Indra's heroic deeds of slaying Vritra (the serpent of drought/obstacles), "
        "the importance of sacrifice (yajna), and the pursuit of wealth (rayi) understood as spiritual abundance."
    ),
    
    "key_suktas": {
        1: "Agni - The Supreme Priest (16 verses) - Opening hymn of Mandala 2",
        12: "Indra & Agni - The Twin Powers (15 verses)",
        19: "Agni - The Purifier (18 verses) - Longest in Mandala 2",
        33: "Agni & Soma - The Purifiers (10 verses)",
        34: "Indra - The Hero (10 verses) - Each verse ends with 'स हि वृत्राणि जिघ्नते'",
        38: "Indra - The Hero - Final hymns of Mandala 2"
    },
    
    "themes": [
        "Agni as the divine messenger and priest",
        "Indra as the Vritra-slayer (fear-conqueror)",
        "The importance of yajna (sacrifice/intentional action)",
        "Soma as divine nectar (peace/devotion)",
        "The twin powers of Indra (strength) and Agni (will)",
        "The Maruts as storms (passionate energies)",
        "The Ashvins as healers"
    ],
    
    "famous_verses": [
        {"ref": "2.1.1", "sanskrit": "त्वमग्ने यज्ञानां होता देवेषु वार्यः", "meaning": "You, O Agne, are the priest of sacrifices, desirable among gods."},
        {"ref": "2.12.1", "sanskrit": "त्वामिदा ह्यो नरः सुतं हरिभ्यां पिबद् इन्द्र", "meaning": "You indeed yesterday, O men, with the bay horses, drank the pressed Soma, O Indra."},
        {"ref": "2.34.1", "sanskrit": "श्रुतं वो ग्रामणीयवो वरूथं गोपामृजिप्यम्", "meaning": "The famous, O leaders, the shelter, the protector, the straight-flying."}
    ],
    
    "psychological_takeaway": (
        "Mandala 2 teaches us that:\n"
        "1. Agni represents your will to act with intention (sacrifice = intentional action)\n"
        "2. Indra represents your courage to face fears (Vritra = fear)\n"
        "3. Soma represents the peace that comes from devotion\n"
        "4. The Maruts remind you that your passions (storms) are not enemies but energies to channel\n"
        "5. The Ashvins remind you that healing is always available\n"
        "6. The repeated phrase 'स हि वृत्राणि जिघ्नते' (He indeed slays the Vritras) reminds you: "
        "you conquer fear not by avoiding it, but by facing it daily."
    ),
    
    "mantra_for_daily_life": (
        "स हि वृत्राणि जिघ्नते\n"
        "He indeed slays the Vritras (fears)\n\n"
        "Face one fear today. Not with force. With presence.\n"
        "That is Indra's thunderbolt. That is your courage."
    )
}

# Helper functions
def get_sukta_info(sukta_num):
    """Return basic info about a sukta"""
    if 1 <= sukta_num <= 43:
        return {
            'sukta': sukta_num,
            'verses': RIGVEDA_M2_SUMMARY['sukta_breakdown'].get(sukta_num, 'Unknown'),
            'deity': _get_deity(sukta_num)
        }
    return None

def _get_deity(sukta_num):
    """Return primary deity for a sukta number"""
    if sukta_num in [1,2,3,4,5,6,9,10,19,32,33,41,42,43]:
        return "Agni"
    elif sukta_num in [11,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31,34,35,36,38,39]:
        return "Indra"
    elif sukta_num in [7,8,12,13,23,24,37,40]:
        return "Indra & Agni"
    else:
        return "Various"

# Print summary
if __name__ == "__main__":
    print("=" * 60)
    print("RIGVEDA MANDALA 2 - COMPLETE SUMMARY")
    print("=" * 60)
    print(f"\nTotal Suktas: {RIGVEDA_M2_SUMMARY['total_suktas']}")
    print(f"Total Verses: {RIGVEDA_M2_SUMMARY['total_verses']}")
    print(f"Rishi: {RIGVEDA_M2_SUMMARY['rishi']}")
    print(f"\nPrimary Deities: {', '.join(RIGVEDA_M2_SUMMARY['primary_deities'])}")
    print(f"\n{RIGVEDA_M2_SUMMARY['overview']}")
    print(f"\n{'='*60}")
    print("Psychological Takeaway:")
    print(RIGVEDA_M2_SUMMARY['psychological_takeaway'])