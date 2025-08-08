"""
動詞パターンルール統合版 - Step 5実装
Step 4に加えて頻出動詞パターンルール4個を追加統合
"""

import re
from datetime import datetime

class VerbPatternRuleEngine:
    """動詞パターンルールエンジン（Step 4拡張版）"""
    
    def __init__(self):
        self.simple_rules = []
        self.medium_rules = []
        self.complex_rules = []
        self.verb_pattern_rules = []
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
        
        # Step 4の複雑ルール（正規表現）
        self.complex_rules = [
            self.rule_be_progressive,         # 進行形 (be + Ving)
            self.rule_to_direction_m2,        # to句
            self.rule_for_purpose_m2,         # for句  
            self.rule_from_source_m3,         # from句
            self.rule_if_clause_m2,           # if節
        ]
        
        # Step 5の動詞パターンルール
        self.verb_pattern_rules = [
            self.rule_v_go_intrans,           # go to場所
            self.rule_v_listen_intrans,       # listen to音楽
            self.rule_v_believe_in,           # believe in信念
            self.rule_v_be_exist_loc,         # be at/in場所
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
    
    # === Step 3: 中程度ルール（既存） ===
    
    def rule_subject_pronoun_np(self, word, context):
        """ルール: subject-pronoun-np-front - 主語判定"""
        word_index = context['word_index']
        words = context['words']
        
        # 主語候補の判定
        subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
        subject_nouns = ['tom', 'mary', 'john', 'sarah', 'ken', 'mike', 'lisa']  # 人名例
        
        # 代名詞の主語判定（優先度を上げる）
        if word.lower() in subject_pronouns:
            # 文の最初、またはwh語の後、またはカンマの後
            if (word_index == 0 or 
                (word_index > 0 and words[word_index-1].lower() in ['why', 'what', 'where', 'when', 'how']) or
                (word_index > 0 and words[word_index-1].endswith(',')) or
                self.is_before_main_verb(word_index, words)):
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
            # 前置詞句として判定、次の単語も含める
            next_word = words[word_index + 1]
            context['skip_next'] = True
            return ('M3', 'phrase')
        
        # 前置詞の次の単語をスキップ
        if word_index > 0 and context.get('skip_next'):
            return ('SKIP', 'internal')
        
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
        
        # -ly 副詞（ただし名詞は除外）
        if (word.lower().endswith('ly') and len(word) > 3 and 
            word.lower() not in ['family', 'daily', 'supply', 'apply']):
            return ('M2', 'word')
        
        return None
    
    # === Step 4: 複雑ルール（既存） ===
    
    def rule_be_progressive(self, word, context):
        """ルール: be-progressive - 進行形 (be動詞 + Ving)"""
        sentence = context['sentence']
        word_index = context['word_index']
        words = context['words']
        
        # 進行形パターン: be動詞 + Ving
        be_forms = ['am', 'is', 'are', 'was', 'were']
        
        if word.lower() in be_forms:
            # 次の単語がing形かチェック（現在の単語から2単語後まで）
            for offset in range(1, min(3, len(words) - word_index)):
                check_word = words[word_index + offset]
                if check_word.lower().endswith('ing') and len(check_word) > 4:
                    # 進行形のbe動詞として判定
                    return ('Aux', 'word')
        
        # Ving形の動詞判定
        if word.lower().endswith('ing') and len(word) > 4:
            # 前の単語（1-2語前まで）にbe動詞があるかチェック
            for offset in range(1, min(3, word_index + 1)):
                check_word = words[word_index - offset]
                if check_word.lower() in be_forms:
                    return ('V', 'word')
        
        return None
    
    def rule_to_direction_m2(self, word, context):
        """ルール: to-direction-M2 - to句"""
        sentence = context['sentence']
        word_index = context['word_index']
        words = context['words']
        
        # "to" で始まる方向・目的表現
        if word.lower() == 'to' and word_index + 1 < len(words):
            # to + 場所/目的
            next_word = words[word_index + 1].lower()
            direction_targets = [
                'school', 'home', 'work', 'tokyo', 'america', 'japan',
                'station', 'airport', 'hospital', 'library', 'park',
                'church', 'university', 'college'
            ]
            
            if next_word in direction_targets or next_word == 'the':
                return ('M2', 'phrase')
        
        return None
    
    def rule_for_purpose_m2(self, word, context):
        """ルール: for-purpose-M2 - for句"""
        word_index = context['word_index']
        words = context['words']
        
        # "for" で始まる目的・理由表現  
        if word.lower() == 'for' and word_index + 1 < len(words):
            # for + 目的/期間
            next_word = words[word_index + 1].lower()
            purpose_targets = [
                'dinner', 'lunch', 'breakfast', 'work', 'study', 'fun',
                'me', 'you', 'him', 'her', 'us', 'them',
                'a', 'an', 'the', 'my', 'your', 'his', 'her',
                'years', 'months', 'weeks', 'days', 'hours'
            ]
            
            if next_word in purpose_targets:
                return ('M2', 'phrase')
        
        return None
    
    def rule_from_source_m3(self, word, context):
        """ルール: from-source-M3 - from句"""
        word_index = context['word_index']
        words = context['words']
        
        # "from" で始まる起点表現
        if word.lower() == 'from' and word_index + 1 < len(words):
            # from + 場所/起点
            next_word = words[word_index + 1].lower()
            source_targets = [
                'home', 'school', 'work', 'tokyo', 'america', 'japan',
                'here', 'there', 'station', 'airport', 'library',
                'monday', 'morning', 'yesterday', 'today',
                'the', 'my', 'your', 'his', 'her'
            ]
            
            if next_word in source_targets:
                return ('M3', 'phrase')
        
        return None
    
    def rule_if_clause_m2(self, word, context):
        """ルール: if-clause-as-M2 - if節"""
        sentence = context['sentence']
        
        # if節の検出（条件節）
        if word.lower() == 'if':
            # if節全体を条件として扱う
            return ('M2', 'clause')
        
        return None
    
    # === Step 5: 動詞パターンルール（新規） ===
    
    def rule_v_go_intrans(self, word, context):
        """ルール: V-go-intrans - go to場所"""
        word_index = context['word_index']
        words = context['words']
        
        # go動詞の判定
        if word.lower() in ['go', 'goes', 'went', 'going', 'gone']:
            # 自動詞として処理（toは別途処理）
            return ('V', 'word')
        
        return None
    
    def rule_v_listen_intrans(self, word, context):
        """ルール: V-listen-intrans - listen to音楽"""
        word_index = context['word_index']
        words = context['words']
        
        # listen動詞の判定  
        if word.lower() in ['listen', 'listens', 'listened', 'listening']:
            return ('V', 'word')
        
        return None
    
    def rule_v_believe_in(self, word, context):
        """ルール: V-believe-in - believe in信念"""
        sentence = context['sentence'].lower()
        word_index = context['word_index']
        words = context['words']
        
        # "believe in" 句動詞の検出
        if word.lower() == 'believe' and word_index + 1 < len(words):
            if words[word_index + 1].lower() == 'in':
                # believe in を句動詞として処理、inは跳ばす指示
                context['skip_next'] = True  
                return ('V', 'phrase')  # believe in を1つの句動詞として処理
        
        # inをスキップする処理（デバッグ用に表示は残す）
        if word.lower() == 'in' and context.get('skip_next'):
            return ('SKIP', 'internal')  # スキップ指示
        
        return None
    
    def rule_v_be_exist_loc(self, word, context):
        """ルール: V-be-exist-loc - be at/in場所"""
        word_index = context['word_index']
        words = context['words']
        
        # be動詞の存在動詞用法（進行形と区別）
        if word.lower() in ['am', 'is', 'are', 'was', 'were']:
            # 次の語がing形でない場合の存在・状態動詞
            if word_index + 1 < len(words):
                next_word = words[word_index + 1]
                if not (next_word.lower().endswith('ing') and len(next_word) > 4):
                    # 進行形でなければ存在・状態動詞
                    return ('V', 'word')
        
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
    
    def apply_complex_rules(self, word, context):
        """複雑ルールを適用（正規表現）"""
        for rule_func in self.complex_rules:
            result = rule_func(word, context)
            if result:
                return result
        return None
    
    def apply_verb_pattern_rules(self, word, context):
        """動詞パターンルールを適用"""
        for rule_func in self.verb_pattern_rules:
            result = rule_func(word, context)
            if result:
                return result
        return None
    
    def enhanced_sentence_analysis(self, sentence):
        """ルール統合版文分析（Step 5版）"""
        words = sentence.replace('.', '').replace('?', '').replace('!', '').split()
        results = []
        skip_next = False
        
        for i, word in enumerate(words):
            # スキップ処理
            if skip_next:
                skip_next = False
                continue
                
            # 文脈情報を作成
            context = {
                'word_index': i,
                'words': words,
                'sentence': sentence
            }
            
            # Step 5: 動詞パターンルールを試行（高優先度）
            rule_result = self.apply_verb_pattern_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                if slot == 'SKIP':
                    continue
                
                # 句動詞の場合は複合形で表示
                display_word = word
                if phrase_type == 'phrase' and context.get('skip_next'):
                    if i + 1 < len(words):
                        display_word = f"{word} {words[i+1]}"
                
                results.append((slot, display_word, phrase_type))
                print(f"   🎪 動詞パターン: '{display_word}' → {slot}({phrase_type})")
                # スキップフラグの確認
                if context.get('skip_next'):
                    skip_next = True
                continue
            
            # Step 4: 複雑ルールを試行
            rule_result = self.apply_complex_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                results.append((slot, word, phrase_type))
                print(f"   ⚡ 複雑ルール: '{word}' → {slot}({phrase_type})")
                continue
            
            # Step 3: 中程度ルールを試行
            rule_result = self.apply_medium_rules(word, context)
            if rule_result:
                slot, phrase_type = rule_result
                if slot == 'SKIP':
                    continue
                    
                # 前置詞句の場合は複合形で表示
                display_word = word
                if phrase_type == 'phrase' and context.get('skip_next'):
                    if i + 1 < len(words):
                        display_word = f"{word} {words[i+1]}"
                
                results.append((slot, display_word, phrase_type))
                print(f"   🔥 中程度ルール: '{display_word}' → {slot}({phrase_type})")
                # スキップフラグの確認
                if context.get('skip_next'):
                    skip_next = True
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


def test_verb_pattern_rules():
    """動詞パターンルールテスト"""
    engine = VerbPatternRuleEngine()
    
    test_sentences = [
        "I go to school every day.",          # V-go-intrans + to句
        "She listens to music.",              # V-listen-intrans + to句
        "We believe in God.",                 # V-believe-in 句動詞
        "Tom is at home.",                    # V-be-exist-loc 存在動詞
        "They are studying English.",         # 進行形（既存機能確認）
        "Why do you go to work?",             # 複合: 疑問詞+go+to句
    ]
    
    print("🧪 動詞パターンルール統合テスト開始 (Step 5)")
    print("=" * 60)
    
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
    test_verb_pattern_rules()
