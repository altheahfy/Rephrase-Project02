"""
Rephrase仕様準拠エンジン実証テスト
5文型フルセットの具体例文で実際の動作を検証し、エラーを発見・修正する
"""

import sys
sys.path.append('.')
from rephrase_spec_compliant_engine import RephraseSpecCompliantEngine

def test_multiple_examples():
    """複数の実例文でテスト"""
    engine = RephraseSpecCompliantEngine()
    
    # テスト例文（5文型フルセットより）
    test_cases = [
        {
            "name": "関係詞節1",
            "sentence": "The experienced manager who had recently taken charge completed the project successfully.",
            "expected_slots": ["S", "V"]
        },
        {
            "name": "関係詞節2", 
            "sentence": "The woman who seemed indecisive knew the answer.",
            "expected_slots": ["S", "V", "O1"]
        },
        {
            "name": "従属節1",
            "sentence": "He figured out the solution because he feared upsetting her.",
            "expected_slots": ["S", "V", "O1", "M3"]
        },
        {
            "name": "単純文",
            "sentence": "She gave him a message.",
            "expected_slots": ["S", "V", "O1", "O2"]
        }
    ]
    
    print("=" * 80)
    print("🧪 Rephrase仕様準拠エンジン実証テスト")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[テスト{i}] {test_case['name']}")
        print(f"例文: {test_case['sentence']}")
        print("-" * 60)
        
        try:
            result = engine.decompose_sentence(test_case['sentence'])
            
            print("📋 分解結果:")
            if result:
                for slot, content in result.items():
                    if isinstance(content, dict):
                        print(f"  {slot}:")
                        for key, value in content.items():
                            print(f"    {key}: {value}")
                    else:
                        print(f"  {slot}: {content}")
            else:
                print("  ⚠️ 結果なし")
            
            # 期待スロットとの比較
            found_slots = set(result.keys())
            expected_slots = set(test_case['expected_slots'])
            
            print(f"\n🔍 スロット検証:")
            print(f"  期待: {expected_slots}")
            print(f"  実際: {found_slots}")
            print(f"  一致: {found_slots == expected_slots}")
            
            if found_slots != expected_slots:
                missing = expected_slots - found_slots
                extra = found_slots - expected_slots
                if missing:
                    print(f"  未検出: {missing}")
                if extra:
                    print(f"  余分: {extra}")
                    
        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()

def test_spacy_dependency_analysis():
    """spaCy依存関係解析の詳細テスト"""
    import spacy
    
    nlp = spacy.load('en_core_web_sm')
    
    test_sentence = "The woman who seemed indecisive knew the answer."
    doc = nlp(test_sentence)
    
    print(f"\n🔍 spaCy依存関係解析詳細: '{test_sentence}'")
    print("-" * 60)
    
    for token in doc:
        print(f"{token.text:<12} | pos: {token.pos_:<6} | dep: {token.dep_:<12} | head: {token.head.text}")
    
    print("\n🔍 依存関係ツリー:")
    for token in doc:
        if token.dep_ == 'ROOT':
            print(f"ROOT: {token.text}")
            _print_children(token, 1)

def _print_children(token, indent):
    """子要素を再帰的に表示"""
    for child in token.children:
        print("  " * indent + f"├─ {child.text} ({child.dep_})")
        _print_children(child, indent + 1)

if __name__ == "__main__":
    # 実証テスト実行
    test_multiple_examples()
    
    print("\n" + "=" * 80)
    
    # spaCy解析詳細表示
    test_spacy_dependency_analysis()
