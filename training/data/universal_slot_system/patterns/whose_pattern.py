"""
Whose Pattern Implementation
whose構文での動詞/名詞同形語修正パターン

既存の個別ハンドラーから統一システムへの移行実装
"""

import re
from typing import Dict, List, Any, Tuple
from ..base_patterns import GrammarPattern


class WhosePattern(GrammarPattern):
    """
    whose構文での動詞/名詞同形語の統一修正パターン
    
    人間の認識: "whose car is red lives here" 
    → whose [名詞] [be動詞] [形容詞] [動詞] [場所] 
    → [動詞]は確実に動詞として扱う
    
    stanza誤判定: lives(NOUN, acl:relcl) → 名詞として関係節修飾
    人間修正: lives(VERB, root) → 動詞としてメイン動詞
    """
    
    def __init__(self):
        super().__init__(
            pattern_name="whose_ambiguous_verb",
            confidence_threshold=0.90
        )
        
        # 動詞/名詞同形語リスト
        self.ambiguous_verbs = [
            'lives', 'works', 'runs', 'goes', 'comes', 
            'stays', 'plays', 'looks', 'sounds', 'seems'
        ]
        
        # whose構文パターン（正規表現）
        self.whose_patterns = [
            # パターン1: whose [名詞] is [形容詞] [動詞] (here|there|in...)
            r'whose\s+\w+\s+is\s+\w+\s+{verb}\s+(here|there|in\s+\w+)',
            
            # パターン2: whose [名詞] [修飾語]* [動詞] (場所表現)
            r'whose\s+\w+.*?\s+{verb}\s+(here|there|in|at|on)\s+\w+',
            
            # パターン3: whose [名詞] [動詞] (副詞) (場所)
            r'whose\s+\w+\s+{verb}\s+\w+\s+(here|there|in|at|on)'
        ]
        
        self.description = "whose構文での動詞/名詞同形語の人間文法的判定"
        
    def detect(self, words: List, sentence: str) -> Dict[str, Any]:
        """
        whose構文パターン検出の統一実装
        
        Args:
            words: Stanza解析後の単語リスト
            sentence: 原文
            
        Returns:
            検出結果辞書
        """
        result = {
            'found': False,
            'ambiguous_verb': None,
            'confidence': 0.0,
            'target_words': [],
            'correction_data': {},
            'pattern_matches': [],
            'keywords_matched': 0,
            'total_keywords': 1
        }
        
        # whose構文チェック
        if 'whose' not in sentence.lower():
            return result
            
        # 各同形語について検証
        for verb_text in self.ambiguous_verbs:
            if verb_text not in sentence.lower():
                continue
                
            # パターンマッチング実行
            pattern_matches = self._check_whose_patterns(sentence, verb_text)
            
            if pattern_matches:
                # 該当する語を探す
                target_word = self._find_target_word(words, verb_text)
                
                if target_word:
                    result.update({
                        'found': True,
                        'ambiguous_verb': target_word,
                        'confidence': 0.95,
                        'target_words': [target_word],
                        'correction_data': {
                            'verb_text': verb_text,
                            'original_upos': target_word.upos,
                            'target_upos': 'VERB',
                            'original_deprel': target_word.deprel,
                            'target_deprel': 'root'
                        },
                        'pattern_matches': pattern_matches,
                        'keywords_matched': 1,
                        'total_keywords': 1,
                        'structure_match_score': 0.9,
                        'pos_consistency_score': 0.8,
                        'semantic_score': 0.85
                    })
                    break
                    
        return result
        
    def correct(self, doc, detection_result: Dict) -> Tuple[Any, Dict]:
        """
        whose構文修正の統一実装
        
        Args:
            doc: Stanza document
            detection_result: detect()の結果
            
        Returns:
            (修正後doc, 修正メタデータ)
        """
        if not detection_result.get('found', False):
            return doc, {}
            
        ambiguous_word = detection_result['ambiguous_verb']
        correction_data = detection_result['correction_data']
        
        # 修正情報を記録（stanzaデータ構造は不変のため、メタデータで管理）
        if not hasattr(doc, 'human_grammar_corrections'):
            doc.human_grammar_corrections = {}
            
        # 統一修正メタデータ作成
        correction_metadata = self.create_correction_metadata(
            ambiguous_word,
            {
                'upos': correction_data['original_upos'],
                'deprel': correction_data['original_deprel']
            },
            {
                'upos': correction_data['target_upos'],
                'deprel': correction_data['target_deprel'],
                'confidence': detection_result['confidence']
            }
        )
        
        # human_grammar_correctionsに追加
        doc.human_grammar_corrections[ambiguous_word.id] = correction_metadata
        
        self.logger.debug(
            f"🧠 whose構文動詞修正: {ambiguous_word.text} "
            f"{correction_data['original_upos']}→{correction_data['target_upos']} "
            f"(人間文法認識)"
        )
        
        return doc, correction_metadata
        
    def is_applicable(self, sentence: str) -> bool:
        """
        whose構文適用可能性チェック
        
        Args:
            sentence: 対象文
            
        Returns:
            適用可能フラグ
        """
        # whose必須 + 同形語存在チェック
        if 'whose' not in sentence.lower():
            return False
            
        # 少なくとも一つの同形語が含まれているか
        sentence_lower = sentence.lower()
        return any(verb in sentence_lower for verb in self.ambiguous_verbs)
        
    def _check_whose_patterns(self, sentence: str, verb_text: str) -> List[str]:
        """
        whose構文パターンのマッチングチェック
        
        Args:
            sentence: 対象文
            verb_text: チェック対象動詞
            
        Returns:
            マッチしたパターンのリスト
        """
        matches = []
        sentence_lower = sentence.lower()
        
        for pattern_template in self.whose_patterns:
            # 動詞を具体的に埋め込んだパターン作成
            pattern = pattern_template.format(verb=verb_text)
            
            if re.search(pattern, sentence_lower):
                matches.append(pattern)
                self.logger.debug(f"🎯 whoseパターンマッチ: {pattern}")
                
        return matches
        
    def _find_target_word(self, words: List, verb_text: str):
        """
        修正対象語を特定
        
        Args:
            words: 単語リスト
            verb_text: 対象動詞テキスト
            
        Returns:
            対象語（見つからない場合はNone）
        """
        for word in words:
            if (word.text.lower() == verb_text and 
                word.upos == 'NOUN' and 
                word.deprel == 'acl:relcl'):
                
                self.logger.debug(
                    f"🔍 修正対象語発見: {word.text} "
                    f"(UPOS:{word.upos}, DEPREL:{word.deprel})"
                )
                return word
                
        return None
        
    def calculate_confidence(self, detection_result: Dict) -> float:
        """
        whose構文専用の信頼度計算
        
        Args:
            detection_result: 検出結果
            
        Returns:
            計算された信頼度
        """
        if not detection_result.get('found', False):
            return 0.0
            
        base_confidence = detection_result.get('confidence', 0.95)
        
        # パターンマッチ数による調整
        pattern_matches = detection_result.get('pattern_matches', [])
        pattern_bonus = min(0.05, len(pattern_matches) * 0.02)
        
        # 構造マッチスコア
        structure_score = detection_result.get('structure_match_score', 0.9)
        
        # 最終信頼度計算
        final_confidence = min(1.0, base_confidence + pattern_bonus + (structure_score - 0.9) * 0.1)
        
        self.logger.debug(
            f"📊 whose信頼度計算: base={base_confidence:.3f}, "
            f"pattern_bonus={pattern_bonus:.3f}, "
            f"structure={structure_score:.3f}, "
            f"final={final_confidence:.3f}"
        )
        
        return final_confidence
