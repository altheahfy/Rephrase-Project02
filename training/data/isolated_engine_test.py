#!/usr/bin/env python3
"""
関係節エンジン単独テスト - 問題の特定
"""

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def test_relative_clause_only():
    """関係節エンジンのみでテスト"""
    print("🧪 関係節エンジン単独テスト")
    print("="*50)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    
    # 関係節エンジンのみ追加
    mapper.add_handler('relative_clause')
    print("✅ 関係節エンジンのみ追加")
    
    # 問題の文章
    sentence = "The car which was crashed is red."
    print(f"\n📖 テスト文章: {sentence}")
    print("-" * 50)
    
    result = mapper.process(sentence)
    
    print(f"⏱️  処理時間: {result['meta']['processing_time']:.3f}秒")
    print(f"\n📊 分解結果:")
    print(f"  メインスロット: {result.get('slots', {})}")
    print(f"  サブスロット: {result.get('sub_slots', {})}")
    print(f"  検出パターン: {result.get('grammar_info', {}).get('detected_patterns', [])}")
    
    return result

def test_passive_voice_only():
    """受動態エンジンのみでテスト"""
    print("\n" + "="*50)
    print("🧪 受動態エンジン単独テスト")
    print("="*50)
    
    # 初期化
    mapper = UnifiedStanzaRephraseMapper(log_level='ERROR')
    
    # 受動態エンジンのみ追加
    mapper.add_handler('passive_voice')
    print("✅ 受動態エンジンのみ追加")
    
    # 問題の文章
    sentence = "The car which was crashed is red."
    print(f"\n📖 テスト文章: {sentence}")
    print("-" * 50)
    
    result = mapper.process(sentence)
    
    print(f"⏱️  処理時間: {result['meta']['processing_time']:.3f}秒")
    print(f"\n📊 分解結果:")
    print(f"  メインスロット: {result.get('slots', {})}")
    print(f"  サブスロット: {result.get('sub_slots', {})}")
    print(f"  検出パターン: {result.get('grammar_info', {}).get('detected_patterns', [])}")
    
    return result

if __name__ == "__main__":
    # 関係節エンジン単独テスト
    rel_result = test_relative_clause_only()
    
    # 受動態エンジン単独テスト
    pass_result = test_passive_voice_only()
    
    print("\n" + "="*60)
    print("🔍 比較分析")
    print("="*60)
    
    print("\n📋 関係節エンジン単独:")
    for key, value in rel_result.get('sub_slots', {}).items():
        print(f"  {key}: {value}")
    
    print("\n📋 受動態エンジン単独:")
    for key, value in pass_result.get('sub_slots', {}).items():
        print(f"  {key}: {value}")
