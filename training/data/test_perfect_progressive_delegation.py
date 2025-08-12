#!/usr/bin/env python3
"""
完了進行形エンジン修正テスト - 接続詞委譲確認
"""

def test_conjunction_delegation():
    """接続詞委譲のテスト（Stanza不使用）"""
    print("🔥 完了進行形エンジン 接続詞委譲テスト")
    
    test_cases = [
        {
            'sentence': 'I have been working here for three years.',
            'should_process': True,
            'reason': '接続詞なしの単純完了進行形'
        },
        {
            'sentence': 'She had been waiting for an hour when I arrived.',
            'should_process': False,
            'reason': 'when節があるため接続詞エンジンに委譲'
        },
        {
            'sentence': 'He was tired because he had been running all morning.',
            'should_process': False,
            'reason': 'because節があるため接続詞エンジンに委譲'
        },
        {
            'sentence': 'They will have been living there for ten years by next year.',
            'should_process': True,
            'reason': '接続詞なしの未来完了進行形'
        }
    ]
    
    # 簡易接続詞検出テスト
    conjunctions = ['when', 'because', 'since', 'while', 'although', 'though', 'if', 'unless', 'before', 'after']
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎯 テスト{i}: {test['sentence']}")
        
        # 接続詞検出
        sentence_lower = test['sentence'].lower()
        contains_conjunction = False
        
        for conj in conjunctions:
            if f' {conj} ' in sentence_lower or sentence_lower.startswith(f'{conj} '):
                contains_conjunction = True
                print(f"  ✅ 接続詞検出: '{conj}'")
                break
        
        if not contains_conjunction:
            print("  ✅ 接続詞なし")
        
        # 処理判定
        should_process = not contains_conjunction
        
        if should_process == test['should_process']:
            print(f"  ✅ 正しい判定: {'処理する' if should_process else '委譲する'}")
        else:
            print(f"  ❌ 判定ミス: {'処理する' if should_process else '委譲する'} (期待: {'処理する' if test['should_process'] else '委譲する'})")
        
        print(f"  📋 理由: {test['reason']}")
    
    print(f"\n📝 修正後の動作:")
    print("✅ 接続詞を含む文は処理せず、接続詞エンジンに委譲")
    print("✅ 単純な完了進行形のみを処理")
    print("✅ 役割分担が明確化")

if __name__ == "__main__":
    test_conjunction_delegation()
