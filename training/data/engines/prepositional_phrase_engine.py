#!/usr/bin/env python3
"""
Prepositional Phrase Engine v1.0 - Priority 6 復旧版
前置詞句エンジン - マルチエンジン協調システム対応

Rephrase Slo        # 時間表現の判定
        time_keywords = [
            'morning', 'evening', 'night', 'afternoon',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'summer', 'winter', 'spring', 'fall', 'autumn',
            "o'clock", 'am', 'pm'
        ] Compliance:
- 専門領域: 前置詞句の検出と分析
- M1 (Modifier1): 時間表現前置詞句
- M2 (Modifier2): 場所表現前置詞句  
- M3 (Modifier3): 手段・目的・その他前置詞句

マルチエンジン協調システム設計思想:
- 前置詞句の専門的処理を担当
- 他の文法構造は専門エンジンに委ねる
- Grammar Master Controller との協調動作
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum

class PrepositionalType(Enum):
    """前置詞句の種類"""
    TIME = "time"           # 時間表現 → M1
    LOCATION = "location"   # 場所表現 → M2  
    MANNER = "manner"       # 手段・方法 → M3
    PURPOSE = "purpose"     # 目的 → M3
    OTHER = "other"         # その他 → M3

class PrepositionalPhraseEngine:
    """前置詞句エンジン - マルチエンジン協調システム対応版"""
    
    def __init__(self):
        print("🎯 前置詞句エンジン初期化中...")
        
        # 前置詞の分類
        self.preposition_categories = {
            # 時間前置詞 (M1)
            PrepositionalType.TIME: {
                'in', 'on', 'at', 'during', 'before', 'after', 
                'since', 'until', 'by', 'for'
            },
            
            # 場所前置詞 (M2)
            PrepositionalType.LOCATION: {
                'in', 'on', 'at', 'under', 'over', 'behind', 
                'in front of', 'next to', 'near', 'beside'
            },
            
            # 手段・方法前置詞 (M3)
            PrepositionalType.MANNER: {
                'by', 'with', 'through', 'via', 'using'
            },
            
            # 目的前置詞 (M3)  
            PrepositionalType.PURPOSE: {
                'for', 'to'
            }
        }
        
        # すべての前置詞のセット
        self.all_prepositions = set()
        for category in self.preposition_categories.values():
            self.all_prepositions.update(category)
            
        print("✅ 前置詞句エンジン初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """標準processメソッド - 上位スロット＋サブスロット対応"""
        print(f"🎯 前置詞句エンジン処理開始: '{text}'")
        
        # 前置詞句を抽出
        prepositional_phrases = self._extract_prepositional_phrases(text)
        
        if not prepositional_phrases:
            print("ℹ️ 前置詞句未検出")
            return {}
            
        # 上位スロット分解
        slots = self._assign_to_slots(prepositional_phrases)
        
        # サブスロット分解を追加
        sub_slots = self._decompose_to_subslots(prepositional_phrases)
        slots.update(sub_slots)
        
        print(f"✅ 前置詞句検出完了: {len([k for k in slots.keys() if not k.startswith('sub-')])}上位スロット + {len([k for k in slots.keys() if k.startswith('sub-')])}サブスロット")
        return slots
    
    def _extract_prepositional_phrases(self, text: str) -> List[Tuple[str, str, str]]:
        """前置詞句を抽出 (前置詞, 目的語, 完全な句)"""
        phrases = []
        
        # 各前置詞について検索
        for prep in sorted(self.all_prepositions, key=len, reverse=True):
            # 前置詞 + 名詞句のパターンを検索
            pattern = r'\b' + re.escape(prep) + r'\s+([^,\.!?;]+?)(?=\s+(?:and|or|but|,|\.|\?|!|;)|\s*$)'
            
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                preposition = prep
                object_phrase = match.group(1).strip()
                full_phrase = f"{preposition} {object_phrase}"
                
                # 重複チェック（より長い句を優先）
                is_duplicate = False
                for existing_prep, existing_obj, existing_full in phrases:
                    if full_phrase in existing_full or existing_full in full_phrase:
                        if len(full_phrase) <= len(existing_full):
                            is_duplicate = True
                            break
                        else:
                            # より長い句で置き換え
                            phrases.remove((existing_prep, existing_obj, existing_full))
                            break
                
                if not is_duplicate:
                    phrases.append((preposition, object_phrase, full_phrase))
        
        return phrases
    
    def _classify_prepositional_phrase(self, preposition: str, object_phrase: str) -> PrepositionalType:
        """前置詞句の種類を分類"""
        prep_lower = preposition.lower()
        obj_lower = object_phrase.lower()
        
        # 時間表現の判定
        time_keywords = [
            'morning', 'evening', 'night', 'afternoon',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'summer', 'winter', 'spring', 'fall', 'autumn',
            "o'clock", 'am', 'pm'
        ]
        
        if any(keyword in obj_lower for keyword in time_keywords):
            return PrepositionalType.TIME
        
        if re.search(r'\d+(:\d+)?\s*(am|pm)', obj_lower):
            return PrepositionalType.TIME
            
        # 場所表現の判定
        location_keywords = [
            'home', 'office', 'school', 'room', 'park', 'station', 'street',
            'city', 'country', 'table', 'chair', 'floor', 'wall', 'library',
            'tokyo', 'kyoto', 'japan', 'america', 'store', 'shop'
        ]
        
        if any(keyword in obj_lower for keyword in location_keywords):
            return PrepositionalType.LOCATION
            
        # 手段・方法の判定
        if prep_lower in ['by', 'with', 'through', 'via', 'using']:
            return PrepositionalType.MANNER
            
        # 目的の判定
        if prep_lower in ['for'] and not any(keyword in obj_lower for keyword in time_keywords):
            return PrepositionalType.PURPOSE
            
        # デフォルト：場所 > 時間 > その他の優先順位
        if prep_lower in ['in', 'on', 'at']:
            return PrepositionalType.LOCATION  # デフォルトで場所扱い
        
        return PrepositionalType.OTHER
    
    def _assign_to_slots(self, phrases: List[Tuple[str, str, str]]) -> Dict[str, str]:
        """前置詞句をRephraseスロットに割り当て"""
        slots = {}
        
        # スロットカウンター
        slot_counters = {'M1': 0, 'M2': 0, 'M3': 0}
        
        for preposition, object_phrase, full_phrase in phrases:
            # 前置詞句の種類を分類
            phrase_type = self._classify_prepositional_phrase(preposition, object_phrase)
            
            # スロット割り当て
            if phrase_type == PrepositionalType.TIME:
                slot_counters['M1'] += 1
                if slot_counters['M1'] == 1:
                    slots['M1'] = full_phrase
                else:
                    # 複数の時間前置詞句がある場合
                    existing = slots.get('M1', '')
                    slots['M1'] = f"{existing}, {full_phrase}" if existing else full_phrase
                    
            elif phrase_type == PrepositionalType.LOCATION:
                slot_counters['M2'] += 1
                if slot_counters['M2'] == 1:
                    slots['M2'] = full_phrase
                else:
                    # 複数の場所前置詞句がある場合
                    existing = slots.get('M2', '')
                    slots['M2'] = f"{existing}, {full_phrase}" if existing else full_phrase
                    
            else:  # MANNER, PURPOSE, OTHER
                slot_counters['M3'] += 1
                if slot_counters['M3'] == 1:
                    slots['M3'] = full_phrase
                else:
                    # 複数のその他前置詞句がある場合
                    existing = slots.get('M3', '')
                    slots['M3'] = f"{existing}, {full_phrase}" if existing else full_phrase
        
        return slots
    
    def _decompose_to_subslots(self, phrases: List[Tuple[str, str, str]]) -> Dict[str, str]:
        """前置詞句をサブスロットに分解 - Gerund エンジン設計準拠"""
        sub_slots = {}
        
        for i, (preposition, object_phrase, full_phrase) in enumerate(phrases, 1):
            # サブスロットの命名規則: sub-m1, sub-m2, sub-m3 + 前置詞・目的語分離
            base_sub_key = f"sub-m{i}"
            prep_sub_key = f"sub-m{i}-prep"  # 前置詞部分
            obj_sub_key = f"sub-m{i}-obj"   # 目的語部分
            
            # 前置詞をサブスロットに格納
            if base_sub_key not in sub_slots:
                sub_slots[prep_sub_key] = preposition.lower()
                sub_slots[obj_sub_key] = object_phrase.lower()
                
                # より詳細な目的語分解（名詞句の場合）
                obj_words = object_phrase.strip().split()
                if len(obj_words) > 1:
                    # 複数語の場合、主要名詞を特定
                    main_noun = obj_words[-1]  # 通常、最後の語が主要名詞
                    modifiers = ' '.join(obj_words[:-1])  # 修飾語群
                    
                    sub_slots[f"{base_sub_key}-noun"] = main_noun.lower()
                    if modifiers.strip():
                        sub_slots[f"{base_sub_key}-mod"] = modifiers.lower()
                else:
                    # 単一語の場合
                    sub_slots[f"{base_sub_key}-noun"] = object_phrase.lower()
        
        return sub_slots

# テスト用
if __name__ == "__main__":
    engine = PrepositionalPhraseEngine()
    
    test_cases = [
        "The book is on the table.",
        "We met at 3 o'clock.",
        "She goes to school by bus.",
        "I study English in the morning at home.",
        "They work from 9 AM to 5 PM in the office."
    ]
    
    for text in test_cases:
        print(f"\n📋 テスト: {text}")
        result = engine.process(text)
        print(f"📊 結果: {result}")
        print("-" * 50)
