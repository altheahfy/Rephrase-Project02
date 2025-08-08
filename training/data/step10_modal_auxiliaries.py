"""
Step 10統合版 - Modal Auxiliaries (should, could, might等) 対応
Step 9をベースにモーダル助動詞を安全に追加
"""

import re
from datetime import datetime

class Step10RuleEngine:
    """Step 10ルールエンジン（Modal Auxiliaries対応版）"""
    
    def __init__(self):
        self.simple_rules = []
        self.medium_rules = []
        self.complex_rules = []
        self.verb_pattern_rules = []
        self.final_special_rules = []
        self.ditransitive_rules = []      # 第4文型
        self.causative_rules = []         # 第5文型
        self.copular_rules = []           # 連結動詞
        self.modal_rules = []             # モーダル助動詞 (Step 10新規)
        self.init_all_rules()
    
    def init_all_rules(self):
        """すべてのルール初期化（Step 10版）"""
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
            self.rule_v_listen_intrans,       # listen to
            self.rule_v_believe_in,           # believe in (フレーズ動詞)
            self.rule_v_be_exist_loc,         # be at 場所
            self.rule_v_recover_intrans,      # recover from
            self.rule_v_leave_intrans,        # leave from場所
            self.rule_v_pay_intrans,          # pay for
            self.rule_v_apologize_intrans,    # apologize for
            self.rule_v_rain_weather,         # it rains天候表現
        ]
        
        # Step 6の特殊動詞ルール
        self.final_special_rules = [
        ]
        
        # Step 8の第4文型・第5文型ルール
        self.ditransitive_rules = [
            self.rule_ditransitive_give,      # give型第4文型
        ]
        
        self.causative_rules = [
            self.rule_causative_make,         # make型第5文型
        ]
        
        # Step 9の連結動詞ルール
        self.copular_rules = [
            self.rule_copular_become,         # become型 SVC1パターン
        ]
        
        # Step 10のモーダル助動詞ルール（新規追加）
        self.modal_rules = [
            self.rule_modal_should,           # should型モーダル
            self.rule_modal_could,            # could型モーダル  
            self.rule_modal_might,            # might/may型モーダル
            self.rule_modal_must,             # must型モーダル
        ]

    # ===== Step 2: 基本ルール =====
    
    def rule_aux_will(self, words):
        """助動詞willのルール"""
        results = []
        for i, word in enumerate(words):
            if word.lower() == "will":
                results.append({
                    'position': i,
                    'slot': 'Aux',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'aux-will',
                    'priority': 10
                })
        return results
    
    def rule_contextual_have(self, words):
        """コンテキスト型haveルール（完了形の判定）"""
        results = []
        for i, word in enumerate(words):
            if word.lower() in ['have', 'has', 'had']:
                # 直後に過去分詞らしき語があれば助動詞として扱う
                if i < len(words) - 1:
                    next_word = words[i + 1].lower()
                    # 簡単な過去分詞パターン（-ed, -en, 不規則動詞）
                    if (next_word.endswith('ed') or 
                        next_word.endswith('en') or 
                        next_word in ['done', 'gone', 'seen', 'been', 'taken', 'made', 'said', 'come']):
                        results.append({
                            'position': i,
                            'slot': 'Aux',
                            'value': word,
                            'type': 'word',
                            'rule_id': 'aux-have',
                            'priority': 10,
                            'note': f'完了形助動詞（後続：{next_word}）'
                        })
        return results

    # ===== Step 3: 中程度ルール =====
    
    def rule_wh_why_front(self, words):
        """疑問詞文頭処理（Why優先版）"""
        results = []
        if len(words) > 0:
            first_word = words[0].lower()
            wh_words = {
                'why': 'M2', 'how': 'M2', 'when': 'M3', 'where': 'M3',
                'what': 'O1', 'who': 'S', 'which': 'O1', 'whose': 'S'
            }
            
            if first_word in wh_words:
                slot = wh_words[first_word]
                results.append({
                    'position': 0,
                    'slot': slot,
                    'value': words[0],
                    'type': 'word',
                    'rule_id': f'wh-{first_word}',
                    'priority': 15,  # 高優先度
                    'note': f'疑問詞文頭配置'
                })
        return results
    
    def rule_subject_pronoun_np(self, words):
        """主語代名詞・名詞句判定（複合主語対応）"""
        results = []
        subject_pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that']
        
        for i, word in enumerate(words):
            if word.lower() in subject_pronouns:
                results.append({
                    'position': i,
                    'slot': 'S',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'subject-pronoun',
                    'priority': 8
                })
        
        # 複合主語の検出（the + 名詞）
        for i, word in enumerate(words):
            if word.lower() == 'the' and i < len(words) - 1:
                next_word = words[i + 1]
                # 一般的な名詞
                common_nouns = ['weather', 'music', 'food', 'tree', 'book', 'car', 'house', 
                              'dog', 'cat', 'bird', 'man', 'woman', 'child', 'student', 'teacher']
                if next_word.lower() in common_nouns:
                    results.append({
                        'position': i,
                        'slot': 'S',
                        'value': f'{word} {next_word}',
                        'type': 'phrase',
                        'rule_id': 'subject-the-noun',
                        'priority': 8,
                        'span': 2,
                        'note': '複合主語（the + 名詞）'
                    })
        
        return results
    
    def rule_time_m3(self, words):
        """時間表現のM3判定（複数語対応）"""
        results = []
        
        # 単語レベルの時間表現
        time_words = [
            'today', 'yesterday', 'tomorrow', 'now', 'then', 'soon', 'early', 'late',
            'morning', 'afternoon', 'evening', 'night', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday', 'january', 'february', 'march',
            'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'
        ]
        
        for i, word in enumerate(words):
            if word.lower() in time_words:
                results.append({
                    'position': i,
                    'slot': 'M3',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'time-m3',
                    'priority': 6
                })
        
        # フレーズレベルの時間表現検出
        text = ' '.join(words).lower()
        time_phrases = [
            'at home', 'at school', 'at work', 'at night', 'in the morning',
            'this morning', 'last night', 'next week', 'last week', 'this week'
        ]
        
        for phrase in time_phrases:
            if phrase in text:
                # フレーズの位置を特定
                phrase_words = phrase.split()
                for i in range(len(words) - len(phrase_words) + 1):
                    if [w.lower() for w in words[i:i+len(phrase_words)]] == phrase_words:
                        # 時間関連フレーズのみM3に
                        if phrase in ['at night', 'in the morning', 'this morning', 'last night', 'next week', 'last week', 'this week']:
                            results.append({
                                'position': i,
                                'slot': 'M3',
                                'value': ' '.join(words[i:i+len(phrase_words)]),
                                'type': 'phrase',
                                'rule_id': 'time-phrase-m3',
                                'priority': 7,
                                'span': len(phrase_words)
                            })
                        break
        
        return results
    
    def rule_place_m3(self, words):
        """場所表現のM3判定"""
        results = []
        
        # 基本的な場所の単語
        place_words = ['here', 'there', 'everywhere', 'somewhere', 'anywhere', 'home']
        
        for i, word in enumerate(words):
            if word.lower() in place_words:
                results.append({
                    'position': i,
                    'slot': 'M3',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'place-m3',
                    'priority': 6
                })
        
        return results
    
    def rule_manner_degree_m2(self, words):
        """様態・程度副詞のM2判定"""
        results = []
        
        manner_words = [
            'quickly', 'slowly', 'carefully', 'easily', 'hard', 'fast', 'well', 'badly',
            'very', 'quite', 'really', 'extremely', 'completely', 'almost', 'nearly'
        ]
        
        for i, word in enumerate(words):
            if word.lower() in manner_words:
                results.append({
                    'position': i,
                    'slot': 'M2',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'manner-m2',
                    'priority': 5
                })
        
        return results

    # ===== Step 4: 複雑ルール =====
    
    def rule_be_progressive(self, words):
        """進行形パターン（be動詞 + 動詞ing）"""
        results = []
        
        be_forms = ['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been']
        
        for i, word in enumerate(words):
            if word.lower() in be_forms:
                # 次の語がing形かチェック
                if i < len(words) - 1:
                    next_word = words[i + 1]
                    if next_word.lower().endswith('ing'):
                        # be動詞を助動詞として扱う
                        results.append({
                            'position': i,
                            'slot': 'Aux',
                            'value': word,
                            'type': 'word',
                            'rule_id': 'be-progressive-aux',
                            'priority': 9,
                            'note': f'進行形助動詞（後続：{next_word}）'
                        })
        
        return results
    
    def rule_to_direction_m2(self, words):
        """to句の処理（方向性のM2）"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'to' and i < len(words) - 1:
                # to + 名詞のパターン
                next_word = words[i + 1]
                # 場所を示すto句（学校、家、仕事など）
                place_targets = ['school', 'home', 'work', 'station', 'hospital', 'store', 'park', 'library']
                
                if next_word.lower() in place_targets:
                    results.append({
                        'position': i,
                        'slot': 'M2',
                        'value': f'{word} {next_word}',
                        'type': 'phrase',
                        'rule_id': 'to-direction-m2',
                        'priority': 7,
                        'span': 2
                    })
        
        return results
    
    def rule_for_purpose_m2(self, words):
        """for句の処理（目的のM2）"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'for' and i < len(words) - 1:
                next_word = words[i + 1]
                # for + 目的語のパターン
                results.append({
                    'position': i,
                    'slot': 'M2',
                    'value': f'{word} {next_word}',
                    'type': 'phrase',
                    'rule_id': 'for-purpose-m2',
                    'priority': 6,
                    'span': 2
                })
        
        return results
    
    def rule_from_source_m3(self, words):
        """from句の処理（起点のM3）"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'from' and i < len(words) - 1:
                next_word = words[i + 1]
                results.append({
                    'position': i,
                    'slot': 'M3',
                    'value': f'{word} {next_word}',
                    'type': 'phrase',
                    'rule_id': 'from-source-m3',
                    'priority': 6,
                    'span': 2
                })
        
        return results
    
    def rule_if_clause_m2(self, words):
        """if節の処理（条件のM2）"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'if':
                # if以降を条件句として扱う簡単版
                results.append({
                    'position': i,
                    'slot': 'M2',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'if-condition-m2',
                    'priority': 8
                })
        
        return results

    # ===== Step 5: 動詞パターンルール =====
    
    def rule_v_go_intrans(self, words):
        """go + to句の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'go':
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'v-go-intrans',
                    'priority': 7,
                    'note': '自動詞go（to句期待）'
                })
        
        return results
    
    def rule_v_listen_intrans(self, words):
        """listen + to句の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'listen':
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'v-listen-intrans',
                    'priority': 7,
                    'note': '自動詞listen（to句期待）'
                })
        
        return results
    
    def rule_v_believe_in(self, words):
        """believe in フレーズ動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'believe' and i < len(words) - 1:
                if words[i + 1].lower() == 'in':
                    # フレーズ動詞として処理
                    results.append({
                        'position': i,
                        'slot': 'V',
                        'value': f'{word} {words[i + 1]}',
                        'type': 'phrase',
                        'rule_id': 'v-believe-in',
                        'priority': 8,
                        'span': 2,
                        'note': 'フレーズ動詞believe in'
                    })
        
        return results
    
    def rule_v_be_exist_loc(self, words):
        """be動詞の存在・場所パターン"""
        results = []
        be_forms = ['am', 'is', 'are', 'was', 'were']
        
        for i, word in enumerate(words):
            if word.lower() in be_forms:
                # 進行形ではない場合のbe動詞
                if i < len(words) - 1:
                    next_word = words[i + 1]
                    if not next_word.lower().endswith('ing'):
                        results.append({
                            'position': i,
                            'slot': 'V',
                            'value': word,
                            'type': 'word',
                            'rule_id': 'v-be-exist',
                            'priority': 6,
                            'note': 'be動詞（存在・状態）'
                        })
        
        return results
    
    def rule_v_recover_intrans(self, words):
        """recover from句の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() == 'recover':
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'v-recover-intrans',
                    'priority': 7,
                    'note': '自動詞recover（from句期待）'
                })
        
        return results
    
    def rule_v_leave_intrans(self, words):
        """leave from場所の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() in ['leave', 'left']:
                # from句と組み合わせる場合は自動詞として扱う
                if i < len(words) - 2:
                    if words[i + 1].lower() == 'from':
                        results.append({
                            'position': i,
                            'slot': 'V',
                            'value': word,
                            'type': 'word',
                            'rule_id': 'v-leave-intrans',
                            'priority': 7,
                            'note': '自動詞leave（from句と共に）'
                        })
        
        return results
    
    def rule_v_pay_intrans(self, words):
        """pay for句の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() in ['pay', 'paid']:
                # for句と組み合わせる場合
                if i < len(words) - 2:
                    if words[i + 1].lower() == 'for':
                        results.append({
                            'position': i,
                            'slot': 'V',
                            'value': word,
                            'type': 'word',
                            'rule_id': 'v-pay-intrans',
                            'priority': 7,
                            'note': '自動詞pay（for句と共に）'
                        })
        
        return results
    
    def rule_v_apologize_intrans(self, words):
        """apologize for句の自動詞パターン"""
        results = []
        
        for i, word in enumerate(words):
            if word.lower() in ['apologize', 'apologized']:
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'v-apologize-intrans',
                    'priority': 7,
                    'note': '自動詞apologize（for句期待）'
                })
        
        return results
    
    def rule_v_rain_weather(self, words):
        """天候表現 it rains"""
        results = []
        
        weather_verbs = ['rain', 'rains', 'rained', 'snow', 'snows', 'snowed']
        
        for i, word in enumerate(words):
            if word.lower() in weather_verbs:
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'v-weather',
                    'priority': 7,
                    'note': '天候動詞'
                })
        
        return results

    # ===== Step 8: 第4文型・第5文型ルール =====
    
    def rule_ditransitive_give(self, words):
        """第4文型：give型動詞（S V O1 O2）"""
        results = []
        
        # give型動詞のリスト
        ditransitive_verbs = ['give', 'gave', 'given', 'send', 'sent', 'show', 'showed', 'shown', 
                            'tell', 'told', 'teach', 'taught', 'buy', 'bought', 'bring', 'brought',
                            'lend', 'lent', 'offer', 'offered']
        
        for i, word in enumerate(words):
            if word.lower() in ditransitive_verbs:
                # 基本的にgive型動詞として動詞スロットに配置
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'ditransitive-give',
                    'priority': 8,
                    'note': '第4文型動詞（SVOO可能）',
                    'pattern': 'ditransitive'
                })
                
                # 後続の語をO1, O2として処理（簡単版）
                if i < len(words) - 2:
                    # 直後の語をO1（間接目的語）として候補に
                    next_word = words[i + 1]
                    if next_word.lower() in ['me', 'you', 'him', 'her', 'us', 'them', 'it']:
                        results.append({
                            'position': i + 1,
                            'slot': 'O1',
                            'value': next_word,
                            'type': 'word',
                            'rule_id': 'ditransitive-o1',
                            'priority': 7,
                            'note': '間接目的語（第4文型）'
                        })
                        
                        # さらに後続をO2（直接目的語）として候補に
                        if i < len(words) - 2:
                            o2_word = words[i + 2]
                            # 冠詞付きの場合は複数語として処理
                            if o2_word.lower() in ['a', 'an', 'the'] and i < len(words) - 3:
                                o2_phrase = f'{o2_word} {words[i + 3]}'
                                results.append({
                                    'position': i + 2,
                                    'slot': 'O2',
                                    'value': o2_phrase,
                                    'type': 'phrase',
                                    'rule_id': 'ditransitive-o2-phrase',
                                    'priority': 7,
                                    'span': 2,
                                    'note': '直接目的語（冠詞+名詞）'
                                })
                            else:
                                results.append({
                                    'position': i + 2,
                                    'slot': 'O2',
                                    'value': o2_word,
                                    'type': 'word',
                                    'rule_id': 'ditransitive-o2',
                                    'priority': 7,
                                    'note': '直接目的語（第4文型）'
                                })
        
        return results
    
    def rule_causative_make(self, words):
        """第5文型：make型動詞（S V O C2）"""
        results = []
        
        # make型動詞のリスト
        causative_verbs = ['make', 'made', 'keep', 'kept', 'find', 'found', 'call', 'called',
                          'consider', 'considered', 'name', 'named', 'leave', 'left']
        
        for i, word in enumerate(words):
            if word.lower() in causative_verbs:
                # 使役・状態変化動詞として動詞スロットに配置
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'causative-make',
                    'priority': 8,
                    'note': '第5文型動詞（SVOC可能）',
                    'pattern': 'causative'
                })
                
                # 後続の語をO, C2として処理（簡単版）
                if i < len(words) - 2:
                    # 直後の語をO（目的語）として候補に
                    next_word = words[i + 1]
                    if next_word.lower() in ['me', 'you', 'him', 'her', 'us', 'them', 'it']:
                        results.append({
                            'position': i + 1,
                            'slot': 'O1',
                            'value': next_word,
                            'type': 'word',
                            'rule_id': 'causative-o1',
                            'priority': 7,
                            'note': '目的語（第5文型）'
                        })
                        
                        # さらに後続をC2（目的格補語）として候補に
                        if i < len(words) - 2:
                            c2_word = words[i + 2]
                            # 形容詞や名詞として補語になりそうなもの
                            if (c2_word.lower() in ['happy', 'sad', 'angry', 'clean', 'dirty', 'ready', 'busy'] or
                                not c2_word.lower() in ['the', 'a', 'an', 'is', 'are', 'was', 'were']):
                                results.append({
                                    'position': i + 2,
                                    'slot': 'C2',
                                    'value': c2_word,
                                    'type': 'word',
                                    'rule_id': 'causative-c2',
                                    'priority': 7,
                                    'note': '目的格補語（第5文型）'
                                })
        
        return results

    # ===== Step 9: 連結動詞ルール =====
    
    def rule_copular_become(self, words):
        """連結動詞become（S V C1パターン）"""
        results = []
        
        # become型連結動詞のリスト
        copular_verbs = ['become', 'became', 'seem', 'seemed', 'appear', 'appeared', 
                        'remain', 'remained', 'sound', 'sounded', 'taste', 'tasted',
                        'look', 'looked', 'feel', 'felt', 'grow', 'grew', 'turn', 'turned']
        
        for i, word in enumerate(words):
            if word.lower() in copular_verbs:
                # 連結動詞として動詞スロットに配置
                results.append({
                    'position': i,
                    'slot': 'V',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'copular-become',
                    'priority': 8,
                    'note': '連結動詞（SVC1パターン）',
                    'pattern': 'copular'
                })
                
                # 後続の語をC1（主語補語）として処理
                if i < len(words) - 1:
                    complement = words[i + 1]
                    
                    # 形容詞リスト
                    adjectives = ['happy', 'sad', 'angry', 'tired', 'excited', 'nervous', 'calm',
                                'big', 'small', 'tall', 'short', 'young', 'old', 'new', 'good', 'bad',
                                'hot', 'cold', 'warm', 'cool', 'dry', 'wet', 'clean', 'dirty',
                                'easy', 'difficult', 'important', 'interesting', 'boring', 'famous',
                                'beautiful', 'ugly', 'strong', 'weak', 'fast', 'slow', 'quiet', 'loud']
                    
                    # 冠詞＋名詞のパターン（a teacher, an artist, the president等）
                    if complement.lower() in ['a', 'an'] and i < len(words) - 2:
                        # a/an + 名詞の形（または a/an + 形容詞 + 名詞）
                        noun = words[i + 2]
                        if i < len(words) - 3 and words[i + 3] in ['teacher', 'student', 'doctor', 'engineer', 'artist', 'writer', 'friend', 'leader', 'member']:
                            # a + 形容詞 + 名詞のパターン
                            full_phrase = f'{complement} {noun} {words[i + 3]}'
                            results.append({
                                'position': i + 1,
                                'slot': 'C1',
                                'value': full_phrase,
                                'type': 'phrase',
                                'rule_id': 'copular-c1-article-adj-noun',
                                'priority': 7,
                                'span': 3,
                                'note': '主語補語（冠詞+形容詞+名詞）'
                            })
                        else:
                            # a/an + 名詞のパターン
                            results.append({
                                'position': i + 1,
                                'slot': 'C1',
                                'value': f'{complement} {noun}',
                                'type': 'phrase',
                                'rule_id': 'copular-c1-article-noun',
                                'priority': 7,
                                'span': 2,
                                'note': '主語補語（冠詞+名詞）'
                            })
                    elif complement.lower() == 'the' and i < len(words) - 2:
                        # the + 名詞の形
                        noun = words[i + 2]
                        results.append({
                            'position': i + 1,
                            'slot': 'C1',
                            'value': f'{complement} {noun}',
                            'type': 'phrase',
                            'rule_id': 'copular-c1-the-noun',
                            'priority': 7,
                            'span': 2,
                            'note': '主語補語（the+名詞）'
                        })
                    elif complement.lower() in adjectives:
                        # 形容詞の場合
                        results.append({
                            'position': i + 1,
                            'slot': 'C1',
                            'value': complement,
                            'type': 'word',
                            'rule_id': 'copular-c1-adjective',
                            'priority': 7,
                            'note': '主語補語（形容詞）'
                        })
                    else:
                        # 一般名詞（teacher, student等）
                        nouns = ['teacher', 'student', 'doctor', 'engineer', 'artist', 'writer',
                                'friend', 'enemy', 'leader', 'member', 'president', 'manager']
                        if complement.lower() in nouns:
                            results.append({
                                'position': i + 1,
                                'slot': 'C1',
                                'value': complement,
                                'type': 'word',
                                'rule_id': 'copular-c1-noun',
                                'priority': 7,
                                'note': '主語補語（名詞）'
                            })
        
        return results

    # ===== Step 10: モーダル助動詞ルール（新規） =====
    
    def rule_modal_should(self, words):
        """should型モーダル助動詞"""
        results = []
        
        should_modals = ['should', 'shouldn\'t', 'ought']
        
        for i, word in enumerate(words):
            if word.lower() in should_modals:
                results.append({
                    'position': i,
                    'slot': 'Aux',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'modal-should',
                    'priority': 10,
                    'note': 'モーダル助動詞（義務・推奨）',
                    'pattern': 'modal'
                })
        
        return results
    
    def rule_modal_could(self, words):
        """could型モーダル助動詞"""
        results = []
        
        could_modals = ['could', 'couldn\'t', 'can', 'can\'t', 'cannot']
        
        for i, word in enumerate(words):
            if word.lower() in could_modals:
                results.append({
                    'position': i,
                    'slot': 'Aux',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'modal-could',
                    'priority': 10,
                    'note': 'モーダル助動詞（能力・可能性）',
                    'pattern': 'modal'
                })
        
        return results
    
    def rule_modal_might(self, words):
        """might/may型モーダル助動詞"""
        results = []
        
        might_modals = ['might', 'may', 'maybe']
        
        for i, word in enumerate(words):
            if word.lower() in might_modals:
                # maybeは文頭の場合のみM2として処理
                if word.lower() == 'maybe' and i == 0:
                    results.append({
                        'position': i,
                        'slot': 'M2',
                        'value': word,
                        'type': 'word',
                        'rule_id': 'modal-maybe-m2',
                        'priority': 9,
                        'note': '可能性副詞（文頭）'
                    })
                elif word.lower() in ['might', 'may']:
                    results.append({
                        'position': i,
                        'slot': 'Aux',
                        'value': word,
                        'type': 'word',
                        'rule_id': 'modal-might',
                        'priority': 10,
                        'note': 'モーダル助動詞（推測・許可）',
                        'pattern': 'modal'
                    })
        
        return results
    
    def rule_modal_must(self, words):
        """must型モーダル助動詞"""
        results = []
        
        must_modals = ['must', 'mustn\'t']
        
        for i, word in enumerate(words):
            if word.lower() in must_modals:
                results.append({
                    'position': i,
                    'slot': 'Aux',
                    'value': word,
                    'type': 'word',
                    'rule_id': 'modal-must',
                    'priority': 10,
                    'note': 'モーダル助動詞（義務・推測）',
                    'pattern': 'modal'
                })
        
        return results

    # ===== 統合処理 =====
    
    def apply_all_rules(self, words):
        """すべてのルールを適用してスロット候補を生成"""
        all_candidates = []
        
        # Step 2: 基本ルール
        for rule in self.simple_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 3: 中程度ルール
        for rule in self.medium_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 4: 複雑ルール
        for rule in self.complex_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 5: 動詞パターンルール
        for rule in self.verb_pattern_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 8: 第4文型・第5文型ルール
        for rule in self.ditransitive_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
            
        for rule in self.causative_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 9: 連結動詞ルール
        for rule in self.copular_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 10: モーダル助動詞ルール（新規）
        for rule in self.modal_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        # Step 6: 特殊ルール（最終処理）
        for rule in self.final_special_rules:
            candidates = rule(words)
            all_candidates.extend(candidates)
        
        return all_candidates
    
    def resolve_conflicts(self, candidates):
        """競合解決（優先度ベース + ポジション重複解決 + スロット重複解決）"""
        if not candidates:
            return {}
        
        # ポジション別にグループ化
        position_groups = {}
        for candidate in candidates:
            pos = candidate['position']
            if pos not in position_groups:
                position_groups[pos] = []
            position_groups[pos].append(candidate)
        
        final_slots = {}
        used_positions = set()
        
        # 各ポジションで最高優先度を選択
        for pos, group in position_groups.items():
            if pos in used_positions:
                continue
                
            # 優先度で降順ソート
            group.sort(key=lambda x: x.get('priority', 0), reverse=True)
            best_candidate = group[0]
            
            slot = best_candidate['slot']
            span = best_candidate.get('span', 1)
            
            # spanを考慮してポジションをマーク
            for i in range(pos, pos + span):
                used_positions.add(i)
            
            # スロット重複の解決（同じスロットには最高優先度の1つだけ）
            if slot not in final_slots:
                final_slots[slot] = []
                final_slots[slot].append({
                    'value': best_candidate['value'],
                    'type': best_candidate['type'],
                    'rule_id': best_candidate['rule_id'],
                    'position': pos,
                    'note': best_candidate.get('note', ''),
                    'pattern': best_candidate.get('pattern', '')
                })
            else:
                # 既にスロットにエントリがある場合、優先度比較
                existing = final_slots[slot][0]
                existing_priority = 0  # デフォルト優先度
                for c in candidates:
                    if (c['position'] == existing['position'] and 
                        c['slot'] == slot and 
                        c['value'] == existing['value']):
                        existing_priority = c.get('priority', 0)
                        break
                
                new_priority = best_candidate.get('priority', 0)
                if new_priority > existing_priority:
                    final_slots[slot] = [{
                        'value': best_candidate['value'],
                        'type': best_candidate['type'],
                        'rule_id': best_candidate['rule_id'],
                        'position': pos,
                        'note': best_candidate.get('note', ''),
                        'pattern': best_candidate.get('pattern', '')
                    }]
        
        return final_slots
    
    def process_sentence(self, sentence):
        """文の処理（Step 10統合版）"""
        if not sentence or sentence.strip() == '':
            return {}
        
        words = sentence.strip().split()
        
        # すべてのルールを適用
        candidates = self.apply_all_rules(words)
        
        # 競合解決
        final_slots = self.resolve_conflicts(candidates)
        
        return final_slots
    
    def format_output(self, slots, sentence):
        """整形された出力"""
        if not slots:
            return f"入力: {sentence}\n結果: 解析できませんでした\n"
        
        output = [f"入力: {sentence}"]
        
        slot_order = ['S', 'Aux', 'V', 'O1', 'O2', 'C1', 'C2', 'M1', 'M2', 'M3']
        
        for slot in slot_order:
            if slot in slots:
                items = slots[slot]
                for item in items:
                    note = f" ({item['note']})" if item['note'] else ""
                    pattern = f" [{item['pattern']}]" if item['pattern'] else ""
                    output.append(f"{slot}: {item['value']}{note}{pattern}")
        
        return '\n'.join(output) + '\n'

def main():
    """Step 10テスト実行"""
    engine = Step10RuleEngine()
    
    print("=== Step 10 Modal Auxiliaries統合テスト ===\n")
    
    test_sentences = [
        # Step 10新機能：モーダル助動詞テスト
        "I should study hard",
        "You could help me",
        "He might come tomorrow",
        "She may leave early",
        "We must finish this work",
        "They can't understand it",
        "You shouldn't worry about that",
        "Maybe I will go there",
        
        # 複合テスト：モーダル + 既存パターン
        "I should become a teacher",
        "You could give him a book", 
        "She might make us happy",
        "We must go to school",
        
        # 既存機能確認
        "I become happy",
        "I give you a book",
        "I make you happy", 
        "Why do you study hard"
    ]
    
    for sentence in test_sentences:
        slots = engine.process_sentence(sentence)
        print(engine.format_output(slots, sentence))

if __name__ == "__main__":
    main()
