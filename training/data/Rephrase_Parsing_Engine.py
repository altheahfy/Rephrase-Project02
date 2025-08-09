# ===== Rephrase Parsing Engine =====
# 完全統合版: ChatGPT 34ルール + サブクローズ分解エンジン
# 目標: すべての英文法ルールに対応した品詞分解システム

import json
import re
import os

class RephraseParsingEngine:
    """完全統合版Rephrase品詞分解エンジン"""
    
    def __init__(self):
        self.engine_name = "Rephrase Parsing Engine v3.0 (spaCy Grammar Integrated)"
        self.rules_data = self.load_rules()
        
        # 形態素ルール拡張を追加
        self.morphology_rules = self.get_morphology_rules()
        
        # spaCyハイブリッド機能追加
        self.spacy_available = self._initialize_spacy()
        
        # 統計情報（デバッグ用）
        self.stats = {
            'morphology_success': 0,
            'spacy_success': 0,
            'spacy_grammar_success': 0,  # 新機能
            'fallback_used': 0,
            'total_analyzed': 0
        }
        
    def get_morphology_rules(self):
        """形態素ルール辞書（語彙制限解決用）"""
        return {
            # 動詞関連
            'ed': 'VERB_PAST',
            'ing': 'VERB_ING',
            's': 'VERB_3SG_OR_NOUN_PLURAL',  # 曖昧
            
            # 名詞関連  
            'tion': 'NOUN',
            'sion': 'NOUN',
            'ment': 'NOUN',
            'ness': 'NOUN',
            'ity': 'NOUN',
            'er': 'NOUN_OR_ADJ',  # teacher, bigger
            'or': 'NOUN',
            'ist': 'NOUN',
            
            # 形容詞関連
            'ful': 'ADJ',
            'less': 'ADJ',
            'able': 'ADJ',
            'ible': 'ADJ',
            'ous': 'ADJ',
            'ive': 'ADJ',
            'al': 'ADJ',
            'ic': 'ADJ',
            
            # 副詞関連
            'ly': 'ADV',
        }
        
    def _initialize_spacy(self):
        """spaCy初期化（警告抑制）"""
        try:
            import warnings
            warnings.filterwarnings("ignore")
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            return True
        except Exception:
            return False
        
    def analyze_word_hybrid(self, word, context=""):
        """ハイブリッド解析: 形態素ルール優先 → spaCy補完"""
        self.stats['total_analyzed'] += 1
        
        # Step 1: 形態素ルール解析
        morph_result = self.analyze_word_morphology(word, context)
        
        # 形態素ルールで確実に判定できた場合
        if (morph_result['pos'] not in ['UNKNOWN', 'VERB_3SG_OR_NOUN_PLURAL', 'NOUN_OR_ADJ']
            and morph_result['confidence'] > 0.8):
            self.stats['morphology_success'] += 1
            morph_result['method'] = 'morphology_primary'
            return morph_result
        
        # Step 2: spaCy補完解析
        if self.spacy_available:
            try:
                # 文脈解析
                if context and word in context:
                    doc = self.nlp(context)
                    for token in doc:
                        if token.text.lower() == word.lower():
                            self.stats['spacy_success'] += 1
                            return {
                                'word': word,
                                'pos': token.pos_,
                                'tag': token.tag_,
                                'lemma': token.lemma_,
                                'confidence': 0.95,
                                'method': 'spacy_context'
                            }
                
                # 単独解析
                doc = self.nlp(word)
                if doc:
                    token = doc[0]
                    self.stats['spacy_success'] += 1
                    return {
                        'word': word,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'lemma': token.lemma_,
                        'confidence': 0.90,
                        'method': 'spacy_single'
                    }
            except:
                pass
        
        # Step 3: フォールバック（形態素ルール結果）
        self.stats['fallback_used'] += 1
        morph_result['method'] = 'morphology_fallback'
        return morph_result
        
    def analyze_sentence_with_spacy_grammar(self, sentence):
        """spaCy文法解析統合版のメイン解析メソッド"""
        if not self.spacy_available:
            print("⚠️ spaCy利用不可。従来手法にフォールバック")
            return self.analyze_sentence(sentence)
        
        print(f"\n=== spaCy統合文法分解: {sentence} ===")
        
        # Step 1: spaCyで品詞・依存関係解析
        doc = self.nlp(sentence)
        tokens_info = self._extract_tokens_info(doc)
        
        # Step 2: 品詞情報を活用したスロット分類
        slots = self._classify_slots_with_spacy(tokens_info, sentence)
        
        # Step 3: 既存ルールとの統合・補完
        enhanced_slots = self._enhance_slots_with_traditional_rules(slots, sentence)
        
        self.stats['spacy_grammar_success'] += len(enhanced_slots)
        return enhanced_slots
    
    def _extract_tokens_info(self, doc):
        """spaCy解析結果からトークン情報を抽出"""
        tokens_info = []
        
        for token in doc:
            if token.is_punct:
                continue
                
            token_info = {
                'text': token.text,
                'pos': token.pos_,
                'tag': token.tag_,
                'lemma': token.lemma_,
                'dep': token.dep_,
                'head': token.head.text if token.head != token else 'ROOT',
                'is_stop': token.is_stop,
                'children': [child.text for child in token.children]
            }
            tokens_info.append(token_info)
        
        return tokens_info
    
    def _classify_slots_with_spacy(self, tokens_info, sentence):
        """spaCy品詞・依存関係情報を活用したスロット分類"""
        slots = {}
        
        # 主語の特定（nsubj, nsubjpass）
        subjects = [t for t in tokens_info if t['dep'] in ['nsubj', 'nsubjpass'] and t['pos'] in ['NOUN', 'PRON']]
        
        # 動詞の特定（ROOT + VERB）
        main_verbs = [t for t in tokens_info if t['dep'] == 'ROOT' and t['pos'] == 'VERB']
        
        # 助動詞の特定（AUX）
        auxiliaries = [t for t in tokens_info if t['pos'] == 'AUX']
        
        # 目的語の特定（dobj, pobj）
        objects = [t for t in tokens_info if t['dep'] in ['dobj', 'pobj'] and t['pos'] in ['NOUN', 'PRON']]
        
        # 補語の特定（acomp, attr）
        complements = [t for t in tokens_info if t['dep'] in ['acomp', 'attr']]
        
        # 修飾語の特定（advmod, amod, npadvmod）
        modifiers_adv = [t for t in tokens_info if t['dep'] in ['advmod', 'npadvmod'] and t['pos'] == 'ADV']
        modifiers_adj = [t for t in tokens_info if t['dep'] == 'amod' and t['pos'] == 'ADJ']
        
        # 疑問詞の特定（品詞タグベース）
        question_words = [t for t in tokens_info if t['tag'] in ['WP', 'WDT', 'WRB'] or 
                         t['text'].lower() in ['what', 'where', 'when', 'who', 'why', 'how']]
        
        # スロット割り当て
        if subjects:
            # 複数主語の場合は結合
            subject_text = ' '.join([s['text'] for s in subjects])
            slots['S'] = [{'value': subject_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 1}]
        
        if auxiliaries:
            aux_text = ' '.join([a['text'] for a in auxiliaries])
            slots['Aux'] = [{'value': aux_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 2}]
        
        if main_verbs:
            verb_text = ' '.join([v['text'] for v in main_verbs])
            slots['V'] = [{'value': verb_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 3}]
        
        if objects:
            obj_text = ' '.join([o['text'] for o in objects])
            slots['O1'] = [{'value': obj_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 4}]
        
        if complements:
            comp_text = ' '.join([c['text'] for c in complements])
            slots['C'] = [{'value': comp_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 5}]
        
        if modifiers_adv:
            adv_text = ' '.join([m['text'] for m in modifiers_adv])
            slots['M3'] = [{'value': adv_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 6}]
        
        if modifiers_adj:
            adj_text = ' '.join([m['text'] for m in modifiers_adj])
            slots['M2'] = [{'value': adj_text, 'confidence': 0.95, 'method': 'spacy_grammar', 'order': 7}]
        
        # 疑問詞の特別処理
        if question_words:
            q_word = question_words[0]
            q_text = q_word['text']
            
            if q_text.lower() in ['what', 'who']:
                slots['O1'] = [{'value': q_text, 'confidence': 0.98, 'method': 'spacy_question', 'order': 1}]
            elif q_text.lower() in ['where', 'when', 'why', 'how']:
                slots['M1'] = [{'value': q_text, 'confidence': 0.98, 'method': 'spacy_question', 'order': 1}]
        
        return slots
    
    def _enhance_slots_with_traditional_rules(self, spacy_slots, sentence):
        """spaCy解析結果を既存ルールで補強"""
        # 既存ルールでの解析も実行
        traditional_slots = self.analyze_sentence(sentence)
        
        enhanced_slots = spacy_slots.copy()
        
        # 既存ルールで補完可能な情報を追加
        for slot, candidates in traditional_slots.items():
            if slot not in enhanced_slots and candidates:
                # spaCyで検出されなかった要素を補完
                enhanced_slots[slot] = candidates
                for candidate in candidates:
                    candidate['method'] = 'traditional_complement'
        
        return enhanced_slots
        
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
            
        # 疑問文チェックを最優先
        if self.is_question(sentence):
            return self.analyze_question(sentence)
            
        # 命令文・呼びかけパターンの検出
        if self.is_imperative_with_vocative(sentence):
            return self.analyze_imperative_with_vocative(sentence)
            
        # 複文の場合、サブクローズ分解を試行
        if self.contains_subclause(sentence):
            return self.analyze_complex_sentence(sentence)
        else:
            return self.analyze_simple_sentence(sentence)
    
    def is_question(self, sentence):
        """疑問文かどうかを判定"""
        sentence = sentence.strip()
        
        # 疑問符で終わる
        if sentence.endswith('?'):
            return True
            
        # 疑問詞で始まる
        wh_words = ['what', 'who', 'where', 'when', 'why', 'how', 'which']
        first_word = sentence.split()[0].lower() if sentence.split() else ""
        if first_word in wh_words:
            return True
            
        # 助動詞で始まる (Do, Does, Did, Can, Will等)
        auxiliary_starts = ['do', 'does', 'did', 'can', 'could', 'will', 'would', 'should', 'may', 'might', 'must', 'am', 'is', 'are', 'was', 'were']
        if first_word in auxiliary_starts:
            return True
            
        return False
    
    def is_imperative_with_vocative(self, sentence):
        """呼びかけ+命令文かどうかを判定"""
        words = sentence.split()
        if len(words) < 2:
            return False
            
        # "You,"で始まる場合（呼びかけのパターン）
        if words[0].lower().rstrip(',') == 'you' and words[0].endswith(','):
            return True
            
        # その他の呼びかけパターン: "Name,"
        if words[0].endswith(','):
            return True
            
        return False
    
    def analyze_imperative_with_vocative(self, sentence):
        """呼びかけ+命令文を解析"""
        words = sentence.split()
        
        # 呼びかけ部分を抽出
        vocative = words[0]  # "You,", "John," など
        command_words = words[1:]  # 命令文部分
        
        if len(command_words) < 1:
            return {}
        
        # 命令文部分を解析
        verb = command_words[0]  # give
        remaining = command_words[1:] if len(command_words) > 1 else []
        
        result = {
            'M1': [{'value': vocative, 'type': 'vocative', 'rule_id': 'imperative-vocative'}],
            'V': [{'value': verb, 'type': 'imperative_verb', 'rule_id': 'imperative-vocative'}]
        }
        
        # 残りの語句を分析
        if remaining:
            objects_and_modifiers = self.parse_imperative_objects_modifiers(remaining)
            result.update(objects_and_modifiers)
        
        return result
    
    def parse_imperative_objects_modifiers(self, words):
        """命令文の目的語と修飾語を分析"""
        result = {}
        
        if not words:
            return result
        
        # "it to me straight"のようなパターンを分析
        i = 0
        
        # 最初の語は通常直接目的語
        if i < len(words):
            result['O1'] = [{'value': words[i], 'type': 'direct_object', 'rule_id': 'imperative-object'}]
            i += 1
        
        # 残りの語句を修飾語として分析
        remaining_words = words[i:]
        modifiers = self.extract_imperative_modifiers(remaining_words)
        result.update(modifiers)
        
        return result
    
    def extract_imperative_modifiers(self, words):
        """命令文の修飾語を抽出（to me straight を分離）"""
        modifiers = {}
        
        if not words:
            return modifiers
        
        i = 0
        while i < len(words):
            # 前置詞句の検出（to me, from him など）
            if words[i].lower() in ['to', 'from', 'for', 'with', 'in', 'at', 'on']:
                if i + 1 < len(words):
                    prep_phrase = f"{words[i]} {words[i+1]}"
                    modifiers['M2'] = [{'value': prep_phrase, 'type': 'prepositional_phrase', 'rule_id': 'imperative-modifier'}]
                    i += 2
                    continue
            
            # 単独の副詞（straight, quickly など）
            if self.is_manner_adverb(words[i].rstrip('.,!?')):
                modifiers['M3'] = [{'value': words[i].rstrip('.,!?'), 'type': 'manner_adverb', 'rule_id': 'imperative-modifier'}]
                i += 1
                continue
                
            i += 1
        
        return modifiers
    
    def is_manner_adverb(self, word):
        """様態副詞かどうかを判定"""
        manner_adverbs = [
            'straight', 'quickly', 'slowly', 'carefully', 'well', 'badly', 
            'fast', 'hard', 'softly', 'loudly', 'quietly', 'clearly',
            'directly', 'honestly', 'simply', 'easily', 'perfectly'
        ]
        return word.lower() in manner_adverbs
    
    def analyze_question(self, sentence):
        """疑問文を解析"""
        words = sentence.split()
        if not words:
            return {}
            
        first_word = words[0].lower()
        
        # wh疑問文の処理
        if first_word in ['what', 'who', 'where', 'when', 'why', 'how', 'which']:
            return self.analyze_wh_question(words)
            
        # yes/no疑問文の処理 (Do, Does, Did等で始まる)
        if first_word in ['do', 'does', 'did']:
            return self.analyze_do_question(words)
            
        # be動詞疑問文の処理 (Are, Is等で始まる)  
        if first_word in ['am', 'is', 'are', 'was', 'were']:
            return self.analyze_be_question(words)
            
        # modal疑問文の処理 (Can, Will等で始まる)
        modal_verbs = ['can', 'could', 'will', 'would', 'should', 'may', 'might', 'must']
        if first_word in modal_verbs:
            return self.analyze_modal_question(words)
            
        # その他は通常解析にフォールバック
        return self.analyze_simple_sentence(sentence)
    
    def analyze_do_question(self, words):
        """Do/Does/Did疑問文を解析"""
        if len(words) < 3:
            return {}
            
        aux = words[0]  # Do/Does/Did
        subject = words[1]  # you/he/she等
        
        # 動詞とその他を分離
        rest = words[2:]
        main_verb = rest[0] if rest else ""
        remaining_text = " ".join(rest[1:]) if len(rest) > 1 else ""
        
        result = {
            'Aux': [{'value': aux, 'type': 'auxiliary', 'rule_id': 'do-question'}],
            'S': [{'value': subject, 'type': 'subject', 'rule_id': 'do-question'}]
        }
        
        if main_verb:
            result['V'] = [{'value': main_verb, 'type': 'verb', 'rule_id': 'do-question'}]
            
        # 残りのテキストを解析して適切なスロットに分類
        if remaining_text:
            # please分離処理
            main_part, please_part = self.separate_please_from_phrase(remaining_text)
            
            # メイン部分を分類
            if main_part:
                slot_info = self.classify_remaining_phrase(main_part)
                result[slot_info['slot']] = [{'value': slot_info['value'], 'type': slot_info['type'], 'rule_id': 'do-question'}]
            
            # please部分があれば追加
            if please_part:
                result['M3'] = [{'value': please_part, 'type': 'polite_expression', 'rule_id': 'do-question'}]
            
        return result
    
    def separate_please_from_phrase(self, phrase):
        """フレーズからpleaseを分離"""
        phrase = phrase.strip()
        phrase_lower = phrase.lower()
        
        # 文末のpleaseを検出
        if phrase_lower.endswith(' please?') or phrase_lower.endswith(' please'):
            please_pos = phrase_lower.rfind(' please')
            main_part = phrase[:please_pos].strip()
            return main_part, 'please'
        elif phrase_lower == 'please' or phrase_lower == 'please?':
            return '', 'please'
        
        return phrase, ''
    
    def separate_object_and_time_modifier(self, words):
        """現在完了の残り部分から目的語と時間修飾語を分離"""
        if not words:
            return '', ''
        
        text = " ".join(words)
        
        # 時間表現のパターン（現在完了でよく使われるもの）
        time_patterns = [
            'for a long time', 'for a while', 'for years', 'for months', 'for weeks', 'for days',
            'since yesterday', 'since last week', 'since last month', 'since last year',
            'since morning', 'since then', 'recently', 'lately', 'just now', 'already',
            'yet', 'ever', 'never', 'before', 'so far'
        ]
        
        # 長いパターンから順にチェック
        sorted_patterns = sorted(time_patterns, key=len, reverse=True)
        
        for pattern in sorted_patterns:
            if pattern in text.lower():
                # 時間表現を除去して目的語部分を取得
                pattern_start = text.lower().find(pattern)
                object_part = text[:pattern_start].strip()
                
                # 時間表現の前後を考慮して正確に抽出
                time_part = text[pattern_start:pattern_start+len(pattern)]
                remaining = text[pattern_start+len(pattern):].strip()
                
                # 時間表現の後に何かあれば結合
                if remaining:
                    time_part += " " + remaining
                
                return object_part.rstrip(',').strip(), time_part.strip()
        
        # 前置詞句で時間を表現する場合（for, since で始まる）
        if text.lower().startswith('for ') or text.lower().startswith('since '):
            # 全体を時間修飾語として扱う
            return '', text
        
        # 前置詞句が混在する場合の分離
        words_list = words
        for i, word in enumerate(words_list):
            if word.lower() in ['for', 'since'] and i > 0:
                # forやsinceより前を目的語、以降を時間修飾語として分離
                object_part = " ".join(words_list[:i]).strip()
                time_part = " ".join(words_list[i:]).strip()
                return object_part, time_part
        
        # 時間表現が見つからない場合は全て目的語とする
        return text, ''
    
    def extract_phrasal_verb(self, words):
        """句動詞を抽出して、動詞部分と残りの部分を分離"""
        if not words:
            return '', ''
        
        # 句動詞パターンの定義
        phrasal_verbs = {
            'sit': ['down', 'up'],
            'stand': ['up', 'down'],
            'wake': ['up'],
            'get': ['up', 'down', 'in', 'out', 'on', 'off'],
            'come': ['in', 'out', 'up', 'down', 'back'],
            'go': ['out', 'in', 'up', 'down', 'away', 'back'],
            'put': ['on', 'off', 'down', 'up'],
            'take': ['off', 'on', 'out', 'up', 'down'],
            'turn': ['on', 'off', 'up', 'down'],
            'pick': ['up', 'out'],
            'look': ['up', 'down', 'out', 'in']
        }
        
        verb = words[0]
        verb_lower = verb.lower()
        
        # 句動詞パターンをチェック
        if len(words) >= 2 and verb_lower in phrasal_verbs:
            particle_candidate = words[1].rstrip('?!.')  # 句読点を除去して比較
            particle_lower = particle_candidate.lower()
            
            if particle_lower in phrasal_verbs[verb_lower]:
                # 句動詞として結合
                phrasal_verb = verb + " " + particle_candidate
                remaining_words = words[2:] if len(words) > 2 else []
                remaining_text = " ".join(remaining_words)
                return phrasal_verb, remaining_text
        
        # 句動詞でない場合は通常の動詞
        remaining_words = words[1:] if len(words) > 1 else []
        remaining_text = " ".join(remaining_words)
        return verb, remaining_text
    
    def classify_verb_complement(self, verb, complement_text):
        """動詞の補語を適切に分類（句動詞の粒子、方向副詞等を考慮）"""
        complement_text = complement_text.strip().rstrip('?')
        complement_words = complement_text.split()
        
        if not complement_words:
            return {'slot': '', 'value': '', 'type': ''}
        
        # 方向副詞のリスト
        directional_adverbs = [
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'away', 'back',
            'forward', 'backward', 'upward', 'downward', 'inside', 'outside', 
            'upstairs', 'downstairs', 'ahead', 'behind', 'here', 'there'
        ]
        
        # 単一の方向副詞の場合
        if len(complement_words) == 1 and complement_words[0].lower() in directional_adverbs:
            return {'slot': 'M2', 'value': complement_text, 'type': 'directional_adverb'}
        
        # 句動詞パターン（verb + particle）の判定
        phrasal_verbs = {
            'sit': ['down', 'up'],
            'stand': ['up', 'down'],
            'wake': ['up'],
            'get': ['up', 'down', 'in', 'out', 'on', 'off'],
            'come': ['in', 'out', 'up', 'down', 'back'],
            'go': ['out', 'in', 'up', 'down', 'away', 'back'],
            'put': ['on', 'off', 'down', 'up'],
            'take': ['off', 'on', 'out', 'up', 'down'],
            'turn': ['on', 'off', 'up', 'down'],
            'pick': ['up', 'out'],
            'look': ['up', 'down', 'out', 'in']
        }
        
        verb_lower = verb.lower()
        first_word = complement_words[0].lower()
        
        # 句動詞+目的語パターン（例：turn on the light）
        if (verb_lower in phrasal_verbs and 
            first_word in phrasal_verbs[verb_lower] and 
            len(complement_words) > 1):
            particle = complement_words[0]
            object_part = " ".join(complement_words[1:])
            return {
                'slot': 'compound',  # 複合要素を示すフラグ
                'particle': {'slot': 'M2', 'value': particle, 'type': 'phrasal_verb_particle'},
                'object': {'slot': 'O1', 'value': object_part, 'type': 'object'}
            }
        
        # 単純な句動詞粒子
        if verb_lower in phrasal_verbs and first_word in phrasal_verbs[verb_lower] and len(complement_words) == 1:
            return {'slot': 'M2', 'value': complement_text, 'type': 'phrasal_verb_particle'}
        
        # 前置詞句の場合
        if any(complement_text.lower().startswith(prep + ' ') for prep in ['to', 'from', 'in', 'at', 'by', 'with', 'for']):
            return {'slot': 'M2', 'value': complement_text, 'type': 'prepositional_phrase'}
        
        # デフォルトは目的語
        return {'slot': 'O1', 'value': complement_text, 'type': 'object'}
    
    def classify_remaining_phrase(self, phrase):
        """フレーズを適切なスロット（O1, M1, M2, M3等）に分類"""
        phrase = phrase.strip().rstrip('?')  # 疑問符を除去
        phrase_lower = phrase.lower()
        
        # 時間表現のパターン
        time_patterns = [
            'every day', 'every morning', 'every evening', 'every week', 'every month', 'every year',
            'yesterday', 'today', 'tomorrow', 'now', 'then', 'always', 'never', 'often', 'sometimes',
            'usually', 'frequently', 'rarely', 'daily', 'weekly', 'monthly', 'yearly'
        ]
        
        # 場所表現のパターン  
        place_patterns = [
            'at home', 'at school', 'at work', 'in the park', 'in the city', 'there', 'here',
            'downtown', 'upstairs', 'downstairs', 'outside', 'inside'
        ]
        
        # 方法・手段表現のパターン
        manner_patterns = [
            'quickly', 'slowly', 'carefully', 'well', 'fast', 'hard', 'softly', 'loudly',
            'by car', 'by train', 'by bus', 'on foot'
        ]
        
        phrase_lower = phrase.lower()
        
        # 時間表現チェック
        for time_expr in time_patterns:
            if time_expr in phrase_lower:
                return {'slot': 'M3', 'value': phrase, 'type': 'time_adverb'}
                
        # 場所表現チェック
        for place_expr in place_patterns:
            if place_expr in phrase_lower:
                return {'slot': 'M2', 'value': phrase, 'type': 'place_adverb'}
        
        # 前置詞句による起点・方向・場所表現のチェック
        if phrase_lower.startswith(('from ', 'to ', 'in ', 'at ', 'on ', 'into ', 'onto ', 'toward ', 'towards ')):
            return {'slot': 'M2', 'value': phrase, 'type': 'prepositional_phrase'}
                
        # 方法表現チェック  
        for manner_expr in manner_patterns:
            if manner_expr in phrase_lower:
                return {'slot': 'M1', 'value': phrase, 'type': 'manner_adverb'}
        
        # 頻度・程度副詞の判定
        if any(word in phrase_lower for word in ['very', 'quite', 'really', 'extremely', 'totally']):
            return {'slot': 'M1', 'value': phrase, 'type': 'degree_adverb'}
        
        # デフォルトは目的語として扱う
        return {'slot': 'O1', 'value': phrase, 'type': 'object'}
    
    def analyze_wh_question(self, words):
        """wh疑問文を解析"""
        if len(words) < 2:
            return {}
            
        wh_word = words[0]
        rest = words[1:]
        
        # wh-wordの後がdo/did/doesの場合
        if rest and rest[0].lower() in ['do', 'does', 'did']:
            if len(rest) >= 3:
                aux = rest[0]
                subject = rest[1] 
                verb = rest[2]
                objects = " ".join(rest[3:]) if len(rest) > 3 else ""
                
                result = {
                    'Aux': [{'value': aux, 'type': 'auxiliary', 'rule_id': 'wh-question', 'order': 2}],
                    'S': [{'value': subject, 'type': 'subject', 'rule_id': 'wh-question', 'order': 3}],
                    'V': [{'value': verb, 'type': 'verb', 'rule_id': 'wh-question', 'order': 4}]
                }
                
                # wh-wordがどのスロットに対応するかを判定
                wh_slot = self.determine_wh_slot(wh_word.lower())
                result[wh_slot] = [{'value': wh_word, 'type': 'wh-word', 'rule_id': 'wh-question', 'order': 1}]
                
                if objects:
                    # wh-wordが目的語でない場合のみO1を追加
                    if wh_slot not in ['O1', 'O2']:
                        result['O1'] = [{'value': objects.rstrip('?'), 'type': 'object', 'rule_id': 'wh-question', 'order': 5}]
                        
                return result
        
        # その他の場合は基本解析
        return self.analyze_simple_sentence(" ".join(words))
    
    def determine_wh_slot(self, wh_word):
        """wh-wordがどのスロットに対応するかを判定"""
        wh_slot_map = {
            'what': 'O1',
            'who': 'S', 
            'where': 'M1',
            'when': 'M1',
            'why': 'M1',
            'how': 'M1',
            'which': 'O1'
        }
        return wh_slot_map.get(wh_word, 'O1')
    
    def analyze_be_question(self, words):
        """be動詞疑問文を解析"""
        if len(words) < 3:
            return {}
            
        be_verb = words[0]
        subject = words[1]
        complement = " ".join(words[2:])
        
        return {
            'Aux': [{'value': be_verb, 'type': 'be_auxiliary', 'rule_id': 'be-question'}],
            'S': [{'value': subject, 'type': 'subject', 'rule_id': 'be-question'}],
            'C': [{'value': complement, 'type': 'complement', 'rule_id': 'be-question'}] if complement else []
        }
    
    def analyze_modal_question(self, words):
        """modal動詞疑問文を解析"""
        if len(words) < 3:
            return {}
            
        modal = words[0]
        subject = words[1]
        
        # 動詞部分を分離
        rest_words = words[2:]
        
        # "Would you please verb..." パターンの処理
        if rest_words and rest_words[0].lower() == 'please' and len(rest_words) > 1:
            verb_part, remaining_text = self.extract_phrasal_verb(rest_words[1:])
            
            result = {
                'Aux': [{'value': modal, 'type': 'modal', 'rule_id': 'modal-question'}],
                'S': [{'value': subject, 'type': 'subject', 'rule_id': 'modal-question'}],
                'M3': [{'value': 'please', 'type': 'polite_expression', 'rule_id': 'modal-question'}],
                'V': [{'value': verb_part, 'type': 'verb', 'rule_id': 'modal-question'}]
            }
            
            if remaining_text:
                main_part, please_part = self.separate_please_from_phrase(remaining_text)
                if main_part:
                    result['O1'] = [{'value': main_part.rstrip('?'), 'type': 'object', 'rule_id': 'modal-question'}]
                if please_part:
                    if 'M3' not in result:
                        result['M3'] = [{'value': please_part, 'type': 'polite_expression', 'rule_id': 'modal-question'}]
                
        else:
            # 通常の "modal subject verb object please" パターン
            verb_part, remaining_text = self.extract_phrasal_verb(rest_words)
            
            result = {
                'Aux': [{'value': modal, 'type': 'modal', 'rule_id': 'modal-question'}],
                'S': [{'value': subject, 'type': 'subject', 'rule_id': 'modal-question'}]
            }
            
            if verb_part:
                result['V'] = [{'value': verb_part, 'type': 'verb', 'rule_id': 'modal-question'}]
                
            if remaining_text:
                # please分離処理
                main_part, please_part = self.separate_please_from_phrase(remaining_text)
                
                # メイン部分を目的語として追加
                if main_part:
                    result['O1'] = [{'value': main_part.rstrip('?'), 'type': 'object', 'rule_id': 'modal-question'}]
                
                # please部分があれば追加
                if please_part:
                    result['M3'] = [{'value': please_part, 'type': 'polite_expression', 'rule_id': 'modal-question'}]
            
        return result
    
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
        
        # 現在時制完了パターンの検出
        perfect_result = self.detect_perfect_pattern(words)
        if perfect_result:
            slots.update(perfect_result)
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
    
    def detect_perfect_pattern(self, words):
        """現在時制完了パターンを検出 (has/have + past participle, 縮約形含む)"""
        have_verbs = ["have", "has", "had"]
        contractions = ["haven't", "hasn't", "hadn't"]  # 縮約形
        
        # 縮約形の処理
        for i, word in enumerate(words):
            word_lower = word.lower()
            if word_lower in contractions:
                # 縮約形を分解
                if word_lower == "haven't":
                    aux_word = "have not"
                elif word_lower == "hasn't":
                    aux_word = "has not"
                elif word_lower == "hadn't":
                    aux_word = "had not"
                
                # 次の語が過去分詞かチェック
                if i + 1 < len(words):
                    next_word = words[i+1]
                    if self.looks_like_past_participle(next_word):
                        subject = " ".join(words[:i]) if i > 0 else "I"
                        
                        # 残りの部分から目的語と修飾語を分離
                        remaining_words = words[i+2:]
                        object_part, time_modifier = self.separate_object_and_time_modifier(remaining_words)
                        
                        result = {
                            'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'present-perfect'}],
                            'Aux': [{'value': aux_word, 'type': 'auxiliary', 'rule_id': 'present-perfect'}],
                            'V': [{'value': next_word, 'type': 'past_participle', 'rule_id': 'present-perfect'}]
                        }
                        
                        # 目的語がある場合
                        if object_part:
                            result['O1'] = [{'value': object_part, 'type': 'object', 'rule_id': 'present-perfect'}]
                        
                        # 時間修飾語がある場合
                        if time_modifier:
                            result['M3'] = [{'value': time_modifier, 'type': 'time_expression', 'rule_id': 'present-perfect'}]
                        
                        return result
        
        # 通常形の処理（have not seenパターンも含む）
        for i, word in enumerate(words):
            if word.lower() in have_verbs:
                # have + not + past participle パターン
                if (i + 2 < len(words) and 
                    words[i+1].lower() == 'not' and 
                    self.looks_like_past_participle(words[i+2])):
                    
                    subject = " ".join(words[:i]) if i > 0 else "I"
                    aux_word = word + " not"
                    past_participle = words[i+2]
                    
                    # 残りの部分から目的語と修飾語を分離
                    remaining_words = words[i+3:]
                    object_part, time_modifier = self.separate_object_and_time_modifier(remaining_words)
                    
                    result = {
                        'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'present-perfect'}],
                        'Aux': [{'value': aux_word, 'type': 'auxiliary', 'rule_id': 'present-perfect'}],
                        'V': [{'value': past_participle, 'type': 'past_participle', 'rule_id': 'present-perfect'}]
                    }
                    
                    # 目的語がある場合
                    if object_part:
                        result['O1'] = [{'value': object_part, 'type': 'object', 'rule_id': 'present-perfect'}]
                    
                    # 時間修飾語がある場合
                    if time_modifier:
                        result['M3'] = [{'value': time_modifier, 'type': 'time_expression', 'rule_id': 'present-perfect'}]
                    
                    return result
                
                # 通常の have + past participle パターン
                elif i + 1 < len(words):
                    next_word = words[i+1]
                    if self.looks_like_past_participle(next_word):
                        subject = " ".join(words[:i]) if i > 0 else "I"
                        
                        # 残りの部分から目的語と修飾語を分離
                        remaining_words = words[i+2:]
                        object_part, time_modifier = self.separate_object_and_time_modifier(remaining_words)
                        
                        result = {
                            'S': [{'value': subject.strip(), 'type': 'subject', 'rule_id': 'present-perfect'}],
                            'Aux': [{'value': word, 'type': 'auxiliary', 'rule_id': 'present-perfect'}],
                            'V': [{'value': next_word, 'type': 'past_participle', 'rule_id': 'present-perfect'}]
                        }
                        
                        # 目的語がある場合
                        if object_part:
                            result['O1'] = [{'value': object_part, 'type': 'object', 'rule_id': 'present-perfect'}]
                        
                        # 時間修飾語がある場合
                        if time_modifier:
                            result['M3'] = [{'value': time_modifier, 'type': 'time_expression', 'rule_id': 'present-perfect'}]
                        
                        return result
        
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
        """過去分詞らしい語かチェック（形態素ルール拡張版）"""
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
    
    def analyze_word_morphology(self, word, context=""):
        """形態素ルール拡張による語彙解析"""
        word_clean = word.lower().rstrip('.,!?')
        
        # 1. 基本語彙チェック（高速）
        basic_vocab = {
            'the': 'DET', 'a': 'DET', 'an': 'DET',
            'is': 'BE_VERB', 'are': 'BE_VERB', 'was': 'BE_VERB', 'were': 'BE_VERB',
            'have': 'AUX_VERB', 'has': 'AUX_VERB', 'had': 'AUX_VERB',
            'do': 'AUX_VERB', 'does': 'AUX_VERB', 'did': 'AUX_VERB',
            'will': 'MODAL', 'would': 'MODAL', 'can': 'MODAL', 'could': 'MODAL',
            'i': 'PRON', 'you': 'PRON', 'he': 'PRON', 'she': 'PRON', 'it': 'PRON',
            'we': 'PRON', 'they': 'PRON', 'me': 'PRON', 'him': 'PRON', 'her': 'PRON'
        }
        
        if word_clean in basic_vocab:
            return {
                'word': word,
                'pos': basic_vocab[word_clean],
                'confidence': 0.95,
                'method': 'basic_vocab'
            }
        
        # 2. 形態素ルール適用
        for suffix, pos in self.morphology_rules.items():
            if word_clean.endswith(suffix):
                return {
                    'word': word,
                    'pos': pos,
                    'confidence': 0.75,
                    'method': f'morphology_{suffix}'
                }
        
        # 3. 文脈推定（フォールバック）
        return {
            'word': word,
            'pos': 'UNKNOWN',
            'confidence': 0.30,
            'method': 'unknown'
        }
    
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
        """基本的なSV(O)パターンを検出（自動詞・他動詞を考慮）"""
        if len(words) < 2:
            return None
            
        # 最初の語を主語、2番目を動詞と仮定
        subject = words[0]
        verb = words[1]
        remaining_words = words[2:] if len(words) > 2 else []
        
        result = {
            'S': [{'value': subject, 'type': 'subject', 'rule_id': 'basic-sv'}],
            'V': [{'value': verb, 'type': 'verb', 'rule_id': 'basic-sv'}]
        }
        
        if remaining_words:
            # 自動詞かどうかを判定
            if self.is_intransitive_verb(verb.lower()):
                # 自動詞の場合：残りは修飾語として分類
                modifiers = self.extract_modifiers_from_words(remaining_words)
                result.update(modifiers)
            else:
                # 他動詞の場合：残りをまず目的語候補として、必要に応じて修飾語を分離
                remaining_text = " ".join(remaining_words)
                
                # 前置詞句がある場合は分離
                if any(word.lower() in ['from', 'to', 'in', 'at', 'on', 'by', 'with', 'for', 'during', 'since'] 
                       for word in remaining_words):
                    # 前置詞句以前を目的語、前置詞句を修飾語として分離
                    object_part, modifiers = self.separate_object_and_modifiers(remaining_words)
                    if object_part:
                        result['O1'] = [{'value': object_part, 'type': 'object', 'rule_id': 'basic-svo'}]
                    result.update(modifiers)
                else:
                    # 前置詞句がない場合は全て目的語
                    result['O1'] = [{'value': remaining_text, 'type': 'object', 'rule_id': 'basic-svo'}]
            
        return result
    
    def is_intransitive_verb(self, verb):
        """動詞が自動詞かどうかを判定"""
        # 主要な自動詞リスト
        intransitive_verbs = [
            'lie', 'sit', 'stand', 'sleep', 'die', 'come', 'go', 'arrive', 'depart', 
            'exist', 'happen', 'occur', 'appear', 'disappear', 'remain', 'stay',
            'rise', 'fall', 'fly', 'swim', 'dance', 'sing', 'laugh', 'cry', 'smile'
        ]
        
        return verb in intransitive_verbs
    
    def separate_object_and_modifiers(self, words):
        """他動詞文で目的語と修飾語を分離"""
        object_words = []
        modifier_start = -1
        
        # 前置詞を探して分離点を特定
        for i, word in enumerate(words):
            if word.lower() in ['from', 'to', 'in', 'at', 'on', 'by', 'with', 'for', 'during', 'since']:
                modifier_start = i
                break
        
        if modifier_start >= 0:
            object_words = words[:modifier_start]
            modifier_words = words[modifier_start:]
            
            object_part = " ".join(object_words) if object_words else ""
            modifiers = self.extract_modifiers_from_words(modifier_words)
            
            return object_part, modifiers
        else:
            # 前置詞句が見つからない場合は全て目的語
            return " ".join(words), {}
    
    def extract_modifiers_from_words(self, words):
        """単語リストから修飾語を抽出してスロットに分類"""
        if not words:
            return {}
            
        modifiers = {}
        remaining_phrase = " ".join(words)
        
        # pleaseの分離処理（文末または句読点の前にある場合）
        please_extracted = False
        if words and words[-1].lower().rstrip('?!.') == 'please':
            # 文末のplease
            modifiers['M3'] = [{'value': 'please', 'type': 'polite_expression'}]
            words = words[:-1]  # pleaseを除外
            please_extracted = True
        elif len(words) >= 2 and words[-2].lower() == 'please' and words[-1] in ['?', '!', '.']:
            # 句読点の前のplease
            modifiers['M3'] = [{'value': 'please', 'type': 'polite_expression'}]
            words = words[:-2] + [words[-1]]  # pleaseのみ除外
            please_extracted = True
        
        # 複数の修飾語が含まれている可能性を考慮して分析
        phrases_to_classify = []
        current_phrase = []
        
        i = 0
        while i < len(words):
            word = words[i]
            current_phrase.append(word)
            
            # 前置詞句の開始を検出 (from, to, in, at, on, etc.)
            if word.lower() in ['from', 'to', 'in', 'at', 'on', 'by', 'with', 'for', 'during', 'since']:
                # 前置詞句の終わりを探す（次の前置詞や文末まで）
                phrase_end = i + 1
                while phrase_end < len(words) and words[phrase_end].lower() not in ['from', 'to', 'in', 'at', 'on', 'by', 'with', 'for', 'during', 'since']:
                    phrase_end += 1
                
                # 前置詞句全体を取得
                prep_phrase = " ".join(words[i:phrase_end])
                phrases_to_classify.append(prep_phrase)
                current_phrase = []
                i = phrase_end
                continue
                
            # 副詞の検出
            elif word.lower() in ['quickly', 'slowly', 'carefully', 'quietly', 'loudly', 'well', 'badly', 'fast', 'hard', 'early', 'late']:
                phrases_to_classify.append(word)
                current_phrase = []
                
            i += 1
        
        # 残りの語句があれば追加
        if current_phrase:
            phrases_to_classify.append(" ".join(current_phrase))
        
        # 各フレーズを分類
        for phrase in phrases_to_classify:
            if phrase.strip():
                slot_info = self.classify_remaining_phrase(phrase.strip())
                slot = slot_info['slot']
                if slot not in modifiers:
                    modifiers[slot] = []
                modifiers[slot].append({
                    'value': slot_info['value'],
                    'type': slot_info['type'],
                    'rule_id': 'present-perfect-modifier'
                })
        
        return modifiers


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
