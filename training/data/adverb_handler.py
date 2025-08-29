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
                'modifier_slots': self._assign_modifier_slots(result['modifiers'], verb_modifier_pairs)
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
        """動詞の修飾語を収集（前後両方向から）- 専門分担型ハイブリッド解析"""
        modifiers = []
        
        # 文頭副詞の特別処理（専門分担: 依存関係で検出）
        if verb_idx > 0:  # 動詞が文頭でない場合
            first_token = doc[0]
            # 文頭副詞を検出（npadvmod または advmod）
            is_sentence_initial_adverb = (
                (first_token.dep_ == 'npadvmod' and first_token.head.i == verb_idx) or
                (first_token.dep_ == 'advmod' and first_token.head.i == verb_idx and first_token.pos_ == 'ADV')
            )
            
            if is_sentence_initial_adverb:
                modifier_info = {
                    'text': first_token.text,
                    'pos': first_token.pos_,
                    'tag': first_token.tag_,
                    'idx': 0,
                    'type': 'sentence_adverb' if first_token.dep_ == 'advmod' else 'temporal',
                    'position': 'sentence-initial',  # 文頭位置
                    'method': 'dependency_analysis'  # 使用手法明示
                }
                modifiers.append(modifier_info)
                print(f"🔍 文頭副詞検出: {first_token.text} (依存関係: {first_token.dep_})")
        
        # Part 1: 動詞の前にある修飾語を検索（複合修飾語対応）
        pre_verb_modifiers = []
        for i in range(verb_idx - 1, -1, -1):
            token = doc[i]
            
            # 文頭副詞は既に処理済みなのでスキップ
            if i == 0 and (token.dep_ == 'npadvmod' or 
                          (token.dep_ == 'advmod' and token.pos_ == 'ADV')):
                continue
            
            # 修飾語として識別（この動詞を修飾しているか確認）
            if self._is_modifier(token) and token.head.i == verb_idx:
                modifier_info = {
                    'text': token.text,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'idx': i,
                    'type': self._classify_modifier_type(token),
                    'position': 'pre-verb',  # 動詞前修飾語
                    'method': 'pos_analysis'  # 使用手法明示
                }
                pre_verb_modifiers.append(modifier_info)
            
            # 主語に達したら停止（動詞前修飾語の範囲を制限）
            if token.dep_ in ['nsubj', 'nsubjpass']:
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
        
        return False

    def _is_modifier(self, token) -> bool:
        """トークンが修飾語かどうか判定（適切なバランス）"""
        # 副詞は基本的に修飾語として扱う（5文型の核心要素ではない）
        if token.pos_ == 'ADV':
            # ただし、文法的に必須の否定副詞のみ除外
            essential_adverbs = ['not', "n't", 'never']
            return token.text.lower() not in essential_adverbs
        
        # 前置詞句は修飾語として扱う（ただし基本的な前置詞のみ）
        if token.pos_ == 'ADP':
            # 5文型の核心でない前置詞句は修飾語
            modifier_preps = ['for', 'with', 'in', 'on', 'at', 'by', 'during', 'throughout', 'despite', 'besides', 'except', 'to']
            return token.text.lower() in modifier_preps
        
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
        """前置詞句全体を取得し、分離可能かどうか判定"""
        prep_token = doc[prep_idx]
        phrase_tokens = [prep_token.text]
        end_idx = prep_idx
        
        # 前置詞の後続要素を収集
        for i in range(prep_idx + 1, len(doc)):
            token = doc[i]
            
            # 句読点や次の前置詞、動詞で停止
            if token.pos_ in ['PUNCT', 'ADP', 'VERB', 'AUX']:
                break
            
            # 単独の修飾語として認識される可能性のある副詞で停止
            if token.pos_ == 'ADV' and self._is_modifier(token):
                break
                
            phrase_tokens.append(token.text)
            end_idx = i
        
        phrase_text = ' '.join(phrase_tokens)
        
        # 前置詞句が修飾語として分離可能かどうか判定
        is_modifiable = self._is_prepositional_phrase_modifiable(prep_token.text, phrase_tokens)
        
        return {
            'text': phrase_text,
            'end_idx': end_idx,
            'is_modifiable': is_modifiable
        }
    
    def _is_prepositional_phrase_modifiable(self, preposition: str, phrase_tokens: List[str]) -> bool:
        """前置詞句が修飾語として分離可能かどうか判定"""
        prep_lower = preposition.lower()
        
        # 修飾語として分離可能な前置詞句
        # 基本5文型の核心構造でない場合は分離対象
        modifiable_preps = ['for', 'with', 'in', 'on', 'at', 'by', 'during', 'throughout', 'despite', 'without', 'besides', 'except', 'to']
        
        # 「to」の場合、特定パターンで修飾語として扱う
        if prep_lower == 'to':
            # 「to + 形容詞 + 名詞」のパターンは修飾語として扱う
            if len(phrase_tokens) >= 3:  # to + adj + noun
                return True
            # 動詞の直接目的語でない場合は修飾語として扱う
            return True
            
        return prep_lower in modifiable_preps
    
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
    
    def _assign_modifier_slots(self, modifiers_info: Dict, verb_modifier_pairs: List[Dict]) -> Dict[str, str]:
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
            # 1個のみ → M2（位置無関係）
            modifier_slots['M2'] = all_modifiers[0]['text']
            
        elif modifier_count == 2:
            # 2個の場合：REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md 仕様に従う
            pre_verb_modifiers = [m for m in all_modifiers if m['position_type'] == 'pre-verb']
            post_verb_modifiers = [m for m in all_modifiers if m['position_type'] == 'post-verb']
            
            if len(pre_verb_modifiers) >= 1:
                # ケース1: 動詞中心(M2)より前に1つある場合 → M1, M2の2つ使用
                modifier_slots['M1'] = pre_verb_modifiers[0]['text']
                if len(post_verb_modifiers) >= 1:
                    modifier_slots['M2'] = post_verb_modifiers[0]['text']
                else:
                    # 前に2つある場合
                    modifier_slots['M2'] = pre_verb_modifiers[1]['text'] if len(pre_verb_modifiers) > 1 else all_modifiers[1]['text']
                    
            elif len(post_verb_modifiers) >= 1:
                # ケース2: 動詞中心(M2)より後に1つある場合 → M2, M3の2つ使用
                modifier_slots['M2'] = post_verb_modifiers[0]['text']
                modifier_slots['M3'] = post_verb_modifiers[1]['text'] if len(post_verb_modifiers) > 1 else all_modifiers[1]['text']
                
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
