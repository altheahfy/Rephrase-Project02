#!/usr/bin/env python3
"""
Phase 2: 時制・相システム実装
V6システムに時制・相検出機能を追加

時制・相パターン:
1. 現在完了: have/has + 過去分詞
2. 過去完了: had + 過去分詞  
3. 未来完了: will have + 過去分詞
4. 現在進行: be + 現在分詞
5. 過去進行: was/were + 現在分詞
6. 未来進行: will be + 現在分詞
7. 現在完了進行: have/has been + 現在分詞
8. 過去完了進行: had been + 現在分詞
9. 未来完了進行: will have been + 現在分詞
10. 受動態各種: be + 過去分詞
11. 仮定法: would/could/should + 動詞
"""

import spacy
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

class TenseAspectType(Enum):
    """時制・相の種類"""
    # 基本時制
    SIMPLE_PRESENT = "simple_present"           # walk/walks
    SIMPLE_PAST = "simple_past"                 # walked
    SIMPLE_FUTURE = "simple_future"             # will walk
    
    # 完了相
    PRESENT_PERFECT = "present_perfect"         # have/has walked
    PAST_PERFECT = "past_perfect"               # had walked
    FUTURE_PERFECT = "future_perfect"           # will have walked
    
    # 進行相
    PRESENT_PROGRESSIVE = "present_progressive" # am/is/are walking
    PAST_PROGRESSIVE = "past_progressive"       # was/were walking  
    FUTURE_PROGRESSIVE = "future_progressive"   # will be walking
    
    # 完了進行
    PRESENT_PERFECT_PROGRESSIVE = "present_perfect_progressive"  # have/has been walking
    PAST_PERFECT_PROGRESSIVE = "past_perfect_progressive"        # had been walking
    FUTURE_PERFECT_PROGRESSIVE = "future_perfect_progressive"   # will have been walking
    
    # 受動態
    PRESENT_PASSIVE = "present_passive"         # am/is/are walked
    PAST_PASSIVE = "past_passive"               # was/were walked
    FUTURE_PASSIVE = "future_passive"           # will be walked
    PERFECT_PASSIVE = "perfect_passive"         # have/has/had been walked
    
    # 法（Modal）
    CONDITIONAL = "conditional"                 # would walk
    SUBJUNCTIVE = "subjunctive"                 # should walk, could walk
    IMPERATIVE = "imperative"                   # walk!

@dataclass
class TenseAspectAnalysis:
    """時制・相分析結果"""
    tense_aspect: TenseAspectType
    auxiliary_verbs: List[str]      # 助動詞群
    main_verb: str                  # 主動詞
    main_verb_form: str             # 動詞の形（原形、過去分詞など）
    confidence: float               # 確信度
    components: Dict[str, str]      # 構成要素
    explanation: str                # 説明
    timeline: str                   # 時間軸での位置

