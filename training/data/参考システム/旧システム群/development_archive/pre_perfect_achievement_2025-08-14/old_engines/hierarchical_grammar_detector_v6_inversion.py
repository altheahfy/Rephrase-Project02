#!/usr/bin/env python3
"""
Phase 1: 倒置構文検出システム実装
V5.1 Universal Systemに倒置構文検出機能を追加

倒置パターン:
1. 否定副詞倒置: Never have I seen...
2. 条件節倒置: Had I known...
3. Only倒置: Only then did I...
4. 頻度副詞倒置: Rarely do we...
5. So/Neither倒置: So do I...
"""

import spacy
import stanza
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from hierarchical_grammar_detector_v5_1 import UniversalHierarchicalDetector, UniversalHierarchicalResult

class InversionType(Enum):
    """倒置構文の種類"""
    NEGATIVE_INVERSION = "negative_inversion"        # Never have I seen...
    CONDITIONAL_INVERSION = "conditional_inversion"  # Had I known...
    ONLY_INVERSION = "only_inversion"               # Only then did I...
    ADVERBIAL_INVERSION = "adverbial_inversion"     # Rarely do we...
    SO_NEITHER_INVERSION = "so_neither_inversion"   # So do I, Neither can he...
    EMPHATIC_INVERSION = "emphatic_inversion"       # Down came the rain...
    NORMAL_ORDER = "normal_order"                   # 通常語順

@dataclass
class InversionAnalysis:
    """倒置構造分析結果"""
    inversion_type: InversionType
    trigger_word: str           # 倒置を引き起こす語
    auxiliary_verb: str         # 助動詞
    subject: str                # 主語
    main_verb: str             # 主動詞
    confidence: float           # 確信度
    original_order: str         # 元の語順推定
    explanation: str            # 倒置の説明

