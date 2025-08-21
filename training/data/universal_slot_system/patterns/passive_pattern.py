"""
Passive Pattern Implementation
受動態パターンの統一修正実装

既存の個別ハンドラーから統一システムへの移行実装
"""

from typing import Dict, List, Any, Tuple
from ..base_patterns import GrammarPattern


class PassivePattern(GrammarPattern):
    """
    受動態パターンの統一修正システム
    
    be動詞 + 過去分詞パターンの受動態判定・修正
    
    人間の認識: "was unexpected" → be + pp → 受動態
    stanza誤判定: unexpected(root) + was(cop) → 補語構文
    人間修正: was(aux) + unexpected(root, passive) → 受動態構造
    """
    
    def __init__(self):
        super().__init__(
            pattern_name="passive_voice",
            confidence_threshold=0.85
        )
        
        # be動詞リスト
        self.be_verbs = ['be', 'am', 'is', 'are', 'was', 'were', 'been', 'being']
        
        # 過去分詞語尾パターン
        self.past_participle_endings = [
            'ed',      # 規則動詞
            'en',      # broken, chosen
            'ated',    # created, related
            'ized',    # realized, organized  
            'ified',   # classified, verified
            'ected',   # connected, expected
            'ested'    # interested, invested
        ]
        
        # 純粋形容詞（過去分詞ではない）語尾
        self.pure_adjective_patterns = ['red', 'ded', 'eed', 'ted']
        
        self.description = "be動詞 + 過去分詞の受動態パターン統一修正"
        
    def detect(self, words: List, sentence: str) -> Dict[str, Any]:
        """
        受動態パターン検出の統一実装
        
        Args:
            words: Stanza解析後の単語リスト  
            sentence: 原文
            
        Returns:
            検出結果辞書
        """
        result = {
            'found': False,
            'be_verb': None,
            'past_participle': None,
            'confidence': 0.0,
            'target_words': [],
            'correction_data': {},
            'pattern_matches': [],
            'keywords_matched': 0,
            'total_keywords': 2  # be動詞 + 過去分詞
        }
        
        # 各単語に文脈情報を追加（位置ベース判定用）
        for word in words:
            word._sentence_words = words
            
        # 構造的パターン認識実行
        passive_detection = self._detect_passive_voice_structural_pattern(words)
        
        if passive_detection['found']:
            be_verb = passive_detection['be_verb']
            past_participle = passive_detection['past_participle']
            
            # stanza誤判定チェック：過去分詞がrootで、be動詞がcop
            is_stanza_misanalysis = (
                past_participle.deprel == 'root' and 
                be_verb.deprel == 'cop'
            )
            
            if is_stanza_misanalysis:
                result.update({
                    'found': True,
                    'be_verb': be_verb,
                    'past_participle': past_participle,
                    'confidence': passive_detection['confidence'],
                    'target_words': [be_verb, past_participle],
                    'correction_data': {
                        'be_verb_original_deprel': be_verb.deprel,
                        'be_verb_target_deprel': 'aux',
                        'past_participle_original_deprel': past_participle.deprel,
                        'past_participle_target_deprel': 'root',
                        'correction_type': 'passive_voice_restructure'
                    },
                    'pattern_matches': ['be_verb_cop_past_participle_root'],
                    'keywords_matched': 2,
                    'structure_match_score': 0.9,
                    'pos_consistency_score': 0.85,
                    'semantic_score': 0.8
                })
                
        return result
        
    def correct(self, doc, detection_result: Dict) -> Tuple[Any, Dict]:
        """
        受動態修正の統一実装
        
        Args:
            doc: Stanza document
            detection_result: detect()の結果
            
        Returns:
            (修正後doc, 修正メタデータ)
        """
        if not detection_result.get('found', False):
            return doc, {}
            
        be_verb = detection_result['be_verb']
        past_participle = detection_result['past_participle']
        correction_data = detection_result['correction_data']
        
        # 修正情報を記録
        if not hasattr(doc, 'human_grammar_corrections'):
            doc.human_grammar_corrections = {}
            
        # be動詞の修正メタデータ
        be_verb_metadata = self.create_correction_metadata(
            be_verb,
            {'deprel': correction_data['be_verb_original_deprel']},
            {
                'deprel': correction_data['be_verb_target_deprel'],
                'confidence': detection_result['confidence']
            }
        )
        
        # 過去分詞の修正メタデータ
        past_participle_metadata = self.create_correction_metadata(
            past_participle,
            {'deprel': correction_data['past_participle_original_deprel']},
            {
                'deprel': correction_data['past_participle_target_deprel'],
                'confidence': detection_result['confidence']
            }
        )
        
        # human_grammar_correctionsに追加
        doc.human_grammar_corrections[be_verb.id] = be_verb_metadata
        doc.human_grammar_corrections[past_participle.id] = past_participle_metadata
        
        # 統合修正メタデータ
        combined_metadata = {
            'correction_type': 'passive_voice',
            'be_verb': be_verb_metadata,
            'past_participle': past_participle_metadata,
            'correction_description': f"Convert '{be_verb.text} {past_participle.text}' to passive voice",
            'confidence': detection_result['confidence'],
            'original_structure': f"{past_participle.text}(root) + {be_verb.text}(cop)",
            'corrected_structure': f"{be_verb.text}(aux) + {past_participle.text}(root, passive)"
        }
        
        self.logger.debug(
            f"🔄 受動態修正: '{be_verb.text} {past_participle.text}' "
            f"→ 受動態 (stanza: {past_participle.text}=root, {be_verb.text}=cop)"
        )
        
        return doc, combined_metadata
        
    def is_applicable(self, sentence: str) -> bool:
        """
        受動態パターン適用可能性チェック
        
        Args:
            sentence: 対象文
            
        Returns:
            適用可能フラグ
        """
        sentence_lower = sentence.lower()
        
        # be動詞存在チェック
        has_be_verb = any(be_verb in sentence_lower for be_verb in self.be_verbs)
        
        # 過去分詞らしき語尾存在チェック
        has_past_participle_ending = any(
            ending in sentence_lower for ending in self.past_participle_endings
        )
        
        return has_be_verb and has_past_participle_ending
        
    def _detect_passive_voice_structural_pattern(self, words):
        """構造的受動態パターン検出の統一実装"""
        result = {'found': False, 'be_verb': None, 'past_participle': None, 'confidence': 0.0}
        
        for i in range(len(words) - 1):
            current = words[i]
            next_word = words[i + 1]
            
            # パターン1: be動詞 + 直後の語
            if self._is_be_verb(current):
                confidence = 0.0
                
                # 直後が明確な過去分詞
                if self._is_past_participle(next_word):
                    confidence = 0.9
                    
                    # 高信頼度パターン
                    if next_word.xpos == 'VBN':
                        confidence = 0.95
                    elif next_word.upos == 'ADJ' and self._has_past_participle_morphology(next_word):
                        confidence = 0.8
                    
                    if confidence > result['confidence']:
                        result.update({
                            'found': True,
                            'be_verb': current,
                            'past_participle': next_word,
                            'confidence': confidence
                        })
            
            # パターン2: be動詞 + 副詞 + 過去分詞
            if (i < len(words) - 2 and 
                self._is_be_verb(current) and 
                words[i + 1].upos == 'ADV' and
                self._is_past_participle(words[i + 2])):
                
                confidence = 0.85
                if confidence > result['confidence']:
                    result.update({
                        'found': True,
                        'be_verb': current,
                        'past_participle': words[i + 2],
                        'confidence': confidence
                    })
        
        return result
        
    def _is_be_verb(self, word):
        """be動詞判定（汎用的・lemmaベース）"""
        return (word.upos == 'AUX' and word.lemma.lower() == 'be')
        
    def _is_past_participle(self, word):
        """過去分詞判定（汎用的・形態論的分析重視）"""
        # 1. stanzaの形態論的判定を最優先
        if word.xpos == 'VBN':  # Past participle
            return True
            
        # 2. be動詞直後の形容詞的語の文脈的判定
        if word.upos == 'ADJ':
            return self._contextual_past_participle_check(word)
        
        return False
        
    def _contextual_past_participle_check(self, word):
        """文脈的過去分詞判定（be動詞直後の形容詞）"""
        # be動詞直後で形容詞タグ → 受動態の可能性
        if self._follows_be_verb_directly(word):
            # 形態論的パターンチェック
            return self._has_past_participle_morphology(word)
        return False
        
    def _follows_be_verb_directly(self, word):
        """直前にbe動詞があるかチェック"""
        if hasattr(word, '_sentence_words'):
            words = word._sentence_words
            word_pos = next((i for i, w in enumerate(words) if w.id == word.id), -1)
            if word_pos > 0:
                prev_word = words[word_pos - 1]
                return self._is_be_verb(prev_word)
        return False
        
    def _has_past_participle_morphology(self, word):
        """形態論的パターンチェック（語尾分析）"""
        text = word.text.lower()
        
        # 規則動詞の-ed語尾（最低4文字以上）
        if text.endswith('ed') and len(text) > 3:
            # ただし純粋な形容詞（kindred, sacred等）を除外
            if not self._is_pure_adjective_ending(text):
                return True
        
        # -en語尾パターン（broken, chosen等）
        if text.endswith('en') and len(text) > 3:
            # listen, kitten等の名詞・動詞を除外
            if not text.endswith(('tten', 'sten', 'chen', 'len')):
                return True
        
        # 特徴的な過去分詞語尾
        if any(text.endswith(ending) for ending in self.past_participle_endings):
            return True
        
        return False
        
    def _is_pure_adjective_ending(self, text):
        """純粋な形容詞語尾（過去分詞ではない）"""
        return any(text.endswith(pattern) for pattern in self.pure_adjective_patterns)
        
    def calculate_confidence(self, detection_result: Dict) -> float:
        """
        受動態専用の信頼度計算
        
        Args:
            detection_result: 検出結果
            
        Returns:
            計算された信頼度
        """
        if not detection_result.get('found', False):
            return 0.0
            
        base_confidence = detection_result.get('confidence', 0.85)
        
        # XPOSタグの信頼性による調整
        past_participle = detection_result.get('past_participle')
        if past_participle:
            if past_participle.xpos == 'VBN':
                # 明確な過去分詞タグ
                pos_bonus = 0.1
            elif past_participle.upos == 'ADJ':
                # 形容詞タグだが形態論的に過去分詞
                pos_bonus = 0.05
            else:
                pos_bonus = 0.0
        else:
            pos_bonus = 0.0
            
        # 構造的一致度
        structure_score = detection_result.get('structure_match_score', 0.9)
        structure_bonus = (structure_score - 0.9) * 0.1
        
        # 最終信頼度計算
        final_confidence = min(1.0, base_confidence + pos_bonus + structure_bonus)
        
        self.logger.debug(
            f"📊 受動態信頼度計算: base={base_confidence:.3f}, "
            f"pos_bonus={pos_bonus:.3f}, "
            f"structure_bonus={structure_bonus:.3f}, "
            f"final={final_confidence:.3f}"
        )
        
        return final_confidence
