#!/usr/bin/env python3
"""
Unified Boundary Expansion Library v1.0
Pure Stanza V3.1から抽出した統一境界拡張メカニズム

特徴:
- スロット別カスタム境界拡張
- 関係代名詞対応
- spaCy統合処理
- 完全に独立・既存システムに影響なし
"""

import spacy
from typing import Dict, List, Optional, Any

class BoundaryExpansionLib:
    """統一境界拡張ライブラリ"""
    
    def __init__(self):
        """境界拡張ライブラリ初期化"""
        print("🚀 統一境界拡張ライブラリ v1.0 初期化中...")
        
        # spaCy NLP パイプライン（境界調整用）
        try:
            self.spacy_nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy準備完了")
        except OSError:
            print("⚠️ spaCy英語モデル未検出・基本機能のみ使用")
            self.spacy_nlp = None
        
        # Pure Stanza V3.1から抽出: step18汎用境界拡張設定
        self.span_expand_deps = ['det', 'poss', 'compound', 'amod', 'nummod', 'case']
        self.relative_pronoun_deps = ['nsubj', 'dobj', 'pobj']  # 関係代名詞の役割
        
        # スロット特化拡張ルール（Pure Stanza V3.1完全抽出版）
        self.slot_specific_expansion_map = {
            # === 主語系（完全拡張）===
            'S': ['det', 'amod', 'compound', 'nmod', 'acl', 'acl:relcl', 'nummod', 'poss', 
                  'case', 'mark'],  # 関係節含む完全主語拡張
            
            # === 動詞系（助動詞・修飾完全対応）===
            'V': ['aux', 'aux:pass', 'auxpass', 'neg', 'advmod', 'compound:prt', 'prt'],
            'Aux': ['neg', 'advmod'],  # 助動詞専用
            
            # === 目的語系（主語と同等拡張）===
            'O1': ['det', 'amod', 'compound', 'nmod', 'acl', 'acl:relcl', 'nummod', 'poss'],
            'O2': ['det', 'amod', 'compound', 'nmod', 'nummod', 'poss'],
            
            # === 補語系（形容詞・名詞補語特化）===
            'C1': ['det', 'amod', 'compound', 'advmod', 'case', 'mark'],  # 比較構文対応強化
            'C2': ['det', 'amod', 'compound', 'to'],  # 不定詞補語対応
            
            # === 修飾語系（各タイプ特化）===
            'M1': ['advmod', 'prep', 'pobj', 'case', 'mark', 'cc', 'conj'],  # 前置詞句・接続詞完全対応
            'M2': ['advmod', 'prep', 'pobj', 'compound'],  # 副詞修飾強化
            'M3': ['advmod', 'prep', 'pobj', 'tmod', 'npadvmod']  # 時間・場所修飾特化
        }
        
        # 後方互換性のため既存マップも保持
        self.slot_expansion_map = self.slot_specific_expansion_map
        
        print("🏗️ 統一境界拡張ライブラリ準備完了")
    
    def expand_span_generic(self, text: str, expansion_context: Optional[Dict] = None) -> str:
        """
        汎用スパン拡張処理（Pure Stanza V3.1 step18メカニズム）
        
        Args:
            text: 拡張対象テキスト
            expansion_context: 拡張コンテキスト設定
            
        Returns:
            境界拡張されたテキスト
        """
        if not self.spacy_nlp:
            return text  # spaCy未利用時は元テキストそのまま
        
        try:
            spacy_doc = self.spacy_nlp(text)
            
            if len(spacy_doc) <= 1:
                return text
                
            # 拡張設定（コンテキストベース）
            expand_deps = expansion_context.get('expand_deps', self.span_expand_deps) if expansion_context else self.span_expand_deps
            
            # 各トークンの境界拡張
            expanded_spans = []
            
            for token in spacy_doc:
                span_start = token.i
                span_end = token.i
                
                # 依存語による拡張
                for child in token.children:
                    if child.dep_ in expand_deps:
                        span_start = min(span_start, child.i)
                        span_end = max(span_end, child.i)
                
                # 関係代名詞の境界拡張
                if token.dep_ in ['relcl', 'acl']:
                    rel_pronouns = self._find_relative_pronouns_in_span(token, spacy_doc)
                    for rel_idx in rel_pronouns:
                        span_start = min(span_start, rel_idx)
                        span_end = max(span_end, rel_idx)
                
                if span_start <= span_end:
                    span_text = ' '.join(spacy_doc[i].text for i in range(span_start, span_end + 1))
                    expanded_spans.append(span_text)
            
            # 重複除去と結合
            unique_spans = list(dict.fromkeys(expanded_spans))  # 順序保持で重複除去
            return ' '.join(unique_spans) if unique_spans else text
            
        except Exception as e:
            print(f"⚠️ 汎用スパン拡張エラー: {e}")
            return text
    
    def expand_span_for_slot(self, text: str, slot_key: str) -> str:
        """
        スロット特化境界拡張（Pure Stanza V3.1完全版）
        
        Args:
            text: 拡張対象テキスト
            slot_key: スロット名（S, V, O1, O2, C1, C2, M1, M2, M3, Aux）
            
        Returns:
            スロット別最適化された境界拡張テキスト
        """
        # スロット特化拡張依存語設定取得
        expand_deps = self.slot_specific_expansion_map.get(slot_key, self.span_expand_deps)
        
        # スロット特化拡張コンテキスト作成
        expansion_context = {
            'expand_deps': expand_deps,
            'slot_type': slot_key,
            'slot_specific': True  # スロット特化モードフラグ
        }
        
        # スロット別特別処理
        if slot_key in ['S', 'O1'] and self._contains_relative_clause(text):
            # 主語・目的語の関係節特化処理
            return self._expand_with_relative_clause_optimization(text, expansion_context)
        elif slot_key == 'V' and self._contains_modal_verb(text):
            # 動詞のモーダル特化処理
            return self._expand_with_modal_optimization(text, expansion_context)
        elif slot_key in ['M1', 'M2', 'M3'] and self._contains_prepositional_phrase(text):
            # 修飾語の前置詞句特化処理
            return self._expand_with_prepositional_optimization(text, expansion_context)
        else:
            # 汎用拡張処理
            return self.expand_span_generic(text, expansion_context)
    
    def _contains_relative_clause(self, text: str) -> bool:
        """関係節含有判定"""
        if not self.spacy_nlp:
            return False
        try:
            doc = self.spacy_nlp(text)
            return any(token.dep_ in ['acl:relcl', 'relcl'] for token in doc)
        except:
            return False
    
    def _contains_modal_verb(self, text: str) -> bool:
        """モーダル動詞含有判定"""
        modal_verbs = {'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'}
        return any(word.lower() in modal_verbs for word in text.split())
    
    def _contains_prepositional_phrase(self, text: str) -> bool:
        """前置詞句含有判定"""
        if not self.spacy_nlp:
            return False
        try:
            doc = self.spacy_nlp(text)
            return any(token.pos_ == 'ADP' for token in doc)
        except:
            return False
    
    def _expand_with_relative_clause_optimization(self, text: str, context: Dict) -> str:
        """関係節最適化拡張"""
        # 関係節特化の拡張処理
        enhanced_deps = context['expand_deps'] + ['mark', 'nsubj:relcl', 'obj:relcl']
        enhanced_context = {**context, 'expand_deps': enhanced_deps}
        return self.expand_span_generic(text, enhanced_context)
    
    def _expand_with_modal_optimization(self, text: str, context: Dict) -> str:
        """モーダル動詞最適化拡張"""
        # モーダル動詞特化の拡張処理
        enhanced_deps = context['expand_deps'] + ['ccomp', 'xcomp', 'advcl']
        enhanced_context = {**context, 'expand_deps': enhanced_deps}
        return self.expand_span_generic(text, enhanced_context)
    
    def _expand_with_prepositional_optimization(self, text: str, context: Dict) -> str:
        """前置詞句最適化拡張"""
        # 前置詞句特化の拡張処理
        enhanced_deps = context['expand_deps'] + ['pcomp', 'pobj', 'agent']
        enhanced_context = {**context, 'expand_deps': enhanced_deps}
        return self.expand_span_generic(text, enhanced_context)
    
    def _find_relative_pronouns_in_span(self, rel_token, spacy_doc) -> List[int]:
        """スパン内関係代名詞インデックス検出（汎用）"""
        rel_indices = []
        
        for child in rel_token.children:
            if (child.pos_ == 'PRON' and 
                child.dep_ in self.relative_pronoun_deps and
                child.text.lower() in ['who', 'whom', 'whose', 'which', 'that']):
                rel_indices.append(child.i)
        
        return rel_indices
    
    def get_expansion_deps_for_slot(self, slot_key: str) -> List[str]:
        """
        スロットタイプ別拡張依存語設定取得（Pure Stanza V3.1完全版）
        
        Args:
            slot_key: スロット名
            
        Returns:
            スロット特化拡張依存語リスト
        """
        return self.slot_specific_expansion_map.get(slot_key, self.span_expand_deps)
    
    def check_requires_expansion(self, text: str) -> bool:
        """
        境界拡張が必要かどうか判定
        
        Args:
            text: 判定対象テキスト
            
        Returns:
            True: 拡張必要, False: 不要
        """
        if not self.spacy_nlp or not text or len(text.strip()) == 0:
            return False
        
        try:
            spacy_doc = self.spacy_nlp(text)
            
            # 修飾語カウント
            modifier_count = sum(1 for token in spacy_doc if token.dep_ in self.span_expand_deps)
            
            # 修飾語が存在すれば拡張対象
            return modifier_count > 0
            
        except Exception:
            return False  # spaCy処理失敗時は基本判定のみ

