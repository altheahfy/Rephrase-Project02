#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完了進行形エンジン 簡易テスト
時間節の上位・サブスロット配置を確認
"""

def simple_test():
    """簡単な文字列操作テスト（Stanza不使用）"""
    print("🔥 完了進行形 時間節配置テスト")
    
    test_cases = [
        {
            'sentence': 'She had been waiting for an hour when I arrived.',
            'expected_upper_m2': '',  # 空であるべき
            'expected_sub_elements': ['I', 'arrived']  # サブスロットに分解されるべき
        },
        {
            'sentence': 'He was tired because he had been running all morning.',
            'expected_note': 'because節は従属節なので完了進行形エンジンでは処理しない'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test['sentence']}")
        
        # 時間節の検出シミュレーション
        sentence = test['sentence']
        
        if 'when I arrived' in sentence:
            print("  ✅ when節検出")
            print("  📋 統合アーキテクチャの原則:")
            print("    - 上位スロットM2: '' (位置情報のみ)")
            print("    - サブスロット: sub-s='I', sub-v='arrived'")
            print("  ❌ 現在の誤った実装: M2='when I arrived'")
            
        elif 'because' in sentence:
            print("  ✅ because節検出")
            print("  📋 統合アーキテクチャの原則:")
            print("    - because節は接続詞エンジンの担当")
            print("    - 完了進行形エンジンは 'he had been running all morning' のみ処理")
            print("  ❌ 現在の問題: 複文全体を処理しようとしている")
    
    print("\n📝 修正が必要な箇所:")
    print("1. 時間節は上位スロットを空にしてサブスロットに分解")
    print("2. because節は完了進行形エンジンの範囲外")
    print("3. 複文の場合は担当部分のみを処理")

if __name__ == "__main__":
    simple_test()
