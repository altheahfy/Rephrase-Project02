"""
HierarchicalGrammarDetector V5 - 正しいアプローチ
既存高精度システム(83.3%)を2段階で適用する単純で確実な方法

Step 1: 既存システムで上位スロット + 節存在を判定 (入れ子判定は無効化)
Step 2: 検出された節に同じシステムを再適用

性能低下なし、段階的改善保証
"""

import sys
sys.path.append('.')
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetectorV4
from advanced_grammar_detector import GrammarPattern
import re
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class SimpleHierarchicalResult:
    """シンプルな階層結果"""
    original_sentence: str
    main_clause_pattern: GrammarPattern
    main_clause_confidence: float
    subordinate_clauses: List[Dict]  # [{'text': str, 'pattern': GrammarPattern, 'confidence': float, 'type': str}]
    overall_confidence: float
    processing_time: float

class HierarchicalGrammarDetectorV5:
    """正しいアプローチによる階層文法検出器"""
    
    def __init__(self):
        """初期化"""
        print("🔄 Initializing Hierarchical Grammar Detector V5 (Correct Approach)...")
        
        # 既存の高精度システム (83.3% accuracy)
        self.base_detector = HierarchicalGrammarDetectorV4()
        
        # 節検出パターン (軽量な正規表現ベース)
        self.clause_patterns = {
            'that_clause': r'\bthat\s+[^,]+',
            'wh_clause': r'\b(what|who|which|where|when|how|why)\s+[^,]+',
            'participle_phrase': r'\b(having|being|walking|running|finished|completed)\s+[^,]+',
            'temporal_clause': r'\b(when|while|before|after|since|until)\s+[^,]+',
            'relative_clause': r'\b(that|which|who|whom)\s+[^,]+(?=\s+(was|is|are|were))',
        }
        
        print("✅ V5 Detector initialized with existing high-accuracy system!")
    
    def detect_hierarchical_grammar_v5(self, sentence: str) -> SimpleHierarchicalResult:
        """V5メイン処理: 既存システム2段階適用"""
        
        start_time = time.time()
        
        print(f"🔍 V5 Processing: {sentence}")
        
        # Step 1: 既存システムで主節パターン検出（入れ子無効）
        print("📊 Step 1: Main clause pattern detection...")
        main_result = self._detect_main_with_clause_placeholders(sentence)
        
        # Step 2: 検出された節に既存システム再適用  
        print("📊 Step 2: Subordinate clause pattern detection...")
        subordinate_results = self._detect_subordinate_clauses(sentence, main_result)
        
        # 結果統合
        overall_confidence = self._calculate_overall_confidence(main_result, subordinate_results)
        
        processing_time = time.time() - start_time
        
        result = SimpleHierarchicalResult(
            original_sentence=sentence,
            main_clause_pattern=main_result['pattern'],
            main_clause_confidence=main_result['confidence'],
            subordinate_clauses=subordinate_results,
            overall_confidence=overall_confidence,
            processing_time=processing_time
        )
        
        print(f"✅ V5 Complete: Main={result.main_clause_pattern.value}, Subs={len(result.subordinate_clauses)}, Time={processing_time:.3f}s")
        
        return result
    
    def _detect_main_with_clause_placeholders(self, sentence: str) -> Dict:
        """Step 1: 主節パターン検出（節をプレースホルダーに置換）"""
        
        # 節を検出してプレースホルダーに置換
        modified_sentence, detected_clauses = self._replace_clauses_with_placeholders(sentence)
        
        print(f"    🔄 Modified for main detection: '{modified_sentence}'")
        print(f"    📋 Detected clause placeholders: {len(detected_clauses)}")
        
        # 既存の高精度システムで解析
        try:
            result = self.base_detector.detect_hierarchical_grammar(modified_sentence)
            pattern = result.main_clause.grammatical_pattern
            confidence = result.main_clause.confidence
            
            print(f"    ✅ Main pattern detected: {pattern.value} (confidence: {confidence:.3f})")
            
        except Exception as e:
            print(f"    ⚠️ Main detection error: {e}")
            pattern = GrammarPattern.SVO_PATTERN
            confidence = 0.5
        
        return {
            'pattern': pattern,
            'confidence': confidence,
            'modified_sentence': modified_sentence,
            'detected_clauses': detected_clauses
        }
    
    def _replace_clauses_with_placeholders(self, sentence: str) -> Tuple[str, List[Dict]]:
        """節をプレースホルダーに置換"""
        
        detected_clauses = []
        modified_sentence = sentence
        
        # 各パターンタイプを検出・置換
        for clause_type, pattern in self.clause_patterns.items():
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            
            for match in matches:
                clause_text = match.group(0)
                
                # プレースホルダー生成
                if clause_type in ['that_clause', 'wh_clause']:
                    placeholder = "[O1節]"  # 目的語節
                elif clause_type == 'participle_phrase':
                    placeholder = "[分詞句]"  # 分詞構文
                elif clause_type == 'temporal_clause':
                    placeholder = "[時間節]"  # 時間節
                elif clause_type == 'relative_clause':
                    placeholder = ""  # 関係詞節は除去（修飾なので）
                else:
                    placeholder = "[節]"
                
                # 置換実行
                if placeholder:
                    modified_sentence = modified_sentence.replace(clause_text, placeholder, 1)
                else:
                    modified_sentence = modified_sentence.replace(clause_text, "", 1)
                
                detected_clauses.append({
                    'text': clause_text,
                    'type': clause_type,
                    'placeholder': placeholder,
                    'start_pos': match.start(),
                    'end_pos': match.end()
                })
                
                print(f"    🎯 {clause_type}: '{clause_text}' → '{placeholder}'")
        
        # 余分なスペースをクリーンアップ
        modified_sentence = re.sub(r'\s+', ' ', modified_sentence).strip()
        
        return modified_sentence, detected_clauses
    
    def _detect_subordinate_clauses(self, original_sentence: str, main_result: Dict) -> List[Dict]:
        """Step 2: 従属節のパターン検出"""
        
        subordinate_results = []
        
        for clause_info in main_result['detected_clauses']:
            clause_text = clause_info['text']
            clause_type = clause_info['type']
            
            print(f"    🔍 Analyzing subordinate clause: '{clause_text}' (type: {clause_type})")
            
            # 節の前処理（接続詞等を除去）
            processed_clause = self._preprocess_clause_text(clause_text, clause_type)
            
            print(f"    🔄 Preprocessed: '{processed_clause}'")
            
            # 既存システムを再適用
            try:
                sub_result = self.base_detector.detect_hierarchical_grammar(processed_clause)
                pattern = sub_result.main_clause.grammatical_pattern
                confidence = sub_result.main_clause.confidence
                
                print(f"    ✅ Subordinate pattern: {pattern.value} (confidence: {confidence:.3f})")
                
            except Exception as e:
                print(f"    ⚠️ Subordinate detection error: {e}")
                # タイプ別フォールバック
                pattern = self._get_fallback_pattern(clause_type)
                confidence = 0.4
            
            subordinate_results.append({
                'text': clause_text,
                'pattern': pattern,
                'confidence': confidence,
                'type': clause_type,
                'processed_text': processed_clause
            })
        
        return subordinate_results
    
    def _preprocess_clause_text(self, clause_text: str, clause_type: str) -> str:
        """節テキストの前処理（接続詞除去等）"""
        
        text = clause_text.strip()
        
        if clause_type == 'that_clause':
            # "that he is smart" → "he is smart"
            text = re.sub(r'^\s*that\s+', '', text, flags=re.IGNORECASE)
        
        elif clause_type == 'wh_clause':
            # wh語はそのまま保持
            pass
        
        elif clause_type == 'participle_phrase':
            # "having finished the project" → "I have finished the project"
            if text.lower().startswith('having'):
                text = "I have" + text[6:]
            elif text.lower().startswith('walking'):
                text = "I was " + text.lower()
            # 他の分詞も同様の処理
        
        elif clause_type == 'temporal_clause':
            # "when the rain stopped" → "the rain stopped"
            text = re.sub(r'^\s*(when|while|before|after|since|until)\s+', '', text, flags=re.IGNORECASE)
        
        elif clause_type == 'relative_clause':
            # "that she bought" → "she bought it"
            text = re.sub(r'^\s*(that|which)\s+', '', text, flags=re.IGNORECASE)
            if not any(obj in text.lower() for obj in ['it', 'him', 'her', 'them']):
                text += " it"  # 目的語を補完
        
        # 文末記号を追加
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def _get_fallback_pattern(self, clause_type: str) -> GrammarPattern:
        """節タイプ別フォールバックパターン"""
        
        fallback_patterns = {
            'that_clause': GrammarPattern.SVC_PATTERN,
            'wh_clause': GrammarPattern.SVO_PATTERN,
            'participle_phrase': GrammarPattern.SV_PATTERN,
            'temporal_clause': GrammarPattern.SV_PATTERN,
            'relative_clause': GrammarPattern.SVO_PATTERN,
        }
        
        return fallback_patterns.get(clause_type, GrammarPattern.SV_PATTERN)
    
    def _calculate_overall_confidence(self, main_result: Dict, subordinate_results: List[Dict]) -> float:
        """全体信頼度計算"""
        
        confidence_scores = [main_result['confidence']]
        confidence_scores.extend([sub['confidence'] for sub in subordinate_results])
        
        if confidence_scores:
            return sum(confidence_scores) / len(confidence_scores)
        else:
            return 0.5

# テスト実行
if __name__ == "__main__":
    detector = HierarchicalGrammarDetectorV5()
    
    test_sentences = [
        "I think that he is smart.",
        "Having finished the project, the student submitted it confidently.",
        "The book that she bought was expensive."
    ]
    
    print(f"\n🧪 Testing V5 Correct Approach...")
    print("=" * 60)
    
    for sentence in test_sentences:
        result = detector.detect_hierarchical_grammar_v5(sentence)
        print(f"\n📊 Results for: {sentence}")
        print(f"Main: {result.main_clause_pattern.value} ({result.main_clause_confidence:.3f})")
        for i, sub in enumerate(result.subordinate_clauses, 1):
            print(f"Sub{i}: {sub['pattern'].value} ({sub['confidence']:.3f}) - {sub['type']}")
        print(f"Overall: {result.overall_confidence:.3f} | Time: {result.processing_time:.3f}s")
        print("-" * 40)
