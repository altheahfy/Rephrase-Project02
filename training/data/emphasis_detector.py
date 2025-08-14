#!/usr/bin/env python3
"""
Phase 3: 強調構文検出システム実装
V7システムに強調構文検出機能を追加

強調構文パターン:
1. It分裂文: It is John who did this.
2. 疑似分裂文: What I need is rest.
3. Do強調: I do believe you.
4. 副詞強調: Never, ever do that again.
5. 語順強調: This I cannot accept.
6. 反復強調: Very, very important.
7. 感嘆強調: What a beautiful day!
8. 倒置強調: Down came the rain. (既存の倒置と統合)
"""

import spacy
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

class EmphasisType(Enum):
    """強調構文の種類"""
    CLEFT_SENTENCE = "cleft_sentence"           # It is John who did this
    PSEUDO_CLEFT = "pseudo_cleft"               # What I need is rest
    WH_CLEFT = "wh_cleft"                       # What John did was leave
    DO_EMPHASIS = "do_emphasis"                 # I do believe you
    ADVERB_EMPHASIS = "adverb_emphasis"         # Never, ever do that
    FRONTING_EMPHASIS = "fronting_emphasis"     # This I cannot accept
    REPETITION_EMPHASIS = "repetition_emphasis" # Very, very important
    EXCLAMATION_EMPHASIS = "exclamation_emphasis" # What a beautiful day!
    INTENSIFIER_EMPHASIS = "intensifier_emphasis" # So very important
    NO_EMPHASIS = "no_emphasis"                 # 強調なし

@dataclass
class EmphasisAnalysis:
    """強調構文分析結果"""
    emphasis_type: EmphasisType
    emphasized_element: str     # 強調される要素
    emphasis_marker: str        # 強調マーカー
    base_sentence: str         # 基本文推定
    confidence: float           # 確信度
    components: Dict[str, str]  # 構成要素
    explanation: str            # 説明
    intensity_level: int        # 強調度 (1-5)

