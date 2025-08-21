"""
AdverbialPattern - Phase 2 副詞構文処理システム
副詞句・副詞節の統一的処理

Phase 2 Component: 予想効果 +6%
対象パターン:
- very carefully (複合副詞句)
- in the morning (前置詞句)
- when he arrived (副詞節)
- more quickly (比較副詞)
"""

from universal_slot_system.base_patterns import BasePattern


class AdverbialPattern(BasePattern):
    def __init__(self):
        super().__init__(pattern_name="adverbial_clause", confidence_threshold=0.85)
        
        # 複合副詞句パターン (ADV + ADV)
        self.complex_adverb_intensifiers = {
            'very', 'quite', 'extremely', 'really', 'so', 'too', 'rather', 
            'fairly', 'pretty', 'absolutely', 'completely', 'totally'
        }
        
        # 前置詞句パターン (将来実装)
        self.prep_patterns = {
            'time': ['in', 'at', 'on', 'during', 'before', 'after'],
            'place': ['in', 'at', 'on', 'under', 'over', 'beside'],
            'manner': ['with', 'by', 'through', 'via']
        }
        
        # 副詞節パターン (将来実装)
        self.clause_markers = {
            'time': ['when', 'while', 'before', 'after', 'until', 'since'],
            'reason': ['because', 'since', 'as'],
            'condition': ['if', 'unless', 'provided'],
            'contrast': ['although', 'though', 'while']
        }
        
    def detect(self, analysis_doc, sentence):
        """副詞構文パターンの検出 (BasePatternインターフェース対応)"""
        
        # Stanza解析結果の検証
        if not hasattr(analysis_doc, 'sentences') or not analysis_doc.sentences:
            return {'found': False, 'confidence': 0.0}
            
        tokens = analysis_doc.sentences[0].words
        
        # Phase 1: 複合副詞句検出 (ADV + ADV)
        complex_adverb_detected = self._detect_complex_adverbs(tokens)
        
        if complex_adverb_detected:
            return {
                'found': True,
                'confidence': self.confidence_threshold,
                'adverb_type': 'complex',
                'pattern_data': complex_adverb_detected
            }
            
        return {'found': False, 'confidence': 0.0}
        
    def _detect_complex_adverbs(self, tokens):
        """複合副詞句の検出 (very carefully, quite slowly等)"""
        
        for i in range(len(tokens) - 1):
            current_token = tokens[i]
            next_token = tokens[i + 1]
            
            # ADV + ADV パターン検出
            if (current_token.upos == 'ADV' and next_token.upos == 'ADV' and
                current_token.text.lower() in self.complex_adverb_intensifiers):
                return {
                    'intensifier': current_token.text,
                    'target_adverb': next_token.text,
                    'phrase': f"{current_token.text} {next_token.text}",
                    'position': i
                }
                
        return None
        
    def correct(self, analysis_doc, detection_result):
        """副詞構文に基づくスロット修正 (BasePatternインターフェース対応)"""
        
        if not detection_result.get('found', False):
            return analysis_doc, {}
            
        if not hasattr(analysis_doc, 'sentences') or not analysis_doc.sentences:
            return analysis_doc, {}
            
        tokens = analysis_doc.sentences[0].words
        
        # 仮のスロットデータで動作テスト
        dummy_slots = {'S': '', 'V': '', 'M2': ''}
        
        # 複合副詞句処理
        enhanced_slots = self._enhance_adverbial_slots(tokens, dummy_slots, "")
        
        correction_metadata = {
            'pattern_applied': self.pattern_name,
            'confidence': detection_result.get('confidence', 0.0),
            'enhanced_slots': self._make_json_safe(enhanced_slots)
        }
        
        return analysis_doc, correction_metadata
        
    def _enhance_adverbial_slots(self, tokens, slot_data, sentence):
        """副詞構文に基づくスロット強化"""
        
        enhanced = slot_data.copy()
        
        # 複合副詞句の処理
        for i in range(len(tokens) - 1):
            current_token = tokens[i]
            next_token = tokens[i + 1]
            
            # ADV + ADV パターン検出・処理
            if (current_token.upos == 'ADV' and next_token.upos == 'ADV' and
                current_token.text.lower() in self.complex_adverb_intensifiers):
                
                adverb_phrase = f"{current_token.text} {next_token.text}"
                
                # M2スロットに複合副詞句を配置
                if 'M2' not in enhanced or not enhanced['M2']:
                    enhanced['M2'] = adverb_phrase
                else:
                    # 既存のM2に追加
                    enhanced['M2'] = f"{enhanced['M2']} {adverb_phrase}"
                
                # サブスロット情報追加
                if 'sub-m2' not in enhanced:
                    enhanced['sub-m2'] = adverb_phrase
                else:
                    enhanced['sub-m2'] = f"{enhanced['sub-m2']}, {adverb_phrase}"
                    
        return enhanced
        
    def _make_json_safe(self, data):
        """JSON安全なデータ変換 (ParticiplePatternと同じ構造)"""
        
        if isinstance(data, dict):
            return {k: self._make_json_safe(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_json_safe(item) for item in data]
        elif hasattr(data, '__dict__'):
            # Stanza Documentオブジェクト等の処理
            return str(data)
        else:
            return data
            
    def get_confidence(self):
        """信頼度スコア"""
        return 0.85  # 複合副詞句は比較的検出しやすい
        
    def get_priority(self):
        """処理優先度"""
        return 3  # ParticiplePattern(4)より低め
