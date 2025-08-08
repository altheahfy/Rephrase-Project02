# ===== Rephrase Parsing Engine =====
# 完全統合版: ChatGPT 34ルール + サブクローズ分解エンジン
# 目標: すべての英文法ルールに対応した品詞分解システム

import json
import re
import os

class RephraseParsingEngine:
    """完全統合版Rephrase品詞分解エンジン"""
    
    def __init__(self):
        self.engine_name = "Rephrase Parsing Engine v1.0"
        self.rules_data = self.load_rules()
        
    def load_rules(self):
        """文法ルールデータを読み込み"""
        rules_file = os.path.join(os.path.dirname(__file__), 'rephrase_rules_v1.0.json')
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: {rules_file} が見つかりません。基本ルールを使用します。")
            return self.get_basic_rules()
    
    def get_basic_rules(self):
        """基本的な文法ルールセット（fallback）"""
        return {
            "cognitive_verbs": ["think", "believe", "know", "realize", "understand", "feel", "guess", "suppose"],
            "modal_verbs": ["will", "would", "can", "could", "may", "might", "must", "should", "ought"],
            "be_verbs": ["am", "is", "are", "was", "were", "being", "been"],
            "have_verbs": ["have", "has", "had"],
            "copular_verbs": ["become", "seem", "appear", "look", "sound", "feel", "taste", "smell"],
            "ditransitive_verbs": ["give", "tell", "show", "send", "teach", "buy", "make", "get"]
        }
    
    def analyze_sentence(self, sentence):
        """文を解析してスロットに分解"""
        sentence = sentence.strip()
        if not sentence:
            return {}
            
        # 複文の場合、サブクローズ分解を試行
        if self.contains_subclause(sentence):
            return self.analyze_complex_sentence(sentence)
        else:
            return self.analyze_simple_sentence(sentence)
    
    def contains_subclause(self, sentence):
        """サブクローズ（複文）を含むかチェック"""
        subclause_indicators = [
            r'\bthat\b',  # that節
            r'\bwhat\b',  # what節
            r'\bwhere\b', # where節  
            r'\bwhen\b',  # when節
            r'\bwhy\b',   # why節
            r'\bhow\b',   # how節
            r'\bwhich\b', # which節
            r'\bwho\b',   # who節
        ]
        
        for indicator in subclause_indicators:
            if re.search(indicator, sentence, re.IGNORECASE):
                return True
        return False
    
    def analyze_complex_sentence(self, sentence):
        """複文を解析（サブクローズ分解）"""
        slots = {}
        words = sentence.split()
        
        # 認知動詞 + that節パターンを検出
        cognitive_result = self.detect_cognitive_verb_pattern(words, sentence)
        if cognitive_result:
            slots.update(cognitive_result)
            return slots
            
        # その他の複文パターンもここで処理可能
        return self.analyze_simple_sentence(sentence)
    
    def detect_cognitive_verb_pattern(self, words, sentence):
        """認知動詞 + that節パターンを検出・分解"""
        cognitive_verbs = self.rules_data.get("cognitive_verbs", ["think", "believe", "know"])
        
        for i, word in enumerate(words):
            if word.lower() in cognitive_verbs:
                # 主語を検出
                subject = " ".join(words[:i]) if i > 0 else "I"
                
                # that節を検出・分解
                remaining = " ".join(words[i+1:])
                
                if "that" in remaining.lower():
                    that_clause = self.extract_that_clause(remaining)
                    subslots = self.analyze_that_clause(that_clause)
                    
                    return {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'cognitive-main'}],
                        'V': [{'value': word, 'type': 'cognitive_verb', 'rule_id': 'cognitive-main', 
                               'subslots': subslots, 'note': f'that節分解済み: {that_clause[:20]}...'}]
                    }
                else:
                    # that省略パターン
                    subslots = self.analyze_that_clause(remaining)
                    
                    return {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'cognitive-main'}],
                        'V': [{'value': word, 'type': 'cognitive_verb', 'rule_id': 'cognitive-main',
                               'subslots': subslots, 'note': f'that省略節分解済み: {remaining[:20]}...'}]
                    }
        
        return None
    
    def extract_that_clause(self, text):
        """that節部分を抽出"""
        text = text.strip()
        
        # "that" で始まる場合
        if text.lower().startswith("that "):
            return text[5:].strip()  # "that "を除去
            
        # "that" が途中にある場合
        that_match = re.search(r'\bthat\s+(.+)$', text, re.IGNORECASE)
        if that_match:
            return that_match.group(1)
            
        return text
    
    def analyze_that_clause(self, clause_text):
        """that節を分解してサブスロットに"""
        if not clause_text.strip():
            return {}
            
        words = clause_text.strip().split()
        if not words:
            return {}
            
        # 基本的なSVO構造を検出
        subslots = {}
        
        # be動詞パターン
        be_verbs = ["is", "are", "was", "were", "am"]
        for i, word in enumerate(words):
            if word.lower() in be_verbs:
                if i > 0:
                    subslots['sub-s'] = " ".join(words[:i])
                subslots['sub-v'] = word
                if i < len(words) - 1:
                    subslots['sub-c'] = " ".join(words[i+1:])
                return subslots
        
        # 一般動詞パターン
        if len(words) >= 2:
            # 最初の語を主語、2番目を動詞と仮定
            subslots['sub-s'] = words[0]
            subslots['sub-v'] = words[1]
            if len(words) > 2:
                subslots['sub-o1'] = " ".join(words[2:])
                
        return subslots
    
    def analyze_simple_sentence(self, sentence):
        """単文を解析"""
        slots = {}
        words = sentence.split()
        
        # 助動詞パターンの検出
        modal_result = self.detect_modal_pattern(words)
        if modal_result:
            slots.update(modal_result)
            return slots
            
        # 受動態パターンの検出  
        passive_result = self.detect_passive_pattern(words)
        if passive_result:
            slots.update(passive_result)
            return slots
        
        # be動詞パターンの検出
        be_result = self.detect_be_verb_pattern(words)
        if be_result:
            slots.update(be_result)
            return slots
            
        # 基本的なSVOパターン
        basic_result = self.detect_basic_svo_pattern(words)
        if basic_result:
            slots.update(basic_result)
            
        return slots
    
    def detect_modal_pattern(self, words):
        """助動詞パターンを検出"""
        modal_verbs = self.rules_data.get("modal_verbs", ["will", "would", "can", "could"])
        
        for i, word in enumerate(words):
            if word.lower() in modal_verbs:
                subject = " ".join(words[:i]) if i > 0 else "I"
                
                # modal + have + past participle パターン
                if i + 2 < len(words) and words[i+1].lower() == "have":
                    return {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'modal-perfect'}],
                        'Aux': [{'value': f"{word} have", 'type': 'modal_perfect', 'rule_id': 'modal-perfect'}],
                        'V': [{'value': words[i+2], 'type': 'past_participle', 'rule_id': 'modal-perfect'}]
                    }
                
                # 基本的な modal + verb パターン
                if i + 1 < len(words):
                    return {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'modal-basic'}],
                        'Aux': [{'value': word, 'type': 'modal_verb', 'rule_id': 'modal-basic'}],
                        'V': [{'value': words[i+1], 'type': 'base_verb', 'rule_id': 'modal-basic'}]
                    }
        
        return None
    
    def detect_passive_pattern(self, words):
        """受動態パターンを検出"""
        be_verbs = ["is", "are", "was", "were", "am", "be", "been", "being"]
        
        for i, word in enumerate(words):
            if word.lower() in be_verbs and i + 1 < len(words):
                # be + past participle パターンを検出
                next_word = words[i+1]
                if self.looks_like_past_participle(next_word):
                    subject = " ".join(words[:i]) if i > 0 else "it"
                    
                    return {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'passive'}],
                        'Aux': [{'value': word, 'type': 'be_verb', 'rule_id': 'passive'}], 
                        'V': [{'value': next_word, 'type': 'past_participle', 'rule_id': 'passive'}]
                    }
        
        return None
    
    def looks_like_past_participle(self, word):
        """過去分詞らしい語かチェック（簡易版）"""
        word = word.lower()
        
        # 規則変化 (-ed)
        if word.endswith('ed'):
            return True
            
        # よく使われる不規則過去分詞
        irregular_past_participles = [
            'written', 'taken', 'given', 'made', 'done', 'seen', 'known',
            'broken', 'spoken', 'chosen', 'driven', 'eaten', 'fallen'
        ]
        
        return word in irregular_past_participles
    
    def detect_be_verb_pattern(self, words):
        """be動詞パターンを検出"""
        be_verbs = ["am", "is", "are", "was", "were"]
        
        for i, word in enumerate(words):
            if word.lower() in be_verbs:
                subject = " ".join(words[:i]) if i > 0 else "I"
                complement = " ".join(words[i+1:]) if i + 1 < len(words) else ""
                
                return {
                    'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'be-verb'}],
                    'V': [{'value': word, 'type': 'be_verb', 'rule_id': 'be-verb'}],
                    'C': [{'value': complement, 'type': 'complement', 'rule_id': 'be-verb'}] if complement else []
                }
        
        return None
    
    def detect_basic_svo_pattern(self, words):
        """基本的なSVOパターンを検出"""
        if len(words) < 2:
            return None
            
        # 最初の語を主語、2番目を動詞と仮定
        subject = words[0]
        verb = words[1]
        object_part = " ".join(words[2:]) if len(words) > 2 else ""
        
        result = {
            'S': [{'value': subject, 'type': 'subject', 'rule_id': 'basic-svo'}],
            'V': [{'value': verb, 'type': 'verb', 'rule_id': 'basic-svo'}]
        }
        
        if object_part:
            result['O1'] = [{'value': object_part, 'type': 'object', 'rule_id': 'basic-svo'}]
            
        return result


