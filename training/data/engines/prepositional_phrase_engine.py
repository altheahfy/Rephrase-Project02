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
    sub_slots: Dict[str, str]  # サブスロット分解
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
                        
        # デフォルト分類（優先順位を考慮）
        if preposition.lower() in ["in", "on", "at"]:
            # 場所表現を優先的に判定
            if re.search(r'home|office|school|room|park|station|street|city|country|table|tokyo|kyoto|library', obj, re.IGNORECASE):
                return PrepositionalType.LOCATION
            # 時間表現を次に判定
            elif re.search(r'morning|evening|night|afternoon|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august|september|october|november|december|summer|winter|spring|fall|autumn|\d+', obj, re.IGNORECASE):
                return PrepositionalType.TIME
        elif preposition.lower() in ["by", "with"]:
            return PrepositionalType.MANNER
        elif preposition.lower() in ["for", "to"]:
            return PrepositionalType.PURPOSE
        elif preposition.lower() in ["about", "of"]:
            return PrepositionalType.TOPIC
        else:
            return PrepositionalType.MANNER  # デフォルト
    
    def analyze_phrase_structure(self, preposition: str, obj: str, phrase_type: PrepositionalType) -> Dict[str, str]:
        """前置詞句の内部構造をサブスロットに分解（Rephrase原則：SV/V構造を持つ複雑な句のみ）"""
        sub_slots = {}
        
        # Rephrase原則：サブスロットはSV構造やV構造を持つ複雑な句にのみ適用
        # 単純な前置詞句（"in the morning", "at home", "by car"など）にはサブスロットを設定しない
        
        # 複合前置詞の分解（V構造やSV構造を持つもののみ）
        if preposition in self.compound_prepositions:
            if preposition == "in order to":
                # "in order to travel abroad" → V構造なのでサブスロット適用
                obj_words = obj.split()
                if obj_words:
                    # 動詞部分を特定
                    verb_part = obj_words[0]  # "travel"
                    sub_slots["sub-v"] = verb_part
                    
                    # 残りは修飾語
                    if len(obj_words) > 1:
                        modifier_part = " ".join(obj_words[1:])  # "abroad"
                        sub_slots["sub-m3"] = modifier_part
                        
            elif preposition == "in front of":
                # "in front of the computer" → 単純な前置詞句なのでサブスロット適用しない
                pass
                
            elif preposition == "because of":
                # "because of work" → 単純な前置詞句なのでサブスロット適用しない
                pass
                
        # 単一前置詞の場合 - 基本的にサブスロット適用しない
        # （単純な前置詞句はRephraseではサブスロット不要）
        
        return sub_slots
                
        return sub_slots
        
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
        """文から前置詞句を抽出（改良版 - 複数前置詞句対応）"""
        phrases = []
        original_sentence = sentence.strip()
        
        # 段階的処理：まず全ての前置詞句を特定し、その後順番に処理
        all_phrase_matches = []
        
        # 1. 複合前置詞の検索（最優先）
        for compound_prep in sorted(self.compound_prepositions, key=len, reverse=True):
            pattern = rf'\b{re.escape(compound_prep)}\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;|$)|\s*$)'
            matches = list(re.finditer(pattern, original_sentence, re.IGNORECASE))
            
            for match in matches:
                obj = match.group(1).strip()
                
                # 目的語の終端を他の前置詞で調整
                obj_words = obj.split()
                clean_obj_words = []
                
                for word in obj_words:
                    if word.lower() in self.all_prepositions and word.lower() not in compound_prep.lower():
                        break
                    clean_obj_words.append(word)
                
                if clean_obj_words:
                    clean_obj = " ".join(clean_obj_words)
                    full_phrase = f"{compound_prep} {clean_obj}"
                    
                    all_phrase_matches.append({
                        'start': match.start(),
                        'end': match.start() + len(full_phrase),
                        'preposition': compound_prep,
                        'object': clean_obj,
                        'full_phrase': full_phrase,
                        'priority': 1  # 最高優先度
                    })
        
        # 2. 単一前置詞の検索
        for prep in sorted(self.all_prepositions, key=len, reverse=True):
            if prep in ["in", "on", "at"]:  # 重要な前置詞を優先処理
                # より包括的なパターン
                pattern = rf'\b{re.escape(prep)}\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;)|\s*$)'
            else:
                if any(prep in cp for cp in self.compound_prepositions):
                    continue  # 複合前置詞の一部はスキップ
                pattern = rf'\b{re.escape(prep)}\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;|$)|\s*$)'
                
            matches = list(re.finditer(pattern, original_sentence, re.IGNORECASE))
            
            for match in matches:
                obj = match.group(1).strip()
                
                # 目的語の終端を他の前置詞で調整
                obj_words = obj.split()
                clean_obj_words = []
                
                for word in obj_words:
                    if word.lower() in self.all_prepositions and word.lower() != prep.lower():
                        break
                    clean_obj_words.append(word)
                
                if clean_obj_words:
                    clean_obj = " ".join(clean_obj_words)
                    full_phrase = f"{prep} {clean_obj}"
                    
                    all_phrase_matches.append({
                        'start': match.start(),
                        'end': match.start() + len(full_phrase),
                        'preposition': prep,
                        'object': clean_obj,
                        'full_phrase': full_phrase,
                        'priority': 2  # 通常優先度
                    })
        
        # 3. 重複排除（位置順で処理してスロット割り当て）
        all_phrase_matches.sort(key=lambda x: x['start'])  # 位置順でソート
        processed_ranges = []
        slot_counter = 1  # M1, M2, M3の順番カウンター
        
        for match_info in all_phrase_matches:
            start, end = match_info['start'], match_info['end']
            
            # 重複チェック
            overlap = False
            for proc_start, proc_end in processed_ranges:
                if not (end <= proc_start or start >= proc_end):  # 重複している
                    overlap = True
                    break
            
            if not overlap:
                # 句の種類を特定（情報として保持）
                phrase_type = self.identify_preposition_type(match_info['preposition'], match_info['object'])
                
                # 位置ベースのスロット割り当て（Rephrase原則）
                if slot_counter == 1:
                    slot = "M1"
                elif slot_counter == 2:
                    slot = "M2"
                else:
                    slot = "M3"
                
                slot_counter += 1
                
                # サブスロット分解
                sub_slots = self.analyze_phrase_structure(match_info['preposition'], match_info['object'], phrase_type)
                
                phrases.append(PrepositionalPhrase(
                    preposition=match_info['preposition'],
                    object=match_info['object'],
                    full_phrase=match_info['full_phrase'],
                    phrase_type=phrase_type,
                    slot_assignment=slot,
                    sub_slots=sub_slots,
                    confidence=0.9 if match_info['priority'] == 1 else 0.85
                ))
                
                processed_ranges.append((start, end))
        
        return phrases
    
    def extract_base_sentence(self, sentence: str, phrases: List[PrepositionalPhrase]) -> str:
        """前置詞句を除いた基本文を抽出（改良版）"""
        base_sentence = sentence
        
        # 処理済み前置詞句を位置順でソートして後ろから削除
        phrase_positions = []
        for phrase in phrases:
            start_pos = base_sentence.find(phrase.full_phrase)
            if start_pos >= 0:
                phrase_positions.append((start_pos, phrase.full_phrase))
        
        # 後ろの位置から順に削除（インデックスのずれを防ぐため）
        phrase_positions.sort(key=lambda x: x[0], reverse=True)
        
        for start_pos, phrase_text in phrase_positions:
            end_pos = start_pos + len(phrase_text)
            base_sentence = base_sentence[:start_pos] + " " + base_sentence[end_pos:]
        
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
        sub_slots_combined = {}
        
        for phrase in prepositional_phrases:
            slot = phrase.slot_assignment
            if phrase.full_phrase not in modifier_slots[slot]:
                modifier_slots[slot].append(phrase.full_phrase)
            
            # サブスロットを統合
            for sub_slot, sub_value in phrase.sub_slots.items():
                if sub_slot not in sub_slots_combined:
                    sub_slots_combined[sub_slot] = []
                if sub_value not in sub_slots_combined[sub_slot]:
                    sub_slots_combined[sub_slot].append(sub_value)
        
        # スロットを統合
        final_slots = base_slots.copy()
        
        for slot, phrases in modifier_slots.items():
            if phrases:
                final_slots[slot] = ", ".join(phrases)
                
        # サブスロットを統合
        for sub_slot, values in sub_slots_combined.items():
            if values:
                final_slots[sub_slot] = ", ".join(values)
        
        # 信頼度計算
        avg_confidence = sum(p.confidence for p in prepositional_phrases) / len(prepositional_phrases)
        
        # 空のスロットをクリーンアップ
        final_slots = {k: v for k, v in final_slots.items() if v and str(v).strip()}
        
        return {
            "engine": self.name,
            "version": self.version,
            "pattern": "prepositional_phrase_analysis",
            "slots": final_slots,
            "prepositional_phrases": [
                {
                    "preposition": p.preposition,
                    "object": p.object,
                    "type": p.phrase_type.value if p.phrase_type else "unknown",
                    "slot": p.slot_assignment,
                    "sub_slots": p.sub_slots
                } for p in prepositional_phrases
            ],
            "confidence": avg_confidence,
            "processed": True
        }

    def process(self, text: str) -> Dict[str, str]:
        """標準のprocessメソッド - マルチエンジン協調システム対応"""
        print(f"🎯 前置詞句エンジン処理開始: '{text}'")
        
        result = self.process_sentence(text)
        if result and result.get("processed"):
            # 標準形式に変換
            slots = result.get("slots", {})
            print(f"✅ 前置詞句検出完了: {len(slots)}スロット")
            return slots
        else:
            print("ℹ️ 前置詞句未検出")
            return {}

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
                if pp['sub_slots']:
                    for sub_slot, sub_value in pp['sub_slots'].items():
                        print(f"        └─ {sub_slot}: {sub_value}")
            success_count += 1
        else:
            print(f"❌ Test {i:2d}: {sentence}")
            # デバッグ: 前置詞句抽出を確認
            phrases = engine.extract_prepositional_phrases(sentence)
            if phrases:
                print(f"    Debug: Found {len(phrases)} phrases but processing failed")
                for p in phrases:
                    print(f"      - {p.full_phrase}")
            else:
                print(f"    Debug: No prepositional phrases found")
            
        print()
    
    print(f"📊 Results: {success_count}/{len(test_sentences)} passed")
    print(f"🎯 Success Rate: {(success_count/len(test_sentences)*100):.1f}%")

if __name__ == "__main__":
    test_prepositional_engine()
