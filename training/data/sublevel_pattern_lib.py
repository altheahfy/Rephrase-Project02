#!/usr/bin/env python3
"""
Sublevel Pattern Library v1.0
Pure Stanza Engine V3.1から抽出したサブレベル専用パターンライブラリ

特徴:
- 関係節・従属節内の5文型パターン認識
- サブレベル専用修飾語マッピング
- Grammar Master Controller V2統合対応
- Pure Stanza V3.1の知識ベース完全抽出
"""

import stanza
from typing import Dict, List, Optional, Any, Tuple
import logging

class SublevelPatternLib:
    """サブレベル専用パターンライブラリ（Pure Stanza V3.1完全版）"""
    
    def __init__(self):
        """サブレベルパターンライブラリ初期化"""
        print("🚀 サブレベル専用パターンライブラリ v1.0 初期化中...")
        
        # Stanza NLP パイプライン（構文解析用）
        try:
            self.nlp = stanza.Pipeline('en', verbose=False)
            print("✅ Stanza構文解析準備完了")
        except Exception as e:
            print(f"⚠️ Stanza初期化エラー: {e}")
            self.nlp = None
        
        # Pure Stanza V3.1から完全抽出: サブレベル専用パターン
        self.sublevel_patterns = self._load_sublevel_patterns()
        
        # サブレベル専用修飾語マッピング
        self.sublevel_modifiers = self._load_sublevel_modifiers()
        
        # 関係代名詞・従属接続詞の識別ルール
        self.relative_pronouns = ['who', 'whom', 'whose', 'which', 'that']
        self.subordinate_conjunctions = ['because', 'although', 'when', 'if', 'since', 'while', 'unless', 'until']
        
        print("🏗️ サブレベル専用パターンライブラリ準備完了")
    
    def _load_sublevel_patterns(self) -> Dict[str, Any]:
        """Pure Stanza V3.1完全抽出: サブレベル専用パターン"""
        return {
            # === サブレベル5文型（関係節・従属節対応） ===
            "SUB_SV": {
                "description": "サブレベル第1文型（主語+動詞）",
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"}
            },
            "SUB_SVC": {
                "description": "サブレベル第2文型（主語+動詞+補語）",
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SUB_SVO": {
                "description": "サブレベル第3文型（主語+動詞+目的語）",
                "required_relations": ["nsubj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "root": "V"}
            },
            "SUB_SVOO": {
                "description": "サブレベル第4文型（主語+動詞+間接目的語+直接目的語）",
                "required_relations": ["nsubj", "iobj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"}
            },
            "SUB_SVOC": {
                "description": "サブレベル第5文型（主語+動詞+目的語+補語）",
                "required_relations": ["nsubj", "obj", "xcomp", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"}
            },
            
            # === 関係代名詞節専用パターン ===
            "REL_SUBJ": {
                "description": "関係代名詞主語節（who runs）",
                "required_relations": ["root"],
                "root_pos": ["VERB"],
                "special": "relative_subject",
                "mapping": {"root": "V"}
            },
            "REL_OBJ": {
                "description": "関係代名詞目的語節（that he bought）",
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "special": "relative_object",
                "mapping": {"nsubj": "S", "root": "V"}
            },
            
            # === 従属節（副詞節）専用パターン ===
            "ADV_CLAUSE": {
                "description": "副詞節（because he runs, when she arrives）",
                "required_relations": ["mark", "nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"mark": "M1", "nsubj": "S", "root": "V"}
            },
            
            # === 分詞構文専用パターン ===
            "PARTICIPLE": {
                "description": "分詞構文（running fast, built yesterday）",
                "required_relations": ["root"],
                "root_pos": ["VERB"],
                "special": "participial",
                "mapping": {"root": "V"}
            },
            
            # === 前置詞句専用パターン ===
            "PREP_PHRASE": {
                "description": "前置詞句（in the garden）",
                "required_relations": ["root", "case"],
                "root_pos": ["NOUN"],
                "mapping": {"root": "C1", "case": "M1"}
            },
            
            # === 比較構文専用パターン ===
            "COMPARATIVE": {
                "description": "比較構文（taller than John）",
                "required_relations": ["root", "case"],
                "root_pos": ["ADJ"],
                "special": "comparison",
                "mapping": {"root": "C1", "case": "M1"}
            }
        }
    
    def _load_sublevel_modifiers(self) -> Dict[str, str]:
        """Pure Stanza V3.1完全抽出: サブレベル専用修飾語マッピング"""
        return {
            # === 基本修飾語 ===
            "det": "M1",        # 限定詞: a, the, this, that
            "amod": "M2",       # 形容詞修飾: tall, beautiful, red
            "advmod": "M3",     # 副詞修飾: very, quite, extremely  
            "case": "M1",       # 前置詞: in, on, at, with, by
            "compound": "M2",   # 複合語: New York, high school
            "nummod": "M1",     # 数量詞: two, many, several
            
            # === サブレベル高次修飾語 ===
            "mark": "M1",       # 従属節マーカー: that, which, who, because, although
            "cc": "M1",         # 等位接続詞: and, or, but
            "conj": "M2",       # 等位要素: books and pens の "pens"
            "appos": "M2",      # 同格: John, the teacher
            "acl": "M2",        # 修飾節: book that I bought
            "acl:relcl": "M2",  # 関係代名詞節: man who runs
            
            # === サブレベル時制・相関連 ===
            "aux": "Aux",       # 助動詞: have, be, will, can
            "aux:pass": "Aux",  # 受動助動詞: be (in "be built")
            "auxpass": "Aux",   # 受動助動詞（別表記）
            "tmod": "M3",       # 時間修飾: yesterday, tomorrow
            
            # === サブレベル前置詞句関連 ===
            "pobj": "C1",       # 前置詞の目的語: in the garden の "garden"
            "pcomp": "C1",      # 前置詞補語
            "agent": "M1",      # 動作主: by him (受動態)
            
            # === サブレベル比較・程度 ===
            "neg": "M3",        # 否定: not, never
            "expl": "M3",       # 虚辞: there (in "there is")
            "dep": "M3",        # その他依存語
            "parataxis": "M2",  # 並列文: He said, "Hello"
        }
    
    def analyze_sublevel_pattern(self, text: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        サブレベル専用パターン解析（Pure Stanza V3.1メソッド）
        
        Args:
            text: 解析対象テキスト
            
        Returns:
            (パターン名, パターン詳細) or None
        """
        if not self.nlp:
            return None
        
        try:
            # Stanza構文解析
            doc = self.nlp(text)
            sent = doc.sentences[0]
            
            # ROOT語検出
            root_word = self._find_root_word(sent)
            if not root_word:
                return None
            
            # サブレベル専用パターンマッチング
            matched_pattern = self._match_sublevel_pattern(sent, root_word)
            
            if matched_pattern:
                pattern_details = self.sublevel_patterns[matched_pattern].copy()
                pattern_details['root_word'] = root_word.text
                pattern_details['root_pos'] = root_word.pos
                pattern_details['text'] = text
                
                return matched_pattern, pattern_details
            
            return None
            
        except Exception as e:
            print(f"⚠️ サブレベルパターン解析エラー: {e}")
            return None
    
    def _find_root_word(self, sent) -> Optional[Any]:
        """ROOT語検出"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _match_sublevel_pattern(self, sent, root_word) -> Optional[str]:
        """Pure Stanza V3.1完全抽出: サブレベル専用パターンマッチング"""
        relations = {word.deprel: word for word in sent.words}
        root_pos = root_word.pos
        
        # === 1. 完全5文型判定（関係節・従属節） ===
        if 'nsubj' in relations and root_pos == 'VERB':
            # 関係代名詞節判定
            if 'mark' in relations:
                mark_word = relations['mark'].text.lower()
                if mark_word in self.relative_pronouns:
                    if 'obj' in relations and 'iobj' in relations:
                        return "SUB_SVOO"  # 関係節内の第4文型
                    elif 'obj' in relations and 'xcomp' in relations:
                        return "SUB_SVOC"  # 関係節内の第5文型
                    elif 'obj' in relations:
                        return "SUB_SVO"   # 関係節内の第3文型
                    else:
                        return "SUB_SV"    # 関係節内の第1文型
            
            # 従属節判定
            elif 'mark' in relations:
                mark_word = relations['mark'].text.lower()
                if mark_word in self.subordinate_conjunctions:
                    return "ADV_CLAUSE"  # 副詞節
            
            # 通常のサブレベル5文型
            elif 'obj' in relations and 'iobj' in relations:
                return "SUB_SVOO"
            elif 'obj' in relations and 'xcomp' in relations:
                return "SUB_SVOC"
            elif 'obj' in relations:
                return "SUB_SVO"
            else:
                return "SUB_SV"
        
        # === 2. SVC系（関係節対応） ===
        if 'nsubj' in relations and 'cop' in relations:
            return "SUB_SVC"
        
        # === 3. 前置詞句判定 ===
        if 'case' in relations and root_pos == 'NOUN':
            case_word = relations['case'].text.lower()
            if case_word in ['than', 'as']:  # 比較構文
                return "COMPARATIVE"
            else:
                return "PREP_PHRASE"
        
        # === 4. 関係代名詞特殊形（主語省略） ===
        if root_pos == 'VERB' and 'nsubj' not in relations:
            # "who runs" のような関係代名詞が主語の場合
            return "REL_SUBJ"
        
        # === 5. 分詞構文判定 ===
        if root_pos == 'VERB' and root_word.text.endswith(('ing', 'ed', 'en')):
            return "PARTICIPLE"
        
        # パターン未検出
        return None
    
    def extract_sublevel_slots(self, text: str, pattern_type: str = None) -> Dict[str, str]:
        """
        サブレベルスロット抽出（Pure Stanza V3.1準拠）
        
        Args:
            text: 抽出対象テキスト
            pattern_type: 指定されたパターンタイプ（オプション）
            
        Returns:
            サブレベルスロット辞書
        """
        # パターンタイプが指定されている場合はそれを使用、なければ分析
        if pattern_type:
            pattern_result = (pattern_type, self.sublevel_patterns.get(pattern_type, {}))
        else:
            pattern_result = self.analyze_sublevel_pattern(text)
        
        if not pattern_result:
            return {}
        
        pattern_name, pattern_details = pattern_result
        
        try:
            # Stanza再解析（スロット抽出用）
            doc = self.nlp(text)
            sent = doc.sentences[0]
            
            slots = {}
            
            # パターンのマッピングに基づいてスロット抽出
            mapping = pattern_details.get('mapping', {})
            relations = {word.deprel: word for word in sent.words}
            
            for dep_rel, slot in mapping.items():
                if dep_rel in relations:
                    word = relations[dep_rel]
                    slots[slot] = word.text
            
            # サブレベル専用修飾語処理
            self._process_sublevel_modifiers(sent, slots)
            
            return slots
            
        except Exception as e:
            print(f"⚠️ サブレベルスロット抽出エラー: {e}")
            return {}
    
    def _process_sublevel_modifiers(self, sent, slots: Dict[str, str]):
        """サブレベル専用修飾語処理"""
        for word in sent.words:
            if word.deprel in self.sublevel_modifiers:
                slot = self.sublevel_modifiers[word.deprel]
                
                # 既存スロットとの重複回避
                if slot not in slots:
                    slots[slot] = word.text
                elif slot.startswith('M'):  # 修飾語は結合可能
                    slots[slot] += f" {word.text}"
    
    def is_complex_structure(self, text: str) -> bool:
        """複雑構造（サブレベル処理対象）判定"""
        if not self.nlp:
            return False
        
        try:
            doc = self.nlp(text)
            sent = doc.sentences[0]
            
            # 複雑構造の判定条件
            has_relative = any(w.deprel == 'acl:relcl' for w in sent.words)
            has_subordinate = any(w.deprel == 'mark' for w in sent.words)
            has_multiple_verbs = len([w for w in sent.words if w.pos == 'VERB']) > 1
            
            return has_relative or has_subordinate or has_multiple_verbs
            
        except Exception as e:
            return False
    
    def get_sublevel_patterns(self) -> List[str]:
        """利用可能なサブレベルパターン一覧取得"""
        return list(self.sublevel_patterns.keys())
    
    def get_pattern_description(self, pattern_name: str) -> str:
        """パターン説明取得"""
        pattern = self.sublevel_patterns.get(pattern_name, {})
        return pattern.get('description', 'Unknown pattern')

if __name__ == "__main__":
    # テスト実行
    print("🧪 サブレベルパターンライブラリテスト")
    
    lib = SublevelPatternLib()
    
    test_cases = [
        "who runs fast",           # REL_SUBJ
        "that he bought",          # REL_OBJ  
        "because she was tired",   # ADV_CLAUSE
        "running quickly",         # PARTICIPLE
        "in the garden"           # PREP_PHRASE
    ]
    
    for text in test_cases:
        result = lib.analyze_sublevel_pattern(text)
        if result:
            pattern, details = result
            print(f"'{text}' → {pattern}: {details['description']}")
        else:
            print(f"'{text}' → No pattern detected")
