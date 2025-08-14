#!/usr/bin/env python3
"""
Direct Rephrase Slot Decomposition System
統合文法検出システムから直接Rephraseスロット分解を実行

従来のアプローチ:
文章 → 文法抽出 → マスター → エンジン招集 → スロット分解

新アプローチ:
文章 → 統合検出 → 直接スロット分解

利点:
1. 処理速度大幅向上
2. 精度向上（中間変換の誤差除去）
3. メンテナンス性向上（システム統合）
4. リアルタイム処理可能
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import spacy

# 既存システムのインポート
from hierarchical_grammar_detector_v5_1 import UniversalHierarchicalDetector
from hierarchical_grammar_detector_v6_inversion import InversionDetector, InversionType

@dataclass
class RephraseSlot:
    """Rephraseスロット情報"""
    slot_id: str           # スロット識別子
    original_text: str     # 元のテキスト  
    slot_type: str         # スロットタイプ（主語、動詞、目的語など）
    rephrase_options: List[str]  # 言い換え候補
    grammar_role: str      # 文法的役割
    complexity_level: int  # 複雑度レベル (1-5)
    dependencies: List[str] # 依存関係

@dataclass  
class RephraseDecomposition:
    """Rephrase分解結果"""
    original_sentence: str
    main_structure: str
    slots: List[RephraseSlot]
    inversion_info: Dict[str, Any]
    complexity_score: float
    total_variations: int  # 可能な組み合わせ数

class DirectRephraseDecomposer:
    """直接Rephraseスロット分解システム"""
    
    def __init__(self):
        print("🚀 Direct Rephrase Decomposer 初期化中...")
        
        # 既存システム統合
        self.hierarchical_detector = UniversalHierarchicalDetector()
        self.inversion_detector = InversionDetector()
        self.nlp = spacy.load("en_core_web_sm")
        
        # スロットタイプ定義
        self.slot_types = {
            'SUBJECT': '主語スロット',
            'VERB': '動詞スロット', 
            'OBJECT': '目的語スロット',
            'COMPLEMENT': '補語スロット',
            'ADVERBIAL': '副詞（句）スロット',
            'DETERMINER': '限定詞スロット',
            'ADJECTIVE': '形容詞スロット',
            'PREPOSITIONAL': '前置詞句スロット',
            'CLAUSE': '節スロット',
            'INVERSION_TRIGGER': '倒置トリガースロット'
        }
        
        # 言い換えパターンデータベース（簡易版）
        self.rephrase_patterns = {
            # 主語言い換え
            'SUBJECT': {
                'I': ['I', 'me', 'myself'],
                'he': ['he', 'him', 'the man', 'this person'],
                'she': ['she', 'her', 'the woman', 'this lady'],
                'they': ['they', 'them', 'these people', 'the group']
            },
            
            # 動詞言い換え
            'VERB': {
                'like': ['like', 'enjoy', 'love', 'appreciate', 'prefer'],
                'go': ['go', 'travel', 'move', 'head', 'proceed'],
                'see': ['see', 'watch', 'observe', 'notice', 'view'],
                'have': ['have', 'possess', 'own', 'hold', 'carry']
            },
            
            # 副詞言い換え
            'ADVERBIAL': {
                'quickly': ['quickly', 'fast', 'rapidly', 'swiftly', 'speedily'],
                'very': ['very', 'extremely', 'quite', 'really', 'highly'],
                'often': ['often', 'frequently', 'regularly', 'commonly', 'usually']
            }
        }
    
    def decompose_to_rephrase_slots(self, sentence: str) -> RephraseDecomposition:
        """文章を直接Rephraseスロットに分解"""
        print(f"\n🔍 直接スロット分解: {sentence}")
        
        # Step 1: 階層構造検出
        hierarchical_result = self.hierarchical_detector.detect_universal_hierarchical_grammar(sentence)
        
        # Step 2: 倒置構造検出
        inversion_result = self.inversion_detector.detect_inversion(sentence)
        
        # Step 3: spaCy詳細解析
        doc = self.nlp(sentence)
        
        # Step 4: 直接スロット生成
        slots = self._extract_rephrase_slots(doc, hierarchical_result, inversion_result)
        
        # Step 5: 複雑度計算
        complexity_score = self._calculate_complexity(slots, inversion_result)
        
        # Step 6: 組み合わせ数計算
        total_variations = self._calculate_total_variations(slots)
        
        return RephraseDecomposition(
            original_sentence=sentence,
            main_structure=hierarchical_result.main_pattern,
            slots=slots,
            inversion_info={
                'type': inversion_result.inversion_type.value,
                'confidence': inversion_result.confidence,
                'explanation': inversion_result.explanation
            },
            complexity_score=complexity_score,
            total_variations=total_variations
        )
    
    def _extract_rephrase_slots(self, doc, hierarchical_result, inversion_result) -> List[RephraseSlot]:
        """spaCy解析から直接Rephraseスロットを抽出"""
        slots = []
        slot_counter = 1
        
        # 倒置構造の場合、特別処理
        if inversion_result.confidence > 0.5:
            # 倒置トリガーをスロットとして追加
            trigger_slot = RephraseSlot(
                slot_id=f"SLOT_{slot_counter}",
                original_text=inversion_result.trigger_word,
                slot_type="INVERSION_TRIGGER",
                rephrase_options=self._get_inversion_alternatives(inversion_result),
                grammar_role="倒置トリガー",
                complexity_level=4,
                dependencies=[]
            )
            slots.append(trigger_slot)
            slot_counter += 1
        
        # 基本的な文法要素をスロット化
        for token in doc:
            if token.dep_ == 'nsubj':  # 主語
                slot = self._create_subject_slot(token, slot_counter)
                slots.append(slot)
                slot_counter += 1
            
            elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':  # 主動詞
                slot = self._create_verb_slot(token, slot_counter)
                slots.append(slot)
                slot_counter += 1
            
            elif token.dep_ in ['obj', 'dobj']:  # 目的語
                slot = self._create_object_slot(token, slot_counter)
                slots.append(slot)
                slot_counter += 1
            
            elif token.dep_ in ['acomp', 'attr']:  # 補語
                slot = self._create_complement_slot(token, slot_counter)
                slots.append(slot)
                slot_counter += 1
            
            elif token.dep_ in ['advmod'] and token.pos_ == 'ADV':  # 副詞
                slot = self._create_adverbial_slot(token, slot_counter)
                slots.append(slot)
                slot_counter += 1
        
        # 階層構造（節）をスロット化
        for clause in hierarchical_result.clauses:
            clause_slot = RephraseSlot(
                slot_id=f"SLOT_{slot_counter}",
                original_text=clause.text,
                slot_type="CLAUSE",
                rephrase_options=self._get_clause_alternatives(clause),
                grammar_role=f"{clause.clause_type}節",
                complexity_level=3,
                dependencies=[]
            )
            slots.append(clause_slot)
            slot_counter += 1
        
        return slots
    
    def _create_subject_slot(self, token, slot_id: int) -> RephraseSlot:
        """主語スロット作成"""
        subject_text = token.text
        alternatives = self.rephrase_patterns.get('SUBJECT', {}).get(subject_text.lower(), [subject_text])
        
        return RephraseSlot(
            slot_id=f"SLOT_{slot_id}",
            original_text=subject_text,
            slot_type="SUBJECT",
            rephrase_options=alternatives,
            grammar_role="主語",
            complexity_level=1,
            dependencies=[]
        )
    
    def _create_verb_slot(self, token, slot_id: int) -> RephraseSlot:
        """動詞スロット作成"""
        verb_text = token.lemma_
        alternatives = self.rephrase_patterns.get('VERB', {}).get(verb_text.lower(), [verb_text])
        
        return RephraseSlot(
            slot_id=f"SLOT_{slot_id}",
            original_text=token.text,
            slot_type="VERB", 
            rephrase_options=alternatives,
            grammar_role="動詞",
            complexity_level=2,
            dependencies=[]
        )
    
    def _create_object_slot(self, token, slot_id: int) -> RephraseSlot:
        """目的語スロット作成"""
        # 名詞句全体を取得（簡易版）
        object_phrase = self._get_noun_phrase(token)
        
        return RephraseSlot(
            slot_id=f"SLOT_{slot_id}",
            original_text=object_phrase,
            slot_type="OBJECT",
            rephrase_options=[object_phrase],  # 簡易版では同じ
            grammar_role="目的語",
            complexity_level=2,
            dependencies=[]
        )
    
    def _create_complement_slot(self, token, slot_id: int) -> RephraseSlot:
        """補語スロット作成"""
        return RephraseSlot(
            slot_id=f"SLOT_{slot_id}",
            original_text=token.text,
            slot_type="COMPLEMENT",
            rephrase_options=[token.text],
            grammar_role="補語",
            complexity_level=2,
            dependencies=[]
        )
    
    def _create_adverbial_slot(self, token, slot_id: int) -> RephraseSlot:
        """副詞スロット作成"""
        adv_text = token.text
        alternatives = self.rephrase_patterns.get('ADVERBIAL', {}).get(adv_text.lower(), [adv_text])
        
        return RephraseSlot(
            slot_id=f"SLOT_{slot_id}",
            original_text=adv_text,
            slot_type="ADVERBIAL",
            rephrase_options=alternatives,
            grammar_role="副詞",
            complexity_level=1,
            dependencies=[]
        )
    
    def _get_noun_phrase(self, token) -> str:
        """名詞句を取得（簡易版）"""
        # 修飾語を含む名詞句の構築
        phrase_tokens = [token]
        
        # 限定詞・形容詞を追加
        for child in token.children:
            if child.dep_ in ['det', 'amod']:
                phrase_tokens.insert(0, child)
        
        return ' '.join([t.text for t in phrase_tokens])
    
    def _get_inversion_alternatives(self, inversion_result) -> List[str]:
        """倒置構造の代替表現"""
        if inversion_result.inversion_type == InversionType.NEGATIVE_INVERSION:
            return [inversion_result.trigger_word, "not once", "at no time"]
        elif inversion_result.inversion_type == InversionType.CONDITIONAL_INVERSION:
            return [inversion_result.original_order]
        else:
            return [inversion_result.trigger_word]
    
    def _get_clause_alternatives(self, clause) -> List[str]:
        """節の代替表現（簡易版）"""
        return [clause.text]  # 実際はより複雑な処理が必要
    
    def _calculate_complexity(self, slots: List[RephraseSlot], inversion_result) -> float:
        """複雑度計算"""
        base_complexity = len(slots) * 0.1
        
        # 倒置構造ボーナス
        if inversion_result.confidence > 0.5:
            base_complexity += 0.3
        
        # スロットタイプ別重み付け
        for slot in slots:
            if slot.slot_type == "CLAUSE":
                base_complexity += 0.2
            elif slot.slot_type == "INVERSION_TRIGGER":
                base_complexity += 0.3
        
        return min(base_complexity, 1.0)
    
    def _calculate_total_variations(self, slots: List[RephraseSlot]) -> int:
        """可能な組み合わせ数計算"""
        total = 1
        for slot in slots:
            total *= len(slot.rephrase_options)
        return total
    
    def print_decomposition_result(self, result: RephraseDecomposition):
        """分解結果を表示"""
        print(f"\n📊 直接スロット分解結果")
        print("=" * 60)
        print(f"🔤 元文: {result.original_sentence}")
        print(f"📋 主構造: {result.main_structure}")
        print(f"📈 複雑度: {result.complexity_score:.2f}")
        print(f"🔢 可能変化数: {result.total_variations}")
        
        if result.inversion_info['confidence'] > 0.5:
            print(f"🔄 倒置: {result.inversion_info['type']} ({result.inversion_info['confidence']:.2f})")
        
        print(f"\n📝 抽出スロット ({len(result.slots)}個):")
        for slot in result.slots:
            print(f"   {slot.slot_id}: [{slot.slot_type}] '{slot.original_text}'")
            print(f"      🔄 候補: {', '.join(slot.rephrase_options)}")
            print(f"      📊 複雑度: {slot.complexity_level}")

def test_direct_decomposition():
    """直接分解システムのテスト"""
    decomposer = DirectRephraseDecomposer()
    
    test_sentences = [
        "I like music.",
        "Never have I seen such beauty.",
        "She gave me a book that was interesting.",
        "The student who studies hard will succeed.",
        "Had I known, I would have come earlier."
    ]
    
    print("🧪 直接Rephraseスロット分解テスト")
    print("=" * 80)
    
    for sentence in test_sentences:
        result = decomposer.decompose_to_rephrase_slots(sentence)
        decomposer.print_decomposition_result(result)

if __name__ == "__main__":
    test_direct_decomposition()
