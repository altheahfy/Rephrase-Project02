"""
🔍 Phase 4: Advanced Structures Detection System
高度構文検出システム - 省略・外置・比較・存在構文

進捗: Phase 1(倒置)✓, Phase 2(時制-アスペクト:100%)✓, Phase 3(強調:100%)✓
Phase 4: 高度構文パターン検出
"""

import spacy
import re
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

class AdvancedStructureType(Enum):
    """高度構文タイプ"""
    ELLIPSIS = "ellipsis"                    # 省略構文
    EXTRAPOSITION = "extraposition"          # 外置構文  
    COMPARATIVE = "comparative"              # 比較構文
    EXISTENTIAL = "existential"             # 存在構文
    CONDITIONAL = "conditional"             # 条件構文
    CONCESSIVE = "concessive"               # 譲歩構文
    CORRELATIVE = "correlative"             # 相関構文
    PARTICIPLE_ABSOLUTE = "participle_absolute"  # 分詞構文
    NO_ADVANCED = "no_advanced"

@dataclass
class AdvancedStructureAnalysis:
    """高度構文分析結果"""
    structure_type: AdvancedStructureType
    main_pattern: str
    sub_patterns: List[str]
    reconstructed_form: str
    confidence: float
    components: Dict[str, str]
    explanation: str
    complexity_level: int

