"""
Step 8統合版 - 第4文型・第5文型対応
Step 6をベースに第4文型(SVOO)と第5文型(SVOC)を安全に追加
"""

import re
from datetime import datetime

class Step8RuleEngine:
    """Step 8ルールエンジン（第4・第5文型対応版）"""
    
    def __init__(self):
        self.simple_rules = []
        self.medium_rules = []
        self.complex_rules = []
        self.verb_pattern_rules = []
        self.final_special_rules = []
        self.ditransitive_rules = []      # 第4文型
        self.causative_rules = []         # 第5文型
        self.init_all_rules()
    
    def init_all_rules(self):
        """すべてのルール初期化（Step 8版）"""
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
        
        # Step 6の最終特殊ルール
        self.final_special_rules = [
            self.rule_v_recover_intrans,      # recover from病気
            self.rule_v_leave_intrans,        # leave for東京
            self.rule_v_pay_intrans,          # pay for本
            self.rule_v_apologize_intrans,    # apologize to/for
            self.rule_v_rain_weather,         # It rains
        ]
        
        # Step 8の新規ルール
        self.ditransitive_rules = [
            self.rule_ditransitive_give,      # 第4文型: S V O1 O2
        ]
        
        self.causative_rules = [
            self.rule_causative_make,         # 第5文型: S V O1 C2
        ]

    # ======================
    # Step 2: 簡単ルール（Step 6から継承）
    # ======================
    def rule_aux_will(self, words):
        """助動詞will検出"""
        result = {}
        for i, word in enumerate(words):
            if word.lower() in ['will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must']:
                result['Aux'] = result.get('Aux', []) + [word]
        return result

    def rule_contextual_have(self, words):
        """文脈的have判定"""
        result = {}
        for i, word in enumerate(words):
            if word.lower() in ['have', 'has', 'had']:
                # 次の語が過去分詞なら助動詞、そうでなければ一般動詞
                if i + 1 < len(words):
                    next_word = words[i + 1].lower()
                    if next_word.endswith('ed') or next_word in ['gone', 'been', 'done', 'seen', 'taken']:
                        result['Aux'] = result.get('Aux', []) + [word]
                    else:
                        result['V'] = result.get('V', []) + [word]
                else:
                    result['V'] = result.get('V', []) + [word]
        return result

    # ======================
    # Step 3: 中程度ルール（Step 6から継承）
    # ======================
    def rule_wh_why_front(self, words):
        """疑問詞Why優先処理"""
        result = {}
        wh_words = ['why', 'when', 'where', 'how', 'what', 'who', 'which', 'whose']
        
        for word in words:
            if word.lower() in wh_words:
                if word.lower() == 'why':
                    result['M3'] = result.get('M3', []) + [word]
                elif word.lower() in ['when']:
                    result['M3'] = result.get('M3', []) + [word]
                elif word.lower() in ['where']:
                    result['M3'] = result.get('M3', []) + [word]
                elif word.lower() in ['how']:
                    result['M2'] = result.get('M2', []) + [word]
                else:
                    result['O1'] = result.get('O1', []) + [word]
        return result

    def rule_subject_pronoun_np(self, words):
        """主語代名詞・名詞句判定"""
        result = {}
        subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'tom', 'mary', 'john']
        
        for word in words:
            if word.lower() in subject_pronouns:
                result['S'] = result.get('S', []) + [word]
        return result

    def rule_time_m3(self, words):
        """時間表現検出"""
        result = {}
        time_words = ['today', 'tomorrow', 'yesterday', 'now', 'then', 'morning', 'evening', 'night']
        
        # 句レベルの時間表現検出
        text = ' '.join(words)
        time_patterns = [
            r'\bevery\s+day\b',
            r'\blast\s+week\b', 
            r'\bnext\s+month\b',
            r'\bin\s+the\s+morning\b',
            r'\bat\s+night\b'
        ]
        
        for pattern in time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                matched_phrase = match.group()
                result['M3'] = result.get('M3', []) + [matched_phrase]
                return result
        
        # 単語レベルの検出
        for word in words:
            if word.lower() in time_words:
                result['M3'] = result.get('M3', []) + [word]
        return result

    def rule_place_m3(self, words):
        """場所表現検出（句動詞対応版）"""
        result = {}
        text = ' '.join(words)
        
        # at homeの特別処理
        if re.search(r'\bat\s+home\b', text, re.IGNORECASE):
            result['M3'] = result.get('M3', []) + ['at home']
            return result
            
        place_words = ['home', 'school', 'work', 'office', 'park', 'station', 'hospital']
        
        for word in words:
            if word.lower() in place_words:
                result['M3'] = result.get('M3', []) + [word]
        return result

    def rule_manner_degree_m2(self, words):
        """様態・程度副詞検出"""
        result = {}
        manner_words = ['quickly', 'slowly', 'carefully', 'loudly', 'quietly', 'well', 'hard']
        
        for word in words:
            if word.lower() in manner_words:
                result['M2'] = result.get('M2', []) + [word]
        return result

    # ======================
    # Step 4-6のルール（簡略化して継承）
    # ======================
    def rule_be_progressive(self, words):
        """be動詞+Ving進行形検出"""
        result = {}
        text = ' '.join(words)
        
        progressive_pattern = r'\b(am|is|are|was|were)\s+(\w+ing)\b'
        matches = re.finditer(progressive_pattern, text, re.IGNORECASE)
        
        for match in matches:
            be_verb = match.group(1)
            ving_verb = match.group(2)
            result['Aux'] = result.get('Aux', []) + [be_verb]
            result['V'] = result.get('V', []) + [ving_verb]
            
        return result

    def rule_to_direction_m2(self, words):
        """to句の方向性検出"""
        result = {}
        text = ' '.join(words)
        
        to_patterns = [
            r'\bto\s+school\b',
            r'\bto\s+work\b',
            r'\bto\s+home\b',
            r'\bto\s+the\s+\w+\b'
        ]
        
        for pattern in to_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                result['M2'] = result.get('M2', []) + ['to']
                break
        return result

    def rule_for_purpose_m2(self, words):
        """for句の目的検出"""
        result = {}
        text = ' '.join(words)
        
        for_pattern = r'\bfor\s+\w+'
        matches = re.finditer(for_pattern, text, re.IGNORECASE)
        
        for match in matches:
            result['M2'] = result.get('M2', []) + ['for']
            break
        return result

    def rule_from_source_m3(self, words):
        """from句の起点検出"""
        result = {}
        text = ' '.join(words)
        
        from_pattern = r'\bfrom\s+\w+'
        matches = re.finditer(from_pattern, text, re.IGNORECASE)
        
        for match in matches:
            result['M3'] = result.get('M3', []) + ['from']
            break
        return result

    def rule_if_clause_m2(self, words):
        """if節検出"""
        result = {}
        text = ' '.join(words)
        
        if re.search(r'\bif\s+', text, re.IGNORECASE):
            result['M2'] = result.get('M2', []) + ['if']
            
        return result

    # 動詞パターンルールと特殊ルールは簡略化（既存ルール）
    def rule_v_go_intrans(self, words):
        """go to場所パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\bgo\s+to\b', text, re.IGNORECASE):
            for word in words:
                if word.lower() == 'go':
                    result['V'] = result.get('V', []) + [word]
                    break
        return result

    def rule_v_listen_intrans(self, words):
        """listen to音楽パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\blisten\s+to\b', text, re.IGNORECASE):
            for word in words:
                if word.lower() in ['listen', 'listens', 'listening']:
                    result['V'] = result.get('V', []) + [word]
                    break
        return result

    def rule_v_believe_in(self, words):
        """believe in信念パターン"""
        result = {}
        text = ' '.join(words)
        believe_pattern = r'\bbelieve\s+in\b'
        if re.search(believe_pattern, text, re.IGNORECASE):
            result['V'] = result.get('V', []) + ['believe in']
        return result

    def rule_v_be_exist_loc(self, words):
        """be動詞存在・場所パターン"""
        result = {}
        be_verbs = ['am', 'is', 'are', 'was', 'were']
        for word in words:
            if word.lower() in be_verbs:
                result['V'] = result.get('V', []) + [word]
        return result

    def rule_v_recover_intrans(self, words):
        """recover from病気パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\brecover\w*\s+from\b', text, re.IGNORECASE):
            for word in words:
                if word.lower().startswith('recover'):
                    result['V'] = result.get('V', []) + [word]
                    break
            from_match = re.search(r'\bfrom\s+(.+)', text, re.IGNORECASE)
            if from_match:
                from_phrase = from_match.group(0)
                result['M3'] = result.get('M3', []) + [from_phrase]
        return result

    def rule_v_leave_intrans(self, words):
        """leave for東京パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\bleave?\w*\s+for\b', text, re.IGNORECASE):
            for word in words:
                if word.lower().startswith('le') and 'leave' in word.lower():
                    result['V'] = result.get('V', []) + [word]
                    break
            for_match = re.search(r'\bfor\s+([^.]+)', text, re.IGNORECASE)
            if for_match:
                for_phrase = for_match.group(0).rstrip('.')
                result['M2'] = result.get('M2', []) + [for_phrase]
        return result

    def rule_v_pay_intrans(self, words):
        """pay for本パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\bpai?d?\w*\s+for\b', text, re.IGNORECASE):
            for word in words:
                if word.lower().startswith('pai') or word.lower() == 'paid':
                    result['V'] = result.get('V', []) + [word]
                    break
            for_match = re.search(r'\bfor\s+([^.]+)', text, re.IGNORECASE)
            if for_match:
                for_phrase = for_match.group(0).rstrip('.')
                result['M2'] = result.get('M2', []) + [for_phrase]
        return result

    def rule_v_apologize_intrans(self, words):
        """apologize to/for パターン"""
        result = {}
        text = ' '.join(words)
        if re.search(r'\bapologi\w+\s+(to|for)\b', text, re.IGNORECASE):
            for word in words:
                if word.lower().startswith('apolog'):
                    result['V'] = result.get('V', []) + [word]
                    break
            prep_match = re.search(r'\b(to|for)\s+([^.]+)', text, re.IGNORECASE)
            if prep_match:
                prep_phrase = prep_match.group(0).rstrip('.')
                result['M2'] = result.get('M2', []) + [prep_phrase]
        return result

    def rule_v_rain_weather(self, words):
        """It rains天気パターン"""
        result = {}
        text = ' '.join(words).lower()
        if re.search(r'\brain\w*', text):
            for word in words:
                if word.lower() == 'it':
                    result['S'] = result.get('S', []) + [word]
                elif word.lower().startswith('rain'):
                    result['V'] = result.get('V', []) + [word]
        return result

    # ======================
    # Step 8: 新規ルール
    # ======================
    def rule_ditransitive_give(self, words):
        """第4文型: S V O1 O2 (give系)"""
        result = {}
        text = ' '.join(words)
        
        # give系動詞の検出
        give_verbs = ['give', 'gives', 'gave', 'given', 'giving',
                     'show', 'shows', 'showed', 'shown', 'showing',
                     'tell', 'tells', 'told', 'telling']
        
        found_verb = None
        verb_index = -1
        
        for i, word in enumerate(words):
            if word.lower() in give_verbs:
                result['V'] = result.get('V', []) + [word]
                found_verb = word.lower()
                verb_index = i
                break
        
        if found_verb and verb_index >= 0:
            # 第4文型パターン: V + O1(人) + O2(物)
            remaining_words = words[verb_index + 1:]
            
            if len(remaining_words) >= 2:
                # O1 (受益者・人)
                o1 = remaining_words[0]
                result['O1'] = result.get('O1', []) + [o1]
                
                # O2 (与えるもの・物) - 残りの語
                o2_words = []
                for word in remaining_words[1:]:
                    # 前置詞や修飾語で終了
                    if word.lower() in ['to', 'from', 'at', 'in', 'on', 'for', 'with']:
                        break
                    o2_words.append(word)
                
                if o2_words:
                    if len(o2_words) == 1:
                        result['O2'] = result.get('O2', []) + o2_words
                    else:
                        o2_phrase = ' '.join(o2_words)
                        result['O2'] = result.get('O2', []) + [o2_phrase]
                        
        return result

    def rule_causative_make(self, words):
        """第5文型: S V O1 C2 (make系)"""
        result = {}
        text = ' '.join(words)
        
        # make系動詞の検出
        make_verbs = ['make', 'makes', 'made', 'making']
        
        found_verb = None
        verb_index = -1
        
        for i, word in enumerate(words):
            if word.lower() in make_verbs:
                result['V'] = result.get('V', []) + [word]
                found_verb = word.lower()
                verb_index = i
                break
        
        if found_verb and verb_index >= 0:
            # 第5文型パターン: V + O1(人) + C2(補語)
            remaining_words = words[verb_index + 1:]
            
            if len(remaining_words) >= 2:
                # O1 (対象・人)
                o1 = remaining_words[0]
                result['O1'] = result.get('O1', []) + [o1]
                
                # C2 (補語) - 残りの語
                c2_words = []
                for word in remaining_words[1:]:
                    # 前置詞で終了
                    if word.lower() in ['to', 'from', 'at', 'in', 'on', 'for', 'with']:
                        break
                    c2_words.append(word)
                
                if c2_words:
                    if len(c2_words) == 1:
                        result['C2'] = result.get('C2', []) + c2_words
                    else:
                        c2_phrase = ' '.join(c2_words)
                        result['C2'] = result.get('C2', []) + [c2_phrase]
                        
        return result

    # ======================
    # メイン処理関数
    # ======================
    def analyze_sentence(self, sentence):
        """文の総合分析（Step 8版）"""
        words = sentence.strip().split()
        result = {}
        
        # 全ルール適用
        all_rule_groups = [
            self.simple_rules,
            self.medium_rules,
            self.complex_rules,
            self.verb_pattern_rules,
            self.final_special_rules,
            self.ditransitive_rules,    # Step 8新規
            self.causative_rules,       # Step 8新規
        ]
        
        for rule_group in all_rule_groups:
            for rule in rule_group:
                rule_result = rule(words)
                for slot, values in rule_result.items():
                    result[slot] = result.get(slot, []) + values
        
        # 未分類要素の処理（改良版）
        used_words = set()
        used_phrases = []
        
        for values in result.values():
            for value in values:
                if ' ' in value:  # 句レベル
                    used_phrases.append(value.lower())
                    for word in value.split():
                        used_words.add(word.lower().rstrip('.,!?'))
                else:  # 単語レベル
                    used_words.add(value.lower().rstrip('.,!?'))
        
        for word in words:
            clean_word = word.rstrip('.,!?').lower()
            if clean_word not in used_words:
                # 句の一部でないかチェック
                is_part_of_phrase = False
                for phrase in used_phrases:
                    if clean_word in phrase.split():
                        is_part_of_phrase = True
                        break
                        
                if not is_part_of_phrase:
                    result['O1'] = result.get('O1', []) + [word]
        
        return result

    def run_test(self):
        """Step 8統合テスト実行"""
        print("🎯 Step 8統合版ルール統合テスト開始 (第4・第5文型対応！)")
        print("=" * 60)
        
        test_sentences = [
            # Step 8の新規テスト例文
            "I give you a book.",              # 第4文型
            "She showed me the picture.",      # 第4文型  
            "He told them the truth.",         # 第4文型
            "I make you happy.",               # 第5文型
            "She made him cry.",               # 第5文型
            
            # 従来例文（一部）
            "He recovered from the illness.",
            "I paid for the book.",
            "We believe in God.",
            "They are studying English.",
        ]
        
        total_rules = 34
        integrated_rules = 23  # Step 8で2個追加: 23/34 = 67.6%
        
        for sentence in test_sentences:
            print(f"\n📝 例文: {sentence}")
            result = self.analyze_sentence(sentence)
            print(f"   📊 検出結果: {result}")
        
        print(f"\n🎊 Step 8完了！")
        print(f"📈 統合率: {integrated_rules}/{total_rules} = {integrated_rules/total_rules*100:.1f}% ✅")
        print(f"🎯 新機能: 第4文型(SVOO) + 第5文型(SVOC)対応！")
        print(f"⚡ 次回: Step 9で更なる統合拡大！")

def main():
    engine = Step8RuleEngine()
    engine.run_test()

if __name__ == "__main__":
    main()
