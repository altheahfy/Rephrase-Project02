#!/usr/bin/env python3
"""
スロット番号正規化システム v1.0
マルチエンジン協調におけるスロット番号の統一・正規化メカニズム

問題:
- エンジンごとに異なるスロット番号体系（C1, C2, C, C_COMP, etc.）
- スロット間の干渉による番号不一致
- 最終結果の一貫性欠如

解決方法:
1. 統一スロット番号体系への正規化
2. エンジン固有番号から標準番号への変換
3. スロット競合時の優先順位制御
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
import re

class StandardSlotType(Enum):
    """標準スロットタイプ定義"""
    S = "S"      # Subject (主語)
    V = "V"      # Verb (動詞)
    O1 = "O1"    # Object1 (第一目的語)
    O2 = "O2"    # Object2 (第二目的語)
    C1 = "C1"    # Complement1 (主格補語)
    C2 = "C2"    # Complement2 (目的格補語)
    M1 = "M1"    # Modifier1 (場所・時間修飾)
    M2 = "M2"    # Modifier2 (方法・程度修飾)
    M3 = "M3"    # Modifier3 (その他修飾)
    AUX = "Aux"  # Auxiliary (助動詞)

@dataclass
class SlotMapping:
    """スロットマッピング情報"""
    engine_slot: str
    standard_slot: StandardSlotType
    priority: int
    context_hint: Optional[str] = None

class SlotNormalizationSystem:
    """スロット番号正規化システム"""
    
    def __init__(self):
        """スロット正規化システム初期化"""
        print("🔧 スロット番号正規化システム v1.0 起動中...")
        
        # エンジン別スロットマッピング定義
        self.engine_slot_mappings = {
            # === 基本5文型エンジン ===
            "Basic5Pattern": {
                "S": SlotMapping("S", StandardSlotType.S, 1),
                "V": SlotMapping("V", StandardSlotType.V, 1),
                "O": SlotMapping("O", StandardSlotType.O1, 1),
                "O1": SlotMapping("O1", StandardSlotType.O1, 1),
                "O2": SlotMapping("O2", StandardSlotType.O2, 1),
                "C": SlotMapping("C", StandardSlotType.C1, 1),
                "C1": SlotMapping("C1", StandardSlotType.C1, 1),
                "C2": SlotMapping("C2", StandardSlotType.C2, 1),
                "M": SlotMapping("M", StandardSlotType.M1, 1),
            },
            
            # === 受動態エンジン ===
            "PassiveVoice": {
                "S": SlotMapping("S", StandardSlotType.S, 2),
                "V_PASS": SlotMapping("V_PASS", StandardSlotType.V, 2),
                "BY_AGENT": SlotMapping("BY_AGENT", StandardSlotType.M1, 2),
                "AUX_BE": SlotMapping("AUX_BE", StandardSlotType.AUX, 2),
            },
            
            # === 比較構文エンジン ===
            "Comparative": {
                "COMP_ADJ": SlotMapping("COMP_ADJ", StandardSlotType.C1, 2),
                "COMP_THAN": SlotMapping("COMP_THAN", StandardSlotType.M2, 2),
                "SUP_ADJ": SlotMapping("SUP_ADJ", StandardSlotType.C1, 3),
            },
            
            # === 関係代名詞エンジン ===
            "RelativePronoun": {
                "REL_S": SlotMapping("REL_S", StandardSlotType.S, 3),
                "REL_V": SlotMapping("REL_V", StandardSlotType.V, 3),
                "REL_O": SlotMapping("REL_O", StandardSlotType.O1, 3),
                "ANTECEDENT": SlotMapping("ANTECEDENT", StandardSlotType.S, 2),
            },
            
            # === 疑問文エンジン ===
            "Interrogative": {
                "WH_WORD": SlotMapping("WH_WORD", StandardSlotType.S, 2),
                "AUX_DO": SlotMapping("AUX_DO", StandardSlotType.AUX, 2),
                "MAIN_V": SlotMapping("MAIN_V", StandardSlotType.V, 2),
            },
            
            # === 時制・完了エンジン ===
            "TenseAspect": {
                "AUX_HAVE": SlotMapping("AUX_HAVE", StandardSlotType.AUX, 2),
                "PAST_PART": SlotMapping("PAST_PART", StandardSlotType.V, 2),
                "AUX_BE": SlotMapping("AUX_BE", StandardSlotType.AUX, 3),
                "PRESENT_PART": SlotMapping("PRESENT_PART", StandardSlotType.V, 3),
            },
            
            # === その他エンジン（例） ===
            "ConditionalMood": {
                "IF_CLAUSE": SlotMapping("IF_CLAUSE", StandardSlotType.M3, 2),
                "MAIN_CLAUSE": SlotMapping("MAIN_CLAUSE", StandardSlotType.S, 1),
            }
        }
        
        # 正規化ルール
        self.normalization_rules = {
            'priority_based': True,     # 優先度ベース正規化
            'context_aware': True,      # コンテキスト考慮
            'conflict_resolution': True, # 競合解決
            'backward_compatibility': True # 後方互換性
        }
        
        # スロット競合解決規則
        self.conflict_resolution_rules = {
            # 同一標準スロットへの複数マッピング時の解決順序
            StandardSlotType.S: ['Basic5Pattern', 'RelativePronoun', 'PassiveVoice'],
            StandardSlotType.V: ['Basic5Pattern', 'TenseAspect', 'PassiveVoice'],
            StandardSlotType.C1: ['Basic5Pattern', 'Comparative', 'RelativePronoun'],
            StandardSlotType.M1: ['Basic5Pattern', 'PassiveVoice', 'ConditionalMood'],
        }
        
        print("✅ スロット正規化システム準備完了")
    
    def normalize_slot_assignments(self, engine_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        エンジン結果からスロット割り当て正規化
        
        Args:
            engine_results: エンジン別結果辞書 {engine_name: {slot: value, ...}}
            
        Returns:
            正規化されたスロット結果辞書 {standard_slot: value}
        """
        print(f"🔧 スロット正規化開始: {len(engine_results)} エンジン結果")
        
        # 1. 標準スロットへのマッピング収集
        standard_slot_candidates = self._collect_slot_candidates(engine_results)
        
        # 2. 競合解決
        resolved_slots = self._resolve_slot_conflicts(standard_slot_candidates)
        
        # 3. 最終正規化
        normalized_result = self._apply_final_normalization(resolved_slots)
        
        print(f"✅ スロット正規化完了: {len(normalized_result)} スロット")
        return normalized_result
    
    def _collect_slot_candidates(self, engine_results: Dict[str, Dict[str, Any]]) -> Dict[StandardSlotType, List[Dict]]:
        """標準スロット候補収集"""
        candidates = {slot_type: [] for slot_type in StandardSlotType}
        
        for engine_name, slots in engine_results.items():
            if engine_name not in self.engine_slot_mappings:
                print(f"⚠️ 未知エンジン: {engine_name} - デフォルトマッピング適用")
                continue
            
            engine_mappings = self.engine_slot_mappings[engine_name]
            
            for engine_slot, value in slots.items():
                if engine_slot in engine_mappings:
                    mapping = engine_mappings[engine_slot]
                    candidate = {
                        'value': value,
                        'engine': engine_name,
                        'original_slot': engine_slot,
                        'priority': mapping.priority,
                        'context_hint': mapping.context_hint
                    }
                    candidates[mapping.standard_slot].append(candidate)
                else:
                    print(f"⚠️ 未対応スロット: {engine_name}.{engine_slot}")
        
        return candidates
    
    def _resolve_slot_conflicts(self, candidates: Dict[StandardSlotType, List[Dict]]) -> Dict[StandardSlotType, Dict]:
        """スロット競合解決"""
        resolved = {}
        
        for slot_type, candidate_list in candidates.items():
            if not candidate_list:
                continue
            
            if len(candidate_list) == 1:
                # 単一候補：そのまま採用
                resolved[slot_type] = candidate_list[0]
            else:
                # 複数候補：競合解決
                resolved[slot_type] = self._resolve_single_slot_conflict(slot_type, candidate_list)
        
        return resolved
    
    def _resolve_single_slot_conflict(self, slot_type: StandardSlotType, candidates: List[Dict]) -> Dict:
        """単一スロット競合解決"""
        print(f"⚔️ 競合解決: {slot_type.value} ({len(candidates)} 候補)")
        
        # 1. 優先度ソート
        sorted_candidates = sorted(candidates, key=lambda x: x['priority'])
        
        # 2. エンジン優先順位適用
        if slot_type in self.conflict_resolution_rules:
            engine_priority = self.conflict_resolution_rules[slot_type]
            
            for preferred_engine in engine_priority:
                for candidate in sorted_candidates:
                    if candidate['engine'] == preferred_engine:
                        print(f"🎯 エンジン優先選択: {preferred_engine}")
                        return candidate
        
        # 3. デフォルト：最高優先度候補
        selected = sorted_candidates[0]
        print(f"🎯 優先度選択: {selected['engine']} (priority: {selected['priority']})")
        return selected
    
    def _apply_final_normalization(self, resolved_slots: Dict[StandardSlotType, Dict]) -> Dict[str, Any]:
        """最終正規化適用"""
        normalized = {}
        
        for slot_type, slot_data in resolved_slots.items():
            standard_key = slot_type.value
            value = slot_data['value']
            
            # 値の正規化
            normalized_value = self._normalize_slot_value(value, slot_type, slot_data)
            
            normalized[standard_key] = normalized_value
        
        return normalized
    
    def _normalize_slot_value(self, value: Any, slot_type: StandardSlotType, metadata: Dict) -> Any:
        """スロット値正規化"""
        if isinstance(value, str):
            # 文字列値の正規化
            normalized = value.strip()
            
            # スロットタイプ別の特別処理
            if slot_type in [StandardSlotType.S, StandardSlotType.O1, StandardSlotType.O2]:
                # 名詞句：冠詞・修飾語の正規化
                normalized = self._normalize_noun_phrase(normalized)
            elif slot_type == StandardSlotType.V:
                # 動詞：時制・活用の正規化
                normalized = self._normalize_verb_phrase(normalized)
            elif slot_type in [StandardSlotType.C1, StandardSlotType.C2]:
                # 補語：形容詞・名詞の正規化
                normalized = self._normalize_complement(normalized)
            
            return normalized
        
        return value
    
    def _normalize_noun_phrase(self, phrase: str) -> str:
        """名詞句正規化"""
        # 冠詞の重複除去
        phrase = re.sub(r'\b(the|a|an)\s+(the|a|an)\s+', r'\1 ', phrase, flags=re.IGNORECASE)
        
        # 余分な空白除去
        phrase = re.sub(r'\s+', ' ', phrase).strip()
        
        return phrase
    
    def _normalize_verb_phrase(self, phrase: str) -> str:
        """動詞句正規化"""
        # 助動詞の重複除去
        auxiliaries = ['is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'can', 'could']
        for aux in auxiliaries:
            pattern = rf'\b{aux}\s+{aux}\b'
            phrase = re.sub(pattern, aux, phrase, flags=re.IGNORECASE)
        
        return phrase.strip()
    
    def _normalize_complement(self, phrase: str) -> str:
        """補語正規化"""
        # 重複形容詞除去
        phrase = re.sub(r'\b(\w+)\s+\1\b', r'\1', phrase)
        
        return phrase.strip()
    
    def get_slot_mapping_info(self, engine_name: str) -> Dict[str, SlotMapping]:
        """エンジンのスロットマッピング情報取得"""
        return self.engine_slot_mappings.get(engine_name, {})
    
    def add_engine_mapping(self, engine_name: str, mappings: Dict[str, SlotMapping]):
        """新規エンジンマッピング追加"""
        self.engine_slot_mappings[engine_name] = mappings
        print(f"✅ エンジンマッピング追加: {engine_name}")
    
    def validate_slot_consistency(self, normalized_result: Dict[str, Any]) -> List[str]:
        """スロット一貫性検証"""
        issues = []
        
        # 基本構造チェック
        if 'S' not in normalized_result:
            issues.append("主語(S)が欠如")
        if 'V' not in normalized_result:
            issues.append("動詞(V)が欠如")
        
        # 文型チェック
        has_o1 = 'O1' in normalized_result
        has_o2 = 'O2' in normalized_result
        has_c1 = 'C1' in normalized_result
        has_c2 = 'C2' in normalized_result
        
        if has_o2 and not has_o1:
            issues.append("O2があるがO1が欠如（SVOO構文エラー）")
        if has_c2 and not has_o1:
            issues.append("C2があるがO1が欠如（SVOC構文エラー）")
        
        return issues

# === テスト・検証用関数 ===

def test_slot_normalization():
    """スロット正規化システムテスト"""
    system = SlotNormalizationSystem()
    
    # テストケース：複数エンジン結果
    test_engine_results = {
        "Basic5Pattern": {
            "S": "the cat",
            "V": "is",
            "C": "happy",
            "M": "today"
        },
        "Comparative": {
            "COMP_ADJ": "happier",
            "COMP_THAN": "than yesterday"
        },
        "TenseAspect": {
            "AUX_BE": "is",
            "PRESENT_PART": "being"
        },
        "PassiveVoice": {
            "S": "the mouse",
            "V_PASS": "was caught", 
            "BY_AGENT": "by the cat"
        }
    }
    
    print("🧪 スロット正規化システムテスト開始")
    print("=" * 60)
    
    # 正規化実行
    normalized = system.normalize_slot_assignments(test_engine_results)
    
    print(f"\n📥 入力エンジン結果:")
    for engine, slots in test_engine_results.items():
        print(f"   {engine}: {slots}")
    
    print(f"\n📤 正規化結果:")
    for slot, value in normalized.items():
        print(f"   {slot}: '{value}'")
    
    # 一貫性検証
    issues = system.validate_slot_consistency(normalized)
    print(f"\n🔍 一貫性検証:")
    if issues:
        for issue in issues:
            print(f"   ⚠️ {issue}")
    else:
        print("   ✅ 一貫性確認済み")
    
    # マッピング情報表示
    print(f"\n📋 マッピング情報例 (Basic5Pattern):")
    mapping_info = system.get_slot_mapping_info("Basic5Pattern")
    for engine_slot, mapping in mapping_info.items():
        print(f"   {engine_slot} → {mapping.standard_slot.value} (priority: {mapping.priority})")
    
    print("\n✅ スロット正規化システムテスト完了")

if __name__ == "__main__":
    test_slot_normalization()