# === テスト・検証用関数 ===

def test_boundary_expansion():
    """境界拡張ライブラリテスト"""
    lib = BoundaryExpansionLib()
    
    test_cases = [
        {
            "text": "the tall man",
            "slot": "S",
            "expected_improved": True,
            "description": "限定詞+形容詞+名詞"
        },
        {
            "text": "very carefully",
            "slot": "M2", 
            "expected_improved": True,
            "description": "副詞修飾"
        },
        {
            "text": "New York City",
            "slot": "O1",
            "expected_improved": True,
            "description": "複合名詞"
        },
        {
            "text": "run",
            "slot": "V",
            "expected_improved": False,
            "description": "単一語（拡張不要）"
        }
    ]
    
    print("🧪 境界拡張ライブラリテスト開始")
    print("=" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['description']}: '{case['text']}'")
        
        # 拡張前
        original = case['text']
        
        # 汎用拡張
        generic_expanded = lib.expand_span_generic(original)
        
        # スロット別拡張
        slot_expanded = lib.expand_span_for_slot(original, case['slot'])
        
        # 拡張必要性判定
        requires_expansion = lib.check_requires_expansion(original)
        
        print(f"   元テキスト: '{original}'")
        print(f"   汎用拡張: '{generic_expanded}'")
        print(f"   {case['slot']}拡張: '{slot_expanded}'")
        print(f"   拡張必要: {requires_expansion}")
        print(f"   期待結果: {'拡張あり' if case['expected_improved'] else '拡張なし'}")
        
        # 結果判定
        improved = (generic_expanded != original) or (slot_expanded != original)
        result = "✅ 成功" if improved == case['expected_improved'] else "❌ 失敗"
        print(f"   {result}")
    
    print(f"\n✅ 境界拡張ライブラリテスト完了")

if __name__ == "__main__":
    test_boundary_expansion()
