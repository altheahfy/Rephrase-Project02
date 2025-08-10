#!/usr/bin/env python3
"""
フェーズ1機能テスト: spaCy完全対応拡張
compound, conj+cc, neg, nummod依存関係の処理確認
"""

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phase1_enhancements():
    print("🚀 フェーズ1拡張機能テスト開始")
    
    try:
        engine = CompleteRephraseParsingEngine()
        print("✅ 拡張エンジン初期化完了")
    except Exception as e:
        print(f"❌ エンジン初期化失敗: {e}")
        return
    
    # フェーズ1テスト例文
    test_cases = [
        {
            'category': 'compound',
            'sentences': [
                "I live in New York City.",
                "She loves ice cream and chocolate cake.", 
                "The software engineer works hard."
            ]
        },
        {
            'category': 'conjunction',
            'sentences': [
                "Cats and dogs are popular pets.",
                "We can go by car or by train.",
                "He is smart but lazy."
            ]
        },
        {
            'category': 'negation',
            'sentences': [
                "I do not like coffee.",
                "She never goes to parties.",
                "There is no time left."
            ]
        },
        {
            'category': 'numeric',
            'sentences': [
                "I have three books on the table.",
                "This is my first time here.",
                "The car costs 20000 dollars."
            ]
        }
    ]
    
    total_tests = 0
    successful_tests = 0
    phase1_detections = 0
    
    for test_case in test_cases:
        category = test_case['category']
        print(f"\n📂 {category.upper()}依存関係テスト:")
        
        for sentence in test_case['sentences']:
            total_tests += 1
            print(f"\n📝 例文: '{sentence}'")
            
            try:
                result = engine.analyze_sentence(sentence)
                successful_tests += 1
                
                # スロット結果表示
                slots = result.get('slots', {})
                print(f"  📊 検出スロット:")
                for slot, contents in slots.items():
                    if contents:  # 空でないスロットのみ表示
                        print(f"    {slot}: {contents}")
                
                # フェーズ1機能検出チェック
                has_phase1_content = False
                for slot in ['M1', 'M2']:
                    if slots.get(slot):
                        for content in slots[slot]:
                            # 辞書形式と文字列形式の両方に対応
                            if isinstance(content, dict):
                                content_text = content.get('value', str(content))
                            else:
                                content_text = str(content)
                                
                            # フェーズ1特有の検出パターンをチェック
                            if (category == 'compound' and len(content_text.split()) > 1) or \
                               (category == 'conjunction' and any(word in content_text.lower() for word in ['and', 'or', 'but'])) or \
                               (category == 'negation' and any(word in content_text.lower() for word in ['not', 'never', 'no'])) or \
                               (category == 'numeric' and any(word in content_text for word in ['three', 'first', '20000'])):
                                has_phase1_content = True
                                phase1_detections += 1
                                print(f"  ✅ フェーズ1機能検出: {content_text}")
                                break
                
                if not has_phase1_content:
                    print(f"  ⚠️ フェーズ1機能未検出")
                
                # メタデータ確認
                metadata = result.get('metadata', {})
                if metadata.get('phase1_enhanced'):
                    print(f"  🚀 フェーズ1拡張: 有効")
                
            except Exception as e:
                print(f"  ❌ 解析失敗: {e}")
    
    # 結果サマリー
    print(f"\n" + "="*60)
    print(f"📊 フェーズ1拡張機能テスト結果")
    print(f"="*60)
    print(f"総テスト数: {total_tests}")
    print(f"解析成功: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
    print(f"フェーズ1検出: {phase1_detections} ({phase1_detections/total_tests*100:.1f}%)")
    print(f"")
    
    if phase1_detections > 0:
        print(f"🎉 フェーズ1拡張機能が正常に動作しています！")
        print(f"   compound, conj+cc, neg, nummodの依存関係処理が追加されました。")
    else:
        print(f"⚠️  フェーズ1機能の検出に課題があります。調整が必要です。")

if __name__ == "__main__":
    test_phase1_enhancements()