class AdvancedStructuresDetector:
    """高度構文検出器"""
    
    def __init__(self):
        print("🔍 Advanced Structures Detector 初期化中...")
        
        # spaCyモデル初期化
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("❌ spaCy英語モデルが見つかりません")
            self.nlp = None
        
        # 省略パターン
        self.ellipsis_patterns = {
            'verb_phrase_ellipsis': [
                r'.*can\s+(\w+),\s*and\s+(\w+)\s+can\s+too.*',  # "John can sing, and Mary can too"
                r'.*will\s+(\w+),\s*and\s+(\w+)\s+will\s+too.*',
                r'.*(\w+)\s+did,\s*and\s+(\w+)\s+did\s+too.*'
            ],
            'noun_phrase_ellipsis': [
                r'.*\b(some|many|few|several)\s+(\w+).*',  # "I bought some books, she bought some too"
                r'.*\b(red|blue|big|small)\s+(one|ones).*'  # "I like the red one"
            ],
            'comparative_ellipsis': [
                r'.*more\s+(\w+)\s+than.*',  # "more intelligent than [someone is]"
                r'.*as\s+(\w+)\s+as.*',      # "as tall as [someone is]"
            ]
        }
        
        # 外置パターン
        self.extraposition_patterns = {
            'it_extraposition': [
                r'^It\s+(is|was)\s+(clear|obvious|certain|important|necessary)\s+that.*',
                r'^It\s+(seems|appears|happens)\s+that.*',
                r'^It\s+(is|was)\s+(easy|hard|difficult|impossible)\s+to.*'
            ],
            'there_extraposition': [
                r'^There\s+(is|are|was|were)\s+(no\s+doubt|no\s+question)\s+that.*'
            ]
        }
        
        # 比較構文パターン
        self.comparative_patterns = {
            'comparative_degree': [
                r'.*(\w+er)\s+than.*',           # "bigger than"
                r'.*more\s+(\w+)\s+than.*',      # "more beautiful than"
                r'.*less\s+(\w+)\s+than.*'       # "less important than"
            ],
            'superlative': [
                r'.*the\s+(\w+est).*',           # "the biggest"
                r'.*the\s+most\s+(\w+).*',       # "the most beautiful"
                r'.*the\s+least\s+(\w+).*'       # "the least important"
            ],
            'equality_comparison': [
                r'.*as\s+(\w+)\s+as.*',          # "as tall as"
                r'.*the\s+same\s+(\w+)\s+as.*'   # "the same height as"
            ]
        }
        
        # 存在構文パターン
        self.existential_patterns = [
            r'^There\s+(is|are|was|were|will\s+be|has\s+been|have\s+been)\s+.*',
            r'^Here\s+(is|are|comes|come)\s+.*'
        ]
        
        # 条件構文パターン  
        self.conditional_patterns = {
            'real_conditional': [
                r'^If\s+.*,\s*.*(will|can|may|might).*',
                r'^When\s+.*,\s*.*will.*'
            ],
            'unreal_conditional': [
                r'^If\s+.*\s+(were|had|could|would|might).*',
                r'^Were\s+.*,\s*.*would.*',
                r'^Had\s+.*,\s*.*would.*'
            ],
            'mixed_conditional': [
                r'^If\s+.*had.*,\s*.*would.*now.*'
            ]
        }
        
        # 譲歩構文パターン
        self.concessive_patterns = [
            r'^(Although|Though|Even\s+though|Despite|In\s+spite\s+of)\s+.*',
            r'^(However|Nevertheless|Nonetheless)\s+.*',
            r'^.*,\s*(however|nevertheless|nonetheless).*'
        ]
        
        # 相関構文パターン
        self.correlative_patterns = [
            r'^(Both|Either|Neither|Not\s+only).*\s+(and|or|nor|but\s+also).*',
            r'^(No\s+sooner|Hardly|Scarcely).*\s+(than|when).*'
        ]

    def detect_advanced_structure(self, sentence: str) -> AdvancedStructureAnalysis:
        """高度構文検出のメイン関数"""
        if not self.nlp:
            return self._create_empty_analysis()
        
        doc = self.nlp(sentence)
        
        # 各構文タイプを順次チェック
        for structure_type in AdvancedStructureType:
            if structure_type == AdvancedStructureType.NO_ADVANCED:
                continue
                
            result = self._check_structure_type(sentence, doc, structure_type)
            if result.structure_type != AdvancedStructureType.NO_ADVANCED:
                return result
        
        return AdvancedStructureAnalysis(
            structure_type=AdvancedStructureType.NO_ADVANCED,
            main_pattern="",
            sub_patterns=[],
            reconstructed_form="",
            confidence=0.0,
            components={},
            explanation="No advanced structure detected",
            complexity_level=0
        )

    def _check_structure_type(self, sentence: str, doc, structure_type: AdvancedStructureType) -> AdvancedStructureAnalysis:
        """特定の構文タイプをチェック"""
        
        if structure_type == AdvancedStructureType.ELLIPSIS:
            return self._analyze_ellipsis(sentence, doc)
        
        elif structure_type == AdvancedStructureType.EXTRAPOSITION:
            return self._analyze_extraposition(sentence, doc)
        
        elif structure_type == AdvancedStructureType.COMPARATIVE:
            return self._analyze_comparative(sentence, doc)
        
        elif structure_type == AdvancedStructureType.EXISTENTIAL:
            return self._analyze_existential(sentence, doc)
        
        elif structure_type == AdvancedStructureType.CONDITIONAL:
            return self._analyze_conditional(sentence, doc)
        
        elif structure_type == AdvancedStructureType.CONCESSIVE:
            return self._analyze_concessive(sentence, doc)
        
        elif structure_type == AdvancedStructureType.CORRELATIVE:
            return self._analyze_correlative(sentence, doc)
        
        elif structure_type == AdvancedStructureType.PARTICIPLE_ABSOLUTE:
            return self._analyze_participle_absolute(sentence, doc)
        
        return self._create_empty_analysis()

    def _analyze_ellipsis(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """省略構文分析"""
        
        # 動詞句省略 (VP ellipsis) - より柔軟なパターン
        # "John can sing, and Mary can too" パターン
        vp_pattern1 = r'(.+?)\s+(can|could|will|would|should|must|might|may)\s+(\w+),?\s+and\s+(.+?)\s+(can|could|will|would|should|must|might|may)\s+(too|also)\.?$'
        match = re.match(vp_pattern1, sentence, re.IGNORECASE)
        if match:
            subject1 = match.group(1).strip()
            aux1 = match.group(2)
            main_verb = match.group(3)
            subject2 = match.group(4).strip()
            aux2 = match.group(5)
            
            reconstructed = f"{subject1} {aux1} {main_verb}, and {subject2} {aux2} {main_verb} too."
            
            return AdvancedStructureAnalysis(
                structure_type=AdvancedStructureType.ELLIPSIS,
                main_pattern="VP ellipsis",
                sub_patterns=["auxiliary_vp_ellipsis"],
                reconstructed_form=reconstructed,
                confidence=0.88,
                components={
                    'subject1': subject1,
                    'subject2': subject2,
                    'auxiliary': aux1,
                    'elided_vp': main_verb
                },
                explanation=f"VP ellipsis: '{main_verb}' omitted in second clause",
                complexity_level=4
            )
        
        # "I bought some books, she bought some too" パターン
        vp_pattern2 = r'(.+?)\s+(\w+)\s+(some|many|few|several)\s+(\w+),?\s+(.+?)\s+(\w+)\s+(some|many|few|several)\s+(too|also)\.?$'
        match = re.match(vp_pattern2, sentence, re.IGNORECASE)
        if match:
            subject1 = match.group(1).strip()
            verb1 = match.group(2)
            det1 = match.group(3)
            noun1 = match.group(4)
            subject2 = match.group(5).strip()
            verb2 = match.group(6)
            det2 = match.group(7)
            
            reconstructed = f"{subject1} {verb1} {det1} {noun1}, {subject2} {verb2} {det2} {noun1} too."
            
            return AdvancedStructureAnalysis(
                structure_type=AdvancedStructureType.ELLIPSIS,
                main_pattern="NP ellipsis",
                sub_patterns=["noun_ellipsis"],
                reconstructed_form=reconstructed,
                confidence=0.82,
                components={
                    'subject1': subject1,
                    'subject2': subject2,
                    'elided_noun': noun1
                },
                explanation=f"NP ellipsis: '{noun1}' omitted in second clause",
                complexity_level=3
            )
        
        # 名詞句省略 "I like the red one" パターン
        np_pattern = r'(.+?)\s+(one|ones)\s*\.?$'
        match = re.search(np_pattern, sentence, re.IGNORECASE)
        if match:
            context = match.group(1)
            pronoun = match.group(2)
            
            # 省略された名詞を推測
            elided_noun = self._extract_noun_from_context(context, pronoun)
            reconstructed = sentence.replace(pronoun, elided_noun)
            
            return AdvancedStructureAnalysis(
                structure_type=AdvancedStructureType.ELLIPSIS,
                main_pattern="NP ellipsis", 
                sub_patterns=["determiner_ellipsis"],
                reconstructed_form=reconstructed,
                confidence=0.75,
                components={
                    'context': context,
                    'pronoun': pronoun,
                    'elided_noun': elided_noun
                },
                explanation=f"NP ellipsis: noun replaced by '{pronoun}'",
                complexity_level=3
            )
        
        return self._create_empty_analysis()

    def _analyze_extraposition(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """外置構文分析"""
        
        # It外置 - より安全な正規表現
        it_patterns = [
            (r'^It\s+(is|was)\s+(clear|obvious|certain|important|necessary|true|false)\s+that\s+(.+)$', 'adjective_extraposition'),
            (r'^It\s+(seems|appears|happens)\s+that\s+(.+)$', 'verb_extraposition'),
            (r'^It\s+(is|was)\s+(easy|hard|difficult|impossible|possible)\s+to\s+(.+)$', 'infinitive_extraposition')
        ]
        
        for pattern, extrap_type in it_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                copula = match.group(1)
                
                if extrap_type == 'adjective_extraposition':
                    predicate = match.group(2)
                    that_clause = match.group(3)
                    subject_clause = that_clause.strip()
                    reconstructed = f"{subject_clause.capitalize()} is {predicate}."
                    extraposed_element = f"that {that_clause}"
                    
                elif extrap_type == 'verb_extraposition':
                    verb = sentence.split()[1]  # seems/appears/happens
                    that_clause = match.group(2)
                    reconstructed = f"{that_clause.capitalize()} {verb}."
                    extraposed_element = f"that {that_clause}"
                    predicate = verb
                    
                elif extrap_type == 'infinitive_extraposition':
                    predicate = match.group(2)
                    to_clause = match.group(3)
                    reconstructed = f"To {to_clause} is {predicate}."
                    extraposed_element = f"to {to_clause}"
                else:
                    predicate = "unknown"
                    extraposed_element = "unknown"
                    reconstructed = sentence
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.EXTRAPOSITION,
                    main_pattern="It-extraposition",
                    sub_patterns=[extrap_type],
                    reconstructed_form=reconstructed,
                    confidence=0.88,
                    components={
                        'dummy_it': 'It',
                        'copula': copula,
                        'predicate': predicate,
                        'extraposed_clause': extraposed_element
                    },
                    explanation="It-extraposition moves heavy subject to sentence-final position",
                    complexity_level=4
                )
        
        # There外置
        there_pattern = r'^There\s+(is|are|was|were)\s+(no\s+doubt|no\s+question)\s+that\s+(.+)$'
        match = re.match(there_pattern, sentence, re.IGNORECASE)
        if match:
            copula = match.group(1)
            noun_phrase = match.group(2)
            that_clause = match.group(3)
            
            return AdvancedStructureAnalysis(
                structure_type=AdvancedStructureType.EXTRAPOSITION,
                main_pattern="There-extraposition",
                sub_patterns=["there_extrap"],
                reconstructed_form=f"{noun_phrase.capitalize()} exists that {that_clause}",
                confidence=0.80,
                components={
                    'dummy_there': 'There',
                    'copula': copula,
                    'noun_phrase': noun_phrase
                },
                explanation="There-extraposition with doubt/question phrases",
                complexity_level=3
            )
        
        return self._create_empty_analysis()

    def _analyze_comparative(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """比較構文分析"""
        
        # 比較級
        for pattern in self.comparative_patterns['comparative_degree']:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                comparative_form = match.group(1)
                
                # 基本形を推定
                if comparative_form.endswith('er'):
                    base_form = comparative_form[:-2]
                else:
                    base_form = comparative_form
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.COMPARATIVE,
                    main_pattern="Comparative degree",
                    sub_patterns=["comparative"],
                    reconstructed_form=sentence,
                    confidence=0.90,
                    components={
                        'comparative_form': comparative_form,
                        'base_form': base_form,
                        'comparison_marker': 'than'
                    },
                    explanation=f"Comparative construction with '{comparative_form}'",
                    complexity_level=3
                )
        
        # 最上級
        for pattern in self.comparative_patterns['superlative']:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                superlative_form = match.group(1)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.COMPARATIVE,
                    main_pattern="Superlative degree",
                    sub_patterns=["superlative"],
                    reconstructed_form=sentence,
                    confidence=0.92,
                    components={
                        'superlative_form': superlative_form,
                        'superlative_marker': 'the'
                    },
                    explanation=f"Superlative construction with '{superlative_form}'",
                    complexity_level=3
                )
        
        # 同等比較
        for pattern in self.comparative_patterns['equality_comparison']:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                adjective = match.group(1)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.COMPARATIVE,
                    main_pattern="Equality comparison",
                    sub_patterns=["as_as_comparison"],
                    reconstructed_form=sentence,
                    confidence=0.87,
                    components={
                        'adjective': adjective,
                        'comparison_marker': 'as...as'
                    },
                    explanation=f"Equality comparison with 'as {adjective} as'",
                    complexity_level=2
                )
        
        return self._create_empty_analysis()

    def _analyze_existential(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """存在構文分析"""
        
        for pattern in self.existential_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                dummy_subject = sentence.split()[0]  # "There" or "Here"
                copula = match.group(1)
                
                # 論理主語を抽出
                words = sentence.split()
                logical_subject = ""
                for i, word in enumerate(words):
                    if word.lower() in ['is', 'are', 'was', 'were']:
                        if i + 1 < len(words):
                            logical_subject = ' '.join(words[i+1:]).rstrip('.')
                        break
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.EXISTENTIAL,
                    main_pattern="Existential there/here",
                    sub_patterns=["there_construction", "here_construction"],
                    reconstructed_form=f"{logical_subject.capitalize()} exists/is present.",
                    confidence=0.85,
                    components={
                        'dummy_subject': dummy_subject,
                        'copula': copula,
                        'logical_subject': logical_subject
                    },
                    explanation=f"Existential construction with dummy '{dummy_subject}'",
                    complexity_level=3
                )
        
        return self._create_empty_analysis()

    def _analyze_conditional(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """条件構文分析"""
        
        # 現実条件文 (Type 1)
        real_patterns = [
            r'^If\s+(.+?),\s*(.+?)\s+(will|can|may|might)\s+(.+)$',
            r'^When\s+(.+?),\s*(.+?)\s+will\s+(.+)$'
        ]
        
        for pattern in real_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                if_clause = match.group(1)
                main_subject = match.group(2)
                modal = match.group(3)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.CONDITIONAL,
                    main_pattern="Real conditional",
                    sub_patterns=["type_1_conditional"],
                    reconstructed_form=sentence,
                    confidence=0.88,
                    components={
                        'condition_marker': sentence.split()[0],
                        'if_clause': if_clause,
                        'main_clause': f"{main_subject} {modal}",
                        'modal_verb': modal
                    },
                    explanation="Real conditional (Type 1): possible future condition",
                    complexity_level=4
                )
        
        # 非現実条件文 (Type 2 & 3)
        unreal_patterns = [
            r'^If\s+(.+?)\s+(were|had|could|would|might)\s+(.+?),\s*(.+?)\s+(would|could|might)\s+(.+)$',
            r'^Were\s+(.+?)\s+(.+?),\s*(.+?)\s+would\s+(.+)$',
            r'^Had\s+(.+?)\s+(.+?),\s*(.+?)\s+would\s+(.+)$'
        ]
        
        for pattern in unreal_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                first_word = sentence.split()[0].lower()
                
                if first_word == 'if':
                    condition_subject = match.group(1)
                    subjunctive = match.group(2)
                    condition_rest = match.group(3)
                    main_clause = f"{match.group(4)} {match.group(5)} {match.group(6)}"
                elif first_word in ['were', 'had']:
                    subjunctive = first_word
                    condition_subject = match.group(1)
                    main_clause = f"{match.group(3)} would {match.group(4)}"
                else:
                    subjunctive = "unknown"
                    condition_subject = "unknown"
                    main_clause = "unknown"
                
                conditional_type = "type_3_conditional" if subjunctive == "had" else "type_2_conditional"
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.CONDITIONAL,
                    main_pattern="Unreal conditional", 
                    sub_patterns=[conditional_type],
                    reconstructed_form=sentence,
                    confidence=0.85,
                    components={
                        'condition_marker': first_word,
                        'subjunctive_marker': subjunctive,
                        'condition_subject': condition_subject,
                        'main_clause': main_clause
                    },
                    explanation="Unreal conditional: hypothetical or counterfactual condition",
                    complexity_level=5
                )
        
        # 混合条件文
        mixed_pattern = r'^If\s+(.+?)had\s+(.+?),\s*(.+?)would\s+(.+?)now(.*)$'
        match = re.match(mixed_pattern, sentence, re.IGNORECASE)
        if match:
            return AdvancedStructureAnalysis(
                structure_type=AdvancedStructureType.CONDITIONAL,
                main_pattern="Mixed conditional",
                sub_patterns=["mixed_conditional"],
                reconstructed_form=sentence,
                confidence=0.82,
                components={
                    'condition_marker': 'If',
                    'past_condition': f"{match.group(1)}had {match.group(2)}",
                    'present_result': f"{match.group(3)}would {match.group(4)}now"
                },
                explanation="Mixed conditional: past condition, present result",
                complexity_level=5
            )
        
        return self._create_empty_analysis()

    def _analyze_concessive(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """譲歩構文分析"""
        
        for pattern in self.concessive_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                concessive_marker = match.group(1)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.CONCESSIVE,
                    main_pattern="Concessive construction",
                    sub_patterns=["although_concessive", "however_concessive"],
                    reconstructed_form=sentence,
                    confidence=0.82,
                    components={
                        'concessive_marker': concessive_marker
                    },
                    explanation=f"Concessive construction with '{concessive_marker}'",
                    complexity_level=4
                )
        
        return self._create_empty_analysis()

    def _analyze_correlative(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """相関構文分析"""
        
        for pattern in self.correlative_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                first_correlative = match.group(1)
                second_correlative = match.group(2)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.CORRELATIVE,
                    main_pattern="Correlative construction",
                    sub_patterns=["both_and", "either_or", "neither_nor", "not_only_but_also"],
                    reconstructed_form=sentence,
                    confidence=0.88,
                    components={
                        'first_correlative': first_correlative,
                        'second_correlative': second_correlative
                    },
                    explanation=f"Correlative construction: '{first_correlative}...{second_correlative}'",
                    complexity_level=4
                )
        
        return self._create_empty_analysis()

    def _analyze_participle_absolute(self, sentence: str, doc) -> AdvancedStructureAnalysis:
        """分詞構文分析"""
        
        # 分詞構文のパターン検出
        participle_patterns = [
            r'^(Having|Being|Done|Finished|Completed)\s+.*,\s*.*',  # Having done..., he...
            r'^.*,\s+(being|having|done|finished)\s+.*',           # He..., being tired
            r'.*\s+(with|without)\s+.*\s+(done|finished|being).*'   # with work done...
        ]
        
        for pattern in participle_patterns:
            match = re.match(pattern, sentence, re.IGNORECASE)
            if match:
                participle_form = match.group(1)
                
                return AdvancedStructureAnalysis(
                    structure_type=AdvancedStructureType.PARTICIPLE_ABSOLUTE,
                    main_pattern="Participle absolute construction",
                    sub_patterns=["present_participle", "past_participle", "absolute_construction"],
                    reconstructed_form=sentence,
                    confidence=0.78,
                    components={
                        'participle_form': participle_form
                    },
                    explanation=f"Participle absolute construction with '{participle_form}'",
                    complexity_level=5
                )
        
        return self._create_empty_analysis()

    def _extract_main_verb_from_context(self, doc, subject: str) -> str:
        """文脈から主動詞を抽出"""
        for token in doc:
            if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
                return token.lemma_
        return "do"  # デフォルト

    def _extract_noun_from_context(self, context: str, pronoun: str) -> str:
        """文脈から省略された名詞を推測"""
        words = context.lower().split()
        common_nouns = ['book', 'car', 'house', 'person', 'thing', 'item']
        
        for noun in common_nouns:
            if noun in words:
                return noun + ('s' if pronoun in ['some', 'many', 'few', 'ones'] else '')
        
        if pronoun == 'one':
            return 'item'
        elif pronoun == 'ones':
            return 'items'
        else:
            return 'things'

    def _create_empty_analysis(self) -> AdvancedStructureAnalysis:
        """空の分析結果"""
        return AdvancedStructureAnalysis(
            structure_type=AdvancedStructureType.NO_ADVANCED,
            main_pattern="",
            sub_patterns=[],
            reconstructed_form="",
            confidence=0.0,
            components={},
            explanation="",
            complexity_level=0
        )

