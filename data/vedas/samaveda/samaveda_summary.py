# data/vedas/samaveda/samaveda_summary.py
# Samaveda - Complete Summary (All 1,875 verses)

SAMAVEDA_COMPLETE_SUMMARY = {
    "name": "Samaveda",
    "meaning": "Veda of Melodies / Knowledge of Chants",
    "total_verses": 1875,
    "total_suktas": "Not applicable (organized as kāṇḍas/arcikas)",
    "language": "Vedic Sanskrit",
    "period": "c. 1200-1000 BCE",
    "recension": "Kauthuma Shakha (most prominent)",
    
    "structure": {
        "purvarcika": {
            "name": "Purvarcika (First Part)",
            "total_verses": 650,
            "sections": {
                "agneya_kanda": {
                    "verses": 114,
                    "deity": "Agni",
                    "description": "Hymns to Agni, the fire god and priest of sacrifice"
                },
                "aindra_kanda": {
                    "verses": 352,
                    "deity": "Indra",
                    "description": "Hymns to Indra, the king of gods and warrior deity"
                },
                "pavamana_kanda": {
                    "verses": 119,
                    "deity": "Soma Pavamana",
                    "description": "Hymns to Soma, the purifying ritual drink"
                },
                "aranya_kanda": {
                    "verses": 55,
                    "deity": "Indra, Agni, Soma",
                    "description": "Forest hymns - mystical and contemplative"
                },
                "mahanamni_mantras": {
                    "verses": 10,
                    "deity": "Hari (Vishnu)",
                    "description": "Great Name mantras - sacred invocations"
                }
            }
        },
        "uttararcika": {
            "name": "Uttararcika (Second Part)",
            "total_verses": 1225,
            "description": "Continuous section of verses derived primarily from Rigveda Mandalas 1, 8, and 9"
        }
    },
    
    "source_breakdown": {
        "from_rigveda": 1771,
        "unique_to_samaveda": 104,
        "note": "Approximately 94.5% of Samaveda verses are from Rigveda"
    },
    
    "primary_deities": [
        "Agni (Fire - the priest and messenger)",
        "Indra (Courage and heroic will)",
        "Soma Pavamana (Purifying essence, clarity, inspiration)",
        "Prajapati (Lord of creatures)",
        "Vishnu (The preserver, invoked in Mahanamni)"
    ],
    
    "key_concepts": {
        "saman": "Melody or chant - the musical rendering of verses",
        "udgitha": "The chanting of Om as part of Samaveda recitation",
        "pavamana": "Purification - especially of Soma and consciousness",
        "stobha": "Interjectory syllables used in chanting",
        "gana": "Song-books that apply melodies to the verses"
    },
    
    "famous_verses": [
        {"ref": "Purvarcika Agneya 1", "sanskrit": "अग्ने पत्नीरिहा वह", 
         "meaning": "O Agni, bring the wives of the gods here."},
        {"ref": "Purvarcika Aindra", "sanskrit": "त्वमिन्द्र मृलयसि", 
         "meaning": "You, O Indra, are merciful."},
        {"ref": "Purvarcika Pavamana", "sanskrit": "सोमः पवते जनिता मतीनाम्", 
         "meaning": "Soma purifies, the father of thoughts."}
    ],
    
    "importance": (
        "The Samaveda is considered the foremost among the Vedas for spiritual practice. "
        "Lord Krishna states in the Bhagavad Gita (10.22): 'Among the Vedas I am Samaveda.' "
        "Its verses are not meant to be recited but chanted with specific melodies (saman). "
        "The Samaveda is the source of Indian classical music and the foundation of the "
        "Udgatr priest's role in Vedic rituals, particularly the Soma sacrifice."
    ),
    
    "psychological_takeaway": (
        "The Samaveda teaches through melody and repetition:\n\n"
        "1. **Purification through repetition** - The Pavamana hymns show that clarity comes from repeated refinement, not sudden insight. One small purification daily.\n"
        "2. **Wildness is sacred** - The Aranya (forest) hymns reveal that untamed, spontaneous parts of your mind are not enemies but sources of wisdom.\n"
        "3. **The Great Name (Hari)** - The Mahanamni mantras teach that silent awareness before action is more powerful than any spoken word. Silence is the great name.\n"
        "4. **Integration of love and wisdom** - The two bay horses of Agni and Indra represent love and wisdom working together. One decision using both.\n"
        "5. **Melody as meditation** - The entire Samaveda is structured for chanting because rhythm and tone bypass the thinking mind and speak directly to the feeling self.\n\n"
        "The ultimate teaching of the Samaveda: You are the melody, not the words. The meaning is in the vibration, not the dictionary. One conscious breath chanted as 'Om' contains the entire Veda."
    ),
    
    "mantra_for_daily_life": {
        "sanskrit": "ॐ हरिः",
        "meaning": "Om Hari - The primordial sound, the remover of obstacles",
        "practice": "Chant 'Om Hari' silently with each breath for 5 minutes daily. Not for results. For presence. The sound is the meditation."
    },
    
    "completion_message": (
        "🎉 SAMAVEDA SAMHITA - COMPLETE! 🎉\n\n"
        f"Total Verses: 1,875\n"
        f"Purvarcika: 650 verses (Agneya, Aindra, Pavamana, Aranya, Mahanamni)\n"
        f"Uttararcika: 1,225 verses\n"
        f"All files saved to: C:\\Users\\SVS\\Documents\\Aryavarta\\data\\vedas\\samaveda\\\n\n"
        "Files created:\n"
        "  - purvarcika_agneya.py (114 verses)\n"
        "  - purvarcika_aindra.py (352 verses)\n"
        "  - purvarcika_pavamana.py (119 verses)\n"
        "  - purvarcika_aranya.py (55 verses)\n"
        "  - mahanamni_mantras.py (10 verses)\n"
        "  - uttararcika.py (1,225 verses)\n"
        "  - samaveda_summary.py (this file)\n\n"
        "May the melodies of the Samaveda bring harmony to your life. 🙏"
    )
}

