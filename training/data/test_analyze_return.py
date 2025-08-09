import sys
sys.path.append('.')
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

# 単純テスト
engine = CompleteRephraseParsingEngine()

class TestAnalyzer:
    def __init__(self):
        self.engine = engine
        self.current_sentence_id = 1
        self.current_construction_id = 1000
        self.vgroup_data = {}
    
    def analyze_and_add_sentence(self, sentence, v_group_key=None):
        """修正版analyze_and_add_sentence"""
        sentence = sentence.strip()
        if not sentence:
            print("❌ 空文字列")
            return False
            
        print(f"\n=== テスト解析: {sentence} ===")
        
        # 品詞分解実行
        slots = self.engine.analyze_sentence(sentence)
        print(f"🔍 slots結果: {type(slots)}")
        print(f"🔍 slots内容: {bool(slots)}")
        
        if not slots:
            print(f"❌ 解析失敗: {sentence}")
            return False
            
        print("✅ 解析成功 - return True")
        return True

# テスト実行
test = TestAnalyzer()
sentence = "He has recovered quickly from a serious injury."
result = test.analyze_and_add_sentence(sentence)
print(f"\n🎯 最終結果: {result}")
