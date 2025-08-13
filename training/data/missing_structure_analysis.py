#!/usr/bin/env python3
"""
Missing 5% Structure Analysis
基本5文型エンジンでカバーできない5%の構造を分析
"""

from engines.basic_five_pattern_engine import BasicFivePatternEngine

def analyze_missing_structures():
    engine = BasicFivePatternEngine()
    
    # 基本5文型でカバーできない可能性がある構造
    challenging_sentences = [
        # 省略構文
        "Yes.",
        "No problem.",
        "Thanks!",
        "Goodbye.",
        
        # 感嘆文
        "What a beautiful day!",
        "How amazing!",
        "Oh my god!",
        
        # 命令文
        "Stop!",
        "Come here.",
        "Don't do that.",
        
        # There構文
        "There is a book on the table.",
        "There are many students.",
        
        # It構文 (虚辞主語)
        "It is raining.",
        "It seems difficult.",
        
        # 倒置文
        "Never have I seen such beauty.",
        "Here comes the bus.",
        
        # 複文（複雑な従属節）
        "What I want is peace.",
        "That he is right is obvious.",
        
        # 分裂文
        "It is John who called.",
        "What I need is help.",
    ]
    
    print("🔍 Missing 5% Structure Analysis")
    print("=" * 60)
    
    detected_count = 0
    total_count = len(challenging_sentences)
    
    for i, sentence in enumerate(challenging_sentences, 1):
        result = engine.process_sentence(sentence)
        status = "✅ 検出成功" if result else "❌ 検出失敗"
        
        print(f"\n{i:2d}. \"{sentence}\"")
        print(f"    {status}")
        
        if result:
            detected_count += 1
            print(f"    パターン: {result['pattern']}")
            print(f"    スロット: {result['slots']}")
    
    coverage = (detected_count / total_count) * 100
    missing_percentage = 100 - coverage
    
    print("\n" + "=" * 60)
    print("📊 Coverage Analysis:")
    print(f"✅ 検出成功: {detected_count}/{total_count} ({coverage:.1f}%)")
    print(f"❌ 検出失敗: {total_count - detected_count}/{total_count} ({missing_percentage:.1f}%)")
    
    if missing_percentage > 0:
        print(f"\n💡 推定される欠けている{missing_percentage:.1f}%の内容:")
        print("  - 省略文・感嘆文・命令文")
        print("  - There構文・It虚辞構文")  
        print("  - 倒置文・分裂文")
        print("  - 複雑な従属節構造")

if __name__ == "__main__":
    analyze_missing_structures()
