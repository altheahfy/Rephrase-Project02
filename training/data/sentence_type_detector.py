#!/usr/bin/env python3
"""
Phase 1.2: 文型認識エンジン（基本版）
既存システムに影響を与えない独立したクラスとして実装
"""

class SentenceTypeDetector:
    """
    文型認識エンジン (基本版)
    肯定文と疑問文の基本的な区別を行う
    """
    
    def __init__(self):
        """初期化"""
        self.wh_words = {'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whose'}
        self.auxiliary_verbs = {'do', 'does', 'did', 'will', 'would', 'can', 'could', 
                               'may', 'might', 'must', 'should', 'shall', 'be', 'am', 
                               'is', 'are', 'was', 'were', 'have', 'has', 'had'}
    
    def detect_sentence_type(self, sentence: str) -> str:
        """
        文型を判定
        
        Args:
            sentence: 入力文
            
        Returns:
            str: 'wh_question', 'yes_no_question', 'statement'
        """
        sentence_lower = sentence.lower().strip()
        words = sentence_lower.split()
        
        if not words:
            return 'statement'
        
        # wh疑問文の判定
        if self._is_wh_question(words):
            return 'wh_question'
        
        # yes/no疑問文の判定
        if self._is_yes_no_question(words, sentence):
            return 'yes_no_question'
        
        # デフォルトは肯定文
        return 'statement'
    
    def _is_wh_question(self, words: list) -> bool:
        """wh疑問文の判定"""
        # 最初の単語がwh-wordか確認
        if words[0] in self.wh_words:
            return True
        
        # "how many", "how much" などの複合wh-word
        if len(words) >= 2 and words[0] == 'how':
            return True
        
        return False
    
    def _is_yes_no_question(self, words: list, original_sentence: str) -> bool:
        """yes/no疑問文の判定"""
        # 疑問符で終わる場合
        if original_sentence.strip().endswith('?'):
            # 最初の単語が助動詞の場合
            if words[0] in self.auxiliary_verbs:
                return True
        
        # 助動詞倒置の判定（より詳細）
        if words[0] in self.auxiliary_verbs:
            # "Are you...?", "Do you...?", "Can you...?" パターン
            return True
        
        return False
    
    def get_detection_confidence(self, sentence: str) -> float:
        """
        判定の信頼度を返す
        
        Args:
            sentence: 入力文
            
        Returns:
            float: 信頼度 (0.0-1.0)
        """
        sentence_type = self.detect_sentence_type(sentence)
        sentence_lower = sentence.lower().strip()
        words = sentence_lower.split()
        
        if sentence_type == 'wh_question':
            # wh-wordが最初にある場合は高信頼度
            if words and words[0] in self.wh_words:
                return 0.95
            elif words and words[0] == 'how':
                return 0.90
            return 0.75
        
        elif sentence_type == 'yes_no_question':
            # 疑問符 + 助動詞倒置の場合は高信頼度
            if sentence.strip().endswith('?') and words and words[0] in self.auxiliary_verbs:
                return 0.90
            elif words and words[0] in self.auxiliary_verbs:
                return 0.75
            return 0.60
        
        else:  # statement
            # 疑問符がなく、助動詞倒置もない場合は高信頼度
            if not sentence.strip().endswith('?') and (not words or words[0] not in self.auxiliary_verbs):
                return 0.85
            return 0.70

def test_sentence_type_detector():
    """文型認識エンジンのテスト"""
    
    detector = SentenceTypeDetector()
    
    test_cases = [
        # wh疑問文
        ("What did you buy?", "wh_question"),
        ("Who is coming?", "wh_question"),
        ("Where are you going?", "wh_question"),
        ("How many books do you have?", "wh_question"),
        
        # yes/no疑問文
        ("Did you buy it?", "yes_no_question"),
        ("Are you coming?", "yes_no_question"),
        ("Can you help me?", "yes_no_question"),
        ("Will you be there?", "yes_no_question"),
        
        # 肯定文
        ("I bought a book.", "statement"),
        ("You are coming.", "statement"),
        ("The car is red.", "statement"),
        ("He finished his homework.", "statement"),
    ]
    
    print("=== 文型認識エンジン テスト ===")
    print()
    
    correct = 0
    total = len(test_cases)
    
    for sentence, expected in test_cases:
        detected = detector.detect_sentence_type(sentence)
        confidence = detector.get_detection_confidence(sentence)
        
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{sentence}'")
        print(f"   期待: {expected}, 判定: {detected}, 信頼度: {confidence:.2f}")
        
        if detected == expected:
            correct += 1
        print()
    
    accuracy = correct / total * 100
    print(f"📊 文型認識精度: {correct}/{total} = {accuracy:.1f}%")
    
    # 成功基準チェック
    if accuracy >= 80.0:
        print("✅ Phase 1.2成功基準達成 (文型判定精度80%以上)")
    else:
        print("❌ Phase 1.2成功基準未達 (文型判定精度80%未満)")
    
    return accuracy >= 80.0

if __name__ == "__main__":
    test_sentence_type_detector()
