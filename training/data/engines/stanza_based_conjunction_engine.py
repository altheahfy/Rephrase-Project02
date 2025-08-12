#!/usr/bin/env python3
"""
Stanza準拠従属接続詞エンジン
ハードコーディングを最小化し、Stanzaの構造解析に依存
"""

import stanza
from typing import Dict, List, Optional, Any

class StanzaBasedConjunctionEngine:
    """Stanza構造解析準拠の接続詞エンジン"""
    
    def __init__(self):
        print("🚀 Stanza準拠接続詞エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 最小限の意味分類（語彙的知識として必要）
        self.semantic_mapping = {
            # 理由 -> M1位置
            'because': 'M1', 'since': 'M1', 'as': 'M1',
            # 条件 -> M1位置  
            'if': 'M1', 'unless': 'M1', 'provided': 'M1',
            # 譲歩 -> M2位置
            'although': 'M2', 'though': 'M2', 'whereas': 'M2',
            # 時間 -> M3位置
            'when': 'M3', 'while': 'M3', 'after': 'M3', 'before': 'M3', 'until': 'M3'
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理 - Stanza構造解析ベース"""
        print(f"🔍 Stanza構造解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # Stanza構造による従属節検出
        subordinate_info = self._analyze_subordinate_structure(sent)
        
        if subordinate_info:
            return self._process_by_stanza_structure(sent, subordinate_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_subordinate_structure(self, sent) -> Optional[Dict]:
        """Stanza構造による従属節分析"""
        structure_info = {
            'mark_word': None,      # mark関係の接続詞
            'advcl_word': None,     # advcl関係の動詞
            'main_verb': None,      # 主節の動詞（root）
            'conjunction_type': None # 意味分類
        }
        
        # 1. 構造要素を特定
        for word in sent.words:
            if word.deprel == 'mark' and word.upos == 'SCONJ':
                structure_info['mark_word'] = word
                # 意味分類を語彙から判定
                lemma = word.lemma.lower()
                structure_info['conjunction_type'] = self.semantic_mapping.get(lemma, 'M1')
                
            elif word.deprel == 'advcl':
                structure_info['advcl_word'] = word
                
            elif word.deprel == 'root':
                structure_info['main_verb'] = word
        
        # 2. 完全性チェック
        if structure_info['mark_word'] or structure_info['advcl_word']:
            print(f"  📋 従属構造検出:")
            print(f"    接続詞: {structure_info['mark_word'].text if structure_info['mark_word'] else '?'}")
            print(f"    従属動詞: {structure_info['advcl_word'].text if structure_info['advcl_word'] else '?'}")
            print(f"    主動詞: {structure_info['main_verb'].text if structure_info['main_verb'] else '?'}")
            return structure_info
        
        return None
    
    def _process_by_stanza_structure(self, sent, structure_info) -> Dict[str, str]:
        """Stanza構造に基づく分解処理"""
        mark_word = structure_info['mark_word']
        advcl_word = structure_info['advcl_word']
        main_verb = structure_info['main_verb']
        conjunction_type = structure_info['conjunction_type']
        
        result = {}
        
        # 単独従属節の場合（主節なし、または advcl検出なし）
        if mark_word and (not main_verb or not advcl_word):
            print("  📝 単独従属節処理")
            return self._process_single_subordinate_clause(sent, mark_word)
        
        # 複合文の場合
        if mark_word and advcl_word and main_verb:
            print(f"  📝 複合文処理 (接続詞位置: {conjunction_type})")
            
            # 従属節要素の抽出
            sub_elements = self._extract_subordinate_elements(sent, advcl_word, mark_word)
            # 主節要素の抽出  
            main_elements = self._extract_main_elements(sent, main_verb)
            
            # Rephrase分解結果の構築
            result.update(sub_elements)
            result.update(main_elements)
            
            return result
        
        return {"error": "構造解析失敗"}
    
    def _process_single_subordinate_clause(self, sent, mark_word) -> Dict[str, str]:
        """単独従属節の処理"""
        result = {}
        
        # 接続詞
        conjunction_type = self.semantic_mapping.get(mark_word.lemma.lower(), 'M1')
        result[f"sub-{conjunction_type.lower()}"] = mark_word.text.lower()
        
        # 従属節の動詞を探す
        subordinate_verb = None
        for word in sent.words:
            if word.upos in ['VERB', 'AUX'] and word.id > mark_word.id:
                subordinate_verb = word
                break
        
        if subordinate_verb:
            # 従属節の要素を抽出
            sub_elements = self._extract_clause_elements(sent, subordinate_verb, "sub-")
            result.update(sub_elements)
        
        print(f"  ✅ 単独従属節結果: {result}")
        return result
    
    def _extract_subordinate_elements(self, sent, advcl_verb, mark_word) -> Dict[str, str]:
        """従属節要素の抽出"""
        elements = {}
        
        # 接続詞の位置分類
        conjunction_type = self.semantic_mapping.get(mark_word.lemma.lower(), 'M1')
        elements[f"sub-{conjunction_type.lower()}"] = mark_word.text.lower()
        
        # 従属節の文法要素
        clause_elements = self._extract_clause_elements(sent, advcl_verb, "sub-")
        elements.update(clause_elements)
        
        return elements
    
    def _extract_main_elements(self, sent, main_verb) -> Dict[str, str]:
        """主節要素の抽出"""
        return self._extract_clause_elements(sent, main_verb, "")
    
    def _extract_clause_elements(self, sent, verb, prefix="") -> Dict[str, str]:
        """節の文法要素抽出"""
        elements = {}
        
        # 動詞周辺の依存関係を分析
        for word in sent.words:
            if word.head == verb.id:
                if word.deprel == 'nsubj':
                    elements[f"{prefix}s"] = word.text
                elif word.deprel == 'obj':
                    elements[f"{prefix}o1"] = word.text
                elif word.deprel == 'iobj':
                    elements[f"{prefix}o2"] = word.text
                elif word.deprel == 'advmod':
                    elements[f"{prefix}m1"] = word.text
            elif word.id == verb.id:
                if word.upos == 'AUX':
                    elements[f"{prefix}aux"] = word.text
                elif word.upos == 'VERB':
                    elements[f"{prefix}v"] = word.text
                elif word.upos == 'ADJ':
                    elements[f"{prefix}c1"] = word.text
        
        return elements
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理"""
        print("  📝 単純文処理")
        
        # root動詞を探す
        main_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                main_verb = word
                break
        
        if main_verb:
            return self._extract_clause_elements(sent, main_verb)
        
        return {"error": "動詞未検出"}

def test_stanza_based_engine():
    """テスト実行"""
    engine = StanzaBasedConjunctionEngine()
    
    test_cases = [
        "Because he is tired",
        "If you come tomorrow",
        "Although she tried hard",
        "When the bell rings",
        "Because he is tired, he went home",
        "If it rains, we stay inside"
    ]
    
    print("\n" + "="*50)
    print("🧪 Stanza準拠接続詞エンジン テスト")
    print("="*50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【Test {i}】 '{test}'")
        result = engine.process(test)
        
        print("📊 結果:")
        for key, value in result.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_stanza_based_engine()
