"""
🔍 複雑文処理ロジックのデバッグ
なぜ節の統合処理が動作していないのか？
"""

from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
import spacy

def debug_complex_processing():
    """複雑文処理のデバッグ"""
    print("🔍 複雑文処理ロジックのデバッグ")
    print("=" * 60)
    
    nlp = spacy.load("en_core_web_sm")
    sentence = ("That afternoon at the crucial point in the presentation, "
               "the manager who had recently taken charge of the project "
               "had to make the committee responsible for implementation "
               "deliver the final proposal flawlessly even though he was "
               "under intense pressure so the outcome would reflect their full potential.")
    
    print("📝 入力文:")
    print(f"   {sentence}")
    print()
    
    # spaCy解析の詳細確認
    print("🔧 spaCy解析結果:")
    doc = nlp(sentence)
    for i, token in enumerate(doc):
        print(f"   [{i:2d}] {token.text:<15} | {token.pos_:<8} | {token.dep_:<15} | head: {token.head.text}")
    print()
    
    # 統合エンジンの処理ステップを追跡
    engine = SimpleUnifiedRephraseSlotIntegrator()
    
    print("🎯 処理ステップの追跡:")
    print("-" * 40)
    
    # 1. 特殊構文判定のチェック
    print("1️⃣ 特殊構文判定:")
    
    # There構文チェック
    is_there = sentence.lower().startswith('there ')
    print(f"   There構文: {is_there}")
    
    # 複文チェック（think that）
    has_think_that = 'think' in sentence.lower() and 'that' in sentence.lower()
    print(f"   think that複文: {has_think_that}")
    
    # 実際には他の複雑構文も処理すべき
    print("   → この文は特殊構文として認識されていない可能性")
    print()
    
    print("2️⃣ 基本要素抽出の問題:")
    
    # 基本要素抽出をシミュレート
    roots = [token for token in doc if token.dep_ == 'ROOT']
    subjects = [token for token in doc if token.dep_ == 'nsubj']
    objects = [token for token in doc if token.dep_ in ['dobj', 'iobj']]
    
    print(f"   ROOT動詞: {[t.text for t in roots]}")
    print(f"   主語(nsubj): {[t.text for t in subjects]}")  
    print(f"   目的語: {[t.text for t in objects]}")
    print()
    
    print("3️⃣ 問題の特定:")
    print("   ❌ 複雑文専用の処理パスが実行されていない")
    print("   ❌ 'think that'パターンにのみ対応、使役動詞は未対応")
    print("   ❌ 関係詞節の特別処理が基本抽出を妨害")
    print()
    
    # 理想的な処理フローを表示
    print("🎯 理想的な処理フロー:")
    print("=" * 40)
    print("1. 使役動詞構文を検出 (make + O + C)")
    print("2. 関係詞節を統合してフレーズ化")
    print("3. 時間表現を文頭修飾語として配置")
    print("4. 副詞節を適切な修飾語スロットに配置")
    print("5. 節単位での意味的分解実行")
    print()
    
    print("💡 修正が必要な箇所:")
    print("- 使役動詞構文の専用処理")
    print("- 関係詞節の句として統合")  
    print("- 副詞節の適切な分離")
    print("- 複雑文判定ロジックの拡張")

if __name__ == "__main__":
    debug_complex_processing()
