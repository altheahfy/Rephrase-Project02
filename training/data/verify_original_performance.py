#!/usr/bin/env python3
"""
元のdynamic_grammar_mapperの実際の性能確認
ChatGPT5パイプライン導入前の元システムの実力を検証
"""

from dynamic_grammar_mapper import DynamicGrammarMapper
import traceback

def test_original_performance():
    """元のシステムの実際の性能テスト"""
    print("🔍 元のdynamic_grammar_mapperの性能確認")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    
    # 簡単な文でテスト
    test_sentences = [
        "I run.",
        "She sings.",
        "Dogs bark.",
        "The cat sleeps.",
        "We study English.",
    ]
    
    print("📝 テスト文:")
    for sentence in test_sentences:
        print(f"   - {sentence}")
    
    print("\n📊 分析結果:")
    print("-" * 40)
    
    for sentence in test_sentences:
        try:
            result = mapper.analyze_sentence(sentence)
            
            print(f"\n📍 '{sentence}':")
            print(f"   ✅ 成功: {type(result)}")
            
            # 重要な結果を表示
            main_slots = result.get('main_slots', {})
            sub_slots = result.get('sub_slots', {})
            slots = result.get('slots', {})
            
            print(f"   📊 main_slots: {main_slots}")
            print(f"   📊 sub_slots: {sub_slots}")
            print(f"   📊 slots: {slots}")
            print(f"   📊 V: {result.get('V', 'None')}")
            
            # スロットが正しく埋まっているかチェック
            if main_slots or slots:
                print(f"   🎯 評価: 正常に分解されている")
            else:
                print(f"   ⚠️ 評価: スロットが空")
                
        except Exception as e:
            print(f"\n📍 '{sentence}':")
            print(f"   ❌ エラー: {type(e).__name__}: {e}")

def compare_before_after_chatgpt5():
    """ChatGPT5導入前後の比較"""
    print("\n🔍 ChatGPT5導入の実際の効果確認")
    print("=" * 60)
    
    mapper = DynamicGrammarMapper()
    sentence = "I run."
    
    print(f"📝 テスト文: '{sentence}'")
    
    # 現在の結果
    print("\n📊 現在の結果（ChatGPT5統合後）:")
    try:
        result = mapper.analyze_sentence(sentence)
        print(f"   ✅ 成功")
        print(f"   📍 main_slots: {result.get('main_slots', {})}")
        print(f"   📍 slots: {result.get('slots', {})}")
        print(f"   📍 V: {result.get('V', 'None')}")
        
        # ChatGPT5固有の結果
        if 'main_verb_detected' in result:
            print(f"   🆕 ChatGPT5追加情報: {result['main_verb_detected']}")
        
    except Exception as e:
        print(f"   ❌ エラー: {e}")

def analyze_actual_improvements():
    """実際の改善点を分析"""
    print("\n🔍 実際の改善点の分析")
    print("=" * 60)
    
    print("📊 検証すべき点:")
    print("   1. 元システムは本当に失敗していたのか？")
    print("   2. ChatGPT5パイプラインは何を改善したのか？")
    print("   3. 実際のメリットは何か？")
    
    print("\n🤔 考察:")
    print("   - 'I run.'のような単純文は元々成功していた可能性が高い")
    print("   - ChatGPT5の真価は複雑な文で発揮される")
    print("   - エラーハンドリングの改善が主な効果かもしれない")
    
    print("\n📝 検証が必要な複雑な文:")
    complex_sentences = [
        "The dog whose tail is wagging runs quickly.",
        "I think that she will come tomorrow.", 
        "The book which I bought yesterday is interesting.",
        "Having finished homework, he went to bed.",
        "Can you help me?",
    ]
    
    mapper = DynamicGrammarMapper()
    
    for sentence in complex_sentences:
        print(f"\n📍 '{sentence}':")
        try:
            result = mapper.analyze_sentence(sentence)
            main_slots = result.get('main_slots', {})
            slots = result.get('slots', {})
            
            if main_slots or slots:
                print(f"   ✅ 成功: {slots}")
            else:
                print(f"   ⚠️ スロット空: 分解に失敗？")
                
        except Exception as e:
            print(f"   ❌ エラー: {e}")

if __name__ == "__main__":
    # 元システム性能テスト
    test_original_performance()
    
    # ChatGPT5導入効果比較
    compare_before_after_chatgpt5()
    
    # 実際の改善点分析
    analyze_actual_improvements()
    
    print("\n🎯 結論:")
    print("ユーザーの指摘通り、元のシステムは単純文で失敗していなかった可能性が高い")
    print("ChatGPT5パイプラインの真価は別の部分にあるはず")
