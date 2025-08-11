"""
Rephrase仕様準拠 統一10スロット分解エンジン v1.0
正しいRephraseアーキテクチャ: 統一アルゴリズムによる再帰的10スロット分解
"""

import spacy
from typing import Dict, Any, Tuple, Optional
from collections import defaultdict

class Universal10SlotDecomposer:
    """統一10スロット分解エンジン - Rephrase仕様準拠"""
    
    def __init__(self):
        print("🚀 統一10スロット分解エンジン v1.0 初期化中...")
        self.nlp = spacy.load('en_core_web_sm')
        
        # 依存関係 → スロットマッピング（統一）
        self.dep_to_slot = {
            # 主要構造
            'nsubj': 'S', 'nsubjpass': 'S',  # 主語
            'aux': 'Aux', 'auxpass': 'Aux',   # 助動詞
            'dobj': 'O1', 'iobj': 'O2',       # 目的語
            'attr': 'C1', 'acomp': 'C1',      # 補語
            'xcomp': 'C2', 'ccomp': 'C2',     # 補語2
            
            # 修飾構造  
            'advmod': 'M2',                   # 副詞修飾
            'advcl': 'M3',                    # 副詞節
            'prep': 'M3',                     # 前置詞句
            'npadvmod': 'M2',                 # 名詞副詞
            
            # 特殊構造
            'relcl': 'relcl_marker',          # 関係節マーカー
            'mark': 'M1',                     # 従属接続詞
        }
        
        print("✅ 統一分解エンジン初期化完了")
    
    def decompose_any_text(self, text: str, depth: int = 0) -> Dict[str, Any]:
        """
        統一10スロット分解メソッド
        - 任意のテキストを10スロット構造に分解
        - 再帰適用により無限階層対応
        """
        indent = "  " * depth
        print(f"{indent}🔍 統一分解開始: '{text}' (depth={depth})")
        
        doc = self.nlp(text)
        root = self._find_root_verb(doc)
        
        if not root:
            print(f"{indent}⚠️ ROOT動詞未検出")
            return {}
        
        print(f"{indent}🎯 ROOT: '{root.text}' ({root.pos_})")
        
        # 統一10スロット抽出
        slots = {}
        
        # 10スロット定義（統一処理）
        slot_extractors = {
            'M1': self._extract_m1,
            'S': self._extract_s, 
            'Aux': self._extract_aux,
            'V': self._extract_v,
            'O1': self._extract_o1,
            'O2': self._extract_o2,
            'C1': self._extract_c1,
            'C2': self._extract_c2,
            'M2': self._extract_m2,
            'M3': self._extract_m3
        }
        
        for slot_name, extractor in slot_extractors.items():
            content, phrase_type = extractor(doc, root)
            
            if content and phrase_type:
                if phrase_type in ['phrase', 'clause']:
                    # 上位スロット空化 + 再帰分解
                    print(f"{indent}📍 {slot_name}スロット: '{content}' ({phrase_type}) → 再帰分解")
                    sub_result = self.decompose_any_text(content, depth + 1)
                    
                    if sub_result:
                        # sub-プレフィックスを付けて格納
                        slots[slot_name] = {}
                        for k, v in sub_result.items():
                            slots[slot_name][f"sub-{k.lower()}"] = v
                        print(f"{indent}✅ {slot_name}: {len(sub_result)}個のサブスロット生成")
                
                elif phrase_type == 'word':
                    # 単語レベル - 上位スロット保持
                    slots[slot_name] = {slot_name.lower(): content}
                    print(f"{indent}✅ {slot_name}: 単語保持 '{content}'")
        
        print(f"{indent}📋 統一分解完了: {len(slots)}スロット")
        return slots
    
    def _find_root_verb(self, doc):
        """ROOT動詞検出"""
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:
                return token
        return None
    
    # 統一スロット抽出メソッド（全て同じパターン）
    def _extract_m1(self, doc, root) -> Tuple[str, str]:
        """M1: 文頭修飾句抽出"""
        return self._generic_extract(doc, root, ['advmod', 'npadvmod'], position='pre')
    
    def _extract_s(self, doc, root) -> Tuple[str, str]:
        """S: 主語抽出"""
        for child in root.children:
            if child.dep_ in ['nsubj', 'nsubjpass']:
                # 関係節チェック
                has_relcl = any(gc.dep_ == 'relcl' for gc in child.children)
                if has_relcl:
                    span = self._expand_span_with_relcl(child, doc)
                    return span, 'clause'  # 関係節がある場合はclause
                else:
                    span = self._basic_span_expansion(child, doc)
                    return span, 'word' if len(span.split()) <= 2 else 'phrase'
        return "", ""
    
    def _extract_aux(self, doc, root) -> Tuple[str, str]:
        """Aux: 助動詞抽出"""
        for child in root.children:
            if child.dep_ in ['aux', 'auxpass']:
                return child.text, 'word'
        return "", ""
    
    def _extract_v(self, doc, root) -> Tuple[str, str]:
        """V: 動詞抽出"""
        return root.text, 'word'
    
    def _extract_o1(self, doc, root) -> Tuple[str, str]:
        """O1: 直接目的語抽出"""
        for child in root.children:
            if child.dep_ == 'dobj':
                span = self._basic_span_expansion(child, doc)
                return span, 'word' if len(span.split()) <= 2 else 'phrase'
        return "", ""
    
    def _extract_o2(self, doc, root) -> Tuple[str, str]:
        """O2: 間接目的語抽出"""
        for child in root.children:
            if child.dep_ == 'iobj':
                span = self._basic_span_expansion(child, doc)
                return span, 'word' if len(span.split()) <= 2 else 'phrase'
        return "", ""
    
    def _extract_c1(self, doc, root) -> Tuple[str, str]:
        """C1: 補語抽出"""
        for child in root.children:
            if child.dep_ in ['attr', 'acomp']:
                span = self._basic_span_expansion(child, doc)
                return span, 'word' if len(span.split()) <= 2 else 'phrase'
        return "", ""
    
    def _extract_c2(self, doc, root) -> Tuple[str, str]:
        """C2: 補語2抽出"""
        for child in root.children:
            if child.dep_ in ['xcomp', 'ccomp']:
                span = self._basic_span_expansion(child, doc)
                return span, 'clause'  # 通常clause
        return "", ""
    
    def _extract_m2(self, doc, root) -> Tuple[str, str]:
        """M2: 副詞句抽出"""
        for child in root.children:
            if child.dep_ == 'advmod':
                return child.text, 'word'
        return "", ""
    
    def _extract_m3(self, doc, root) -> Tuple[str, str]:
        """M3: 副詞節抽出"""
        for child in root.children:
            if child.dep_ == 'advcl':
                span = self._basic_span_expansion(child, doc)
                return span, 'clause'  # 副詞節はclause
        return "", ""
    
    def _generic_extract(self, doc, root, dep_types, position='any') -> Tuple[str, str]:
        """汎用的な抽出メソッド"""
        for child in root.children:
            if child.dep_ in dep_types:
                if position == 'pre' and child.i > root.i:
                    continue
                span = self._basic_span_expansion(child, doc)
                return span, 'word' if len(span.split()) <= 2 else 'phrase'
        return "", ""
    
    def _basic_span_expansion(self, token, doc) -> str:
        """基本的なスパン拡張"""
        expand_deps = ['det', 'amod', 'compound', 'poss']
        
        start = token.i
        end = token.i
        
        for child in token.children:
            if child.dep_ in expand_deps:
                start = min(start, child.i)
                end = max(end, child.i)
        
        return ' '.join([doc[i].text for i in range(start, end + 1)])
    
    def _expand_span_with_relcl(self, token, doc) -> str:
        """関係節を含むスパン拡張"""
        # 基本拡張
        span = self._basic_span_expansion(token, doc)
        
        # 関係節を含めて拡張  
        for child in token.children:
            if child.dep_ == 'relcl':
                # 関係代名詞を含める
                for relcl_child in child.children:
                    if relcl_child.dep_ == 'nsubj' and relcl_child.pos_ == 'PRON':
                        span += f" {relcl_child.text}"
                        break
                
                # 関係節全体を含める（後で再帰分解される）
                relcl_span = self._get_full_clause_span(child, doc)
                span += f" {relcl_span}"
                break
        
        return span.strip()
    
    def _get_full_clause_span(self, clause_root, doc) -> str:
        """節の完全なスパンを取得"""
        tokens = [clause_root]
        
        def collect_tokens(token):
            for child in token.children:
                tokens.append(child)
                collect_tokens(child)
        
        collect_tokens(clause_root)
        
        # 順序でソート
        tokens.sort(key=lambda t: t.i)
        
        return ' '.join([t.text for t in tokens])

def test_universal_decomposer():
    """統一分解エンジンテスト"""
    decomposer = Universal10SlotDecomposer()
    
    test_cases = [
        "She gave him a message.",
        "The woman who seemed indecisive knew the answer.",
        "He figured out the solution because he feared upsetting her."
    ]
    
    print("=" * 80)
    print("🧪 統一10スロット分解エンジンテスト")
    print("=" * 80)
    
    for i, sentence in enumerate(test_cases, 1):
        print(f"\n[テスト{i}] {sentence}")
        print("-" * 60)
        
        result = decomposer.decompose_any_text(sentence)
        
        print(f"\n📋 分解結果:")
        for slot, content in result.items():
            if isinstance(content, dict):
                print(f"  {slot}:")
                for key, value in content.items():
                    print(f"    {key}: {value}")
            else:
                print(f"  {slot}: {content}")

if __name__ == "__main__":
    test_universal_decomposer()
