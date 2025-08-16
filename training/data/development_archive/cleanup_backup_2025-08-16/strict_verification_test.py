#!/usr/bin/env python3
"""
厳密検証機能付きテスト - ユーザー確認必須版
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import json

# 期待結果の定義（ユーザーと一緒に作成）
EXPECTED_RESULTS = {
    "The car which was crashed is red.": {
        "description": "関係代名詞+受動態の複合構造",
        "expected_slots": {
            # メイン文構造
            "main_structure": "The car [which was crashed] is red",
            "main_subject": "The car which was crashed",
            "main_verb": "is", 
            "main_complement": "red",
            
            # 関係節構造
            "relative_clause": "which was crashed",
            "rel_pronoun": "which",
            "rel_aux": "was",
            "rel_verb": "crashed",
            "rel_type": "subject_relative_passive"
        }
    },
    
    "The book I read yesterday was boring.": {
        "description": "省略目的語関係代名詞",
        "expected_slots": {
            "main_structure": "The book [I read yesterday] was boring",
            "main_subject": "The book I read yesterday", 
            "main_verb": "was",
            "main_complement": "boring",
            
            "relative_clause": "I read yesterday",
            "rel_pronoun": "[omitted]",
            "rel_subject": "I",
            "rel_verb": "read",
            "rel_modifier": "yesterday",
            "rel_type": "object_relative_omitted"
        }
    }
}

def strict_verification_test():
    """厳密検証付きテスト"""
    print("🔬 厳密検証機能付きテスト開始")
    print("="*60)
    print("⚠️  各結果をユーザーが直接確認する必要があります")
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')  # ログ抑制
    mapper.add_handler('relative_clause')
    mapper.add_handler('passive_voice')
    
    verified_count = 0
    total_tests = len(EXPECTED_RESULTS)
    
    for sentence, expected in EXPECTED_RESULTS.items():
        print(f"\n" + "="*60)
        print(f"📋 テスト: {sentence}")
        print(f"📝 説明: {expected['description']}")
        print("-"*60)
        
        # 処理実行
        result = mapper.process(sentence)
        
        print(f"⏱️  処理時間: {result['meta']['processing_time']:.3f}秒")
        
        # 実際の結果表示
        print("\n📊 実際の分解結果:")
        print(f"  メインスロット: {result.get('slots', {})}")
        print(f"  サブスロット: {result.get('sub_slots', {})}")
        
        # 期待結果表示
        print(f"\n📋 期待される構造:")
        expected_slots = expected['expected_slots']
        for key, value in expected_slots.items():
            print(f"  {key}: {value}")
        
        # 詳細比較
        print(f"\n🔍 詳細比較:")
        comparison_results = detailed_comparison(result, expected_slots)
        
        # ユーザー確認
        user_approved = user_confirmation(sentence, result, comparison_results)
        
        if user_approved:
            verified_count += 1
            print("✅ ユーザー承認済み")
        else:
            print("❌ 要修正")
    
    print(f"\n📈 厳密検証結果:")
    print(f"  総テスト数: {total_tests}")
    print(f"  ユーザー承認数: {verified_count}")
    print(f"  承認率: {verified_count/total_tests*100:.1f}%")
    
    if verified_count == total_tests:
        print("🎉 全テスト承認 - システム正常")
    else:
        print("⚠️  修正が必要なテストがあります")

def detailed_comparison(actual_result, expected_slots):
    """詳細比較"""
    comparisons = []
    
    # 実際の結果から重要な要素を抽出
    slots = actual_result.get('slots', {})
    sub_slots = actual_result.get('sub_slots', {})
    grammar_info = actual_result.get('grammar_info', {})
    
    # 主要項目の比較
    if 'main_subject' in expected_slots:
        # メイン主語の推定（sub-sまたは構造から）
        actual_main_subject = sub_slots.get('sub-s', '不明')
        expected_main_subject = expected_slots['main_subject']
        
        match = actual_main_subject == expected_main_subject
        comparisons.append({
            'item': 'メイン主語',
            'expected': expected_main_subject,
            'actual': actual_main_subject,
            'match': match
        })
    
    return comparisons

def user_confirmation(sentence, result, comparisons):
    """ユーザー最終確認"""
    
    print(f"\n👤 ユーザー確認:")
    print(f"❓ この分解結果は正確ですか？")
    
    while True:
        choice = input("\n選択肢: (y)正確 (n)不正確 (d)詳細表示 (q)終了: ").strip().lower()
        
        if choice == 'y':
            return True
        elif choice == 'n':
            reason = input("❓ どの部分が不正確ですか？: ")
            print(f"📝 不正確理由記録: {reason}")
            return False
        elif choice == 'd':
            print("\n📋 詳細情報:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif choice == 'q':
            return False
        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    strict_verification_test()