class EmphasisDetector:
    """強調構文検出エンジン"""
    
    def __init__(self):
        print("💪 Emphasis Detector 初期化中...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # 強調パターン定義
        self.emphasis_patterns = {
            EmphasisType.CLEFT_SENTENCE: {
                'patterns': [
                    r'^It\s+(is|was)\s+.+\s+(who|that|which)\s+',
                    r'^It\s+(is|was)\s+(not\s+)?.+\s+(who|that|which)\s+'
                ],
                'confidence_base': 0.95,
                'intensity': 4
            },
            
            EmphasisType.PSEUDO_CLEFT: {
                'patterns': [
                    r'^(What|Where|When|Why|How)\s+.+\s+(is|was)\s+',
                    r'^(All|Everything|Nothing)\s+.+\s+(is|was)\s+'
                ],
                'confidence_base': 0.90,
                'intensity': 4
            },
            
            EmphasisType.DO_EMPHASIS: {
                'patterns': [
                    r'\b(do|does|did)\s+(believe|think|know|understand|agree|love|like|want|need)\b',
                    r'\bI\s+(do|does|did)\s+\w+\s+you\b'
                ],
                'confidence_base': 0.85,
                'intensity': 3
            },
            
            EmphasisType.EXCLAMATION_EMPHASIS: {
                'patterns': [
                    r'^What\s+(a|an)\s+.+!$',
                    r'^How\s+.+!$',
                    r'^Such\s+(a|an)\s+.+!$'
                ],
                'confidence_base': 0.92,
                'intensity': 5
            }
        }
        
        # 強調副詞・形容詞
        self.intensifiers = {
            'extreme': ['extremely', 'incredibly', 'absolutely', 'completely', 'totally', 'utterly', 'perfectly'],
            'high': ['very', 'really', 'quite', 'rather', 'pretty', 'fairly', 'highly'],
            'repetitive': ['so', 'such', 'too'],
            'negative': ['never', 'not', 'hardly', 'scarcely', 'barely']
        }
        
        # 語順強調マーカー
        self.fronting_markers = {
            'object_fronting': ['this', 'that', 'such'],
            'complement_fronting': ['happy', 'sad', 'angry', 'tired'],
            'adverbial_fronting': ['never', 'rarely', 'here', 'there', 'now', 'then']
        }
    
    def detect_emphasis(self, sentence: str) -> EmphasisAnalysis:
        """強調構文を検出"""
        doc = self.nlp(sentence)
        
        # 各強調タイプをチェック
        for emphasis_type in EmphasisType:
            if emphasis_type == EmphasisType.NO_EMPHASIS:
                continue
                
            analysis = self._check_emphasis_type(sentence, doc, emphasis_type)
            if analysis.confidence > 0.5:
                return analysis
        
        # 強調なし
        return EmphasisAnalysis(
            emphasis_type=EmphasisType.NO_EMPHASIS,
            emphasized_element="",
            emphasis_marker="",
            base_sentence=sentence,
            confidence=0.0,
            components={},
            explanation="No emphasis detected",
            intensity_level=0
        )
    
    def _check_emphasis_type(self, sentence: str, doc, emphasis_type: EmphasisType) -> EmphasisAnalysis:
        """特定の強調タイプをチェック"""
        
        if emphasis_type == EmphasisType.CLEFT_SENTENCE:
            return self._analyze_cleft_sentence(sentence, doc)
        
        elif emphasis_type == EmphasisType.PSEUDO_CLEFT:
            return self._analyze_pseudo_cleft(sentence, doc)
        
        elif emphasis_type == EmphasisType.DO_EMPHASIS:
            return self._analyze_do_emphasis(sentence, doc)
        
        elif emphasis_type == EmphasisType.EXCLAMATION_EMPHASIS:
            return self._analyze_exclamation_emphasis(sentence, doc)
        
        elif emphasis_type == EmphasisType.ADVERB_EMPHASIS:
            return self._analyze_adverb_emphasis(sentence, doc)
        
        elif emphasis_type == EmphasisType.FRONTING_EMPHASIS:
            return self._analyze_fronting_emphasis(sentence, doc)
        
        elif emphasis_type == EmphasisType.REPETITION_EMPHASIS:
            return self._analyze_repetition_emphasis(sentence, doc)
        
        elif emphasis_type == EmphasisType.INTENSIFIER_EMPHASIS:
            return self._analyze_intensifier_emphasis(sentence, doc)
        
        return self._create_empty_analysis()
    
    def _analyze_cleft_sentence(self, sentence: str, doc) -> EmphasisAnalysis:
        """It分裂文分析"""
        # Pattern: It is/was + NP + who/that/which + clause
        cleft_pattern = r'^It\s+(is|was)\s+([^,]+?)\s+(who|that|which)\s+(.+)$'
        match = re.match(cleft_pattern, sentence, re.IGNORECASE)
        
        if not match:
            return self._create_empty_analysis()
        
        be_verb = match.group(1)
        emphasized_np = match.group(2).strip()
        relative_pronoun = match.group(3)
        clause = match.group(4).strip()
        
        # 基本文を推定
        if relative_pronoun.lower() == 'who':
            base_sentence = f"{emphasized_np} {clause}"
        elif relative_pronoun.lower() == 'that':
            base_sentence = f"{emphasized_np} {clause}"
        else:
            base_sentence = f"{clause} {emphasized_np}"
        
        return EmphasisAnalysis(
            emphasis_type=EmphasisType.CLEFT_SENTENCE,
            emphasized_element=emphasized_np,
            emphasis_marker=f"It {be_verb} ... {relative_pronoun}",
            base_sentence=base_sentence,
            confidence=0.95,
            components={
                'copula': f"It {be_verb}",
                'focus': emphasized_np,
                'relative_pronoun': relative_pronoun,
                'presupposition': clause
            },
            explanation=f"It-cleft emphasizes '{emphasized_np}' as the focused element",
            intensity_level=4
        )
    
    def _analyze_pseudo_cleft(self, sentence: str, doc) -> EmphasisAnalysis:
        """疑似分裂文分析"""
        # Pattern: WH-word + clause + is/was + NP
        pseudo_pattern = r'^(What|Where|When|Why|How|All|Everything|Nothing)\s+(.+?)\s+(is|was)\s+(.+)$'
        match = re.match(pseudo_pattern, sentence, re.IGNORECASE)
        
        if not match:
            return self._create_empty_analysis()
        
        wh_word = match.group(1)
        wh_clause = match.group(2).strip()
        be_verb = match.group(3)
        focus_element = match.group(4).strip()
        
        # 基本文を推定
        if wh_word.lower() == 'what':
            base_sentence = f"You need {focus_element}" if 'need' in wh_clause else f"The answer is {focus_element}"
        else:
            base_sentence = f"{focus_element} {wh_clause}"
        
        return EmphasisAnalysis(
            emphasis_type=EmphasisType.PSEUDO_CLEFT,
            emphasized_element=focus_element,
            emphasis_marker=f"{wh_word} ... {be_verb}",
            base_sentence=base_sentence,
            confidence=0.90,
            components={
                'wh_element': wh_word,
                'presupposition': wh_clause,
                'focus': focus_element
            },
            explanation=f"Pseudo-cleft emphasizes '{focus_element}' using {wh_word}-clause",
            intensity_level=4
        )
    
    def _analyze_do_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """Do強調分析"""
        words = sentence.split()
        
        # Do強調パターンを探す
        for i, word in enumerate(words):
            if word.lower() in ['do', 'does', 'did'] and i + 1 < len(words):
                next_word = words[i + 1].lower()
                
                # 拡張された一般的な動詞でdo強調をチェック
                emphasis_verbs = ['believe', 'think', 'know', 'understand', 'agree', 
                                'love', 'like', 'want', 'need', 'hope', 'wish',
                                'finish', 'complete', 'work', 'study', 'help',
                                'come', 'go', 'try', 'care', 'matter', 'exist']
                
                # より緩和された条件：動詞リストまたは動詞の形態的特徴
                if (next_word in emphasis_verbs or 
                    # 動詞らしい語尾パターン
                    (len(next_word) > 3 and next_word not in ['have', 'will', 'can', 'may', 'must']) or
                    # 文脈から強調判定（感情的な文）
                    any(emotion_word in sentence.lower() for emotion_word in 
                        ['really', 'truly', 'certainly', 'definitely', 'absolutely'])):
                    
                    emphasized_verb = words[i + 1]
                    base_sentence = ' '.join(words[:i] + words[i+1:])  # doを除去
                    
                    return EmphasisAnalysis(
                        emphasis_type=EmphasisType.DO_EMPHASIS,
                        emphasized_element=emphasized_verb,
                        emphasis_marker=word,
                        base_sentence=base_sentence,
                        confidence=0.85,
                        components={
                            'emphasis_auxiliary': word,
                            'emphasized_verb': emphasized_verb
                        },
                        explanation=f"Do-emphasis strengthens the assertion of '{emphasized_verb}'",
                        intensity_level=3
                    )
        
        return self._create_empty_analysis()
    
    def _analyze_exclamation_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """感嘆強調分析"""
        # What a/an + NP!
        what_pattern = r'^What\s+(a|an)\s+(.+?)!$'
        match = re.match(what_pattern, sentence, re.IGNORECASE)
        
        if match:
            article = match.group(1)
            noun_phrase = match.group(2).strip()
            base_sentence = f"It is {article} {noun_phrase}."
            
            return EmphasisAnalysis(
                emphasis_type=EmphasisType.EXCLAMATION_EMPHASIS,
                emphasized_element=noun_phrase,
                emphasis_marker="What a/an ... !",
                base_sentence=base_sentence,
                confidence=0.92,
                components={'exclamative': 'What', 'focus': noun_phrase},
                explanation=f"Exclamative 'What a/an' emphasizes the degree of '{noun_phrase}'",
                intensity_level=5
            )
        
        # How + ADJ/ADV!
        how_pattern = r'^How\s+(.+?)!$'
        match = re.match(how_pattern, sentence, re.IGNORECASE)
        
        if match:
            adjective_phrase = match.group(1).strip()
            base_sentence = f"It is {adjective_phrase}."
            
            return EmphasisAnalysis(
                emphasis_type=EmphasisType.EXCLAMATION_EMPHASIS,
                emphasized_element=adjective_phrase,
                emphasis_marker="How ... !",
                base_sentence=base_sentence,
                confidence=0.92,
                components={'exclamative': 'How', 'focus': adjective_phrase},
                explanation=f"Exclamative 'How' emphasizes the degree of '{adjective_phrase}'",
                intensity_level=5
            )
        
        # Such a/an + NP! パターンを追加
        such_pattern = r'^Such\s+(a|an)\s+(.+?)!?$'
        match = re.match(such_pattern, sentence, re.IGNORECASE)
        
        if match:
            article = match.group(1)
            noun_phrase = match.group(2).strip().rstrip('!')
            base_sentence = f"It is {article} {noun_phrase}."
            
            return EmphasisAnalysis(
                emphasis_type=EmphasisType.EXCLAMATION_EMPHASIS,
                emphasized_element=noun_phrase,
                emphasis_marker="Such a/an ... !",
                base_sentence=base_sentence,
                confidence=0.88,
                components={'exclamative': 'Such', 'focus': noun_phrase},
                explanation=f"Exclamative 'Such a/an' emphasizes the degree of '{noun_phrase}'",
                intensity_level=4
            )
        
        return self._create_empty_analysis()
    
    def _analyze_adverb_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """副詞強調分析"""
        words = sentence.split()
        
        # 反復副詞をチェック
        for i in range(len(words) - 1):
            if words[i].lower() == words[i + 1].lower():
                repeated_word = words[i]
                
                # 強調副詞の反復
                if repeated_word.lower() in ['very', 'so', 'never', 'really', 'quite']:
                    base_sentence = ' '.join(words[:i] + words[i+1:])  # 1つの反復を除去
                    
                    return EmphasisAnalysis(
                        emphasis_type=EmphasisType.REPETITION_EMPHASIS,
                        emphasized_element=repeated_word,
                        emphasis_marker=f"{repeated_word}, {repeated_word}",
                        base_sentence=base_sentence,
                        confidence=0.88,
                        components={'repeated_element': repeated_word},
                        explanation=f"Repetition of '{repeated_word}' for emphasis",
                        intensity_level=3
                    )
        
        # 強調副詞の累積
        intensifier_count = 0
        intensifiers_found = []
        
        for word in words:
            for level, intensifier_list in self.intensifiers.items():
                if word.lower() in intensifier_list:
                    intensifier_count += 1
                    intensifiers_found.append((word, level))
        
        if intensifier_count >= 2:
            intensifier_words = [word for word, level in intensifiers_found]
            base_sentence = sentence  # 簡易版では同じ
            
            return EmphasisAnalysis(
                emphasis_type=EmphasisType.INTENSIFIER_EMPHASIS,
                emphasized_element=' '.join(intensifier_words),
                emphasis_marker='multiple intensifiers',
                base_sentence=base_sentence,
                confidence=0.75,
                components={'intensifiers': intensifiers_found},
                explanation=f"Multiple intensifiers {intensifier_words} create emphasis",
                intensity_level=min(intensifier_count, 5)
            )
        
        return self._create_empty_analysis()
    
    def _analyze_fronting_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """語順強調（前置）分析"""
        words = sentence.split()
        
        if len(words) < 3:
            return self._create_empty_analysis()
        
        first_word = words[0].lower()
        
        # 目的語前置: "This I cannot accept"
        if first_word in ['this', 'that', 'these', 'those']:
            # 代名詞 + 主語 + 動詞 パターン
            if len(words) >= 3:
                object_element = words[0]
                subject = words[1]
                verb_phrase = ' '.join(words[2:])
                
                # 通常語順に変換
                base_sentence = f"{subject} {verb_phrase} {object_element.lower()}"
                
                return EmphasisAnalysis(
                    emphasis_type=EmphasisType.FRONTING_EMPHASIS,
                    emphasized_element=object_element,
                    emphasis_marker="object fronting",
                    base_sentence=base_sentence,
                    confidence=0.80,
                    components={'fronted_element': object_element, 'type': 'object'},
                    explanation=f"Object '{object_element}' fronted for emphasis",
                    intensity_level=3
                )
        
        # 形容詞前置: "Happy I am not"
        if first_word in ['happy', 'sad', 'angry', 'tired', 'excited', 'worried']:
            complement = words[0]
            rest_sentence = ' '.join(words[1:])
            base_sentence = f"{rest_sentence} {complement.lower()}"
            
            return EmphasisAnalysis(
                emphasis_type=EmphasisType.FRONTING_EMPHASIS,
                emphasized_element=complement,
                emphasis_marker="complement fronting",
                base_sentence=base_sentence,
                confidence=0.75,
                components={'fronted_element': complement, 'type': 'complement'},
                explanation=f"Complement '{complement}' fronted for emphasis",
                intensity_level=3
            )
        
        return self._create_empty_analysis()
    
    def _analyze_repetition_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """反復強調分析"""
        words = sentence.split()
        
        # 反復パターンを検出
        for i in range(len(words) - 1):
            current_word = words[i].lower().strip(',')
            next_word = words[i + 1].lower().strip(',')
            
            # 同じ単語の反復（very, very / so, so / such, such）
            if current_word == next_word and current_word in ['very', 'so', 'such', 'really', 'quite']:
                # 強調対象を探す（通常は反復語の後に続く形容詞・名詞）
                emphasized_element = ""
                if i + 2 < len(words):
                    emphasized_element = words[i + 2]
                elif i > 0:
                    emphasized_element = words[i - 1]
                
                base_sentence = sentence.replace(f"{words[i]}, {words[i + 1]}", words[i])
                
                return EmphasisAnalysis(
                    emphasis_type=EmphasisType.REPETITION_EMPHASIS,
                    emphasized_element=emphasized_element,
                    emphasis_marker=f"{current_word}, {current_word}",
                    base_sentence=base_sentence,
                    confidence=0.82,
                    components={
                        'repeated_word': current_word,
                        'target': emphasized_element
                    },
                    explanation=f"Repetition of '{current_word}' emphasizes intensity",
                    intensity_level=4
                )
        
        return self._create_empty_analysis()
    
    def _analyze_intensifier_emphasis(self, sentence: str, doc) -> EmphasisAnalysis:
        """強調語強調分析（既に_analyze_adverb_emphasisでカバー）"""
        return self._create_empty_analysis()
    
    def _create_empty_analysis(self) -> EmphasisAnalysis:
        """空の分析結果"""
        return EmphasisAnalysis(
            emphasis_type=EmphasisType.NO_EMPHASIS,
            emphasized_element="",
            emphasis_marker="",
            base_sentence="",
            confidence=0.0,
            components={},
            explanation="",
            intensity_level=0
        )

def test_emphasis_detection():
    """強調構文検出テスト"""
    detector = EmphasisDetector()
    
    test_sentences = [
        # It分裂文
        "It is John who broke the window.",
        "It was the book that I needed.",
        
        # 疑似分裂文
        "What I need is rest.",
        "What John did was leave early.",
        "All I want is peace.",
        
        # Do強調
        "I do believe you are right.",
        "She does love classical music.",
        "They did finish on time.",
        
        # 感嘆強調
        "What a beautiful day!",
        "How wonderful!",
        "Such a lovely garden!",
        
        # 反復強調
        "Very, very important decision.",
        "So, so tired today.",
        
        # 語順強調
        "This I cannot accept.",
        "Happy I am not.",
        
        # 強調なし（比較用）
        "I read books every day.",
        "She is a good student.",
    ]
    
    print("💪 強調構文検出テスト")
    print("=" * 80)
    
    for sentence in test_sentences:
        print(f"\n🔍 分析: {sentence}")
        result = detector.detect_emphasis(sentence)
        
        if result.confidence > 0.5:
            print(f"   📊 強調タイプ: {result.emphasis_type.value}")
            print(f"   🎯 強調要素: {result.emphasized_element}")
            print(f"   🔧 強調マーカー: {result.emphasis_marker}")
            print(f"   📝 基本文推定: {result.base_sentence}")
            print(f"   💡 説明: {result.explanation}")
            print(f"   💪 強調度: {result.intensity_level}/5")
            print(f"   📈 確信度: {result.confidence:.2f}")
        else:
            print(f"   ✅ 強調なし")

if __name__ == "__main__":
    test_emphasis_detection()
