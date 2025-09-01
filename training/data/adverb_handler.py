#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdverbHandler: 副詞・修飾語処理ハンドラー
spaCy品詞分析ベース（ハードコーディング禁止）
責任分担原則に基づく専門ハンドラー
"""

import spacy
from typing import Dict, Any, List, Tuple

class AdverbHandler:
    """副詞・修飾語処理ハンドラー（spaCy POS判定ベース）"""
    
    def __init__(self):
        """初期化"""
        self.name = "AdverbHandler"
        self.version = "spaCy_v1.0"
        self.nlp = spacy.load('en_core_web_sm')  # spaCy品詞判定用
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        副詞・修飾語処理メイン
        
        Args:
            text: 処理対象の英語文
            
        Returns:
            Dict: 処理結果
        """
        try:
            # 文全体をspaCyで解析
            doc = self.nlp(text)
            
            # 動詞と修飾語のペアを特定
            verb_modifier_pairs = self._identify_verb_modifier_pairs(doc)
            
            if not verb_modifier_pairs:
                # 修飾語がない場合も成功として扱う（元のテキストをそのまま返す）
                return {
                    'success': True,
                    'separated_text': text,
                    'modifiers': {},
                    'verb_positions': {},
                    'modifier_slots': {}
                }
            
            # 修飾語を分離したテキストと修飾語情報を返す
            result = self._separate_modifiers(doc, verb_modifier_pairs)
            
            return {
                'success': True,
                'separated_text': result['separated_text'],
                'modifiers': result['modifiers'],
                'verb_positions': result['verb_positions'],
                'modifier_slots': self._assign_modifier_slots(result['modifiers'], verb_modifier_pairs, doc)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'処理エラー: {str(e)}'}
    
    def _identify_verb_modifier_pairs(self, doc) -> List[Dict]:
        """動詞と修飾語のペアを特定"""
        pairs = []
        
        for i, token in enumerate(doc):
            # 動詞を見つける
            if token.pos_ in ['VERB', 'AUX']:
                verb_info = {
                    'verb_idx': i,
                    'verb_text': token.text,
                    'verb_lemma': token.lemma_,
                    'modifiers': []
                }
                
                # 動詞の後続修飾語を収集
                modifiers = self._collect_verb_modifiers(doc, i)
                if modifiers:
                    verb_info['modifiers'] = modifiers
                    pairs.append(verb_info)
        
        return pairs
    
    def _collect_verb_modifiers(self, doc, verb_idx: int) -> List[Dict]:
        """動詞の修飾語を収集（前後両方向から）- 専門分担型ハイブリッド解析（受動態対応）"""
        modifiers = []
        
        # 🎯 名詞節境界を先にチェック（that節、wh節、whether節、if節）
        noun_clause_boundaries = self._detect_noun_clause_boundaries(doc)
        main_clause_verb_idx = self._find_main_clause_verb(doc)
        
        # 現在の動詞が主文の動詞でない場合、修飾語分離をスキップ
        if verb_idx != main_clause_verb_idx:
            print(f"🔧 名詞節内動詞検出: verb_idx={verb_idx}, main_verb_idx={main_clause_verb_idx} → 修飾語分離スキップ")
            return modifiers
        
        # 🎯 受動態検出: 主動詞を特定
        main_verb_idx = self._find_main_verb_for_modifiers(doc, verb_idx)
        effective_verb_idx = main_verb_idx if main_verb_idx != verb_idx else verb_idx
        print(f"🔧 修飾語基準動詞: verb_idx={verb_idx}, effective_verb_idx={effective_verb_idx}")
        
        # 文頭時間表現の特別処理（「Every morning」などの複合表現）
        if verb_idx > 1:  # 動詞が複合表現の後に位置する場合
            # npadvmodとして分析される時間表現を検索
            for i in range(min(verb_idx, 3)):  # 文頭から3語程度をチェック
                token = doc[i]
                if token.dep_ == 'npadvmod' and token.head.i == verb_idx:
                    # 時間表現の開始位置を特定（決定詞があるかチェック）
                    start_idx = i
                    if i > 0 and doc[i-1].dep_ == 'det' and doc[i-1].head.i == i:
                        start_idx = i - 1  # 決定詞から開始
                    
                    # 時間表現のテキストを構築
                    time_tokens = []
                    for j in range(start_idx, i + 1):
                        if doc[j].pos_ not in ['PUNCT']:  # 句読点を除く
                            time_tokens.append(doc[j].text)
                    
                    time_text = ' '.join(time_tokens)
                    
                    modifier_info = {
                        'text': time_text,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'idx': start_idx,
                        'type': 'temporal',
                        'position': 'sentence-initial',
                        'method': 'dependency_analysis'
                    }
                    modifiers.append(modifier_info)
                    print(f"🔍 文頭時間表現検出: {time_text} (依存関係: {token.dep_})")
                    break  # 最初の時間表現のみ処理
        
        # 文頭副詞の特別処理（「Actually」などの文副詞）
        if verb_idx > 0:  # 動詞が文頭でない場合
            first_token = doc[0]
            # 文頭副詞を検出（advmod または 一般的な文副詞）
            sentence_adverbs = ['actually', 'honestly', 'frankly', 'clearly', 'obviously', 'certainly', 'definitely', 'unfortunately', 'fortunately', 'hopefully']
            
            is_sentence_adverb = (
                (first_token.dep_ == 'advmod' and first_token.head.i == verb_idx and first_token.pos_ == 'ADV') or
                (first_token.text.lower() in sentence_adverbs and first_token.pos_ == 'ADV')
            )
            
            if is_sentence_adverb and not any(mod for mod in modifiers if mod['idx'] == 0):
                modifier_info = {
                    'text': first_token.text,
                    'pos': first_token.pos_,
                    'tag': first_token.tag_,
                    'idx': 0,
                    'type': 'sentence_adverb',
                    'position': 'sentence-initial',
                    'method': 'dependency_analysis'
                }
                modifiers.append(modifier_info)
                print(f"🔍 文頭副詞検出: {first_token.text} (依存関係: {first_token.dep_})")
        
        
        # 文頭副詞の特別処理（Actually, Fortunately等）
        if verb_idx > 0:
            first_token = doc[0]
            # 文頭副詞として明示的に検出
            sentence_adverbs = ['actually', 'fortunately', 'unfortunately', 'honestly', 'basically', 'obviously', 'clearly', 'frankly', 'seriously', 'literally']
            
            if (first_token.text.lower() in sentence_adverbs and 
                first_token.pos_ == 'ADV' and
                first_token.dep_ == 'advmod'):
                
                modifier_info = {
                    'text': first_token.text,
                    'pos': first_token.pos_,
                    'tag': first_token.tag_,
                    'idx': 0,
                    'type': 'sentence_adverb',
                    'position': 'sentence-initial',
                    'method': 'dependency_analysis'
                }
                modifiers.append(modifier_info)
                print(f"🔍 文頭副詞検出: {first_token.text} (依存関係: {first_token.dep_})")
        
        
        # Part 1: 動詞の前にある修飾語を検索（複合修飾語対応・受動態対応）
        pre_verb_modifiers = []
        for i in range(effective_verb_idx - 1, -1, -1):  # effective_verb_idx を使用
            token = doc[i]
            
            # 既に処理済みの文頭時間表現はスキップ
            if any(mod for mod in modifiers if mod['idx'] <= i <= mod['idx'] + len(mod['text'].split()) - 1):
                continue
            
            # 修飾語として識別（この動詞を修飾しているか確認・受動態対応）
            if self._is_modifier(token):
                # 受動態の場合: 副詞が主動詞を修飾する場合を特別処理
                is_passive_adverb = (
                    effective_verb_idx != verb_idx and  # 受動態
                    token.pos_ == 'ADV' and 
                    effective_verb_idx < len(doc) and
                    (token.head.i == effective_verb_idx or token.head.i == verb_idx)
                )
                
                if token.head.i == verb_idx or is_passive_adverb:
                    # 受動態の場合、位置を主動詞基準で再計算
                    position_type = 'pre-verb' if i < effective_verb_idx else 'post-verb'
                    
                    modifier_info = {
                        'text': token.text,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'idx': i,
                        'type': self._classify_modifier_type(token),
                        'position': position_type,  # 主動詞基準の位置
                        'method': 'pos_analysis_passive_aware',  # 受動態対応手法
                        'effective_verb_idx': effective_verb_idx  # デバッグ用
                    }
                    pre_verb_modifiers.append(modifier_info)
                    print(f"🔍 受動態副詞検出: {token.text} (位置: {position_type}, 基準動詞idx: {effective_verb_idx})")
            
            # 主語に達したら停止（動詞前修飾語の範囲を制限）
            if token.dep_ in ['nsubj', 'nsubjpass']:
                break
                break
        
        # 複合修飾語の結合処理（例: "very carefully"）
        pre_verb_modifiers = self._merge_compound_modifiers(doc, pre_verb_modifiers)
        modifiers.extend(pre_verb_modifiers)
        
        # Part 2: 動詞の直後から文末まで（または次の主要要素まで）を検索
        i = verb_idx + 1
        while i < len(doc):
            token = doc[i]
            
            # 句読点で停止
            if token.pos_ == 'PUNCT':
                break
            
            # 次の動詞で停止（主節の動詞など）
            if token.pos_ in ['VERB', 'AUX'] and self._is_main_clause_verb(doc, i):
                break
            
            # 時間表現の特別処理（"every day", "last week", "next month"など）
            if token.text.lower() in ['every', 'each', 'last', 'next', 'this', 'that'] and i + 1 < len(doc):
                next_token = doc[i + 1]
                # 時間名詞をチェック
                time_nouns = ['day', 'week', 'month', 'year', 'morning', 'afternoon', 'evening', 'night', 'time', 'moment', 
                             'summer', 'winter', 'spring', 'autumn', 'fall', 'season', 'today', 'tomorrow', 'yesterday']
                if next_token.text.lower() in time_nouns:
                    time_phrase = f"{token.text} {next_token.text}"
                    modifier_info = {
                        'text': time_phrase,
                        'pos': 'ADV',  # 時間副詞句として扱う
                        'tag': 'RB',
                        'idx': i,
                        'type': 'temporal_phrase',
                        'phrase_end': i + 1,
                        'position': 'post-verb',
                        'method': 'compound_detection'
                    }
                    modifiers.append(modifier_info)
                    print(f"🔍 時間副詞句検出: {time_phrase}")
                    # 前置詞句の残りの部分をスキップ
                    i = i + 2
                    continue
            
            # 単体時間名詞の処理（"day"が単独で現れる場合も）
            if (token.text.lower() in ['day', 'week', 'month', 'year', 'morning', 'afternoon', 'evening', 'night'] and 
                i > 0 and doc[i-1].text.lower() in ['every', 'each', 'last', 'next', 'this', 'that']):
                # 前のトークンと合わせて時間表現として処理
                prev_token = doc[i-1]
                time_phrase = f"{prev_token.text} {token.text}"
                
                # 既に処理済みかチェック
                already_processed = any(mod for mod in modifiers if mod['idx'] == i-1)
                if not already_processed:
                    modifier_info = {
                        'text': time_phrase,
                        'pos': 'ADV',  # 時間副詞句として扱う
                        'tag': 'RB',
                        'idx': i-1,
                        'type': 'temporal_phrase',
                        'phrase_end': i,
                        'position': 'post-verb',
                        'method': 'retroactive_compound_detection'
                    }
                    modifiers.append(modifier_info)
                    print(f"🔍 遡及時間副詞句検出: {time_phrase}")
                    continue
            
            # 修飾語として識別（保守的判定）
            if self._is_modifier(token):
                # 前置詞句の場合は全体をチェック
                if token.pos_ == 'ADP':
                    prep_phrase = self._get_prepositional_phrase(doc, i)
                    if prep_phrase['is_modifiable']:
                        modifier_info = {
                            'text': prep_phrase['text'],
                            'pos': token.pos_,
                            'tag': token.tag_,
                            'idx': i,
                            'type': 'prepositional_phrase',
                            'phrase_end': prep_phrase['end_idx'],
                            'position': 'post-verb'  # 動詞後修飾語
                        }
                        modifiers.append(modifier_info)
                        # 前置詞句の残りの部分をスキップ
                        i = prep_phrase['end_idx'] + 1
                        continue
                else:
                    modifier_info = {
                        'text': token.text,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'idx': i,
                        'type': self._classify_modifier_type(token),
                        'position': 'post-verb'  # 動詞後修飾語
                    }
                    modifiers.append(modifier_info)
            
            i += 1
        
        # 複合修飾語の結合処理（post-verb修飾語にも適用）
        modifiers = self._merge_compound_modifiers(doc, modifiers)
        
        return modifiers
    
    def _merge_compound_modifiers(self, doc, modifiers: List[Dict]) -> List[Dict]:
        """適切な修飾語のみを結合（例: "very carefully" → 1つの修飾語）"""
        if len(modifiers) <= 1:
            return modifiers
        
        # インデックス順でソート
        modifiers.sort(key=lambda x: x['idx'])
        
        merged = []
        i = 0
        
        while i < len(modifiers):
            current = modifiers[i]
            
            # 次の修飾語と隣接しているかチェック
            if i + 1 < len(modifiers):
                next_mod = modifiers[i + 1]
                
                # 隣接している（間に1トークンまで許容）
                if next_mod['idx'] - current['idx'] <= 2:
                    # 結合可能かチェック（厳格な条件）
                    if self._can_merge_modifiers(doc, current, next_mod):
                        # 複合修飾語として結合
                        start_idx = current['idx']
                        end_idx = next_mod['idx']
                        
                        # 結合テキストを作成
                        compound_text = ' '.join([doc[j].text for j in range(start_idx, end_idx + 1)])
                        
                        merged_modifier = {
                            'text': compound_text,
                            'pos': next_mod['pos'],  # メインの修飾語のPOSを使用
                            'tag': next_mod['tag'],
                            'idx': start_idx,
                            'type': next_mod['type'],
                            'position': current['position'],
                            'method': 'compound_merge'
                        }
                        
                        merged.append(merged_modifier)
                        i += 2  # 両方の修飾語をスキップ
                        continue
            
            # 結合しない場合はそのまま追加
            merged.append(current)
            i += 1
        
        return merged
    
    def _can_merge_modifiers(self, doc, first_mod: Dict, second_mod: Dict) -> bool:
        """2つの修飾語が結合可能かチェック（厳格な条件）"""
        first_token = doc[first_mod['idx']]
        second_token = doc[second_mod['idx']]
        
        # 前置詞句は他の修飾語と結合しない
        if first_mod['type'] == 'prepositional_phrase' or second_mod['type'] == 'prepositional_phrase':
            return False
        
        # 程度副詞 + 副詞 の組み合わせ
        degree_adverbs = ['very', 'quite', 'rather', 'extremely', 'incredibly', 'really', 'truly', 'highly', 'perfectly', 'completely']
        
        if (first_token.text.lower() in degree_adverbs and 
            first_token.pos_ == 'ADV' and 
            second_token.pos_ == 'ADV'):
            return True
        
        # 時間表現の結合（last week, next month, etc.）
        time_determiners = ['last', 'next', 'this', 'every']
        time_nouns = ['week', 'month', 'year', 'day', 'morning', 'afternoon', 'evening', 'night']
        
        if (first_token.text.lower() in time_determiners and 
            second_token.text.lower() in time_nouns and
            second_mod['idx'] - first_mod['idx'] == 1):  # 厳密に隣接
            return True
        
        # 注意: 副詞 + and + 副詞 は結合しない（分離してM-slotに個別に割り当てる）
        
        return False

    def _is_modifier(self, token) -> bool:
        """トークンが修飾語かどうか判定（spaCy依存関係ベース）"""
        # 副詞は基本的に修飾語として扱う（5文型の核心要素ではない）
        if token.pos_ == 'ADV':
            # ただし、文法的に必須の否定副詞のみ除外
            essential_adverbs = ['not', "n't", 'never']
            return token.text.lower() not in essential_adverbs
        
        # 前置詞句の判定：spaCyの依存関係を使用
        if token.pos_ == 'ADP':
            # 前置詞が動詞を修飾しているかチェック（依存関係 prep）
            if token.dep_ == 'prep' and token.head.pos_ == 'VERB':
                return True
            # または前置詞が動詞に対して副詞的に機能している場合
            if token.dep_ in ['prep', 'advmod'] and token.head.pos_ in ['VERB', 'ADJ', 'ADV']:
                return True
            # 5文型の必須要素（to不定詞など）は除外
            essential_prep_patterns = [
                'to',  # to不定詞（ただし副詞的用法は含める）
            ]
            if token.text.lower() in essential_prep_patterns:
                # to不定詞の場合、副詞的用法なら修飾語として扱う
                if token.text.lower() == 'to' and token.dep_ == 'aux':
                    return False  # 不定詞のto
                # その他の副詞的なtoは修飾語
                return True
            return True  # その他の前置詞は基本的に修飾語
        
        # 明確な時間・場所副詞（場所副詞here/thereは修飾語として扱う）
        if token.pos_ in ['NOUN', 'PROPN']:
            temporal_locative = ['yesterday', 'today', 'tomorrow', 'here', 'there', 'week', 'month', 'year', 'morning', 'afternoon', 'evening', 'night']
            return token.text.lower() in temporal_locative
        
        # 形容詞が副詞的に使われている場合（時間表現など）
        if token.pos_ == 'ADJ':
            time_adjectives = ['last', 'next', 'daily', 'weekly', 'monthly', 'yearly']
            return token.text.lower() in time_adjectives
        
        # 場所副詞here/thereは修飾語として扱う
        if token.pos_ == 'ADV' and token.text.lower() in ['here', 'there']:
            return True
        
        return False
    
    def _is_adverbial_noun(self, token) -> bool:
        """副詞的な名詞かどうか判定（場所・時間など）"""
        # 場所・時間を表す一般的な語
        adverbial_patterns = [
            'here', 'there', 'everywhere', 'somewhere',
            'today', 'yesterday', 'tomorrow', 'now',
            'home', 'abroad', 'upstairs', 'downtown'
        ]
        
        return token.text.lower() in adverbial_patterns
    
    def _get_prepositional_phrase(self, doc, prep_idx: int) -> Dict:
        """前置詞句全体を取得し、分離可能かどうか判定（spaCy依存関係ベース）"""
        prep_token = doc[prep_idx]
        phrase_tokens = [prep_token.text]
        end_idx = prep_idx
        
        # spaCyの依存関係を使って前置詞句の範囲を特定
        # 前置詞の子要素（通常はpobj = prepositional object）を探す
        phrase_indices = {prep_idx}
        
        def add_subtree(token):
            """トークンとその子要素を再帰的に追加"""
            phrase_indices.add(token.i)
            for child in token.children:
                add_subtree(child)
        
        # 前置詞の子要素（目的語とその修飾語）を取得
        for child in prep_token.children:
            if child.dep_ == 'pobj':  # prepositional object
                add_subtree(child)
        
        # インデックスをソートして連続的な句を作成
        sorted_indices = sorted(phrase_indices)
        
        # 連続している範囲のみを取得（途切れる場合は前置詞句の終了）
        continuous_indices = [prep_idx]
        for idx in sorted_indices:
            if idx > prep_idx and (not continuous_indices or idx == continuous_indices[-1] + 1):
                continuous_indices.append(idx)
            elif idx > prep_idx:
                break  # 連続性が途切れた
        
        # フレーズテキストを作成
        phrase_tokens = [doc[i].text for i in continuous_indices]
        end_idx = continuous_indices[-1]
        phrase_text = ' '.join(phrase_tokens)
        
        # 前置詞句が修飾語として分離可能かどうか判定
        is_modifiable = self._is_prepositional_phrase_modifiable_by_dependency(prep_token)
        
        return {
            'text': phrase_text,
            'end_idx': end_idx,
            'is_modifiable': is_modifiable
        }
    
    def _is_prepositional_phrase_modifiable_by_dependency(self, prep_token) -> bool:
        """spaCyの依存関係に基づいて前置詞句が修飾語として分離可能かどうか判定"""
        # 前置詞が動詞を修飾している場合（dep_=prep）は通常修飾語
        if prep_token.dep_ == 'prep' and prep_token.head.pos_ == 'VERB':
            return True
        
        # 副詞的修飾（advmod）の場合も修飾語
        if prep_token.dep_ == 'advmod':
            return True
        
        # agent句（受動文のby句）は修飾語
        if prep_token.dep_ == 'agent':
            return True
        
        # 5文型の必須要素かどうかチェック
        # - dobj, iobj, attr, acomp などの場合は必須要素なので分離不可
        essential_deps = ['dobj', 'iobj', 'attr', 'acomp', 'xcomp', 'ccomp']
        if prep_token.dep_ in essential_deps:
            return False
        
        # その他は基本的に修飾語として扱う
        return True
    
    def _classify_modifier_type(self, token) -> str:
        """修飾語の種類を分類"""
        if token.pos_ == 'ADV':
            return 'adverb'
        elif token.pos_ == 'ADP':
            return 'prepositional'
        elif self._is_adverbial_noun(token):
            return 'adverbial_noun'
        else:
            return 'other'
    
    def _is_main_clause_verb(self, doc, verb_idx: int) -> bool:
        """主節の動詞かどうか判定（関係節内の動詞と区別）"""
        # 簡易判定：関係代名詞より後にある動詞は関係節、
        # それより前または関係代名詞がない場合は主節
        relative_pronouns = ['who', 'which', 'that', 'whom', 'whose']
        
        # 関係代名詞の位置を特定
        rel_pronoun_idx = None
        for i, token in enumerate(doc):
            if token.text.lower() in relative_pronouns:
                rel_pronoun_idx = i
                break
        
        # 関係代名詞がない場合、主節の動詞
        if rel_pronoun_idx is None:
            return True
        
        # 関係代名詞より後の最初の動詞は関係節、その後は主節
        if verb_idx > rel_pronoun_idx:
            # 関係節内の最初の動詞をチェック
            first_rel_verb_idx = None
            for i in range(rel_pronoun_idx + 1, len(doc)):
                if doc[i].pos_ in ['VERB', 'AUX']:
                    first_rel_verb_idx = i
                    break
            
            # 関係節内の最初の動詞ではない場合、主節の動詞
            return verb_idx != first_rel_verb_idx
        
        return True
    
    def _separate_modifiers(self, doc, verb_modifier_pairs: List[Dict]) -> Dict:
        """修飾語を分離したテキストと修飾語情報を生成"""
        separated_tokens = []
        modifiers_info = {}
        verb_positions = {}
        
        modifier_indices = set()
        
        # 修飾語のインデックスを収集
        for pair in verb_modifier_pairs:
            verb_idx = pair['verb_idx']
            verb_text = pair['verb_text']
            
            # 動詞位置を記録
            verb_positions[verb_idx] = {
                'original_text': verb_text,
                'modifiers': []
            }
            
            for modifier in pair['modifiers']:
                modifier_idx = modifier['idx']
                modifier_text = modifier['text']
                
                # 結合された修飾語の場合、すべてのトークンインデックスを収集
                if modifier.get('method') == 'compound_merge':
                    # 結合された修飾語のすべてのトークンを削除対象にする
                    phrase_parts = modifier_text.split()
                    current_idx = modifier_idx
                    for part in phrase_parts:
                        if current_idx < len(doc):
                            modifier_indices.add(current_idx)
                            current_idx += 1
                elif modifier['type'] == 'prepositional_phrase':
                    # 前置詞句のすべてのトークンを削除対象にする
                    phrase_parts = modifier_text.split()
                    current_idx = modifier_idx
                    for part in phrase_parts:
                        if current_idx < len(doc) and doc[current_idx].text == part:
                            modifier_indices.add(current_idx)
                            current_idx += 1
                elif modifier['type'] == 'temporal_phrase':
                    # 時間副詞句のすべてのトークンを削除対象にする（"every day"など）
                    phrase_parts = modifier_text.split()
                    current_idx = modifier_idx
                    for part in phrase_parts:
                        if current_idx < len(doc) and doc[current_idx].text.lower() == part.lower():
                            modifier_indices.add(current_idx)
                            current_idx += 1
                            modifier_indices.add(current_idx)
                            current_idx += 1
                elif ' ' in modifier_text:
                    # 複数語の修飾語（時間表現などを含む）
                    phrase_parts = modifier_text.split()
                    current_idx = modifier_idx
                    for part in phrase_parts:
                        if current_idx < len(doc) and doc[current_idx].text == part:
                            modifier_indices.add(current_idx)
                            current_idx += 1
                else:
                    # 単一語の修飾語
                    modifier_indices.add(modifier_idx)
                
                # 修飾語情報を記録
                if verb_idx not in modifiers_info:
                    modifiers_info[verb_idx] = []
                
                modifiers_info[verb_idx].append({
                    'text': modifier['text'],
                    'type': modifier['type'],
                    'pos': modifier['pos'],
                    'idx': modifier['idx']  # インデックス情報を保持
                })
                
                verb_positions[verb_idx]['modifiers'].append(modifier['text'])
        
        # 副詞間の接続詞「and」を削除対象に追加
        for i in range(len(doc) - 2):
            if (i in modifier_indices and  # 最初の副詞
                i + 1 < len(doc) and doc[i + 1].text.lower() == 'and' and
                i + 2 in modifier_indices and  # 次の副詞
                doc[i].pos_ == 'ADV' and doc[i + 2].pos_ == 'ADV'):
                modifier_indices.add(i + 1)  # 「and」を削除対象に追加
        
        # 修飾語を除いたテキストを構築
        for i, token in enumerate(doc):
            if i not in modifier_indices:
                separated_tokens.append(token.text)
        
        separated_text = ' '.join(separated_tokens)
        
        return {
            'separated_text': separated_text,
            'modifiers': modifiers_info,
            'verb_positions': verb_positions
        }
    
    def _assign_modifier_slots(self, modifiers_info: Dict, verb_modifier_pairs: List[Dict], doc) -> Dict[str, str]:
        """
        REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md仕様に従って修飾語をMスロットに配置
        
        【前後分散配置ルール】（2025年8月確定版）:
        1個のみ → M2（位置無関係）
        2個の場合：
        - 前に1つ、後に1つ → M1（前）, M3（後）, M2は空
        - 前のみ2つ → M1, M2
        - 後のみ2つ → M2, M3
        3個 → M1, M2, M3（位置順）
        """
        modifier_slots = {}
        
        if not modifiers_info:
            return modifier_slots
        
        # 全修飾語を収集（重複除去付き）
        all_modifiers = []
        seen_modifiers = set()  # 重複防止
        
        for verb_idx, modifier_list in modifiers_info.items():
            for modifier_info in modifier_list:
                modifier_text = modifier_info['text']
                
                # 重複チェック
                if modifier_text in seen_modifiers:
                    continue
                seen_modifiers.add(modifier_text)
                
                # 動詞位置を取得
                verb_position = verb_idx
                modifier_position = modifier_info.get('idx', 0)
                
                all_modifiers.append({
                    'text': modifier_text,
                    'verb_idx': verb_idx,
                    'modifier_idx': modifier_position,
                    'position_type': 'pre-verb' if modifier_position < verb_position else 'post-verb'
                })
        
        # 修飾語を文中の位置順でソート
        all_modifiers.sort(key=lambda x: x['modifier_idx'])
        
        modifier_count = len(all_modifiers)
        
        if modifier_count == 1:
            # 🔥 REPHRASE仕様：1個のみ → 必ずM2に配置（位置無関係）
            modifier = all_modifiers[0]
            modifier_slots['M2'] = modifier['text']
            
        elif modifier_count == 2:
            # 特別ケース: 「副詞 and 副詞」パターンを先にチェック
            if (all_modifiers[1]['modifier_idx'] - all_modifiers[0]['modifier_idx'] == 2):
                # 間に「and」があるかチェック
                and_idx = all_modifiers[0]['modifier_idx'] + 1
                if and_idx < len(doc) and doc[and_idx].text.lower() == 'and':
                    # 「quickly」と「and carefully」として分割
                    modifier_slots['M2'] = all_modifiers[0]['text']
                    modifier_slots['M3'] = f"and {all_modifiers[1]['text']}"
                    print(f"🔧 「副詞 and 副詞」パターン検出: M2='{all_modifiers[0]['text']}', M3='and {all_modifiers[1]['text']}'")
                    return modifier_slots
                    
            # 2個の場合：距離ベースルール適用
            
            # 動詞位置を取得（最初の動詞を使用）
            verb_idx = all_modifiers[0]['verb_idx']
            
            # 各修飾語と動詞の距離を計算
            modifier1 = all_modifiers[0]
            modifier2 = all_modifiers[1]
            
            distance1 = abs(modifier1['modifier_idx'] - verb_idx)
            distance2 = abs(modifier2['modifier_idx'] - verb_idx)
            
            # 🔧 Agent句（by句）の特別処理
            by_clause_modifiers = []
            regular_modifiers = []
            
            for modifier in all_modifiers:
                if modifier['text'].lower().startswith('by '):
                    by_clause_modifiers.append(modifier)
                else:
                    regular_modifiers.append(modifier)
            
            # Agent句がある場合の特別配置: M2（副詞）, M3（by句）
            if len(by_clause_modifiers) == 1 and len(regular_modifiers) == 1:
                modifier_slots['M2'] = regular_modifiers[0]['text']
                modifier_slots['M3'] = by_clause_modifiers[0]['text']
                return modifier_slots
            
            # 距離ベース配置: 動詞に近い方がM2、遠い方がM1/M3
            if distance1 <= distance2:
                # modifier1が動詞に近い
                closer_modifier = modifier1
                farther_modifier = modifier2
            else:
                # modifier2が動詞に近い
                closer_modifier = modifier2
                farther_modifier = modifier1
            
            # 動詞に近い修飾語は常にM2
            modifier_slots['M2'] = closer_modifier['text']
            
            # 遠い修飾語は位置によってM1またはM3
            if farther_modifier['modifier_idx'] < verb_idx:
                modifier_slots['M1'] = farther_modifier['text']  # 動詞より前
            else:
                modifier_slots['M3'] = farther_modifier['text']  # 動詞より後
            
        elif modifier_count == 3:
            # 3個 → M1, M2, M3（位置順）
            modifier_slots['M1'] = all_modifiers[0]['text']
            modifier_slots['M2'] = all_modifiers[1]['text']
            modifier_slots['M3'] = all_modifiers[2]['text']
        
        return modifier_slots
    
    def _get_verb_positions(self, verb_modifier_pairs: List[Dict]) -> List[int]:
        """動詞の位置リストを取得"""
        positions = []
        for pair in verb_modifier_pairs:
            positions.append(pair['verb_idx'])
        return positions
    
    def _find_main_verb_for_modifiers(self, doc, verb_idx: int) -> int:
        """
        修飾語処理用の主動詞を検出（受動態対応）
        
        Args:
            doc: spaCy Doc オブジェクト
            verb_idx: 現在の動詞インデックス
            
        Returns:
            int: 主動詞のインデックス
        """
        # 受動態パターンの検出
        verb_token = doc[verb_idx]
        
        # be動詞の場合、次の過去分詞を探す
        if verb_token.lemma_ == 'be' or verb_token.text.lower() in ['am', 'is', 'are', 'was', 'were', 'being']:
            for i in range(verb_idx + 1, len(doc)):
                next_token = doc[i]
                # 副詞はスキップ
                if next_token.pos_ == 'ADV':
                    continue
                # 過去分詞を発見
                if next_token.pos_ == 'VERB' and next_token.tag_ == 'VBN':
                    print(f"🔧 受動態主動詞検出: be動詞idx={verb_idx} → 主動詞idx={i} ({next_token.text})")
                    return i
                # 他の品詞に達したら停止
                if next_token.pos_ in ['NOUN', 'PRON', 'PROPN', 'ADP']:
                    break
        
        # 通常の動詞の場合はそのまま返す
        return verb_idx

    def _detect_noun_clause_boundaries(self, doc) -> List[Dict]:
        """名詞節の境界を検出"""
        boundaries = []
        
        for i, token in enumerate(doc):
            # that節の検出
            if token.text.lower() == 'that' and token.dep_ == 'mark':
                boundaries.append({
                    'type': 'that_clause',
                    'start': i,
                    'connector': 'that'
                })
            
            # wh節の検出
            elif token.text.lower() in ['what', 'who', 'whom', 'whose', 'which', 'where', 'when', 'why', 'how']:
                if token.dep_ in ['nsubj', 'dobj', 'pobj', 'advmod']:
                    boundaries.append({
                        'type': 'wh_clause',
                        'start': i,
                        'connector': token.text.lower()
                    })
            
            # whether/if節の検出
            elif token.text.lower() in ['whether', 'if'] and token.dep_ == 'mark':
                boundaries.append({
                    'type': 'whether_if_clause',
                    'start': i,
                    'connector': token.text.lower()
                })
        
        return boundaries
    
    def _find_main_clause_verb(self, doc) -> int:
        """主文の動詞位置を特定（助動詞文対応）"""
        # 最初にROOTを探す
        root_idx = -1
        for i, token in enumerate(doc):
            if token.dep_ == 'ROOT':
                root_idx = i
                break
        
        if root_idx == -1:
            return -1
        
        # 助動詞文の場合、実際の主動詞を探す
        root_token = doc[root_idx]
        
        # "used to", "going to" などの助動詞構造を特定
        if (root_token.text.lower() in ['used', 'going'] and 
            root_idx + 1 < len(doc) and 
            doc[root_idx + 1].text.lower() == 'to'):
            
            # 次の動詞（xcomp）を主動詞として扱う
            for i in range(root_idx + 2, len(doc)):
                token = doc[i]
                if token.dep_ == 'xcomp' and token.pos_ == 'VERB':
                    print(f"🔧 助動詞文主動詞検出: {root_token.text} to {token.text} → 主動詞は {token.text} (idx: {i})")
                    return i
        
        # その他の助動詞の場合も確認
        if root_token.pos_ in ['AUX', 'VERB']:
            # xcompまたはvcompが主動詞の可能性
            for i in range(root_idx + 1, len(doc)):
                token = doc[i]
                if token.dep_ in ['xcomp', 'ccomp'] and token.pos_ == 'VERB':
                    print(f"🔧 助動詞文主動詞検出: {root_token.text} + {token.text} → 主動詞は {token.text} (idx: {i})")
                    return i
        
        return root_idx