class TenseAspectDetector:
    """時制・相検出エンジン"""
    
    def __init__(self):
        print("🕒 Tense-Aspect Detector 初期化中...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # 助動詞分類
        self.auxiliary_verbs = {
            'be_forms': ['be', 'am', 'is', 'are', 'was', 'were', 'been', 'being'],
            'have_forms': ['have', 'has', 'had', 'having'],
            'modal_verbs': ['will', 'would', 'can', 'could', 'may', 'might', 'shall', 'should', 'must', 'ought'],
            'do_forms': ['do', 'does', 'did']
        }
        
        # 動詞形態パターン
        self.verb_patterns = {
            'base_form': 'VB',      # walk
            'present_3sg': 'VBZ',   # walks  
            'past_form': 'VBD',     # walked
            'past_participle': 'VBN',  # walked
            'present_participle': 'VBG'  # walking
        }
    
    def detect_tense_aspect(self, sentence: str) -> TenseAspectAnalysis:
        """時制・相を検出"""
        doc = self.nlp(sentence)
        
        # 動詞句を抽出
        verb_phrase = self._extract_verb_phrase(doc)
        
        if not verb_phrase:
            return self._create_default_analysis()
        
        # パターン解析
        analysis = self._analyze_verb_phrase(verb_phrase, doc)
        
        return analysis
    
    def _extract_verb_phrase(self, doc) -> Dict[str, Any]:
        """文から動詞句を抽出"""
        # ROOT動詞を見つける
        root_verb = None
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                root_verb = token
                break
        
        if not root_verb:
            return {}
        
        # 動詞句の構成要素を収集
        auxiliaries = []
        main_verb = root_verb
        
        # 助動詞を収集（ROOT動詞の子要素から）
        for child in root_verb.children:
            if child.dep_ == 'aux' or child.dep_ == 'auxpass':
                auxiliaries.append({
                    'text': child.text,
                    'lemma': child.lemma_,
                    'pos': child.tag_,
                    'type': self._classify_auxiliary(child.text.lower())
                })
        
        # 助動詞を語順でソート
        auxiliaries.sort(key=lambda x: x['text'])  # 簡易ソート
        
        return {
            'main_verb': {
                'text': main_verb.text,
                'lemma': main_verb.lemma_,  
                'pos': main_verb.tag_,
                'form': self._get_verb_form(main_verb.tag_)
            },
            'auxiliaries': auxiliaries,
            'full_phrase': ' '.join([aux['text'] for aux in auxiliaries] + [main_verb.text])
        }
    
    def _classify_auxiliary(self, aux_text: str) -> str:
        """助動詞を分類"""
        if aux_text in self.auxiliary_verbs['be_forms']:
            return 'be'
        elif aux_text in self.auxiliary_verbs['have_forms']:
            return 'have'
        elif aux_text in self.auxiliary_verbs['modal_verbs']:
            return 'modal'
        elif aux_text in self.auxiliary_verbs['do_forms']:
            return 'do'
        else:
            return 'unknown'
    
    def _get_verb_form(self, pos_tag: str) -> str:
        """POS tagから動詞形態を判定"""
        form_mapping = {
            'VB': 'base_form',
            'VBZ': 'present_3sg', 
            'VBD': 'past_form',
            'VBN': 'past_participle',
            'VBG': 'present_participle',
            'VBP': 'present_form'
        }
        return form_mapping.get(pos_tag, 'unknown')
    
    def _analyze_verb_phrase(self, verb_phrase: Dict, doc) -> TenseAspectAnalysis:
        """動詞句を分析して時制・相を判定"""
        auxiliaries = verb_phrase.get('auxiliaries', [])
        main_verb = verb_phrase.get('main_verb', {})
        
        aux_types = [aux['type'] for aux in auxiliaries]
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        main_verb_form = main_verb.get('form', '')
        
        # パターンマッチング
        
        # 1. 完了時制パターン
        if 'have' in aux_types and main_verb_form == 'past_participle':
            return self._analyze_perfect_tense(auxiliaries, main_verb, doc)
        
        # 2. 進行時制パターン  
        if 'be' in aux_types and main_verb_form == 'present_participle':
            return self._analyze_progressive_tense(auxiliaries, main_verb, doc)
        
        # 3. 受動態パターン
        if 'be' in aux_types and main_verb_form == 'past_participle':
            return self._analyze_passive_voice(auxiliaries, main_verb, doc)
        
        # 4. 未来時制パターン
        if 'modal' in aux_types and any(aux in ['will', 'shall'] for aux in aux_texts):
            return self._analyze_future_tense(auxiliaries, main_verb, doc)
        
        # 5. 法（conditional, subjunctive）
        if 'modal' in aux_types and any(aux in ['would', 'could', 'should', 'might', 'may'] for aux in aux_texts):
            return self._analyze_modal_verbs(auxiliaries, main_verb, doc)
        
        # 6. 単純時制
        return self._analyze_simple_tense(auxiliaries, main_verb, doc)
    
    def _analyze_perfect_tense(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """完了時制分析"""
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        
        # 現在完了進行: have/has been + -ing
        if len(auxiliaries) == 2 and 'been' in aux_texts and main_verb['form'] == 'present_participle':
            tense_type = TenseAspectType.PRESENT_PERFECT_PROGRESSIVE
            explanation = "Present perfect progressive: action started in past, continues to present"
            timeline = "past → present (ongoing)"
        
        # 過去完了進行: had been + -ing  
        elif 'had' in aux_texts and 'been' in aux_texts and main_verb['form'] == 'present_participle':
            tense_type = TenseAspectType.PAST_PERFECT_PROGRESSIVE
            explanation = "Past perfect progressive: ongoing action completed before past reference point"
            timeline = "past ← past (completed ongoing)"
        
        # 現在完了: have/has + past participle
        elif any(aux in ['have', 'has'] for aux in aux_texts):
            tense_type = TenseAspectType.PRESENT_PERFECT
            explanation = "Present perfect: past action with present relevance"
            timeline = "past → present (relevant)"
        
        # 過去完了: had + past participle
        elif 'had' in aux_texts:
            tense_type = TenseAspectType.PAST_PERFECT
            explanation = "Past perfect: action completed before past reference point"
            timeline = "past ← past (completed)"
        
        else:
            return self._create_default_analysis()
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=aux_texts,
            main_verb=main_verb['text'],
            main_verb_form=main_verb['form'],
            confidence=0.9,
            components={'perfect_marker': 'have/has/had', 'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _analyze_progressive_tense(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """進行時制分析"""
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        
        # 未来進行: will be + -ing
        if 'will' in aux_texts and any(be_form in aux_texts for be_form in ['be']):
            tense_type = TenseAspectType.FUTURE_PROGRESSIVE
            explanation = "Future progressive: ongoing action in the future"
            timeline = "present → future (ongoing)"
        
        # 過去進行: was/were + -ing
        elif any(aux in ['was', 'were'] for aux in aux_texts):
            tense_type = TenseAspectType.PAST_PROGRESSIVE
            explanation = "Past progressive: ongoing action in the past"
            timeline = "past (ongoing)"
        
        # 現在進行: am/is/are + -ing
        elif any(aux in ['am', 'is', 'are'] for aux in aux_texts):
            tense_type = TenseAspectType.PRESENT_PROGRESSIVE
            explanation = "Present progressive: ongoing action now"
            timeline = "present (ongoing)"
        
        else:
            return self._create_default_analysis()
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=aux_texts,
            main_verb=main_verb['text'],
            main_verb_form=main_verb['form'],
            confidence=0.85,
            components={'progressive_marker': 'be + -ing', 'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _analyze_passive_voice(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """受動態分析"""
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        
        # 完了受動態: have/has/had been + past participle
        if any(have_form in aux_texts for have_form in ['have', 'has', 'had']) and 'been' in aux_texts:
            tense_type = TenseAspectType.PERFECT_PASSIVE
            explanation = "Perfect passive: completed action, focus on recipient"
            timeline = "past → present/past (completed, recipient focus)"
        
        # 過去受動態: was/were + past participle
        elif any(aux in ['was', 'were'] for aux in aux_texts):
            tense_type = TenseAspectType.PAST_PASSIVE
            explanation = "Past passive: past action, focus on recipient"
            timeline = "past (recipient focus)"
        
        # 現在受動態: am/is/are + past participle
        elif any(aux in ['am', 'is', 'are'] for aux in aux_texts):
            tense_type = TenseAspectType.PRESENT_PASSIVE
            explanation = "Present passive: present action, focus on recipient"
            timeline = "present (recipient focus)"
        
        # 未来受動態: will be + past participle
        elif 'will' in aux_texts and 'be' in aux_texts:
            tense_type = TenseAspectType.FUTURE_PASSIVE
            explanation = "Future passive: future action, focus on recipient"
            timeline = "future (recipient focus)"
        
        else:
            return self._create_default_analysis()
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=aux_texts,
            main_verb=main_verb['text'],
            main_verb_form=main_verb['form'],
            confidence=0.9,
            components={'passive_marker': 'be + past_participle', 'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _analyze_future_tense(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """未来時制分析"""
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        
        # 未来完了進行: will have been + -ing
        if 'will' in aux_texts and 'have' in aux_texts and 'been' in aux_texts:
            tense_type = TenseAspectType.FUTURE_PERFECT_PROGRESSIVE
            explanation = "Future perfect progressive: ongoing action completed by future point"
            timeline = "present → future (completed ongoing)"
        
        # 未来完了: will have + past participle  
        elif 'will' in aux_texts and 'have' in aux_texts:
            tense_type = TenseAspectType.FUTURE_PERFECT
            explanation = "Future perfect: action completed by future reference point"
            timeline = "present → future (completed)"
        
        # 単純未来: will + base form
        else:
            tense_type = TenseAspectType.SIMPLE_FUTURE
            explanation = "Simple future: action in the future"
            timeline = "present → future"
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=aux_texts,
            main_verb=main_verb['text'],
            main_verb_form=main_verb['form'],
            confidence=0.88,
            components={'future_marker': 'will', 'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _analyze_modal_verbs(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """法（modal）分析"""
        aux_texts = [aux['text'].lower() for aux in auxiliaries]
        
        if any(aux in ['would', 'could'] for aux in aux_texts):
            tense_type = TenseAspectType.CONDITIONAL
            explanation = "Conditional: hypothetical or polite action"
            timeline = "hypothetical"
        
        elif any(aux in ['should', 'ought'] for aux in aux_texts):
            tense_type = TenseAspectType.SUBJUNCTIVE
            explanation = "Subjunctive: obligation, recommendation, or possibility"
            timeline = "hypothetical/obligation"
        
        else:
            tense_type = TenseAspectType.CONDITIONAL
            explanation = f"Modal verb '{aux_texts[0]}': expresses modality"
            timeline = "modal context"
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=aux_texts,
            main_verb=main_verb['text'],
            main_verb_form=main_verb['form'],
            confidence=0.8,
            components={'modal': aux_texts[0], 'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _analyze_simple_tense(self, auxiliaries: List, main_verb: Dict, doc) -> TenseAspectAnalysis:
        """単純時制分析"""
        main_verb_form = main_verb.get('form', '')
        
        if main_verb_form == 'past_form':
            tense_type = TenseAspectType.SIMPLE_PAST
            explanation = "Simple past: completed action in the past"
            timeline = "past (completed)"
        
        elif main_verb_form in ['present_3sg', 'present_form', 'base_form']:
            tense_type = TenseAspectType.SIMPLE_PRESENT
            explanation = "Simple present: habitual action or general truth"
            timeline = "present (habitual/general)"
        
        else:
            return self._create_default_analysis()
        
        return TenseAspectAnalysis(
            tense_aspect=tense_type,
            auxiliary_verbs=[aux['text'] for aux in auxiliaries],
            main_verb=main_verb['text'],
            main_verb_form=main_verb_form,
            confidence=0.75,
            components={'main_verb': main_verb['text']},
            explanation=explanation,
            timeline=timeline
        )
    
    def _create_default_analysis(self) -> TenseAspectAnalysis:
        """デフォルト分析結果"""
        return TenseAspectAnalysis(
            tense_aspect=TenseAspectType.SIMPLE_PRESENT,
            auxiliary_verbs=[],
            main_verb="",
            main_verb_form="unknown",
            confidence=0.0,
            components={},
            explanation="Unable to determine tense/aspect",
            timeline="unknown"
        )

def test_tense_aspect_detection():
    """時制・相検出テスト"""
    detector = TenseAspectDetector()
    
    test_sentences = [
        "I walk to school.",                           # 単純現在
        "She walked home yesterday.",                  # 単純過去
        "They will arrive tomorrow.",                  # 単純未来
        "I have finished my homework.",                # 現在完了
        "She had left before I came.",                 # 過去完了
        "We will have completed by then.",             # 未来完了
        "He is reading a book.",                       # 現在進行
        "They were playing soccer.",                   # 過去進行
        "I will be working tomorrow.",                 # 未来進行
        "She has been studying for hours.",            # 現在完了進行
        "The book was written by him.",                # 過去受動
        "The house is being built.",                   # 現在受動進行
        "I would go if I could.",                      # 条件法
        "You should study harder.",                    # 仮定法
        "They might come later.",                      # 可能性
    ]
    
    print("🕒 時制・相検出テスト")
    print("=" * 80)
    
    for sentence in test_sentences:
        print(f"\n🔍 分析: {sentence}")
        result = detector.detect_tense_aspect(sentence)
        
        print(f"   📊 時制・相: {result.tense_aspect.value}")
        print(f"   🔧 助動詞: {', '.join(result.auxiliary_verbs) if result.auxiliary_verbs else 'なし'}")
        print(f"   🎯 主動詞: {result.main_verb} ({result.main_verb_form})")
        print(f"   💡 説明: {result.explanation}")
        print(f"   ⏰ 時間軸: {result.timeline}")
        print(f"   📈 確信度: {result.confidence:.2f}")

if __name__ == "__main__":
    test_tense_aspect_detection()
