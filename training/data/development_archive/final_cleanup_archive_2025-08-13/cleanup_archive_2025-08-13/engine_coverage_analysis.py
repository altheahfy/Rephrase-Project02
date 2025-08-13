#!/usr/bin/env python3
"""
Engine Coverage Analysis
各文構造がどのエンジンの担当範囲かを分析
"""

def analyze_engine_responsibilities():
    """失敗した構造を担当エンジンで分類"""
    
    failed_structures = [
        "Yes.",           # 省略文
        "No problem.",    # 省略文  
        "Thanks!",        # 省略文
        "Goodbye.",       # 省略文
        "What a beautiful day!",  # 感嘆文
        "How amazing!",   # 感嘆文
        "Oh my god!",     # 感嘆文
        "Stop!",          # 命令文
        "Come here.",     # 命令文
        "Don't do that.", # 命令文（否定）
        "It is John who called.",  # 分裂文・強調構文
    ]
    
    # 現在実装済みエンジンとその担当範囲
    engine_coverage = {
        "QUESTION": {
            "description": "疑問文形成システム",
            "structures": ["What a beautiful day!", "How amazing!"],
            "reason": "感嘆文は疑問詞Whatを使った構造なので疑問文エンジンが処理可能"
        },
        "MODAL": {
            "description": "助動詞システム", 
            "structures": ["Don't do that."],
            "reason": "否定命令文はdo助動詞を含むため"
        },
        "INVERSION": {
            "description": "倒置文システム",
            "structures": ["It is John who called."],
            "reason": "分裂文は倒置を伴う強調構文"
        },
        "CONJUNCTION": {
            "description": "接続詞システム",
            "structures": [],
            "reason": "省略文の復元時に接続詞が関わる場合がある"
        },
        "専用エンジン未実装": {
            "description": "省略文・命令文専用エンジンが必要",
            "structures": [
                "Yes.", "No problem.", "Thanks!", "Goodbye.",  # 省略文
                "Stop!", "Come here."  # 命令文（肯定）
            ],
            "reason": "これらは既存エンジンの範疇を超えた特殊構造"
        }
    }
    
    print("🔍 Engine Coverage Analysis")
    print("=" * 60)
    
    total_failed = len(failed_structures)
    covered_by_existing = 0
    
    for engine, info in engine_coverage.items():
        if info["structures"]:
            print(f"\n🎯 {engine}: {info['description']}")
            print(f"   担当構造: {len(info['structures'])}個")
            for structure in info["structures"]:
                print(f"   - '{structure}'")
            print(f"   理由: {info['reason']}")
            covered_by_existing += len(info["structures"])
    
    uncovered = total_failed - covered_by_existing
    
    print(f"\n📊 Coverage Summary:")
    print(f"   失敗構造総数: {total_failed}")
    print(f"   既存エンジンでカバー可能: {covered_by_existing} ({covered_by_existing/total_failed*100:.1f}%)")
    print(f"   専用エンジン必要: {uncovered} ({uncovered/total_failed*100:.1f}%)")
    
    print(f"\n💡 結論:")
    print(f"   欠けている5%のうち、{covered_by_existing/total_failed*100:.1f}%は既存エンジンで対応可能")
    print(f"   真の欠落は省略文・命令文エンジンのみ（{uncovered/total_failed*100:.1f}%）")

if __name__ == "__main__":
    analyze_engine_responsibilities()
