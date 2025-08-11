#!/usr/bin/env python3
"""
Phase 2: 階層的Clause分解エンジン
Pure Stanza Engine v3を基盤とした複文対応

設計原則:
1. v3の成功原則を完全継承（ゼロハードコーディング・パターン駆動）
2. 各clauseにv3エンジンを再帰適用
3. 段階的で確実な拡張
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pure_stanza_engine_v3 import PureStanzaEngineV3
import stanza
from typing import Dict, List, Optional, Any, Tuple

class HierarchicalClauseEngine(PureStanzaEngineV3):
    """階層的Clause分解エンジン（Phase 2）"""
    
    def __init__(self):
        super().__init__()
        self.subordinate_relations = ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'csubj']
        
    def analyze_complex_sentence(self, text: str) -> Dict[str, Any]:
        """複文の階層的分析（Phase 2のメイン機能）"""
        print(f"\n🎯 Phase2: 複文階層分析開始 '{text}'")
        
        # Stanza解析
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 文構造の分類
        subordinate_clauses = self._extract_subordinate_clauses(sent)
        sentence_type = "complex" if subordinate_clauses else "simple"
        
        print(f"📋 文型分類: {sentence_type} ({len(subordinate_clauses)}個の従属節)")
        
        if sentence_type == "simple":
            # 単文の場合はv3エンジンをそのまま適用
            simple_result = super().decompose(text)
            return {
                "sentence_type": "simple",
                "main_clause": {
                    "clause_type": "main",
                    "slots": simple_result
                },
                "subordinate_clauses": [],
                "total_clauses": 1
            }
        
        # 複文の場合の階層的処理
        main_clause_result = self._analyze_main_clause(sent)
        subordinate_results = []
        
        for clause_info in subordinate_clauses:
            clause_result = self._analyze_subordinate_clause(sent, clause_info)
            subordinate_results.append(clause_result)
        
        # 統合結果
        return {
            "sentence_type": "complex",
            "main_clause": main_clause_result,
            "subordinate_clauses": subordinate_results,
            "total_clauses": 1 + len(subordinate_results)
        }
    
    def _extract_subordinate_clauses(self, sent) -> List[Dict[str, Any]]:
        """従属節情報の抽出"""
        subordinate_clauses = []
        
        for word in sent.words:
            if word.deprel in self.subordinate_relations:
                # 従属節の構成単語を収集
                clause_words = self._collect_clause_words(sent, word)
                
                # 従属接続詞の特定
                connector = self._find_connector(clause_words)
                
                clause_info = {
                    "head_word": word,
                    "relation": word.deprel,
                    "words": clause_words,
                    "connector": connector
                }
                subordinate_clauses.append(clause_info)
                print(f"🔍 従属節検出: '{word.text}' ({word.deprel}) 接続詞:'{connector}'")
        
        return subordinate_clauses
    
    def _analyze_main_clause(self, sent) -> Dict[str, Any]:
        """主節の分析（従属節を除外してv3適用）"""
        print("\n📋 主節分析:")
        
        # 主節の単語のみを抽出
        main_clause_words = self._extract_main_clause_words(sent)
        main_clause_text = self._reconstruct_clause_text(main_clause_words)
        
        print(f"📌 主節テキスト: '{main_clause_text}'")
        
        # v3エンジンで主節を分析
        try:
            main_slots = super().decompose(main_clause_text)
            return {
                "clause_type": "main",
                "text": main_clause_text,
                "slots": main_slots
            }
        except Exception as e:
            print(f"❌ 主節分析エラー: {e}")
            return {
                "clause_type": "main",
                "text": main_clause_text,
                "slots": {},
                "error": str(e)
            }
    
    def _analyze_subordinate_clause(self, sent, clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """個別従属節の分析（v3エンジン再帰適用）"""
        head_word = clause_info["head_word"]
        clause_words = clause_info["words"]
        connector = clause_info["connector"]
        
        print(f"\n📋 従属節分析: '{head_word.text}' ({clause_info['relation']})")
        
        # 従属節テキストの再構成
        clause_text = self._reconstruct_clause_text(clause_words)
        print(f"📌 従属節テキスト: '{clause_text}'")
        
        # v3エンジンで従属節を分析
        try:
            subordinate_slots = super().decompose(clause_text)
            return {
                "clause_type": "subordinate",
                "relation": clause_info["relation"],
                "connector": connector,
                "text": clause_text,
                "slots": subordinate_slots
            }
        except Exception as e:
            print(f"❌ 従属節分析エラー: {e}")
            return {
                "clause_type": "subordinate",
                "relation": clause_info["relation"],
                "connector": connector,
                "text": clause_text,
                "slots": {},
                "error": str(e)
            }
    
    def _extract_main_clause_words(self, sent) -> List[Any]:
        """主節の単語のみ抽出（従属節を除外）"""
        subordinate_word_ids = set()
        
        # 従属節に属する単語IDを収集
        for word in sent.words:
            if word.deprel in self.subordinate_relations:
                subordinate_word_ids.update(self._get_subtree_word_ids(sent, word))
        
        # 主節の単語のみ抽出
        main_words = []
        for word in sent.words:
            if word.id not in subordinate_word_ids:
                main_words.append(word)
        
        return main_words
    
    def _collect_clause_words(self, sent, head_word) -> List[Any]:
        """従属節の構成単語を収集"""
        clause_words = []
        subtree_ids = self._get_subtree_word_ids(sent, head_word)
        
        for word in sent.words:
            if word.id in subtree_ids:
                clause_words.append(word)
        
        return clause_words
    
    def _get_subtree_word_ids(self, sent, head_word) -> set:
        """指定した語を頂点とする部分木の単語IDを取得"""
        subtree_ids = {head_word.id}
        
        def add_children(word_id):
            for word in sent.words:
                if word.head == word_id and word.id not in subtree_ids:
                    subtree_ids.add(word.id)
                    add_children(word.id)
        
        add_children(head_word.id)
        return subtree_ids
    
    def _find_connector(self, clause_words) -> str:
        """従属接続詞を特定"""
        for word in clause_words:
            if word.deprel == 'mark':
                return word.text
        return ""
    
    def _reconstruct_clause_text(self, words: List[Any]) -> str:
        """単語リストからクローズテキストを再構成"""
        # 単語をIDでソート
        sorted_words = sorted(words, key=lambda w: w.id)
        return " ".join([w.text for w in sorted_words])

def test_hierarchical_engine():
    """Phase 2エンジンのテスト"""
    print("🎯 Phase 2: 階層的Clause分解エンジン テスト開始\n")
    
    try:
        engine = HierarchicalClauseEngine()
        print("✅ Phase 2エンジン初期化完了\n")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    test_sentences = [
        # 単文（v3基盤の継続動作確認）
        "He succeeded.",
        "They are working.",
        
        # 複文（Phase 2新機能）
        "He succeeded even though he was under intense pressure.",
        "She passed the test because she is very intelligent.",
        "We waited while they are working.",
        "I will help you if you need it.",
        "The man who is tall walks quickly.",
        "I know that he is happy."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print('='*80)
        
        result = engine.analyze_complex_sentence(sentence)
        
        print(f"\n📊 Phase2 分析結果:")
        print(f"📋 文型: {result.get('sentence_type', 'unknown')}")
        print(f"📋 節数: {result.get('total_clauses', 0)}")
        
        # 主節結果
        main_clause = result.get('main_clause', {})
        print(f"\n🏛️ 主節:")
        print(f"  テキスト: '{main_clause.get('text', 'N/A')}'")
        print(f"  スロット: {main_clause.get('slots', {})}")
        if 'error' in main_clause:
            print(f"  ⚠️ エラー: {main_clause['error']}")
        
        # 従属節結果
        for i, sub_clause in enumerate(result.get('subordinate_clauses', [])):
            print(f"\n🔗 従属節 {i+1}:")
            print(f"  接続: '{sub_clause.get('connector', '')}' ({sub_clause.get('relation', 'N/A')})")
            print(f"  テキスト: '{sub_clause.get('text', 'N/A')}'")
            print(f"  スロット: {sub_clause.get('slots', {})}")
            if 'error' in sub_clause:
                print(f"  ⚠️ エラー: {sub_clause['error']}")

if __name__ == "__main__":
    test_hierarchical_engine()
