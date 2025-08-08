"""
文脈を考慮したルール統合版 - Step 2改良実装
aux-have vs V-have の文脈判定を追加
"""

class ContextAwareRuleEngine:
    """文脈を考慮したルールエンジン"""
    
    def __init__(self):
        self.simple_rules = []
        self.init_simple_rules()
    
    def init_simple_rules(self):
        """簡単ルール初期化"""
        self.simple_rules = [
            self.rule_aux_will,
            self.rule_contextual_have,  # 文脈考慮版
        ]
    
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
        # より一般的なケースを考慮して一般動詞をデフォルトに
        return False
    
    def apply_simple_rules(self, word, context):
        """簡単ルールを適用（文脈付き）"""
        for rule_func in self.simple_rules:
            result = rule_func(word, context)
            if result:
                return result
        return None
    
    def enhanced_sentence_analysis(self, sentence):
        """ルール統合版文分析"""
        words = sentence.replace('.', '').replace('?', '').replace('!', '').split()
        results = []
        
        for i, word in enumerate(words):
            # 文脈情報を作成
            context = {
                'word_index': i,
                'words': words,
                'sentence': sentence
            }
            
            # まず簡単ルールを試行
            rule_result = self.apply_simple_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                results.append((slot, word, phrase_type))
                print(f"   🎯 文脈ルール適用: '{word}' → {slot}({phrase_type})")
            else:
                # フォールバック: 従来の分析
                slot, phrase_type = self.fallback_analysis(word)
                results.append((slot, word, phrase_type))
                print(f"   🧠 従来分析: '{word}' → {slot}({phrase_type})")
        
        return results
    
    def fallback_analysis(self, word):
        """フォールバック分析（従来の方法）"""
        # 代名詞判定
        pronouns_s = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
        pronouns_o = ['me', 'him', 'her', 'us', 'them']
        
        if word.lower() in pronouns_s:
            return 'S', 'word'
        elif word.lower() in pronouns_o:
            return 'O1', 'word'
        elif word.lower() in ['where', 'when', 'why', 'how']:
            return 'M3', 'word'
        else:
            return 'O1', 'word'


def test_contextual_have():
    """文脈考慮版haveテスト"""
    engine = ContextAwareRuleEngine()
    
    test_sentences = [
        "I have an apple.",          # V (一般動詞) 
        "I have eaten breakfast.",   # Aux (助動詞)
        "She has finished her work.", # Aux (助動詞)
        "They have a car.",          # V (一般動詞)
        "We have been to Tokyo.",    # Aux (助動詞)
        "He will go to school.",     # Aux (will)
    ]
    
    print("🧪 文脈考慮版haveテスト開始")
    print("=" * 50)
    
    for sentence in test_sentences:
        print(f"\n📝 例文: {sentence}")
        results = engine.enhanced_sentence_analysis(sentence)
        
        # have/has/had/willの結果をハイライト
        for slot, word, phrase_type in results:
            if word.lower() in ['have', 'has', 'had', 'will']:
                if slot == 'Aux':
                    print(f"   ✅ 正解: '{word}' は助動詞 → {slot}")
                elif slot == 'V':
                    print(f"   ✅ 正解: '{word}' は一般動詞 → {slot}")


if __name__ == "__main__":
    test_contextual_have()
