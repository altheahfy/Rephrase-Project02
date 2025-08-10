#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
チェック6: 句動詞（phrasal verbs）の包括的検出テスト
turn off, put on, break down, give up, look after など
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import spacy

def analyze_phrasal_verbs():
    """句動詞のspaCy解析確認"""
    nlp = spacy.load("en_core_web_sm")
    
    test_sentences = [
        "Turn off the light.",           # turn off (分離可能)
        "She put on her coat.",          # put on (分離可能)
        "The car broke down yesterday.", # break down (分離不可能)
        "I gave up smoking.",            # give up (分離可能) 
        "Look after the children.",      # look after (分離不可能)
        "He turned the music down.",     # turn down (分離型)
        "Pick up the phone.",            # pick up (分離可能)
        "They called off the meeting.",  # call off (分離型)
    ]
    
    print("=== 句動詞のspaCy依存関係分析 ===\n")
    
    for sentence in test_sentences:
        print(f"📝 例文: '{sentence}'")
        doc = nlp(sentence)
        
        # 動詞と関連する粒子（副詞・前置詞）を探す
        for token in doc:
            if token.pos_ == 'VERB':
                verb = token.text
                particles = []
                
                # 動詞の子要素から粒子を探す
                for child in token.children:
                    if child.dep_ in ['prt', 'prep', 'advmod'] and child.pos_ in ['ADP', 'ADV']:
                        particles.append((child.text, child.dep_, child.pos_))
                
                if particles:
                    print(f"  🔍 動詞: {verb}")
                    print(f"  🔍 粒子: {particles}")
                    phrasal_verb = f"{verb} {' '.join([p[0] for p in particles])}"
                    print(f"  ✅ 句動詞候補: '{phrasal_verb}'")
        
        print(f"  📊 全tokens: {[(t.text, t.pos_, t.dep_) for t in doc]}")
        print()

def test_phrasal_verb_parsing():
    """句動詞のM2スロット検出テスト"""
    test_sentences = [
        "Turn off the light.",
        "She put on her coat.", 
        "The car broke down yesterday.",
        "I gave up smoking.",
        "Look after the children.",
        "He turned the music down.",
        "Pick up the phone.",
        "They called off the meeting.",
    ]
    
    parser = CompleteRephraseParsingEngine()
    
    print("\n=== チェック6: 句動詞M2スロット検出テスト ===\n")
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"📝 例文{i:02d}: '{sentence}'")
        
        # 解析実行
        result = parser.analyze_sentence(sentence)
        
        if result:
            m2_slots = result.get('slots', {}).get('M2', [])
            
            # 句動詞粒子確認
            phrasal_verb_found = False
            for slot in m2_slots:
                if isinstance(slot, dict) and 'value' in slot:
                    value = slot['value'].lower()
                    # 一般的な句動詞粒子をチェック
                    particles = ['off', 'on', 'up', 'down', 'out', 'in', 'away', 'back', 'over', 'after']
                    if any(particle in value for particle in particles):
                        phrasal_verb_found = True
                        break
            
            print(f"  🔍 M2スロット: {m2_slots}")
            
            if phrasal_verb_found:
                print(f"  ✅ 句動詞粒子がM2に正しく記録されています")
            else:
                print(f"  ❌ 句動詞粒子がM2に記録されていません")
        else:
            print(f"  ❌ 解析エラー")
        
        print()

if __name__ == "__main__":
    analyze_phrasal_verbs()
    test_phrasal_verb_parsing()
