#!/usr/bin/env python3
"""
Sublevel Pattern Library Debug Test
サブレベルパターンライブラリの個別デバッグテスト

Grammar Master Controller統合前に、サブレベルパターンライブラリ単体で
の動作を確認し、パターン検出が正常に機能するかをテストします。
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from sublevel_pattern_lib import SublevelPatternLib
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def debug_sublevel_pattern_lib():
    """サブレベルパターンライブラリ単体テスト"""
    print("🔧 Sublevel Pattern Library Debug Test")
    print("=" * 60)
    
    # ライブラリ初期化
    lib = SublevelPatternLib()
    
    if not lib.nlp:
        print("❌ Stanza NLP パイプラインの初期化に失敗しました")
        return
    
    # テストケース
    test_cases = [
        "that he is smart",      # SUB_SVC期待
        "that they work hard",   # SUB_SV期待
        "that she loves music",  # SUB_SVO期待
        "who lives next door",   # REL_SUBJ期待
        "that I read",           # REL_OBJ期待
        "When it rains",         # ADV_CLAUSE期待
    ]
    
    print("\n🧪 Individual Pattern Analysis Tests:")
    print("-" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n【Test {i}】: '{text}'")
        
        try:
            # パターン解析
            result = lib.analyze_sublevel_pattern(text)
            
            if result:
                pattern_name, pattern_details = result
                print(f"   ✅ Pattern Detected: {pattern_name}")
                print(f"   📋 Root Word: {pattern_details.get('root_word', 'N/A')}")
                print(f"   🏷️  Root POS: {pattern_details.get('root_pos', 'N/A')}")
                
                # サブレベルスロット抽出テスト
                slots = lib.extract_sublevel_slots(text, pattern_name)
                if slots:
                    print(f"   🔍 Sublevel Slots: {slots}")
                else:
                    print("   ⚠️  No sublevel slots extracted")
            else:
                print("   ❌ No pattern detected")
                
                # Stanza解析結果を表示して問題を調査
                try:
                    doc = lib.nlp(text)
                    sent = doc.sentences[0]
                    print("   🔍 Stanza Analysis:")
                    for word in sent.words:
                        print(f"      {word.text}: {word.pos} ({word.deprel})")
                except Exception as parse_error:
                    print(f"   ❌ Stanza parse error: {parse_error}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # パターン定義確認
    print(f"\n📚 Available Patterns: {list(lib.sublevel_patterns.keys())}")
    print(f"🔤 Relative Pronouns: {lib.relative_pronouns}")
    print(f"🔗 Subordinate Conjunctions: {lib.subordinate_conjunctions}")

if __name__ == "__main__":
    debug_sublevel_pattern_lib()
