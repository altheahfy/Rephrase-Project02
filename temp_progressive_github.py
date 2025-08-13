#!/usr/bin/env python3
"""
Progressive Tenses Engine v1.0
進行形エンジン - be動詞 + -ing構文の完全処理

Rephrase Slot System Compliance:
- S (Subject): 主語スロット
- V (Verb): be動詞スロット  
- O1 (Object1): 進行形動詞スロット (-ing形)
- M1-M3 (Modifiers): 修飾語スロット
- Aux (Auxiliary): 助動詞スロット (will, can, etc.)
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ProgressiveResult:
    """進行形解析結果"""
    pattern_type: str
    slots: Dict[str, str]
    confidence: float
    tense: str
    aspect: str

class ProgressiveTensesEngine:
    """進行形エンジン - be + -ing構文の解析と処理"""
    
    def __init__(self):
        """エンジン初期化"""
        self.name = "Progressive Tenses Engine"
        self.version = "1.0"
        
        # be動詞活用形
        self.be_verbs = {
            "am", "is", "are", "was", "were", 
            "being", "been", "be"
        }
        
        # 助動詞パターン
        self.auxiliaries = {
            "will", "would", "can", "could", "may", "might",
            "shall", "should", "must", "have", "has", "had"
        }
        
        # 進行形パターン定義
        self.progressive_patterns = [
            # 現在進行形
            {
                "name": "present_continuous",
                "pattern": r"^(.*?)\s*(am|is|are)\s+([a-zA-Z]+ing)\s*(.*?)$",
                "tense": "present",
                "aspect": "continuous"
            },
            # 過去進行形
            {
                "name": "past_continuous", 
                "pattern": r"^(.*?)\s*(was|were)\s+([a-zA-Z]+ing)\s*(.*?)$",
                "tense": "past",
                "aspect": "continuous"
            },
            # 未来進行形 (will be + -ing)
            {
                "name": "future_continuous",
                "pattern": r"^(.*?)\s*(will|shall)\s+be\s+([a-zA-Z]+ing)\s*(.*?)$", 
                "tense": "future",
                "aspect": "continuous"
            },
            # 助動詞 + be + -ing
            {
                "name": "modal_continuous",
                "pattern": r"^(.*?)\s*(can|could|may|might|must|should|would)\s+be\s+([a-zA-Z]+ing)\s*(.*?)$",
                "tense": "modal", 
                "aspect": "continuous"
            },
            # 現在完了進行形
            {
                "name": "present_perfect_continuous",
                "pattern": r"^(.*?)\s*(have|has)\s+been\s+([a-zA-Z]+ing)\s*(.*?)$",
                "tense": "present_perfect",
                "aspect": "continuous" 
            },
            # 過去完了進行形
            {
                "name": "past_perfect_continuous",
                "pattern": r"^(.*?)\s*(had)\s+been\s+([a-zA-Z]+ing)\s*(.*?)$",
                "tense": "past_perfect", 
                "aspect": "continuous"
            },
            # 受動進行形 (being + past participle)
            {
                "name": "passive_continuous",
                "pattern": r"^(.*?)\s*(am|is|are|was|were)\s+being\s+([a-zA-Z]+(?:ed|en|d))\s*(.*?)$",
                "tense": "passive",
                "aspect": "continuous"
            }
        ]
        
        # 不規則動詞の-ing形チェック
        self.irregular_ing_forms = {
            "lying", "dying", "tying", "running", "swimming", 
            "getting", "putting", "cutting", "sitting", "hitting"
        }
        
    def is_valid_ing_form(self, word: str) -> bool:
        """有効な-ing形かチェック"""
        if not word.endswith("ing"):
            return False
            
        # 不規則形チェック
        if word in self.irregular_ing_forms:
            return True
            
        # 基本的な-ing形ルール
        if len(word) >= 4:  # 最低4文字 (例: sing -> singing)
            return True
            
        return False
        
    def extract_subject(self, subject_text: str) -> str:
        """主語の抽出と整理"""
        if not subject_text or subject_text.strip() == "":
            return ""
            
        subject = subject_text.strip()
        
        # 冠詞や限定詞の処理
        subject = re.sub(r"^(the|a|an|this|that|these|those|my|your|his|her|our|their)\s+", "", subject)
        
        # 複数の単語を適切に分離
        subject = re.sub(r"([a-z])([A-Z])", r"\1 \2", subject)
        
        return subject
        
    def extract_modifiers(self, modifier_text: str) -> Dict[str, str]:
        """修飾語の抽出と分類"""
        modifiers = {"M1": "", "M2": "", "M3": ""}
        
        if not modifier_text or modifier_text.strip() == "":
            return modifiers
            
        mod_text = modifier_text.strip()
        
        # 時間表現 (M1)
        time_patterns = [
            r"\b(now|today|yesterday|tomorrow|currently|presently)\b",
            r"\b(at \d+:\d+|in the morning|in the evening|at night)\b",
            r"\b(this week|last week|next week|this year)\b"
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, mod_text, re.IGNORECASE)
            if match and modifiers["M1"] == "":
                modifiers["M1"] = match.group(0)
                mod_text = re.sub(pattern, "", mod_text, flags=re.IGNORECASE).strip()
                break
        
        # 場所表現 (M2) 
        location_patterns = [
            r"\b(at home|at work|at school|in the office)\b",
            r"\b(in [A-Z][a-z]+|at [A-Z][a-z]+)\b",
            r"\b(here|there|everywhere|somewhere)\b"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, mod_text, re.IGNORECASE)
            if match and modifiers["M2"] == "":
                modifiers["M2"] = match.group(0)
                mod_text = re.sub(pattern, "", mod_text, flags=re.IGNORECASE).strip()
                break
                
        # その他の修飾語 (M3)
        if mod_text.strip():
            modifiers["M3"] = mod_text.strip()
            
        return modifiers
        
    def analyze_progressive_pattern(self, sentence: str) -> Optional[ProgressiveResult]:
        """進行形パターンの解析"""
        sentence = sentence.strip()
        
        for pattern_info in self.progressive_patterns:
            pattern = pattern_info["pattern"]
            match = re.match(pattern, sentence, re.IGNORECASE)
            
            if match:
                groups = match.groups()
                
                if pattern_info["name"] == "passive_continuous":
                    # 受動進行形: being + past participle
                    subject = self.extract_subject(groups[0]) if groups[0] else ""
                    be_verb = groups[1] if len(groups) > 1 else ""
                    past_participle = groups[2] if len(groups) > 2 else ""
                    remainder = groups[3] if len(groups) > 3 else ""
                    
                    modifiers = self.extract_modifiers(remainder)
                    
                    slots = {
                        "S": subject,
                        "V": be_verb,
                        "O1": f"being {past_participle}",
                        "M1": modifiers.get("M1", ""),
                        "M2": modifiers.get("M2", ""), 
                        "M3": modifiers.get("M3", ""),
                        "Aux": ""
                    }
                    
                elif pattern_info["name"] in ["future_continuous", "modal_continuous"]:
                    # 助動詞 + be + -ing
                    subject = self.extract_subject(groups[0]) if groups[0] else ""
                    auxiliary = groups[1] if len(groups) > 1 else ""
                    ing_verb = groups[2] if len(groups) > 2 else ""
                    remainder = groups[3] if len(groups) > 3 else ""
                    
                    if not self.is_valid_ing_form(ing_verb):
                        continue
                        
                    modifiers = self.extract_modifiers(remainder)
                    
                    slots = {
                        "S": subject,
                        "V": "be", 
                        "O1": ing_verb,
                        "M1": modifiers.get("M1", ""),
                        "M2": modifiers.get("M2", ""),
                        "M3": modifiers.get("M3", ""), 
                        "Aux": auxiliary
                    }
                    
                elif pattern_info["name"] in ["present_perfect_continuous", "past_perfect_continuous"]:
                    # 完了進行形: have/has/had + been + -ing
                    subject = self.extract_subject(groups[0]) if groups[0] else ""
                    perfect_aux = groups[1] if len(groups) > 1 else ""
                    ing_verb = groups[2] if len(groups) > 2 else ""
                    remainder = groups[3] if len(groups) > 3 else ""
                    
                    if not self.is_valid_ing_form(ing_verb):
                        continue
                        
                    modifiers = self.extract_modifiers(remainder)
                    
                    slots = {
                        "S": subject,
                        "V": "been",
                        "O1": ing_verb, 
                        "M1": modifiers.get("M1", ""),
                        "M2": modifiers.get("M2", ""),
                        "M3": modifiers.get("M3", ""),
                        "Aux": perfect_aux
                    }
                    
                else:
                    # 基本進行形: be + -ing
                    subject = self.extract_subject(groups[0]) if groups[0] else ""
                    be_verb = groups[1] if len(groups) > 1 else ""
                    ing_verb = groups[2] if len(groups) > 2 else ""
                    remainder = groups[3] if len(groups) > 3 else ""
                    
                    if not self.is_valid_ing_form(ing_verb):
                        continue
                        
                    modifiers = self.extract_modifiers(remainder)
                    
                    slots = {
                        "S": subject,
                        "V": be_verb,
                        "O1": ing_verb,
                        "M1": modifiers.get("M1", ""), 
                        "M2": modifiers.get("M2", ""),
                        "M3": modifiers.get("M3", ""),
                        "Aux": ""
                    }
                
                # 空スロットを削除
                cleaned_slots = {k: v for k, v in slots.items() if v.strip()}
                
                return ProgressiveResult(
                    pattern_type=pattern_info["name"],
                    slots=cleaned_slots,
                    confidence=0.95,
                    tense=pattern_info["tense"], 
                    aspect=pattern_info["aspect"]
                )
                
        return None
        
    def process_sentence(self, sentence: str) -> Optional[Dict]:
        """文の進行形解析処理"""
        if not sentence or len(sentence.strip()) < 5:
            return None
            
        result = self.analyze_progressive_pattern(sentence)
        
        if result:
            return {
                "engine": self.name,
                "version": self.version,
                "pattern": result.pattern_type,
                "slots": result.slots,
                "confidence": result.confidence,
                "tense": result.tense,
                "aspect": result.aspect,
                "processed": True
            }
            
        return None

# テスト用のメイン関数
def test_progressive_engine():
    """進行形エンジンのテスト"""
    engine = ProgressiveTensesEngine()
    
    test_sentences = [
        # 現在進行形
        "I am studying English now",
        "She is working at the office", 
        "They are playing soccer",
        
        # 過去進行形
        "He was reading a book yesterday",
        "We were watching TV last night",
        
        # 未来進行形
        "I will be traveling tomorrow",
        "She will be working late tonight",
        
        # 助動詞 + be + -ing
        "You should be studying harder",
        "We might be leaving early",
        
        # 現在完了進行形
        "I have been working here for 5 years",
        "They have been waiting for hours",
        
        # 過去完了進行形
        "She had been studying before the exam",
        
        # 受動進行形
        "The house is being built",
        "The car was being repaired"
    ]
    
    print(f"🧪 Testing {engine.name} v{engine.version}")
    print("=" * 60)
    
    success_count = 0
    
    for i, sentence in enumerate(test_sentences, 1):
        result = engine.process_sentence(sentence)
        
        if result:
            print(f"✅ Test {i:2d}: {sentence}")
            print(f"    Pattern: {result['pattern']}")
            print(f"    Tense: {result['tense']} | Aspect: {result['aspect']}")
            print(f"    Slots: {result['slots']}")
            success_count += 1
        else:
            print(f"❌ Test {i:2d}: {sentence}")
            
        print()
    
    print(f"📊 Results: {success_count}/{len(test_sentences)} passed")
    print(f"🎯 Success Rate: {(success_count/len(test_sentences)*100):.1f}%")

if __name__ == "__main__":
    test_progressive_engine()