def print_samaveda_summary():
    """Print complete summary of Samaveda"""
    print("=" * 80)
    print("SAMAVEDA - COMPLETE SUMMARY")
    print("The Veda of Melodies")
    print("=" * 80)
    
    print(f"\n📜 BASIC INFORMATION:")
    print(f"   Name: {SAMAVEDA_COMPLETE_SUMMARY['name']}")
    print(f"   Meaning: {SAMAVEDA_COMPLETE_SUMMARY['meaning']}")
    print(f"   Total Verses: {SAMAVEDA_COMPLETE_SUMMARY['total_verses']}")
    print(f"   Recension: {SAMAVEDA_COMPLETE_SUMMARY['recension']}")
    print(f"   Period: {SAMAVEDA_COMPLETE_SUMMARY['period']}")
    
    print(f"\n📚 STRUCTURE:")
    print(f"   Purvarcika (First Part): {SAMAVEDA_COMPLETE_SUMMARY['structure']['purvarcika']['total_verses']} verses")
    for section, details in SAMAVEDA_COMPLETE_SUMMARY['structure']['purvarcika']['sections'].items():
        print(f"      ├─ {section.replace('_', ' ').title()}: {details['verses']} verses ({details['deity']})")
    print(f"   Uttararcika (Second Part): {SAMAVEDA_COMPLETE_SUMMARY['structure']['uttararcika']['total_verses']} verses")
    
    print(f"\n🔱 PRIMARY DEITIES:")
    for deity in SAMAVEDA_COMPLETE_SUMMARY['primary_deities']:
        print(f"   - {deity}")
    
    print(f"\n🧠 PSYCHOLOGICAL TAKEWAY:")
    print(SAMAVEDA_COMPLETE_SUMMARY['psychological_takeaway'][:500] + "...")
    
    print(f"\n📿 DAILY MANTRA:")
    print(f"   Sanskrit: {SAMAVEDA_COMPLETE_SUMMARY['mantra_for_daily_life']['sanskrit']}")
    print(f"   Meaning: {SAMAVEDA_COMPLETE_SUMMARY['mantra_for_daily_life']['meaning']}")
    print(f"   Practice: {SAMAVEDA_COMPLETE_SUMMARY['mantra_for_daily_life']['practice']}")
    
    print(f"\n{'='*80}")
    print(SAMAVEDA_COMPLETE_SUMMARY['completion_message'])

if __name__ == "__main__":
    print_samaveda_summary()