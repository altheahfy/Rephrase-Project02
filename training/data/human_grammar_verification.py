#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人間文法認識 vs Stanza比較検証システム

目的:
1. 人間文法認識の結果がスロットに反映されているかを確認
2. Stanzaフォールバックが隠れて動作していないかを検証
3. 具体的な差異を可視化
"""

import json
import sys
import os
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def create_comparison_test():
    """人間文法認識 vs Stanza の比較テスト"""
    
    # テスト用文章（人間文法認識で検出されるパターンを含む）
    test_sentences = [
        "The car whose owner is rich lives here.",           # possessive_relative
        "He looks as if he were a king.",                    # compound_conjunction  
        "The book was written carefully.",                   # passive_voice
        "The woman who works here is smart.",               # standard_relative
    ]
    
    print("🔍 人間文法認識 vs Stanza比較検証開始")
    print("=" * 70)
    
    # マッパー初期化
    mapper = UnifiedStanzaRephraseMapper()
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト {i}: {sentence}")
        print("-" * 50)
        
        # 通常処理実行
        result = mapper.process(sentence)
        
        print(f"✅ 処理結果:")
        print(f"   メインスロット数: {len(result.get('slots', {}))}")
        print(f"   サブスロット数: {len(result.get('sub_slots', {}))}")
        
        # スロット内容詳細表示
        if result.get('slots'):
            print(f"   メインスロット: {result['slots']}")
        if result.get('sub_slots'):
            print(f"   サブスロット: {result['sub_slots']}")
        
        # エラーチェック
        if 'error' in result:
            print(f"   ⚠️ エラー: {result['error']}")
        
        # 人間文法認識メタデータチェック
        processing_time = result.get('meta', {}).get('processing_time', 0)
        print(f"   処理時間: {processing_time:.3f}s")
    
    print("\n" + "=" * 70)
    print("🏁 比較検証完了")

def extract_human_grammar_corrections():
    """人間文法認識の修正情報を抽出（デバッグ用）"""
    
    # より詳細なログ設定で実行
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    print("\n🧠 人間文法認識詳細ログ検証")
    print("=" * 50)
    
    mapper = UnifiedStanzaRephraseMapper()
    test_sentence = "The car whose owner is rich lives here."
    
    print(f"テスト文: {test_sentence}")
    
    # デバッグモードで実行
    result = mapper.process(test_sentence)
    
    # 結果の詳細分析
    print(f"\n📊 結果分析:")
    print(f"スロット: {result.get('slots', {})}")
    print(f"サブスロット: {result.get('sub_slots', {})}")
    
    return result

if __name__ == "__main__":
    # 基本比較テスト
    create_comparison_test()
    
    # 詳細ログ検証
    extract_human_grammar_corrections()
