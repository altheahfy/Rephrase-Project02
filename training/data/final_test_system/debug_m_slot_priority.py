#!/usr/bin/env python3
"""
M1/M2配置優先度問題のデバッグスクリプト
最も多い失敗パターン「主節:M1不一致,M2不一致」を調査
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def debug_m_placement():
    """M配置問題のデバッグ"""
    mapper = UnifiedStanzaRephraseMapper()
    
    # 失敗ケース：M1/M2不一致が多い例文を検証
    test_cases = [
        ("The message was sent yesterday.", "M1:yesterday → M2:yesterday"),
        ("The car was repaired last week.", "M1:last week → M2:last week"),
        ("The students study hard for exams.", "M2:hard, M1:for exams → M2:hard, M3:for exams"),
        ("The student writes essays carefully for better grades.", "M1:carefully, M2:for better grades → M2:carefully, M3:for better grades")
    ]
    
    print("🔍 M配置優先度デバッグ")
    print("=" * 60)
    
    for sentence, expectation in test_cases:
        print(f"\n🧪 テスト: {sentence}")
        print(f"期待: {expectation}")
        
        try:
            result = mapper.process(sentence)
            
            # M配置状況表示
            m_slots = {}
            for key, value in result.items():
                if key.startswith('M') and value:
                    m_slots[key] = value
            
            print(f"システム M配置: {m_slots}")
            
            # 詳細解析情報表示
            if hasattr(mapper, '_determine_optimal_main_adverb_slot'):
                print("🔧 M配置ロジック詳細:")
                # adverbial_modifierハンドラーを直接呼び出してデバッグ
                import stanza
                nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
                doc = nlp(sentence)
                
                # 副詞候補をチェック
                for sent in doc.sentences:
                    for word in sent.words:
                        if word.upos == 'ADV' or (word.deprel in ['advmod', 'obl', 'obl:tmod']):
                            optimal_slot = mapper._determine_optimal_main_adverb_slot(
                                word.text, 
                                word.deprel, 
                                word.upos, 
                                result
                            )
                            print(f"  {word.text} ({word.deprel}, {word.upos}) → {optimal_slot}")
                            
        except Exception as e:
            print(f"❌ エラー: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    debug_m_placement()