def test_advanced_structures():
    """高度構文検出テスト"""
    detector = AdvancedStructuresDetector()
    
    test_sentences = [
        # 省略構文
        "John can sing, and Mary can too.",
        "I bought some books, she bought some too.",
        "I like the red one.",
        
        # 外置構文
        "It is clear that he is guilty.",
        "It seems that she is right.",
        "It is easy to learn English.",
        
        # 比較構文
        "She is taller than her sister.",
        "This is the most beautiful flower.",
        "He is as smart as his brother.",
        
        # 存在構文
        "There are many students in the classroom.",
        "Here comes the bus.",
        
        # 条件構文
        "If it rains tomorrow, we will stay home.",
        "If I were rich, I would travel the world.",
        "Were he here, he would help us.",
        
        # 譲歩構文
        "Although it was raining, we went out.",
        "However hard he tried, he couldn't succeed.",
        
        # 相関構文
        "Both John and Mary came to the party.",
        "Either you leave or I leave.",
        "Not only is he smart but also hardworking.",
        
        # 分詞構文
        "Having finished his work, he went home.",
        "Being tired, she went to bed early.",
        
        # 通常文（比較用）
        "I study English every day.",
        "She is a good teacher."
    ]
    
    print("🔍 高度構文検出テスト")
    print("=" * 80)
    
    success_count = 0
    total_advanced = 0
    
    for sentence in test_sentences:
        result = detector.detect_advanced_structure(sentence)
        
        if result.structure_type != AdvancedStructureType.NO_ADVANCED:
            print(f"\n🔍 分析: {sentence}")
            print(f"   📊 構文タイプ: {result.structure_type.value}")
            print(f"   🎯 主パターン: {result.main_pattern}")
            print(f"   🔧 副パターン: {', '.join(result.sub_patterns)}")
            print(f"   📝 復元形: {result.reconstructed_form}")
            print(f"   💡 説明: {result.explanation}")
            print(f"   💪 複雑度: {result.complexity_level}/5")
            print(f"   📈 確信度: {result.confidence:.2f}")
            success_count += 1
        else:
            print(f"\n🔍 分析: {sentence}")
            print("   ✅ 高度構文なし")
        
        # 期待される高度構文の数をカウント（通常文以外）
        if not any(simple_pattern in sentence.lower() for simple_pattern in 
                  ["i study", "she is a good"]):
            total_advanced += 1
    
    print(f"\n" + "=" * 80)
    print(f"📊 Phase 4 高度構文検出結果:")
    print(f"   🎯 検出成功: {success_count}/{total_advanced}")
    print(f"   📈 成功率: {success_count/total_advanced*100:.1f}%")
    print(f"   🔥 対応構文: 8タイプ (省略・外置・比較・存在・条件・譲歩・相関・分詞)")

if __name__ == "__main__":
    test_advanced_structures()
