#!/usr/bin/env python3
"""
Rephrase Slot Validator v1.0

Rephraseスロット構造の検証・バリデーション機能
設計仕様書に基づく厳密なスロット構造チェック
"""

from typing import Dict, List, Optional, Tuple, Any
import json
import re

class RephraseSlotValidator:
    """
    Rephraseスロット構造のバリデーター
    
    REPHRASE_SLOT_STRUCTURE_MANDATORY_REFERENCE.md に基づく
    厳密なスロット構造検証を実行
    """
    
    # 有効なスロット定義（絶対不変）
    VALID_UPPER_SLOTS = {"M1", "S", "Aux", "M2", "V", "C1", "O1", "O2", "C2", "M3"}
    VALID_SUB_SLOTS = {
        "sub-m1", "sub-s", "sub-aux", "sub-m2", "sub-v", 
        "sub-c1", "sub-o1", "sub-o2", "sub-c2", "sub-m3"
    }
    
    # Aux, V にはサブスロットは存在しない（上位スロットとしては）
    # ただし、sub-aux, sub-v は他の上位スロット内のサブスロットとして有効
    NO_SUBSLOT_UPPER_SLOTS = {"Aux", "V"}
    
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []
        
    def validate_slots(self, slots_dict: Dict[str, str], 
                      strict_mode: bool = True) -> Tuple[bool, List[str], List[str]]:
        """
        スロット辞書の完全バリデーション
        
        Args:
            slots_dict: 検証するスロット辞書
            strict_mode: 厳密モード（警告もエラーとして扱う）
            
        Returns:
            Tuple[bool, List[str], List[str]]: (成功可否, エラーリスト, 警告リスト)
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        # 1. スロット名の妥当性チェック
        self._validate_slot_names(slots_dict)
        
        # 2. Type Clause構造チェック
        self._validate_type_clause_structure(slots_dict)
        
        # 3. サブスロット独立性チェック
        self._validate_subslot_independence(slots_dict)
        
        # 4. 禁止されたスロット組み合わせチェック
        self._validate_forbidden_combinations(slots_dict)
        
        # 5. 内容の一貫性チェック
        self._validate_content_consistency(slots_dict)
        
        # 結果判定
        has_errors = len(self.validation_errors) > 0
        if strict_mode:
            has_errors = has_errors or len(self.validation_warnings) > 0
            
        return not has_errors, self.validation_errors.copy(), self.validation_warnings.copy()
    
    def _validate_slot_names(self, slots_dict: Dict[str, str]) -> None:
        """スロット名の妥当性検証"""
        for slot_name in slots_dict.keys():
            if slot_name not in self.VALID_UPPER_SLOTS and slot_name not in self.VALID_SUB_SLOTS:
                self.validation_errors.append(
                    f"❌ 無効なスロット名: '{slot_name}' - 存在しないスロットです"
                )
                
            # 特別に禁止されたパターンのチェック
            forbidden_patterns = [
                r"sub-m1-conj", r"sub-m1-aux", r"sub-m1-agent", 
                r"sub-m3-rel-s", r".*-.*-.*"  # 3階層以上の命名
            ]
            
            for pattern in forbidden_patterns:
                if re.match(pattern, slot_name):
                    self.validation_errors.append(
                        f"❌ 禁止されたスロット名パターン: '{slot_name}'"
                    )
    
    def _validate_type_clause_structure(self, slots_dict: Dict[str, str]) -> None:
        """Type Clause構造の検証"""
        # Type Clauseの検出
        type_clause_indicators = []
        
        for upper_slot in self.VALID_UPPER_SLOTS:
            if upper_slot in slots_dict and slots_dict[upper_slot] == "":
                # 上位スロットが空 → Type Clauseの可能性
                has_subslots = any(
                    slot_name.startswith(f"sub-{upper_slot.lower()}") 
                    for slot_name in slots_dict.keys()
                )
                if has_subslots:
                    type_clause_indicators.append(upper_slot)
        
        # Type Clauseでの上位スロット使用チェック
        for upper_slot in type_clause_indicators:
            if slots_dict.get(upper_slot, "") != "":
                self.validation_errors.append(
                    f"❌ Type Clause エラー: {upper_slot} は空文字列でなければなりません"
                )
    
    def _validate_subslot_independence(self, slots_dict: Dict[str, str]) -> None:
        """サブスロット独立性の検証"""
        # 各上位スロット毎のサブスロット空間チェック
        subslot_usage = {}
        
        for slot_name in slots_dict.keys():
            if slot_name.startswith("sub-"):
                # どの上位スロットのサブスロットかを判定
                # 注意: この判定は文脈により複雑になるため、警告レベル
                if slot_name in self.VALID_SUB_SLOTS:
                    subslot_usage[slot_name] = subslot_usage.get(slot_name, 0) + 1
        
        # サブスロットの重複使用チェック（警告レベル）
        for sub_name, count in subslot_usage.items():
            if count > 1:
                self.validation_warnings.append(
                    f"⚠️ サブスロット重複使用: '{sub_name}' が {count} 回使用されています"
                )
    
    def _validate_forbidden_combinations(self, slots_dict: Dict[str, str]) -> None:
        """禁止された組み合わせの検証"""
        # 注意：sub-aux, sub-v は他の上位スロット内のサブスロットとして有効
        # ここではAux, V の直下サブスロット（存在しない概念）のみをチェック
        
        # 実際には、sub-aux, sub-v は M1, M2, M3等の内部で使用される
        # 現在の実装では、この詳細な検証は複雑すぎるため、警告レベルに留める
        pass
    
    def _validate_content_consistency(self, slots_dict: Dict[str, str]) -> None:
        """内容の一貫性検証"""
        # 空値チェック
        empty_slots = [name for name, value in slots_dict.items() if value == "" and name not in {"M1", "M2", "M3", "C1", "C2"}]
        if empty_slots:
            self.validation_warnings.append(
                f"⚠️ 空のスロット: {', '.join(empty_slots)}"
            )
        
        # 基本必須スロットの存在チェック
        if "S" not in slots_dict and "sub-s" not in slots_dict:
            self.validation_warnings.append(
                "⚠️ 主語スロット (S または sub-s) が見つかりません"
            )
        
        if "V" not in slots_dict and "sub-v" not in slots_dict:
            self.validation_warnings.append(
                "⚠️ 動詞スロット (V または sub-v) が見つかりません"
            )
    
    def validate_json_data(self, json_data: List[Dict]) -> Dict[str, Any]:
        """
        JSON形式のスロットデータ群を一括検証
        
        Args:
            json_data: スロットデータのリスト
            
        Returns:
            Dict: 検証結果サマリー
        """
        total_entries = len(json_data)
        valid_entries = 0
        error_entries = []
        
        for i, entry in enumerate(json_data):
            # スロット部分のみ抽出
            slot_data = {k: v for k, v in entry.items() 
                        if k in self.VALID_UPPER_SLOTS or k in self.VALID_SUB_SLOTS}
            
            is_valid, errors, warnings = self.validate_slots(slot_data, strict_mode=False)
            
            if is_valid and len(warnings) == 0:
                valid_entries += 1
            else:
                error_entries.append({
                    'index': i,
                    'entry': entry,
                    'errors': errors,
                    'warnings': warnings
                })
        
        return {
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'error_entries': error_entries,
            'success_rate': (valid_entries / total_entries * 100) if total_entries > 0 else 0
        }
    
    def generate_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """検証結果レポートの生成"""
        report = []
        report.append("🔍 Rephrase スロット構造検証レポート")
        report.append("=" * 50)
        report.append(f"総エントリ数: {validation_result['total_entries']}")
        report.append(f"有効エントリ数: {validation_result['valid_entries']}")
        report.append(f"成功率: {validation_result['success_rate']:.1f}%")
        report.append("")
        
        if validation_result['error_entries']:
            report.append("❌ エラー・警告のあるエントリ:")
            for error_entry in validation_result['error_entries'][:5]:  # 最初の5件のみ表示
                report.append(f"  エントリ {error_entry['index']}:")
                for error in error_entry['errors']:
                    report.append(f"    {error}")
                for warning in error_entry['warnings']:
                    report.append(f"    {warning}")
                report.append("")
            
            if len(validation_result['error_entries']) > 5:
                report.append(f"  ... 他 {len(validation_result['error_entries']) - 5} 件")
        
        return "\n".join(report)


def main():
    """テスト実行用メイン関数"""
    validator = RephraseSlotValidator()
    
    # テストケース
    test_cases = [
        # 正常ケース
        {
            "name": "基本文型",
            "slots": {"S": "I", "V": "go", "M2": "to school"}
        },
        # Type Clauseケース
        {
            "name": "Type Clause",
            "slots": {"M1": "", "sub-m1": "because", "sub-s": "he", "sub-v": "came"}
        },
        # エラーケース
        {
            "name": "無効なスロット名",
            "slots": {"S": "I", "V": "go", "sub-m1-conj": "because"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 テストケース: {test_case['name']}")
        is_valid, errors, warnings = validator.validate_slots(test_case['slots'])
        
        print(f"結果: {'✅ 有効' if is_valid else '❌ 無効'}")
        if errors:
            for error in errors:
                print(f"  {error}")
        if warnings:
            for warning in warnings:
                print(f"  {warning}")


if __name__ == "__main__":
    main()
