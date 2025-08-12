#!/usr/bin/env python3
"""
シンプル関係節処理 - Rephrase原則準拠
複雑な統一処理を避けて、直接的に期待する結果を生成
"""

import stanza

class SimpleRelativeClauseEngine:
    """シンプルな関係節処理エンジン"""
    
    def __init__(self):
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ シンプル関係節エンジン準備完了")
    
    def process(self, text: str) -> dict:
        """シンプルな関係節処理"""
        print(f"🔍 処理: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 依存構造分析
        words_info = {}
        for word in sent.words:
            words_info[word.id] = {
                'text': word.text,
                'pos': word.pos,
                'deprel': word.deprel,
                'head': word.head
            }
        
        # ROOT語特定
        root_word = next((w for w in sent.words if w.head == 0), None)
        
        # 関係節検出
        rel_verb = next((w for w in sent.words if w.deprel == 'acl:relcl'), None)
        
        if rel_verb and root_word.pos == 'NOUN':
            return self._process_relative_clause(sent, root_word, rel_verb)
        else:
            return {"error": "関係節未検出"}
    
    def _process_relative_clause(self, sent, root_noun, rel_verb):
        """関係節の直接処理"""
        result = {}
        
        # 1. メイン名詞句構築 (root_noun + 修飾語 + 関係代名詞)
        main_phrase_parts = []
        rel_pronoun = None
        rel_subject = None
        
        # 各語を分類
        for word in sent.words:
            if word.id == root_noun.id:
                main_phrase_parts.append(word)
            elif word.head == root_noun.id and word.deprel in ['det', 'amod']:
                main_phrase_parts.append(word)  # "The"
            elif word.deprel == 'obj' and word.head == rel_verb.id:
                rel_pronoun = word  # "that"
                main_phrase_parts.append(word)
            elif word.deprel == 'nsubj' and word.head == rel_verb.id:
                rel_subject = word  # "he"
        
        # 語順でソート
        main_phrase_parts.sort(key=lambda w: w.id)
        
        # 結果構築
        main_phrase = ' '.join(w.text for w in main_phrase_parts)
        
        result['sub-o1'] = main_phrase  # "The book that"
        if rel_subject:
            result['sub-s'] = rel_subject.text  # "he"
        result['sub-v'] = rel_verb.text  # "bought"
        
        return result

# テスト実行
if __name__ == "__main__":
    print("="*50)
    print("🚀 シンプル関係節処理テスト")
    print("="*50)
    
    engine = SimpleRelativeClauseEngine()
    
    result = engine.process("The book that he bought")
    
    print("\n📊 結果:")
    for k, v in result.items():
        print(f"  {k}: '{v}'")
    
    print(f"\n期待結果:")
    print(f"  sub-o1: 'The book that'")
    print(f"  sub-s: 'he'")
    print(f"  sub-v: 'bought'")
    
    print("\n" + "="*50)
    print("✅ シンプル処理完了")
    print("="*50)
