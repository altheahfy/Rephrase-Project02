#!/usr/bin/env python3
"""
smoothly副詞の検出問題の詳細分析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def detailed_adverb_analysis():
    sentence = "The car that was quickly repaired yesterday runs smoothly."
    mapper = UnifiedStanzaRephraseMapper()
    
    print(f"ANALYZING: {sentence}")
    print("=" * 70)
    
    # 内部的にStanza文書を分析
    stanza_doc = mapper._get_stanza_analysis(sentence)
    
    print("STANZA WORD ANALYSIS:")
    for word in stanza_doc.sentences[0].words:
        print(f"  ID={word.id:2d} TEXT='{word.text:12s}' POS={word.upos:6s} DEP={word.deprel:15s} HEAD={word.head}")
    
    print("\nADVERB DETECTION ANALYSIS:")
    time_keywords = [
        'today', 'yesterday', 'tomorrow', 'now', 'then', 'recently', 'soon',
        'early', 'late', 'before', 'after', 'during', 'while', 'until',
        'morning', 'afternoon', 'evening', 'night', 'day', 'week', 'month', 'year',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    for word in stanza_doc.sentences[0].words:
        is_deprel_match = word.deprel in ['advmod', 'obl', 'obl:tmod', 'obl:npmod', 'obl:agent', 'nmod:tmod']
        is_pos_match = word.upos == 'ADV'
        is_time_keyword = word.text.lower() in time_keywords
        
        is_adverb = is_deprel_match or is_pos_match or is_time_keyword
        
        print(f"  {word.text}:")
        print(f"    deprel_match: {is_deprel_match} ({word.deprel})")
        print(f"    pos_match: {is_pos_match} ({word.upos})")
        print(f"    time_keyword: {is_time_keyword}")
        print(f"    -> IS_ADVERB: {is_adverb}")
        
        if word.text == "smoothly":
            print("    *** SMOOTHLY TARGET WORD ***")

if __name__ == "__main__":
    detailed_adverb_analysis()