class InversionDetector:
    """倒置構文検出エンジン"""
    
    def __init__(self):
        print("🔧 Inversion Detector 初期化中...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # 倒置トリガー語彙
        self.inversion_triggers = {
            InversionType.NEGATIVE_INVERSION: {
                'triggers': ['never', 'rarely', 'seldom', 'hardly', 'scarcely', 'barely', 'little', 'nowhere', 'not once', 'at no time'],
                'pattern': r'^(Never|Rarely|Seldom|Hardly|Scarcely|Barely|Little|Nowhere)\s+(have|has|had|do|does|did|will|would|can|could|should|shall|may|might)\s+',
                'confidence_base': 0.9
            },
            
            InversionType.CONDITIONAL_INVERSION: {
                'triggers': ['had', 'were', 'should', 'could', 'would'],
                'pattern': r'^(Had|Were|Should|Could|Would)\s+[A-Z][a-z]*\s+',
                'confidence_base': 0.95
            },
            
            InversionType.ONLY_INVERSION: {
                'triggers': ['only'],
                'pattern': r'^Only\s+(then|when|after|before|if|by|through|in|with)\s+.*(do|does|did|have|has|had|can|could|will|would|should|may|might)',
                'confidence_base': 0.88
            },
            
            InversionType.ADVERBIAL_INVERSION: {
                'triggers': ['here', 'there', 'now', 'then', 'thus', 'so'],
                'pattern': r'^(Here|There|Now|Then|Thus|So)\s+(comes?|goes?|stands?|sits?|lies?|runs?)\s+',
                'confidence_base': 0.85
            },
            
            InversionType.SO_NEITHER_INVERSION: {
                'triggers': ['so', 'neither', 'nor'],
                'pattern': r'^(So|Neither|Nor)\s+(do|does|did|have|has|had|can|could|will|would|should|am|is|are|was|were)\s+',
                'confidence_base': 0.92
            },
            
            InversionType.EMPHATIC_INVERSION: {
                'triggers': ['down', 'up', 'out', 'in', 'away', 'off'],
                'pattern': r'^(Down|Up|Out|In|Away|Off)\s+(comes?|goes?|runs?|flies?|falls?)\s+',
                'confidence_base': 0.80
            }
        }
    
    def detect_inversion(self, sentence: str) -> InversionAnalysis:
        """倒置構造を検出"""
        doc = self.nlp(sentence)
        
        # 各倒置タイプをチェック
        for inversion_type, config in self.inversion_triggers.items():
            analysis = self._check_inversion_type(sentence, doc, inversion_type, config)
            if analysis.confidence > 0.5:
                return analysis
        
        # 通常語順
        return InversionAnalysis(
            inversion_type=InversionType.NORMAL_ORDER,
            trigger_word="",
            auxiliary_verb="",
            subject="",
            main_verb="",
            confidence=0.0,
            original_order=sentence,
            explanation="Normal word order detected"
        )
    
    def _check_inversion_type(self, sentence: str, doc, inversion_type: InversionType, config: Dict) -> InversionAnalysis:
        """特定の倒置タイプをチェック"""
        words = sentence.split()
        if len(words) < 3:
            return self._create_empty_analysis()
        
        first_word = words[0].lower()
        trigger_words = config['triggers']
        
        # トリガー語チェック
        if not any(first_word.startswith(trigger.lower()) for trigger in trigger_words):
            return self._create_empty_analysis()
        
        # パターン別詳細解析
        if inversion_type == InversionType.NEGATIVE_INVERSION:
            return self._analyze_negative_inversion(sentence, doc, config)
        
        elif inversion_type == InversionType.CONDITIONAL_INVERSION:
            return self._analyze_conditional_inversion(sentence, doc, config)
        
        elif inversion_type == InversionType.ONLY_INVERSION:
            return self._analyze_only_inversion(sentence, doc, config)
        
        elif inversion_type == InversionType.SO_NEITHER_INVERSION:
            return self._analyze_so_neither_inversion(sentence, doc, config)
        
        elif inversion_type == InversionType.ADVERBIAL_INVERSION:
            return self._analyze_adverbial_inversion(sentence, doc, config)
        
        elif inversion_type == InversionType.EMPHATIC_INVERSION:
            return self._analyze_emphatic_inversion(sentence, doc, config)
        
        return self._create_empty_analysis()
    
    def _analyze_negative_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """否定副詞倒置分析"""
        words = sentence.split()
        
        if len(words) < 4:
            return self._create_empty_analysis()
        
        trigger = words[0]  # Never, Rarely, etc.
        potential_aux = words[1]  # have, do, can, etc.
        potential_subject = words[2]  # I, you, we, etc.
        
        # 助動詞チェック
        aux_verbs = {'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'could', 'should', 'shall', 'may', 'might', 'am', 'is', 'are', 'was', 'were'}
        
        if potential_aux.lower() not in aux_verbs:
            return self._create_empty_analysis()
        
        # 主語チェック（代名詞または名詞）
        subject_tokens = [token for token in doc if token.text.lower() == potential_subject.lower()]
        if not subject_tokens or subject_tokens[0].pos_ not in ['PRON', 'NOUN', 'PROPN']:
            return self._create_empty_analysis()
        
        # 主動詞を探す
        main_verb = ""
        for i in range(3, len(words)):
            token = doc[min(i, len(doc)-1)]
            if token.pos_ == 'VERB':
                main_verb = token.text
                break
        
        # 元の語順を推定
        if potential_aux.lower() in ['have', 'has', 'had']:
            original_order = f"{potential_subject} {potential_aux} {trigger.lower()} {' '.join(words[3:])}"
        else:
            original_order = f"{potential_subject} {potential_aux} not {' '.join(words[3:])}"
        
        return InversionAnalysis(
            inversion_type=InversionType.NEGATIVE_INVERSION,
            trigger_word=trigger,
            auxiliary_verb=potential_aux,
            subject=potential_subject,
            main_verb=main_verb,
            confidence=config['confidence_base'],
            original_order=original_order,
            explanation=f"Negative adverb '{trigger}' triggers subject-auxiliary inversion"
        )
    
    def _analyze_conditional_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """条件節倒置分析"""
        words = sentence.split()
        
        if len(words) < 3:
            return self._create_empty_analysis()
        
        aux_verb = words[0]  # Had, Were, Should, etc.
        subject = words[1]   # I, you, he, etc.
        
        # 条件節助動詞チェック
        conditional_aux = {'had', 'were', 'should', 'could', 'would'}
        if aux_verb.lower() not in conditional_aux:
            return self._create_empty_analysis()
        
        # 主動詞を探す
        main_verb = ""
        for token in doc:
            if token.pos_ == 'VERB' and token.text.lower() != aux_verb.lower():
                main_verb = token.text
                break
        
        # 元の語順推定
        if aux_verb.lower() == 'had':
            original_order = f"If {subject} had {' '.join(words[2:])}"
        elif aux_verb.lower() == 'were':
            original_order = f"If {subject} were {' '.join(words[2:])}"
        else:  # should, could, would
            original_order = f"If {subject} {aux_verb.lower()} {' '.join(words[2:])}"
        
        return InversionAnalysis(
            inversion_type=InversionType.CONDITIONAL_INVERSION,
            trigger_word=aux_verb,
            auxiliary_verb=aux_verb,
            subject=subject,
            main_verb=main_verb,
            confidence=config['confidence_base'],
            original_order=original_order,
            explanation=f"Conditional clause inversion with '{aux_verb}' (= 'If {subject} {aux_verb.lower()}...')"
        )
    
    def _analyze_only_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """Only倒置分析"""
        words = sentence.split()
        
        # "Only then did I realize..." パターン
        only_adverbials = ['then', 'when', 'after', 'before', 'if', 'by', 'through', 'in', 'with', 'recently', 'yesterday']
        
        if len(words) < 4 or words[0].lower() != 'only':
            return self._create_empty_analysis()
        
        # Only + adverbial を探す
        adverbial_phrase = []
        inversion_start = -1
        
        for i in range(1, len(words)):
            if words[i].lower() in ['do', 'does', 'did', 'have', 'has', 'had', 'can', 'could', 'will', 'would', 'should']:
                inversion_start = i
                break
            adverbial_phrase.append(words[i])
        
        if inversion_start == -1:
            return self._create_empty_analysis()
        
        aux_verb = words[inversion_start]
        subject = words[inversion_start + 1] if inversion_start + 1 < len(words) else ""
        
        # 元の語順推定
        adverbial_part = ' '.join(adverbial_phrase)
        remaining_part = ' '.join(words[inversion_start + 2:])
        original_order = f"{subject} {aux_verb} {remaining_part} only {adverbial_part}"
        
        return InversionAnalysis(
            inversion_type=InversionType.ONLY_INVERSION,
            trigger_word="only " + adverbial_part,
            auxiliary_verb=aux_verb,
            subject=subject,
            main_verb="",
            confidence=config['confidence_base'],
            original_order=original_order,
            explanation=f"'Only {adverbial_part}' at sentence beginning triggers inversion"
        )
    
    def _analyze_so_neither_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """So/Neither倒置分析"""
        words = sentence.split()
        
        if len(words) < 3:
            return self._create_empty_analysis()
        
        trigger = words[0]     # So, Neither, Nor
        aux_verb = words[1]    # do, can, will, etc.
        subject = words[2]     # I, you, he, etc.
        
        # 元の語順推定
        if trigger.lower() == 'so':
            original_order = f"{subject} {aux_verb} too"
        else:  # Neither, Nor
            original_order = f"{subject} {aux_verb} not either"
        
        return InversionAnalysis(
            inversion_type=InversionType.SO_NEITHER_INVERSION,
            trigger_word=trigger,
            auxiliary_verb=aux_verb,
            subject=subject,
            main_verb="",
            confidence=config['confidence_base'],
            original_order=original_order,
            explanation=f"'{trigger}' triggers auxiliary-subject inversion for agreement/disagreement"
        )
    
    def _analyze_adverbial_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """副詞倒置分析"""
        words = sentence.split()
        
        if len(words) < 3:
            return self._create_empty_analysis()
        
        trigger = words[0]    # Here, There, Down, etc.
        verb = words[1]       # comes, goes, runs, etc.
        subject = words[2]    # the bus, John, etc.
        
        original_order = f"{subject} {verb} {trigger.lower()}"
        
        return InversionAnalysis(
            inversion_type=InversionType.ADVERBIAL_INVERSION,
            trigger_word=trigger,
            auxiliary_verb="",
            subject=subject,
            main_verb=verb,
            confidence=config['confidence_base'],
            original_order=original_order,
            explanation=f"Adverb '{trigger}' fronted for emphasis, causing subject-verb inversion"
        )
    
    def _analyze_emphatic_inversion(self, sentence: str, doc, config: Dict) -> InversionAnalysis:
        """強調倒置分析"""
        return self._analyze_adverbial_inversion(sentence, doc, config)  # 同じロジック
    
    def _create_empty_analysis(self) -> InversionAnalysis:
        """空の分析結果"""
        return InversionAnalysis(
            inversion_type=InversionType.NORMAL_ORDER,
            trigger_word="",
            auxiliary_verb="",
            subject="",
            main_verb="",
            confidence=0.0,
            original_order="",
            explanation=""
        )

class HierarchicalGrammarDetectorV6(UniversalHierarchicalDetector):
    """V6: 倒置構文検出機能付き階層文法検出システム"""
    
    def __init__(self):
        super().__init__()
        self.inversion_detector = InversionDetector()
        print("✅ V6: Inversion detection capability added")
    
    def detect_comprehensive_grammar(self, sentence: str) -> Dict[str, Any]:
        """包括的文法検出（倒置構文を含む）"""
        # Step 1: 基本的な階層検出（V5.1）
        v5_result = self.detect_universal_hierarchical_grammar(sentence)
        
        # Step 2: 倒置構文検出
        inversion_analysis = self.inversion_detector.detect_inversion(sentence)
        
        # Step 3: 結果統合
        result = {
            'sentence': sentence,
            'main_pattern': v5_result.main_pattern,
            'clauses': [
                {
                    'text': clause.text,
                    'type': clause.clause_type,
                    'internal_pattern': clause.internal_pattern
                }
                for clause in v5_result.clauses
            ],
            'inversion': {
                'type': inversion_analysis.inversion_type.value,
                'trigger_word': inversion_analysis.trigger_word,
                'auxiliary_verb': inversion_analysis.auxiliary_verb,
                'subject': inversion_analysis.subject,
                'main_verb': inversion_analysis.main_verb,
                'confidence': inversion_analysis.confidence,
                'original_order': inversion_analysis.original_order,
                'explanation': inversion_analysis.explanation
            },
            'complexity_enhanced': inversion_analysis.confidence > 0.5,
            'total_grammar_elements': len(v5_result.clauses) + (1 if inversion_analysis.confidence > 0.5 else 0)
        }
        
        return result

def test_inversion_detection():
    """倒置構文検出テスト"""
    detector = HierarchicalGrammarDetectorV6()
    
    test_sentences = [
        "Never have I seen such a beautiful sunset.",
        "Little did I know what would happen.",
        "Had I known earlier, I would have acted.",
        "Rarely do we see such dedication.",
        "Only then did I realize the truth.",
        "So do I agree with your opinion.",
        "Neither can he solve this problem.",
        "Down came the heavy rain.",
        "Here comes the bus.",
        "I think that he is smart.",  # 通常語順（比較用）
        "She is reading a book.",     # 通常語順（比較用）
    ]
    
    print("🧪 倒置構文検出テスト")
    print("=" * 80)
    
    for sentence in test_sentences:
        print(f"\n🔍 分析: {sentence}")
        result = detector.detect_comprehensive_grammar(sentence)
        
        print(f"   📊 基本パターン: {result['main_pattern']}")
        print(f"   📊 節数: {len(result['clauses'])}")
        
        inversion = result['inversion']
        if inversion['confidence'] > 0.5:
            print(f"   🔄 倒置タイプ: {inversion['type']}")
            print(f"   🎯 トリガー語: {inversion['trigger_word']}")
            print(f"   💡 説明: {inversion['explanation']}")
            print(f"   🔄 元の語順: {inversion['original_order']}")
            print(f"   📈 確信度: {inversion['confidence']:.2f}")
        else:
            print(f"   ✅ 通常語順")
        
        print(f"   🌟 複雑度向上: {'Yes' if result['complexity_enhanced'] else 'No'}")

if __name__ == "__main__":
    test_inversion_detection()
