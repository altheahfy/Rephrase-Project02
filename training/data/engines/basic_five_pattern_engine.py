#!/usr/bin/env python3
"""
Basic Five Pattern Engine - Lightweight Integrated Version
Pure Stanza Engine V3.1から抽出した知識ベースによる軽量基本5文型エンジン

Features:
1. Pure Stanza Engine V3.1の知識ベースを継承
2. Grammar Master Controller統合仕様準拠
3. ハードコーディング排除（知識ベース駆動）
4. 基本5文型 + 助動詞構文に特化
"""

import stanza
from typing import Dict, List, Optional, Any
import time

class BasicFivePatternEngine:
    """基本5文型エンジン（統合型軽量版）"""
    
    def __init__(self):
        """統合仕様対応の軽量5文型エンジン初期化"""
        print("🚀 Basic Five Pattern Engine 初期化中...")
        
        # Stanza NLP パイプライン
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # Pure Stanza Engine V3.1から抽出した知識ベース
        self.sentence_patterns = self._load_sentence_patterns()
        self.modifier_mappings = self._load_modifier_mappings()
        
        self.name = "BasicFivePatternEngine"
        self.version = "1.0"
        
        print("✅ 基本5文型エンジン準備完了")
    
    def _load_sentence_patterns(self) -> Dict[str, Any]:
        """Pure Stanza Engine V3.1から抽出：基本文型パターン"""
        return {
            # 基本5文型（優先度を調整）
            "SVOO": {
                "required_relations": ["nsubj", "iobj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "iobj": "O1", "obj": "O2", "root": "V"},
                "priority": 1  # 最高優先度（最も具体的）
            },
            "SVOC": {
                "required_relations": ["nsubj", "obj", "xcomp", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "xcomp": "C2", "root": "V"},
                "priority": 2
            },
            "SVO": {
                "required_relations": ["nsubj", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "obj": "O1", "root": "V"},
                "priority": 3
            },
            "SVC": {
                "required_relations": ["nsubj", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"},
                "priority": 4
            },
            "SV": {
                "required_relations": ["nsubj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "root": "V"},
                "priority": 5  # 最も汎用的なので低優先度
            },
            
            # 助動詞構文（Pure Stanza Engine V3.1から継承）
            "S_AUX_VO": {
                "required_relations": ["nsubj", "aux", "obj", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "aux": "Aux", "obj": "O1", "root": "V"},
                "priority": 6
            },
            "S_AUX_VC": {
                "required_relations": ["nsubj", "aux", "cop", "root"],
                "root_pos": ["ADJ", "NOUN"],
                "mapping": {"nsubj": "S", "aux": "Aux", "cop": "V", "root": "C1"},
                "priority": 7
            },
            "S_AUX_V": {
                "required_relations": ["nsubj", "aux", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj": "S", "aux": "Aux", "root": "V"},
                "priority": 8
            },
            
            # 受動態パターン
            "PASSIVE": {
                "required_relations": ["nsubj:pass", "aux:pass", "root"],
                "root_pos": ["VERB"],
                "mapping": {"nsubj:pass": "S", "aux:pass": "Aux", "root": "V"},
                "priority": 9
            }
        }
    
    def _load_modifier_mappings(self) -> Dict[str, str]:
        """Pure Stanza Engine V3.1から抽出：修飾語マッピング（基本5文型に特化）"""
        return {
            # 基本修飾語（文型構造に関わるもののみ）
            "advmod": "M2",     # 副詞修飾語（quickly, hard, etc.）
            "nmod": "M1",       # 名詞修飾語
            "obl": "M3",        # 斜格語（前置詞句など）
            "tmod": "M3",       # 時間修飾
            "neg": "M3",        # 否定
            
            # 除外する修飾語（他エンジンの役割）
            # "det": 冠詞・限定詞は基本5文型では扱わない
            # "case": 前置詞は前置詞句エンジンの役割
            # "aux": 助動詞はモーダルエンジンの役割
            # "agent": 動作主は受動態エンジンの役割
        }
    
    def process_sentence(self, sentence: str) -> Optional[Dict]:
        """統合仕様準拠のメイン処理メソッド"""
        if not sentence or len(sentence.strip()) < 2:
            return None
        
        start_time = time.time()
        
        try:
            # Stanza解析
            doc = self.nlp(sentence)
            sent = doc.sentences[0]
            
            # 基本5文型の検出と処理
            result = self._analyze_basic_patterns(sent)
            
            if result:
                processing_time = time.time() - start_time
                return {
                    "engine": self.name,
                    "version": self.version,
                    "pattern": result["pattern"],
                    "slots": result["slots"],
                    "confidence": result["confidence"],
                    "processing_time": processing_time,
                    "processed": True
                }
                
        except Exception as e:
            print(f"⚠️ Basic Pattern Engine Error: {e}")
            return None
        
        return None
    
    def _analyze_basic_patterns(self, sent) -> Optional[Dict]:
        """知識ベース駆動の基本文型解析"""
        
        # ROOT語検出
        root_word = self._find_root_word(sent)
        if not root_word:
            return None
        
        # 依存関係マップ構築
        dep_relations = {}
        for word in sent.words:
            if word.deprel not in dep_relations:
                dep_relations[word.deprel] = []
            dep_relations[word.deprel].append(word)
        
        # パターンマッチング（優先度順）
        for pattern_name, pattern_info in sorted(
            self.sentence_patterns.items(), 
            key=lambda x: x[1]["priority"]
        ):
            if self._matches_pattern(pattern_info, dep_relations, root_word):
                slots = self._build_slots(pattern_info, dep_relations, sent)
                if slots:
                    return {
                        "pattern": pattern_name,
                        "slots": slots,
                        "confidence": self._calculate_confidence(pattern_name, slots)
                    }
        
        return None
    
    def _matches_pattern(self, pattern_info: Dict, dep_relations: Dict, root_word) -> bool:
        """パターンマッチング判定"""
        # 必要な依存関係の存在確認
        required_relations = pattern_info["required_relations"]
        for rel in required_relations:
            if rel not in dep_relations:
                return False
        
        # ROOT語の品詞チェック
        root_pos_allowed = pattern_info["root_pos"]
        if root_word.pos not in root_pos_allowed:
            return False
        
        return True
    
    def _build_slots(self, pattern_info: Dict, dep_relations: Dict, sent) -> Dict[str, str]:
        """スロット構築（知識ベース駆動）"""
        slots = {}
        mapping = pattern_info["mapping"]
        
        # メインスロット構築
        for dep_rel, slot in mapping.items():
            if dep_rel in dep_relations:
                words = dep_relations[dep_rel]
                if words:
                    # 複数の語がある場合は最初の語を使用
                    target_word = words[0]
                    # 語句境界の拡張
                    expanded_text = self._expand_phrase_boundary(target_word, sent)
                    slots[slot] = expanded_text
            elif dep_rel == "root":
                # ROOT語の処理
                root_word = self._find_root_word(sent)
                if root_word and slot in ["V"]:
                    slots[slot] = root_word.text
        
        # 修飾語の処理
        modifier_slots = {"M1": [], "M2": [], "M3": []}
        for word in sent.words:
            if word.deprel in self.modifier_mappings:
                slot = self.modifier_mappings[word.deprel]
                if slot.startswith("M"):  # M1, M2, M3スロット
                    expanded_text = self._expand_phrase_boundary(word, sent)
                    if expanded_text not in modifier_slots[slot]:
                        modifier_slots[slot].append(expanded_text)
        
        # 修飾語スロットを統合
        for slot, values in modifier_slots.items():
            if values:
                slots[slot] = ", ".join(values)
        
        return slots
    
    def _find_root_word(self, sent):
        """ROOT語検出"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _expand_phrase_boundary(self, word, sent) -> str:
        """基本5文型に適した語句境界拡張"""
        # 語句境界拡張の依存関係（基本文型構造に必要なもののみ）
        expand_deps = ['compound', 'amod', 'nummod']  # 複合語、形容詞、数量詞のみ
        
        words_to_include = [word]
        
        # 子要素の探索
        for other_word in sent.words:
            if (other_word.head == word.id and 
                other_word.deprel in expand_deps):
                words_to_include.append(other_word)
        
        # 冠詞・限定詞は基本文型では含める（スロットには設定しない）
        for other_word in sent.words:
            if (other_word.head == word.id and 
                other_word.deprel == 'det'):
                words_to_include.append(other_word)
        
        # 位置順でソート
        words_to_include.sort(key=lambda w: w.id)
        
        return " ".join([w.text for w in words_to_include])
    
    def _calculate_confidence(self, pattern_name: str, slots: Dict) -> float:
        """信頼度計算"""
        base_confidence = 0.85
        
        # スロット数によるボーナス
        slot_bonus = len(slots) * 0.02
        
        # パターン固有のボーナス
        pattern_bonus = {
            "SVO": 0.05,    # 最も一般的
            "SV": 0.03,     # シンプル
            "SVC": 0.04,    # 明確な構造
            "SVOO": 0.08,   # 複雑だが明確
            "SVOC": 0.06    # 複雑構造
        }.get(pattern_name, 0.0)
        
        confidence = min(0.98, base_confidence + slot_bonus + pattern_bonus)
        return confidence

def test_basic_five_pattern_engine():
    """テスト関数"""
    engine = BasicFivePatternEngine()
    
    test_sentences = [
        "I love programming.",
        "She is a teacher.",
        "He gave her a book.",
        "We consider him smart.",
        "The dog runs quickly.",
        "I can speak English.",
        "They are working hard.",
        "The book was written by John."
    ]
    
    print("\n🧪 Testing Basic Five Pattern Engine")
    print("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n✅ Test {i}: {sentence}")
        result = engine.process_sentence(sentence)
        if result:
            print(f"    Pattern: {result['pattern']}")
            print(f"    Slots: {result['slots']}")
            print(f"    Confidence: {result['confidence']:.3f}")
        else:
            print("    ❌ No pattern detected")

if __name__ == "__main__":
    test_basic_five_pattern_engine()
