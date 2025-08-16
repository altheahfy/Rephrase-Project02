#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参照基準バリデーションシステム
手動確認作業を自動化するための正解基準確立ツール
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class ReferenceValidationSystem:
    """正解基準確立・検証システム"""
    
    def __init__(self):
        self.mapper = UnifiedStanzaRephraseMapper()
        self.mapper.add_handler('basic_five_pattern')
        self.mapper.add_handler('relative_clause') 
        self.mapper.add_handler('adverbial_modifier')
        
        # 正解基準データベース（あなたの手動確認結果をベースに構築）
        self.reference_database = {}
    
    def establish_reference(self, test_name, sentence, expected_result, notes=""):
        """
        正解基準を確立
        
        Args:
            test_name: テスト名（例: "test12", "test30"）
            sentence: テスト文章
            expected_result: あなたが確認した正解結果
            notes: 補足説明
        """
        self.reference_database[test_name] = {
            "sentence": sentence,
            "expected": expected_result,
            "notes": notes,
            "validated_by": "manual_inspection",
            "timestamp": "2025-08-16"
        }
        
        print(f"✅ 正解基準確立: {test_name}")
        print(f"📝 文章: {sentence}")
        print(f"🎯 期待結果: {expected_result}")
        if notes:
            print(f"💡 備考: {notes}")
        print("="*50)
    
    def validate_current_implementation(self, test_name):
        """
        現在の実装を正解基準と照合
        
        Args:
            test_name: テスト名
            
        Returns:
            dict: 検証結果
        """
        if test_name not in self.reference_database:
            return {"error": f"テスト '{test_name}' の正解基準が未確立"}
        
        reference = self.reference_database[test_name]
        sentence = reference["sentence"]
        expected = reference["expected"]
        
        print(f"🧪 実装検証: {test_name}")
        print(f"📝 文章: {sentence}")
        
        try:
            # 現在の実装で実行
            result = self.mapper.process(sentence)
            actual_main = result.get('slots', {})
            actual_sub = result.get('sub_slots', {})
            
            # 検証実行
            validation_results = []
            all_correct = True
            
            # 期待されるメインスロットをチェック
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            for slot, expected_value in expected_main.items():
                actual_value = actual_main.get(slot, "MISSING")
                is_correct = actual_value == expected_value
                if not is_correct:
                    all_correct = False
                
                validation_results.append({
                    'type': 'main_slot',
                    'slot': slot,
                    'expected': expected_value,
                    'actual': actual_value,
                    'correct': is_correct
                })
            
            # 期待されるサブスロットをチェック
            for slot, expected_value in expected_sub.items():
                actual_value = actual_sub.get(slot, "MISSING")
                is_correct = actual_value == expected_value
                if not is_correct:
                    all_correct = False
                
                validation_results.append({
                    'type': 'sub_slot',
                    'slot': slot,
                    'expected': expected_value,
                    'actual': actual_value,
                    'correct': is_correct
                })
            
            # 結果レポート
            print(f"🔍 実際の結果:")
            print(f"   Main slots: {actual_main}")
            print(f"   Sub slots: {actual_sub}")
            print("="*30)
            
            passed_tests = sum(1 for r in validation_results if r['correct'])
            total_tests = len(validation_results)
            
            for result in validation_results:
                status = "✅ PASS" if result['correct'] else "❌ FAIL"
                print(f"   {status} {result['type']} '{result['slot']}': '{result['actual']}' (期待: '{result['expected']}')")
            
            print("="*30)
            print(f"📊 結果: {passed_tests}/{total_tests} 項目が正解基準と一致")
            
            return {
                "test_name": test_name,
                "all_correct": all_correct,
                "passed": passed_tests,
                "total": total_tests,
                "details": validation_results,
                "actual_result": {"main_slots": actual_main, "sub_slots": actual_sub}
            }
            
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def save_reference_database(self, filepath="reference_standards.json"):
        """正解基準データベースを保存"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.reference_database, f, ensure_ascii=False, indent=2)
        print(f"💾 正解基準データベース保存: {filepath}")
    
    def load_reference_database(self, filepath="reference_standards.json"):
        """正解基準データベースを読み込み"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.reference_database = json.load(f)
            print(f"📂 正解基準データベース読み込み: {filepath}")
            print(f"📊 登録済みテスト数: {len(self.reference_database)}")
        except FileNotFoundError:
            print(f"⚠️ データベースファイルが見つかりません: {filepath}")


def demo_reference_establishment():
    """正解基準確立のデモ"""
    
    validator = ReferenceValidationSystem()
    
    print("🎯 正解基準確立システム デモ")
    print("="*50)
    
    # Test30の正解基準を確立（あなたの手動確認結果をベースに）
    validator.establish_reference(
        test_name="test30",
        sentence="The house where I was born is in Tokyo.",
        expected_result={
            "main_slots": {
                "S": "",  # 関係節により空
                "V": "is",
                "C2": "in Tokyo"
            },
            "sub_slots": {
                "sub-m3": "The house where",
                "sub-s": "I",
                "sub-aux": "was", 
                "sub-v": "born"
            }
        },
        notes="階層的解析アプローチ（Stanza→spaCy→Rephrase独自ルール）テスト"
    )
    
    # 現在の実装を検証
    result = validator.validate_current_implementation("test30")
    
    if result.get("all_correct"):
        print("🎉 実装が正解基準と完全一致！")
    else:
        print("⚠️ 修正が必要な項目があります")
    
    # 正解基準データベースを保存
    validator.save_reference_database()
    
    return validator

if __name__ == "__main__":
    demo_reference_establishment()
