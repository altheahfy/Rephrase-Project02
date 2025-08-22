#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人間文法認識のみでのスロット分解テスト

このテストは、人間文法認識システムが独立してスロット分解を
正確に実行できるかを検証するためのものです。
"""

import json
import os
import sys
from pathlib import Path

# プロジェクトルートを設定
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_human_only_slot_decomposition():
    """人間文法認識のみでのスロット分解テスト"""
    
    print("=" * 60)
    print("🧠 人間文法認識のみスロット分解テスト")
    print("=" * 60)
    
    # テストデータをロード
    test_data_path = project_root / "my_test_sentences.json"
    if not test_data_path.exists():
        print(f"❌ テストデータが見つかりません: {test_data_path}")
        return
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # データ構造を変換
    test_data = []
    for key, test_case in raw_data['data'].items():
        test_data.append(test_case)
    
    # マッパーを初期化（人間専用テストモード）
    mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')
    
    print(f"📝 テスト対象文数: {len(test_data)}")
    print()
    
    results = []
    
    for i, test_case in enumerate(test_data, 1):
        sentence = test_case['sentence']
        expected_main = test_case['expected']['main_slots']
        expected_sub = test_case['expected']['sub_slots']
        
        print(f"🔍 テスト {i}: {sentence}")
        
        # 人間文法認識のみで処理
        result = mapper.process(sentence)
        
        actual_main = result['slots']
        actual_sub = result['sub_slots']
        
        print(f"  📋 期待値（主節）: {expected_main}")
        print(f"  📋 実際値（主節）: {actual_main}")
        print(f"  📋 期待値（関係節）: {expected_sub}")
        print(f"  📋 実際値（関係節）: {actual_sub}")
        
        # 主節スロットの比較
        main_match = True
        for slot, expected_value in expected_main.items():
            actual_value = actual_main.get(slot, "")
            if actual_value != expected_value:
                main_match = False
                print(f"    ❌ 主節スロット不一致: {slot} (期待: '{expected_value}', 実際: '{actual_value}')")
        
        # 関係節スロットの比較
        sub_match = True
        for slot, expected_value in expected_sub.items():
            actual_value = actual_sub.get(slot, "")
            if actual_value != expected_value:
                sub_match = False
                print(f"    ❌ 関係節スロット不一致: {slot} (期待: '{expected_value}', 実際: '{actual_value}')")
        
        test_passed = main_match and sub_match
        
        if test_passed:
            print(f"  ✅ テスト {i} 成功")
        else:
            print(f"  ❌ テスト {i} 失敗")
        
        results.append({
            'sentence': sentence,
            'passed': test_passed,
            'expected_main': expected_main,
            'actual_main': actual_main,
            'expected_sub': expected_sub,
            'actual_sub': actual_sub,
            'processing_time': result['meta']['processing_time']
        })
        
        print(f"  ⏱️ 処理時間: {result['meta']['processing_time']:.3f}秒")
        print()
    
    # 統計情報
    passed_count = sum(1 for r in results if r['passed'])
    total_count = len(results)
    accuracy = (passed_count / total_count) * 100 if total_count > 0 else 0
    
    print("=" * 60)
    print("📊 テスト結果統計")
    print("=" * 60)
    print(f"成功: {passed_count}/{total_count} ({accuracy:.1f}%)")
    print(f"失敗: {total_count - passed_count}/{total_count}")
    
    avg_time = sum(r['processing_time'] for r in results) / len(results) if results else 0
    print(f"平均処理時間: {avg_time:.3f}秒")
    
    if accuracy == 100.0:
        print("🎉 全テストに成功！人間文法認識システムは期待通りに動作しています。")
    else:
        print("⚠️ 一部のテストで問題が検出されました。詳細を確認してください。")
    
    return results

if __name__ == "__main__":
    test_human_only_slot_decomposition()
