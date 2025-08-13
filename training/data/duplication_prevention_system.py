#!/usr/bin/env python3
"""
境界拡張重複防止システム v1.0
マルチエンジン協調における境界拡張の重複防止メカニズム

問題:
- 'The cat' → 'The The The cat' など境界拡張による重複
- 複数エンジンによる同一テキスト拡張
- スロット間の干渉による品質劣化

解決方法:
1. 適用履歴管理による重複検出
2. 拡張結果の正規化
3. エンジン間調整メカニズム
"""

import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ExpansionRecord:
    """境界拡張記録"""
    original_text: str
    expanded_text: str
    slot_type: str
    engine_name: str
    expansion_type: str
    timestamp: str

class DuplicationPreventionSystem:
    """境界拡張重複防止システム"""
    
    def __init__(self):
        """重複防止システム初期化"""
        print("🛡️ 境界拡張重複防止システム v1.0 起動中...")
        
        # 適用履歴管理
        self.expansion_history: Dict[str, List[ExpansionRecord]] = defaultdict(list)
        self.applied_expansions: Set[str] = set()
        self.normalized_cache: Dict[str, str] = {}
        
        # 重複パターン検出設定
        self.duplication_patterns = [
            r'\b(\w+)\s+\1\s+\1\b',  # 連続3回重複 (the the the)
            r'\b(\w+)\s+\1\b',       # 連続2回重複 (the the)
            r'\b(a|an|the)\s+(a|an|the)\b',  # 冠詞重複
            r'\b(is|are|was|were)\s+(is|are|was|were)\b',  # be動詞重複
        ]
        
        # 正規化設定
        self.normalization_rules = {
            'article_normalization': True,
            'whitespace_normalization': True,
            'case_normalization': False,
            'punctuation_normalization': True
        }
        
        print("✅ 重複防止システム準備完了")
    
    def prevent_expansion_duplication(self, text: str, slot_type: str, 
                                    engine_name: str, expansion_func) -> str:
        """
        境界拡張重複防止メイン処理
        
        Args:
            text: 対象テキスト
            slot_type: スロットタイプ
            engine_name: エンジン名
            expansion_func: 拡張関数
            
        Returns:
            重複防止された拡張テキスト
        """
        print(f"🔍 重複防止処理開始: '{text}' [{slot_type}] by {engine_name}")
        
        # 1. キャッシュ確認
        cache_key = f"{text}|{slot_type}|{engine_name}"
        if cache_key in self.normalized_cache:
            cached_result = self.normalized_cache[cache_key]
            print(f"📋 キャッシュヒット: '{cached_result}'")
            return cached_result
        
        # 2. 既存重複検出
        if self._has_existing_duplication(text):
            print(f"⚠️ 既存重複検出: '{text}'")
            normalized = self._normalize_existing_duplication(text)
            print(f"🔧 正規化結果: '{normalized}'")
            text = normalized
        
        # 3. 境界拡張実行
        try:
            expanded_text = expansion_func(text)
            print(f"🚀 拡張実行: '{text}' → '{expanded_text}'")
        except Exception as e:
            print(f"❌ 拡張処理エラー: {e}")
            return text
        
        # 4. 新規重複検出・修正
        if self._has_new_duplication(expanded_text, text):
            print(f"🚨 新規重複検出: '{expanded_text}'")
            corrected_text = self._correct_new_duplication(expanded_text, text)
            print(f"🔧 重複修正: '{expanded_text}' → '{corrected_text}'")
            expanded_text = corrected_text
        
        # 5. 履歴記録
        self._record_expansion(text, expanded_text, slot_type, engine_name)
        
        # 6. キャッシュ保存
        self.normalized_cache[cache_key] = expanded_text
        
        print(f"✅ 重複防止完了: '{expanded_text}'")
        return expanded_text
    
    def _has_existing_duplication(self, text: str) -> bool:
        """既存重複判定"""
        for pattern in self.duplication_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _normalize_existing_duplication(self, text: str) -> str:
        """既存重複正規化"""
        normalized = text
        
        # 連続重複除去
        for pattern in self.duplication_patterns:
            if pattern == r'\b(\w+)\s+\1\s+\1\b':
                # 3回重複 → 1回
                normalized = re.sub(pattern, r'\1', normalized, flags=re.IGNORECASE)
            elif pattern == r'\b(\w+)\s+\1\b':
                # 2回重複 → 1回
                normalized = re.sub(pattern, r'\1', normalized, flags=re.IGNORECASE)
        
        # 特殊ケース処理
        normalized = self._handle_special_duplications(normalized)
        
        return normalized.strip()
    
    def _has_new_duplication(self, expanded: str, original: str) -> bool:
        """新規重複判定"""
        # 拡張前後で新たな重複が発生したか
        original_duplications = sum(1 for p in self.duplication_patterns 
                                  if re.search(p, original, re.IGNORECASE))
        expanded_duplications = sum(1 for p in self.duplication_patterns 
                                  if re.search(p, expanded, re.IGNORECASE))
        
        return expanded_duplications > original_duplications
    
    def _correct_new_duplication(self, expanded: str, original: str) -> str:
        """新規重複修正"""
        corrected = expanded
        
        # パターン別修正
        for pattern in self.duplication_patterns:
            corrected = re.sub(pattern, r'\1', corrected, flags=re.IGNORECASE)
        
        # 過剰修正防止: 元テキストの意味を保持
        if self._is_over_corrected(corrected, original):
            print("⚠️ 過剰修正検出 - 調整中...")
            corrected = self._adjust_over_correction(corrected, original, expanded)
        
        return corrected.strip()
    
    def _handle_special_duplications(self, text: str) -> str:
        """特殊重複パターン処理"""
        special_cases = [
            # 冠詞特殊パターン
            (r'\bthe\s+the\s+(\w+)', r'the \1'),
            (r'\ba\s+a\s+(\w+)', r'a \1'),
            (r'\ban\s+an\s+(\w+)', r'an \1'),
            
            # 動詞特殊パターン  
            (r'\bis\s+is\b', 'is'),
            (r'\bare\s+are\b', 'are'),
            (r'\bwas\s+was\b', 'was'),
            (r'\bwere\s+were\b', 'were'),
            
            # 修飾語重複
            (r'\bvery\s+very\b', 'very'),
            (r'\bquite\s+quite\b', 'quite'),
        ]
        
        normalized = text
        for pattern, replacement in special_cases:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        return normalized
    
    def _is_over_corrected(self, corrected: str, original: str) -> bool:
        """過剰修正判定"""
        # 長さが大幅に短縮された場合
        length_ratio = len(corrected) / max(len(original), 1)
        if length_ratio < 0.5:
            return True
        
        # 重要語彙が消失した場合
        original_words = set(original.lower().split())
        corrected_words = set(corrected.lower().split())
        lost_words = original_words - corrected_words
        
        important_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were'}
        lost_important = lost_words & important_words
        
        return len(lost_important) > len(original_words) * 0.3
    
    def _adjust_over_correction(self, corrected: str, original: str, expanded: str) -> str:
        """過剰修正調整"""
        # より保守的な修正を適用
        words = expanded.split()
        adjusted_words = []
        previous_word = None
        
        for word in words:
            if previous_word and word.lower() == previous_word.lower():
                # 連続する同一語の2つ目以降をスキップ
                continue
            adjusted_words.append(word)
            previous_word = word
        
        return ' '.join(adjusted_words)
    
    def _record_expansion(self, original: str, expanded: str, slot_type: str, engine_name: str):
        """拡張履歴記録"""
        from datetime import datetime
        
        record = ExpansionRecord(
            original_text=original,
            expanded_text=expanded,
            slot_type=slot_type,
            engine_name=engine_name,
            expansion_type="boundary_expansion",
            timestamp=datetime.now().isoformat()
        )
        
        self.expansion_history[original].append(record)
        self.applied_expansions.add(f"{original}|{slot_type}|{engine_name}")
    
    def get_expansion_statistics(self) -> Dict:
        """拡張統計情報取得"""
        total_expansions = sum(len(records) for records in self.expansion_history.values())
        unique_texts = len(self.expansion_history)
        cache_hits = len(self.normalized_cache)
        
        engine_stats = defaultdict(int)
        slot_stats = defaultdict(int)
        
        for records in self.expansion_history.values():
            for record in records:
                engine_stats[record.engine_name] += 1
                slot_stats[record.slot_type] += 1
        
        return {
            'total_expansions': total_expansions,
            'unique_texts': unique_texts,
            'cache_hits': cache_hits,
            'engine_distribution': dict(engine_stats),
            'slot_distribution': dict(slot_stats)
        }
    
    def clear_cache(self):
        """キャッシュクリア"""
        self.normalized_cache.clear()
        print("🗑️ キャッシュクリア完了")
    
    def reset_history(self):
        """履歴リセット"""
        self.expansion_history.clear()
        self.applied_expansions.clear()
        self.clear_cache()
        print("🔄 履歴リセット完了")

