#!/usr/bin/env python3
"""
Prepositional Phrase Engine v1.0
前置詞句エンジン - 前置詞句の包括的処理

Rephrase Slot System Compliance:
- S (Subject): 主語スロット
- V (Verb): 動詞スロット  
- O1, O2 (Objects): 目的語スロット
- M1 (Modifier1): 時間表現前置詞句
- M2 (Modifier2): 場所表現前置詞句
- M3 (Modifier3): 手段・目的・その他前置詞句
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

class PrepositionalType(Enum):
    """前置詞句の種類"""
    TIME = "time"           # 時間表現
    LOCATION = "location"   # 場所表現  
    MANNER = "manner"       # 方法・手段
    PURPOSE = "purpose"     # 目的
    CAUSE = "cause"         # 原因・理由
    ACCOMPANIMENT = "accompaniment"  # 同伴
    TOPIC = "topic"         # 話題・関連
    SOURCE = "source"       # 起点・出所
    DIRECTION = "direction" # 方向

@dataclass
class PrepositionalPhrase:
    """前置詞句の解析結果"""
    preposition: str
    object: str
    full_phrase: str
    phrase_type: PrepositionalType
    slot_assignment: str  # M1, M2, M3
    confidence: float

@dataclass
class PrepositionalResult:
    """前置詞句エンジンの解析結果"""
    pattern_type: str
    slots: Dict[str, str]
    prepositional_phrases: List[PrepositionalPhrase]
    confidence: float
    processed: bool

class PrepositionalPhraseEngine:
    """前置詞句エンジン - 前置詞句の包括的解析"""
    
    def __init__(self):
        """エンジン初期化"""
        self.name = "Prepositional Phrase Engine"
        self.version = "1.0"
        
        # 前置詞の分類定義
        self.preposition_categories = {
            # 時間前置詞 (M1 slot)
            PrepositionalType.TIME: {
                "in": ["in the morning", "in the evening", "in January", "in 2024", "in summer"],
                "on": ["on Monday", "on January 1st", "on weekends", "on time"],
                "at": ["at 3 o'clock", "at noon", "at night", "at dawn", "at midnight"],
                "during": ["during the meeting", "during lunch", "during class"],
                "before": ["before dinner", "before class", "before 5 PM"],
                "after": ["after work", "after school", "after lunch"],
                "since": ["since yesterday", "since 2020", "since morning"],
                "until": ["until tomorrow", "until 5 PM", "until next week"],
                "by": ["by tomorrow", "by next week", "by 5 PM"],
                "for": ["for two hours", "for a week", "for a long time"]
            },
            
            # 場所前置詞 (M2 slot)
            PrepositionalType.LOCATION: {
                "in": ["in the room", "in Tokyo", "in the office", "in the park"],
                "on": ["on the table", "on the floor", "on the wall", "on the street"],
                "at": ["at home", "at work", "at school", "at the station"],
                "under": ["under the bridge", "under the table", "under the tree"],
                "over": ["over the bridge", "over the mountain", "over there"],
                "above": ["above the clouds", "above the ground"],
                "below": ["below the surface", "below the line"],
                "beside": ["beside the river", "beside me", "beside the house"],
                "behind": ["behind the building", "behind the door"],
                "in front of": ["in front of the house", "in front of me"],
                "next to": ["next to the bank", "next to him"],
                "between": ["between the buildings", "between us"],
                "among": ["among the trees", "among friends"],
                "near": ["near the station", "near here"],
                "around": ["around the corner", "around the world"]
            },
            
            # 手段・方法前置詞 (M3 slot)
            PrepositionalType.MANNER: {
                "by": ["by car", "by train", "by bus", "by plane", "by email"],
                "with": ["with a pen", "with my hands", "with care", "with difficulty"],
                "through": ["through email", "through practice", "through experience"],
                "via": ["via email", "via Tokyo", "via the internet"],
                "using": ["using a computer", "using this method"]
            },
            
            # 目的前置詞 (M3 slot)
            PrepositionalType.PURPOSE: {
                "for": ["for my family", "for work", "for fun", "for practice"],
                "to": ["to help you", "to study English", "to buy food"],
                "in order to": ["in order to succeed", "in order to understand"]
            },
            
            # 同伴前置詞 (M3 slot)  
            PrepositionalType.ACCOMPANIMENT: {
                "with": ["with my friend", "with my family", "with colleagues"],
                "without": ["without help", "without money", "without permission"]
            },
            
            # 話題・関連前置詞 (M3 slot)
            PrepositionalType.TOPIC: {
                "about": ["about the movie", "about work", "about life"],
                "of": ["of great importance", "of high quality", "of interest"],
                "regarding": ["regarding this matter", "regarding your request"],
                "concerning": ["concerning the problem", "concerning your health"]
            },
            
            # 原因・理由前置詞 (M3 slot)
            PrepositionalType.CAUSE: {
                "because of": ["because of rain", "because of you", "because of traffic"],
                "due to": ["due to weather", "due to technical problems"],
                "owing to": ["owing to circumstances", "owing to delays"]
            }
        }
        
        # 前置詞の基本リスト
        self.all_prepositions = set()
        for category in self.preposition_categories.values():
            for prep in category.keys():
                self.all_prepositions.add(prep)
        
        # 複合前置詞（句として扱う）
        self.compound_prepositions = {
            "in front of", "in spite of", "because of", "due to", 
            "owing to", "in order to", "next to", "instead of",
            "according to", "thanks to", "in addition to"
        }
    
    def identify_preposition_type(self, preposition: str, obj: str) -> PrepositionalType:
        """前置詞句の種類を特定"""
        # 文脈による判定
        full_phrase = f"{preposition} {obj}".lower()
        
        # 各カテゴリで検索
        for phrase_type, prep_dict in self.preposition_categories.items():
            if preposition.lower() in prep_dict:
                # 例文パターンとマッチするかチェック  
                for example in prep_dict[preposition.lower()]:
                    if self._phrases_similar(full_phrase, example):
                        return phrase_type
                        
                # 時間表現のパターンマッチング
                if phrase_type == PrepositionalType.TIME:
                    if re.search(r'\d+:\d+|\d+(am|pm)|morning|evening|night|monday|tuesday|january|summer|winter', obj, re.IGNORECASE):
                        return PrepositionalType.TIME
                        
                # 場所表現のパターンマッチング
                elif phrase_type == PrepositionalType.LOCATION:
                    if re.search(r'home|office|school|room|park|station|street|city|country', obj, re.IGNORECASE):
                        return PrepositionalType.LOCATION
                        
        # デフォルト分類
        if preposition.lower() in ["in", "on", "at"] and re.search(r'morning|evening|night|\d+', obj):
            return PrepositionalType.TIME
        elif preposition.lower() in ["in", "on", "at"] and re.search(r'home|office|school|room', obj):  
            return PrepositionalType.LOCATION
        elif preposition.lower() in ["by", "with"]:
            return PrepositionalType.MANNER
        elif preposition.lower() in ["for", "to"]:
            return PrepositionalType.PURPOSE
        elif preposition.lower() in ["about", "of"]:
            return PrepositionalType.TOPIC
        else:
            return PrepositionalType.MANNER  # デフォルト
    
    def _phrases_similar(self, phrase1: str, phrase2: str) -> bool:
        """2つの前置詞句が類似しているかチェック"""
        # 簡単な類似性チェック - 共通単語の存在
        words1 = set(phrase1.split())
        words2 = set(phrase2.split())
        
        # 前置詞を除外して比較
        content_words1 = words1 - self.all_prepositions
        content_words2 = words2 - self.all_prepositions
        
        if content_words1 & content_words2:  # 共通単語があれば類似
            return True
            
        return False
    
    def extract_prepositional_phrases(self, sentence: str) -> List[PrepositionalPhrase]:
        """文から前置詞句を抽出"""
        phrases = []
        sentence = sentence.strip()
        processed_positions = set()  # 処理済み位置を記録
        
        # 複合前置詞の処理（優先）
        for compound_prep in sorted(self.compound_prepositions, key=len, reverse=True):
            pattern = rf'\b{re.escape(compound_prep)}\s+([^,\.!?;]+)'
            matches = list(re.finditer(pattern, sentence, re.IGNORECASE))
            
            for match in matches:
                start, end = match.span()
                if any(pos in range(start, end) for pos in processed_positions):
                    continue  # 重複部分はスキップ
                    
                prep_words = compound_prep.split()
                obj = match.group(1).strip()
                
                # 目的語の終端を調整（他の前置詞や句読点で切る）
                obj_words = obj.split()
                clean_obj_words = []
                
                for word in obj_words:
                    if word.lower() in self.all_prepositions:
                        break  # 次の前置詞で停止
                    clean_obj_words.append(word)
                
                if clean_obj_words:
                    obj = " ".join(clean_obj_words)
                    full_phrase = f"{compound_prep} {obj}"
                    
                    # 句の種類を特定
                    phrase_type = self.identify_preposition_type(compound_prep, obj)
                    
                    # スロット割り当て
                    if phrase_type == PrepositionalType.TIME:
                        slot = "M1"
                    elif phrase_type == PrepositionalType.LOCATION:
                        slot = "M2"  
                    else:
                        slot = "M3"
                    
                    phrases.append(PrepositionalPhrase(
                        preposition=compound_prep,
                        object=obj,
                        full_phrase=full_phrase,
                        phrase_type=phrase_type,
                        slot_assignment=slot,
                        confidence=0.9
                    ))
                    
                    # 処理済み位置をマーク
                    processed_positions.update(range(start, start + len(full_phrase)))
        
        # 単一前置詞の処理
        for prep in sorted(self.all_prepositions, key=len, reverse=True):
            if prep in [cp.split()[0] for cp in self.compound_prepositions]:
                continue  # 複合前置詞の一部は単独処理しない
                
            pattern = rf'\b{re.escape(prep)}\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;|$)|\s*$)'
            matches = list(re.finditer(pattern, sentence, re.IGNORECASE))
            
            for match in matches:
                start, end = match.span()
                if any(pos in range(start, end) for pos in processed_positions):
                    continue  # 重複部分はスキップ
                
                obj = match.group(1).strip()
                
                # 目的語の終端を調整
                obj_words = obj.split()
                clean_obj_words = []
                
                for word in obj_words:
                    if word.lower() in self.all_prepositions and word.lower() != prep.lower():
                        break  # 次の前置詞で停止
                    clean_obj_words.append(word)
                
                if clean_obj_words:
                    obj = " ".join(clean_obj_words)
                    full_phrase = f"{prep} {obj}"
                    
                    # 句の種類を特定
                    phrase_type = self.identify_preposition_type(prep, obj)
                    
                    # スロット割り当て
                    if phrase_type == PrepositionalType.TIME:
                        slot = "M1"
                    elif phrase_type == PrepositionalType.LOCATION:
                        slot = "M2"
                    else:
                        slot = "M3"
                    
                    phrases.append(PrepositionalPhrase(
                        preposition=prep,
                        object=obj,
                        full_phrase=full_phrase,
                        phrase_type=phrase_type,
                        slot_assignment=slot,
                        confidence=0.85
                    ))
                    
                    # 処理済み位置をマーク
                    phrase_start = sentence.find(full_phrase)
                    if phrase_start >= 0:
                        processed_positions.update(range(phrase_start, phrase_start + len(full_phrase)))
        
        return phrases
    
    def extract_base_sentence(self, sentence: str, phrases: List[PrepositionalPhrase]) -> str:
        """前置詞句を除いた基本文を抽出"""
        base_sentence = sentence
        
        # 前置詞句を除去
        for phrase in phrases:
            base_sentence = base_sentence.replace(phrase.full_phrase, " ", 1)
        
        # 余分な空白を整理
        base_sentence = re.sub(r'\s+', ' ', base_sentence).strip()
        
        return base_sentence
    
    def analyze_base_sentence(self, base_sentence: str) -> Dict[str, str]:
        """基本文のS+V+O構造を解析"""
        slots = {"S": "", "V": "", "O1": "", "O2": "", "C1": "", "C2": "", "Aux": ""}
        
        # 簡単なS+V+O解析
        words = base_sentence.split()
        
        if len(words) >= 2:
            # 助動詞チェック
            auxiliaries = {"do", "does", "did", "will", "would", "can", "could", "should", "may", "might", "must", "have", "has", "had", "am", "is", "are", "was", "were"}
            
            if words[0].lower() in auxiliaries:
                slots["Aux"] = words[0]
                if len(words) > 1:
                    slots["S"] = words[1] 
                if len(words) > 2:
                    slots["V"] = words[2]
                if len(words) > 3:
                    slots["O1"] = " ".join(words[3:])
            else:
                slots["S"] = words[0]
                if len(words) > 1:
                    slots["V"] = words[1]
                if len(words) > 2:
                    slots["O1"] = " ".join(words[2:])
        
        # 空スロットを削除
        return {k: v for k, v in slots.items() if v.strip()}
    
    def process_sentence(self, sentence: str) -> Optional[Dict]:
        """前置詞句を含む文の解析処理"""
        if not sentence or len(sentence.strip()) < 5:
            return None
        
        # 前置詞句を抽出
        prepositional_phrases = self.extract_prepositional_phrases(sentence)
        
        if not prepositional_phrases:
            return None  # 前置詞句が見つからない場合
        
        # 基本文を抽出
        base_sentence = self.extract_base_sentence(sentence, prepositional_phrases)
        
        # 基本文構造を解析
        base_slots = self.analyze_base_sentence(base_sentence)
        
        # 前置詞句をスロットに配置（重複排除）
        modifier_slots = {"M1": [], "M2": [], "M3": []}
        
        for phrase in prepositional_phrases:
            slot = phrase.slot_assignment
            if phrase.full_phrase not in modifier_slots[slot]:
                modifier_slots[slot].append(phrase.full_phrase)
        
        # スロットを統合
        final_slots = base_slots.copy()
        
        for slot, phrases in modifier_slots.items():
            if phrases:
                final_slots[slot] = ", ".join(phrases)
        
        # 信頼度計算
        avg_confidence = sum(p.confidence for p in prepositional_phrases) / len(prepositional_phrases)
        
        return {
            "engine": self.name,
            "version": self.version,
            "pattern": "prepositional_phrase_analysis",
            "slots": final_slots,
            "prepositional_phrases": [
                {
                    "preposition": p.preposition,
                    "object": p.object,
                    "type": p.phrase_type.value,
                    "slot": p.slot_assignment
                } for p in prepositional_phrases
            ],
            "confidence": avg_confidence,
            "processed": True
        }

# テスト用のメイン関数
def test_prepositional_engine():
    """前置詞句エンジンのテスト"""
    engine = PrepositionalPhraseEngine()
    
    test_sentences = [
        # 時間表現 (M1)
        "I study English in the morning at home",
        "She works from 9 AM to 5 PM at the office",
        "We meet on Monday during lunch",
        
        # 場所表現 (M2)  
        "The book is on the table in the room",
        "He lives near the station in Tokyo",
        "They walk in the park behind the school",
        
        # 手段・目的表現 (M3)
        "I travel by car with my family",
        "She writes with a pen for practice", 
        "We communicate through email about work",
        
        # 複合前置詞
        "He sits in front of the computer because of work",
        "She studies English in order to travel abroad",
        
        # 複数の前置詞句
        "I study at home in the morning with my friend for the exam",
        "She works in Tokyo at a big company with her colleagues",
        "They travel by train to Kyoto during the holiday for sightseeing"
    ]
    
    print(f"🧪 Testing {engine.name} v{engine.version}")
    print("=" * 60)
    
    success_count = 0
    
    for i, sentence in enumerate(test_sentences, 1):
        result = engine.process_sentence(sentence)
        
        if result:
            print(f"✅ Test {i:2d}: {sentence}")
            print(f"    Slots: {result['slots']}")
            print(f"    Prepositional Phrases: {len(result['prepositional_phrases'])}")
            for pp in result['prepositional_phrases']:
                print(f"      - {pp['preposition']} {pp['object']} ({pp['type']}) → {pp['slot']}")
            success_count += 1
        else:
            print(f"❌ Test {i:2d}: {sentence}")
            
        print()
    
    print(f"📊 Results: {success_count}/{len(test_sentences)} passed")
    print(f"🎯 Success Rate: {(success_count/len(test_sentences)*100):.1f}%")

if __name__ == "__main__":
    test_prepositional_engine()