def test_parsing_engine():
    """Parsing Engineのテスト"""
    print("=== Rephrase Parsing Engine テスト ===")
    
    engine = RephraseParsingEngine()
    
    test_sentences = [
        # 基本パターン
        "I run fast",
        "She is happy", 
        "I will go",
        
        # 助動詞パターン
        "I could have done it",
        "She must have finished",
        
        # 受動態パターン  
        "The book is written by John",
        "The window was broken",
        
        # 認知動詞 + that節
        "I think that he is smart",
        "She believes that we are ready",
        "I know what he thinks",
        
        # 複合パターン
        "I think that the book should be written",
        "She believes that I could have done better",
    ]
    
    for sentence in test_sentences:
        print(f"\n入力: {sentence}")
        try:
            slots = engine.analyze_sentence(sentence)
            
            if not slots:
                print("  ❌ スロットが検出されませんでした")
                continue
                
            for slot, candidates in slots.items():
                if candidates:
                    candidate = candidates[0]
                    value = candidate['value']
                    note = candidate.get('note', candidate.get('type', ''))
                    rule_id = candidate.get('rule_id', '')
                    
                    print(f"  {slot}: {value} ({note}) [rule: {rule_id}]")
                    
                    # サブスロット情報があれば表示
                    if 'subslots' in candidate and candidate['subslots']:
                        for sub_slot, sub_value in candidate['subslots'].items():
                            print(f"    └─ {sub_slot}: {sub_value}")
                            
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_parsing_engine()