# === テスト・検証用関数 ===

def test_duplication_prevention():
    """重複防止システムテスト"""
    system = DuplicationPreventionSystem()
    
    # テストケース
    test_cases = [
        {
            "input": "The the cat",
            "slot": "S",
            "engine": "Basic5Pattern",
            "description": "既存重複（冠詞）",
            "expected_improvement": True
        },
        {
            "input": "very very quickly",
            "slot": "M2", 
            "engine": "AdverbialModifier",
            "description": "既存重複（副詞）",
            "expected_improvement": True
        },
        {
            "input": "normal text",
            "slot": "O1",
            "engine": "Basic5Pattern",
            "description": "正常テキスト",
            "expected_improvement": False
        },
        {
            "input": "is is running",
            "slot": "V",
            "engine": "VerbCluster",
            "description": "動詞重複",
            "expected_improvement": True
        }
    ]
    
    print("🧪 重複防止システムテスト開始")
    print("=" * 60)
    
    def mock_expansion_func(text):
        # モック拡張関数（重複を意図的に発生）
        if "normal" in text:
            return text + " expanded"
        return text + " " + text.split()[0]  # 最初の語を重複
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['description']}: '{case['input']}'")
        
        # 重複防止処理実行
        result = system.prevent_expansion_duplication(
            case['input'], 
            case['slot'], 
            case['engine'], 
            mock_expansion_func
        )
        
        print(f"   入力: '{case['input']}'")
        print(f"   出力: '{result}'")
        
        # 改善判定
        improved = case['input'] != result and not system._has_existing_duplication(result)
        expected = case['expected_improvement']
        
        status = "✅ 成功" if improved == expected else "❌ 失敗"
        print(f"   結果: {status}")
    
    # 統計情報表示
    print(f"\n📊 拡張統計情報:")
    stats = system.get_expansion_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ 重複防止システムテスト完了")

if __name__ == "__main__":
    test_duplication_prevention()
