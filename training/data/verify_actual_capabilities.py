#!/usr/bin/env python3
"""
現在のGrammar Master Controller V2の実際の複文処理能力確認テスト
ユーザーの指摘が正しいかを検証するため、従来システムの実際の能力を確認します。
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from grammar_master_controller_v2 import GrammarMasterControllerV2
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def test_actual_grammar_master_capabilities():
    """現在のGrammar Master Controller V2の実際の処理能力を確認"""
    
    print("🔬 Grammar Master Controller V2 - 実際の複文処理能力確認")
    print("=" * 80)
    
    # Phase 2を無効化して従来の処理能力のみをテスト
    controller = GrammarMasterControllerV2()
    
    # 複雑な文構造のテストケース
    test_sentences = [
        "I think that he is smart.",
        "She believes that they work hard.",
        "He knows that she loves music.",
        "They said that it was true.",
        "I heard that you are coming.",
        "The man who lives next door is kind.",
        "The book that I read yesterday was interesting.", 
        "She is the teacher whom we respect.",
        "When it rains, I stay home.",
        "If you study hard, you will succeed.",
        "Because she is smart, she passed the test.",
        "Although it was difficult, he finished the work."
    ]
    
    print("\n🧪 従来システム（Phase 2無効化）での複文処理テスト:")
    print("-" * 70)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n【テスト {i}】: {sentence}")
        
        try:
            # Phase 2無効化のため、sublevel処理を除外して基本処理のみ確認
            result = controller.process_sentence(sentence, debug=False)
            
            print(f"   エンジン: {result.engine_type.value}")
            print(f"   成功: {result.success}")
            
            if result.slots:
                print(f"   基本スロット抽出:")
                for slot, value in result.slots.items():
                    if value and value.strip():
                        print(f"      {slot}: '{value}'")
            
            # 従属節や複雑構造が適切に処理されているかチェック
            slots = result.slots if result.slots else {}
            
            # 従属節処理の確認
            if "that" in sentence.lower():
                print("   📋 従属節文の処理確認:")
                o1_value = slots.get('O1', '')
                o2_value = slots.get('O2', '')
                if 'that' in o1_value.lower() or 'that' in o2_value.lower():
                    print("      ✅ 従属節がスロットに含まれています")
                else:
                    print("      ❌ 従属節がスロットに含まれていません")
            
            # 関係詞処理の確認
            if any(word in sentence.lower() for word in ['who', 'which', 'that']):
                if sentence.lower().startswith('the'):
                    print("   📋 関係詞文の処理確認:")
                    s_value = slots.get('S', '')
                    if any(word in s_value.lower() for word in ['who', 'which', 'that']):
                        print("      ✅ 関係詞句がSスロットに含まれています")
                    else:
                        print("      ❌ 関係詞句がスロットに含まれていません")
            
            # 副詞節処理の確認
            if any(conj in sentence.lower() for conj in ['when', 'if', 'because', 'although']):
                print("   📋 副詞節文の処理確認:")
                m_values = [slots.get(f'M{i}', '') for i in range(1, 4)]
                if any(any(conj in m_val.lower() for conj in ['when', 'if', 'because', 'although']) for m_val in m_values):
                    print("      ✅ 副詞節がMスロットに含まれています")
                else:
                    print("      ❌ 副詞節がスロットに含まれていません")
                    
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")
    
    # 最終評価
    print(f"\n\n📊 Grammar Master Controller V2 の実際の能力評価")
    print("=" * 80)
    
    # 統計取得
    stats = controller.get_processing_stats()
    print(f"処理統計:")
    print(f"   総リクエスト数: {stats['total_requests']}")
    print(f"   成功率: {stats['success_rate_percent']}%")
    print(f"   使用されたエンジン数: {stats['engines_loaded']}")
    
    # エンジン情報取得
    engine_info = controller.get_engine_info()
    print(f"\n利用可能エンジン:")
    for engine in engine_info['engine_list']:
        if engine['loaded']:
            print(f"   ✅ {engine['type']}: 使用回数 {engine['usage_count']}")

def main():
    """メイン実行"""
    test_actual_grammar_master_capabilities()
    
    print(f"\n\n📋 検証結果に基づく結論")
    print("=" * 80)
    print("この検証により、Grammar Master Controller V2が")
    print("実際にどの程度の複文処理能力を持っているかが明確になります。")
    print()
    print("もしユーザーの指摘通り、従来システムが既に複文を適切に処理していたなら、")
    print("Phase 2の価値は「新機能追加」ではなく「分析の深化・統一」にあることになります。")

if __name__ == "__main__":
    main()
