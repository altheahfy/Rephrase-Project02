#!/usr/bin/env python3
"""
Simple Relative Clause Engine - シンプル関係節処理
Stanzaの構造をそのまま活用した直接的なRephrase分解

核心原則:
1. Stanzaの依存構造をそのまま使用
2. 先行詞+関係代名詞の結合
3. 余計な再帰処理なし
4. 直接的なRephrase出力
"""

import stanza
from typing import Dict, List, Optional, Any

class SimpleRelativeEngine:
    """シンプル関係節エンジン"""
    
    def __init__(self):
        print("🚀 シンプル関係節エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理"""
        print(f"🔍 処理開始: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 関係節検出
        if self._has_relative_clause(sent):
            return self._process_relative_clause(sent)
        else:
            return self._process_simple_sentence(sent)
    
    def _has_relative_clause(self, sent) -> bool:
        """関係節を含むかチェック"""
        return any(w.deprel == 'acl:relcl' for w in sent.words)
    
    def _process_relative_clause(self, sent) -> Dict[str, str]:
        """関係節の直接処理"""
        print("📖 関係節処理")
        
        # === 1. 要素特定 ===
        rel_verb = self._find_by_deprel(sent, 'acl:relcl')  # "bought"
        if not rel_verb:
            return {"error": "関係動詞未検出"}
        
        # 先行詞（関係動詞の頭）
        antecedent = self._find_by_id(sent, rel_verb.head)  # "book" 
        
        # 関係代名詞（関係動詞の目的語/主語）
        rel_pronoun = self._find_by_head_and_deprel(sent, rel_verb.id, 'obj')  # "that"
        if not rel_pronoun:
            rel_pronoun = self._find_by_head_and_deprel(sent, rel_verb.id, 'nsubj')  # 主語の場合
        
        # 関係節内主語
        rel_subject = self._find_by_head_and_deprel(sent, rel_verb.id, 'nsubj')  # "he"
        
        print(f"  先行詞: {antecedent.text if antecedent else '?'}")
        print(f"  関係代名詞: {rel_pronoun.text if rel_pronoun else '?'}")
        print(f"  関係節主語: {rel_subject.text if rel_subject else '?'}")
        print(f"  関係動詞: {rel_verb.text}")
        
        # === 2. 先行詞句構築 ===
        noun_phrase = self._build_noun_phrase(sent, antecedent, rel_pronoun)
        print(f"  構築句: '{noun_phrase}'")
        
        # === 3. Rephrase分解 ===
        result = {
            "O1": "",  # 上位スロット空
        }
        
        # 関係代名詞の役割に応じて配置
        if rel_pronoun and rel_pronoun.deprel == 'obj':
            result["sub-o1"] = noun_phrase  # 目的語なのでsub-o1
        elif rel_pronoun and rel_pronoun.deprel == 'nsubj':
            result["sub-s"] = noun_phrase   # 主語なのでsub-s
        else:
            result["sub-o1"] = noun_phrase  # デフォルト
        
        if rel_subject:
            result["sub-s"] = rel_subject.text
        
        result["sub-v"] = rel_verb.text
        
        return result
    
    def _build_noun_phrase(self, sent, antecedent, rel_pronoun) -> str:
        """先行詞句を構築（修飾語含む）"""
        if not antecedent:
            return rel_pronoun.text if rel_pronoun else ""
        
        # 先行詞の修飾語を収集
        modifiers = []
        for word in sent.words:
            if word.head == antecedent.id and word.deprel in ['det', 'amod', 'compound']:
                modifiers.append(word)
        
        # 語順でソート
        phrase_words = modifiers + [antecedent]
        if rel_pronoun:
            phrase_words.append(rel_pronoun)
        
        phrase_words.sort(key=lambda w: w.id)
        return ' '.join(w.text for w in phrase_words)
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理"""
        print("📝 単純文処理")
        
        root = self._find_root(sent)
        if not root:
            return {"error": "ROOT未検出"}
        
        result = {}
        
        # 基本要素抽出
        for word in sent.words:
            if word.deprel == 'nsubj':
                result["S"] = word.text
            elif word.deprel == 'obj':
                result["O1"] = word.text
            elif word.deprel == 'root':
                result["V"] = word.text
        
        return result
    
    # === ヘルパーメソッド ===
    def _find_by_deprel(self, sent, deprel: str):
        """依存関係で語を検索"""
        return next((w for w in sent.words if w.deprel == deprel), None)
    
    def _find_by_id(self, sent, word_id: int):
        """IDで語を検索"""
        return next((w for w in sent.words if w.id == word_id), None)
    
    def _find_by_head_and_deprel(self, sent, head_id: int, deprel: str):
        """頭IDと依存関係で語を検索"""
        return next((w for w in sent.words if w.head == head_id and w.deprel == deprel), None)
    
    def _find_root(self, sent):
        """ROOT語を検索"""
        return next((w for w in sent.words if w.head == 0), None)

# === テスト実行 ===
if __name__ == "__main__":
    print("="*60)
    print("🚀 シンプル関係節エンジン テスト")
    print("="*60)
    
    engine = SimpleRelativeEngine()
    
    # 関係節テスト
    test_text = "The book that he bought"
    print(f"\n📖 テスト: '{test_text}'")
    print("-" * 40)
    
    result = engine.process(test_text)
    
    print("\n📊 結果:")
    for key, value in result.items():
        print(f"  {key}: '{value}'")
    
    print(f"\n🎯 期待結果:")
    print(f"  O1: '' (空)")
    print(f"  sub-o1: 'The book that'") 
    print(f"  sub-s: 'he'")
    print(f"  sub-v: 'bought'")
    
    print("\n" + "="*60)
    print("🎯 シンプル直接処理完了！")
    print("="*60)
