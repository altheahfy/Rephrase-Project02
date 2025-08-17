#!/usr/bin/env python3
"""
複合副詞配置問題の詳細分析
テスト31,32,33,34,46,47,48の問題パターンを特定
"""
import sys
sys.path.append('..')
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def analyze_compound_adverb_issues():
    """複合副詞配置の具体的問題を分析"""
    
    # 問題例文
    test_cases = [
        {
            "id": 31,
            "sentence": "The book which was carefully written by Shakespeare is famous.",
            "expected": {
                "V": "is", "C1": "famous",
                "sub-s": "The book which", "sub-v": "written", "sub-aux": "was",
                "sub-m1": "carefully", "sub-m2": "by Shakespeare"
            }
        },
        {
            "id": 32, 
            "sentence": "The car that was quickly repaired yesterday runs smoothly.",
            "expected": {
                "V": "runs", "M1": "smoothly",
                "sub-s": "The car that", "sub-v": "repaired", "sub-aux": "was",
                "sub-m1": "quickly", "sub-m2": "yesterday"
            }
        },
        {
            "id": 34,
            "sentence": "The student who studies diligently always succeeds academically.",
            "expected": {
                "V": "succeeds", "M1": "always", "M2": "academically",
                "sub-s": "The student who", "sub-v": "studies",
                "sub-m1": "diligently"
            }
        }
    ]
    
    mapper = UnifiedStanzaRephraseMapper()
    
    print("🔍 複合副詞配置問題の詳細分析")
    print("=" * 60)
    
    for case in test_cases:
        print(f"\n📝 テスト{case['id']}: {case['sentence']}")
        
        result = mapper.process(case["sentence"])
        
        print(f"📊 システム出力:")
        for slot, value in result.items():
            if value:
                print(f"   {slot}: {value}")
        
        print(f"📋 期待値:")
        for slot, value in case["expected"].items():
            print(f"   {slot}: {value}")
        
        print(f"❌ 問題分析:")
        # 副詞の重複配置をチェック
        result_adverbs = {k: v for k, v in result.items() if k.startswith(('M', 'sub-m')) and v}
        expected_adverbs = {k: v for k, v in case["expected"].items() if k.startswith(('M', 'sub-m'))}
        
        print(f"   システム副詞: {result_adverbs}")
        print(f"   期待副詞: {expected_adverbs}")
        
        # 重複チェック
        duplicates = []
        for slot, value in result_adverbs.items():
            for other_slot, other_value in result_adverbs.items():
                if slot != other_slot and value in other_value:
                    duplicates.append((slot, other_slot, value))
        
        if duplicates:
            print(f"   🔴 重複副詞: {duplicates}")
        
        print("-" * 40)

if __name__ == "__main__":
    analyze_compound_adverb_issues()
