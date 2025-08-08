"""
中程度ルール統合版 - Step 3実装
Step 2の文脈考慮版に中程度ルール5個を追加統合
"""

import re
from datetime import datetime

class MediumRuleEngine:
    """中程度ルールエンジン（Step 2拡張版）"""
    
    def __init__(self):
        self.simple_rules = []
        self.medium_rules = []
        self.init_all_rules()
    
    def init_all_rules(self):
        """すべてのルール初期化"""
        # Step 2の簡単ルール
        self.simple_rules = [
            self.rule_aux_will,
            self.rule_contextual_have,
        ]
        
        # Step 3の中程度ルール（優先度順）
        self.medium_rules = [
            self.rule_wh_why_front,           # 疑問詞最優先
            self.rule_subject_pronoun_np,     # 主語判定
            self.rule_time_m3,                # 時間表現
            self.rule_place_m3,               # 場所表現
            self.rule_manner_degree_m2,       # 様態副詞
        ]
    
    # === Step 2: 簡単ルール（既存） ===
    
    def rule_aux_will(self, word, context):
        """ルール: aux-will"""
        if word.lower() == 'will':
            return ('Aux', 'word')
        return None
    
    def rule_contextual_have(self, word, context):
        """ルール: 文脈考慮版have判定"""
        if word.lower() not in ['has', 'have', 'had']:
            return None
        
        # 文脈分析
        word_index = context['word_index']
        words = context['words']
        
        # 助動詞パターンの判定
        if self.is_auxiliary_have(word, word_index, words):
            return ('Aux', 'word')
        else:
            return ('V', 'word')
    
    def is_auxiliary_have(self, word, word_index, words):
        """haveが助動詞かどうかを文脈から判定"""
        
        # 1. 次の単語が過去分詞形かチェック
        if word_index + 1 < len(words):
            next_word = words[word_index + 1].lower()
            
            # 明らかな過去分詞パターン
            past_participle_patterns = [
                'been', 'done', 'seen', 'gone', 'taken', 'given', 'made', 
                'eaten', 'written', 'spoken', 'broken', 'chosen', 'driven',
                'found', 'bought', 'thought', 'brought', 'taught', 'caught',
                'finished', 'started', 'decided', 'arrived', 'studied'
            ]
            
            # -ed で終わる規則動詞の過去分詞
            if next_word.endswith('ed') and len(next_word) > 3:
                return True
                
            # 不規則動詞の過去分詞
            if next_word in past_participle_patterns:
                return True
        
        # 2. 一般動詞パターンの判定
        if word_index + 1 < len(words):
            next_word = words[word_index + 1].lower()
            
            # 明らかに目的語になる単語（冠詞、名詞など）
            direct_object_indicators = [
                'a', 'an', 'the', 'my', 'your', 'his', 'her', 'our', 'their',
                'some', 'many', 'much', 'apple', 'book', 'car', 'house', 'dog',
                'cat', 'money', 'time', 'problem', 'idea', 'question'
            ]
            
            if next_word in direct_object_indicators:
                return False  # 一般動詞
        
        # 3. デフォルト判定（文脈が不明確な場合）
        return False
    
    # === Step 3: 中程度ルール（新規） ===
    
    def rule_subject_pronoun_np(self, word, context):
        """ルール: subject-pronoun-np-front - 主語判定"""
        word_index = context['word_index']
        words = context['words']
        
        # 主語候補の判定
        subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
        subject_nouns = ['tom', 'mary', 'john', 'sarah', 'ken', 'mike', 'lisa']  # 人名例
        
        # 代名詞の主語判定
        if word.lower() in subject_pronouns:
            # 文の最初または動詞の前にある場合
            if word_index == 0 or self.is_before_main_verb(word_index, words):
                return ('S', 'word')
        
        # 固有名詞の主語判定
        if word.lower() in subject_nouns or word[0].isupper():
            if word_index == 0 or self.is_before_main_verb(word_index, words):
                return ('S', 'word')
        
        return None
    
    def rule_wh_why_front(self, word, context):
        """ルール: wh-why-front - 疑問詞why"""
        # 疑問詞全般の判定（優先度を上げる）
        wh_words = ['why', 'what', 'where', 'when', 'how', 'who', 'which']
        if word.lower() in wh_words and context['word_index'] == 0:
            return ('M3', 'word')
        return None
    
    def rule_time_m3(self, word, context):
        """ルール: time-M3 - 時間表現"""
        words = context['words']
        word_index = context['word_index']
        
        # 個別の時間単語判定
        time_words = [
            'yesterday', 'today', 'tomorrow', 'morning', 'afternoon', 'evening', 'night',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'week', 'month', 'year', 'ago'
        ]
        
        if word.lower() in time_words:
            return ('M3', 'word')
        
        # 複合時間表現の検出
        if word.lower() == 'last' and word_index + 1 < len(words):
            if words[word_index + 1].lower() in ['night', 'week', 'month', 'year']:
                return ('M3', 'phrase')
        
        if word.lower() == 'this' and word_index + 1 < len(words):
            if words[word_index + 1].lower() in ['morning', 'afternoon', 'evening', 'weekend']:
                return ('M3', 'phrase')
        
        if word.lower() == 'next' and word_index + 1 < len(words):
            if words[word_index + 1].lower() in ['week', 'month', 'year']:
                return ('M3', 'phrase')
        
        return None
    
    def rule_place_m3(self, word, context):
        """ルール: place-M3 - 場所表現"""
        sentence = context['sentence'].lower()
        word_index = context['word_index']
        words = context['words']
        
        # 前置詞による場所表現
        if word.lower() in ['on', 'in', 'under', 'by', 'at'] and word_index + 1 < len(words):
            # 前置詞句として判定
            return ('M3', 'phrase')
        
        return None
    
    def rule_manner_degree_m2(self, word, context):
        """ルール: manner-degree-M2 - 様態・程度副詞"""
        # 様態副詞パターン
        manner_adverbs = [
            'quickly', 'slowly', 'carefully', 'quietly', 'loudly',
            'well', 'badly', 'hard', 'fast', 'early', 'late',
            'very', 'quite', 'really', 'extremely', 'fairly'
        ]
        
        if word.lower() in manner_adverbs:
            return ('M2', 'word')
        
        # -ly 副詞
        if word.lower().endswith('ly') and len(word) > 3:
            return ('M2', 'word')
        
        return None
    
    # === ヘルパーメソッド ===
    
    def is_before_main_verb(self, word_index, words):
        """主動詞の前にあるかチェック"""
        main_verbs = [
            'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did',
            'go', 'goes', 'went', 'come', 'comes', 'came',
            'see', 'sees', 'saw', 'get', 'gets', 'got'
        ]
        
        for i in range(word_index + 1, len(words)):
            if words[i].lower() in main_verbs:
                return True
        return False
    
    # === メイン分析エンジン ===
    
    def apply_simple_rules(self, word, context):
        """簡単ルールを適用（文脈付き）"""
        for rule_func in self.simple_rules:
            result = rule_func(word, context)
            if result:
                return result
        return None
    
    def apply_medium_rules(self, word, context):
        """中程度ルールを適用"""
        for rule_func in self.medium_rules:
            result = rule_func(word, context)
            if result:
                return result
        return None
    
    def enhanced_sentence_analysis(self, sentence):
        """ルール統合版文分析（Step 3版）"""
        words = sentence.replace('.', '').replace('?', '').replace('!', '').split()
        results = []
        
        for i, word in enumerate(words):
            # 文脈情報を作成
            context = {
                'word_index': i,
                'words': words,
                'sentence': sentence
            }
            
            # Step 3: 中程度ルールを試行（優先）
            rule_result = self.apply_medium_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                results.append((slot, word, phrase_type))
                print(f"   🔥 中程度ルール: '{word}' → {slot}({phrase_type})")
                continue
            
            # Step 2: 簡単ルールを試行
            rule_result = self.apply_simple_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                results.append((slot, word, phrase_type))
                print(f"   🎯 簡単ルール: '{word}' → {slot}({phrase_type})")
                continue
            
            # フォールバック: 従来の分析
            slot, phrase_type = self.fallback_analysis(word)
            results.append((slot, word, phrase_type))
            print(f"   🧠 従来分析: '{word}' → {slot}({phrase_type})")
        
        return results
    
    def fallback_analysis(self, word):
        """フォールバック分析（従来の方法）"""
        # 代名詞判定
        pronouns_o = ['me', 'him', 'her', 'us', 'them']
        
        if word.lower() in pronouns_o:
            return 'O1', 'word'
        elif word.lower() in ['where', 'when', 'what', 'how']:
            return 'M3', 'word'
        else:
            return 'O1', 'word'


def test_medium_rules():
    """中程度ルールテスト"""
    engine = MediumRuleEngine()
    
    test_sentences = [
        "I have an apple.",                    # S:I, V:have
        "Why do you study English?",          # M3:Why, S:you
        "She came here yesterday morning.",   # S:She, M3:yesterday morning
        "Tom lives in Tokyo.",                # S:Tom, M3:in Tokyo
        "We work very hard.",                 # S:We, M2:very, M2:hard
        "They will go to school quickly.",   # S:They, Aux:will, M2:to school, M2:quickly
    ]
    
    print("🧪 中程度ルール統合テスト開始 (Step 3)")
    print("=" * 55)
    
    for sentence in test_sentences:
        print(f"\\n📝 例文: {sentence}")
        results = engine.enhanced_sentence_analysis(sentence)
        
        # 重要な結果をサマリー
        key_slots = {}
        for slot, word, phrase_type in results:
            if slot not in key_slots:
                key_slots[slot] = []
            key_slots[slot].append(word)
        
        print(f"   📊 検出結果: {dict(key_slots)}")


if __name__ == "__main__":
    test_medium_rules()
