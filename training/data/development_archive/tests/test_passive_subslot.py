#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""受動態エンジン サブスロット処理テスト"""

from engines.passive_voice_engine import PassiveVoiceEngine
import stanza

def test_subslot_passive_processing():
    """サブスロット受動態処理テスト"""
    print("🔥 受動態エンジン サブスロット処理テスト開始")
    
    engine = PassiveVoiceEngine()
    nlp = stanza.Pipeline('en', verbose=False)
    
    # 従属節内の受動態テスト
    test_clauses = [
        "the work has been completed by the experienced team",    # 受動態（完了形+by句）
        "the house is being built",                              # 受動態（進行形）
        "she writes letters every day"                           # 能動態（対照）
    ]
    
    for i, clause in enumerate(test_clauses, 1):
        print(f"\n📝 サブスロットテスト{i}: {clause}")
        
        # Stanza解析
        doc = nlp(clause)
        sent = doc.sentences[0]
        
        try:
            # サブスロット専用処理
            result = engine.process_as_subslot(sent)
            if result:
                print(f"✅ サブスロット結果: {result}")
            else:
                print("❌ 処理失敗")
        except Exception as e:
            print(f"💥 エラー: {e}")
    
    # 統合例：接続詞節での受動態
    print(f"\n🎯 統合例: 接続詞節内受動態")
    complex_sentence = "Because the work has been completed by the experienced team, we can proceed."
    print(f"完全文: {complex_sentence}")
    
    # 従属節部分のみ抽出して処理
    subordinate_clause = "the work has been completed by the experienced team"
    doc = nlp(subordinate_clause)
    sent = doc.sentences[0]
    
    print(f"従属節: {subordinate_clause}")
    subslot_result = engine.process_as_subslot(sent)
    print(f"サブスロット分解: {subslot_result}")
    
    print("\n🎉 サブスロット処理テスト完了")

if __name__ == "__main__":
    test_subslot_passive_processing()
