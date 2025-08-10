#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全上位スロット用 包括的テストスイート

O1で達成した100%活用を全スロットで実現するための
包括的テストケース集
"""

from step14_universal_subslot import UniversalSubslotGenerator
import json

def comprehensive_slot_test():
    """包括的スロットテスト - 各スロットで10サブスロット活用を目指す"""
    print("🚀 包括的スロットテスト開始")
    print("🎯 目標: 全スロットで10サブスロット最大活用")
    print("=" * 80)
    
    generator = UniversalSubslotGenerator()
    
    # より複雑で包括的なテストケース
    comprehensive_tests = {
        "S": [
            "The very intelligent young students who were studying hard",
            "My extremely kind older sister who always helps me",
            "Those beautiful red cars that were parked outside yesterday"
        ],
        
        "O1": [
            "that he is definitely studying English very hard today",
            "the extremely beautiful red sports car with leather seats",
            "giving him a very expensive birthday present yesterday"
        ],
        
        "O2": [
            "to his very kind elderly mother who lives in Tokyo",
            "for the extremely talented young musicians in our school",
            "with her best friend who was studying abroad last year"
        ],
        
        "C1": [
            "extremely happy and excited about the wonderful news today",
            "a very successful young businessman who works in Tokyo",
            "quite tired but still determined to finish the important work"
        ],
        
        "C2": [
            "absolutely impossible to solve without proper mathematical knowledge",
            "the most beautiful song that I have ever heard before",
            "completely different from what we had expected yesterday"
        ],
        
        "M1": [
            "very carefully and quietly in the early morning hours",
            "extremely fast with great skill and amazing precision today",
            "quite often during the cold winter months every year"
        ],
        
        "M2": [
            "always working diligently until very late at night",
            "frequently visiting the beautiful old library downtown",
            "sometimes playing tennis with his best friends outside"
        ],
        
        "M3": [
            "under the beautiful old bridge that was built centuries ago",
            "during the extremely busy holiday season last December",
            "throughout the entire difficult period when everything was changing"
        ]
    }
    
    results = {}
    slot_utilization = {}
    
    for slot_name, test_sentences in comprehensive_tests.items():
        print(f"\n{'='*60}")
        print(f"🎯 {slot_name}スロット包括テスト")
        print(f"📊 テスト文数: {len(test_sentences)}")
        
        slot_results = []
        all_subslots_found = set()
        
        for i, sentence in enumerate(test_sentences, 1):
            print(f"\n--- テスト{i}: {slot_name}スロット ---")
            print(f"📝 入力: '{sentence}'")
            
            subslots = generator.generate_subslots_for_slot(slot_name, sentence)
            slot_results.append({
                'sentence': sentence,
                'subslots': subslots,
                'subslot_count': len(subslots)
            })
            
            # サブスロット種類を記録
            for subslot_type in subslots.keys():
                all_subslots_found.add(subslot_type)
            
            print(f"📊 検出サブスロット数: {len(subslots)}")
            for sub_type, sub_data in subslots.items():
                print(f"   ✅ {sub_type}: '{sub_data['text']}'")
            
            if len(subslots) == 0:
                print("   ⚠️  サブスロット未検出")
        
        # スロット統計
        total_subslots = sum([r['subslot_count'] for r in slot_results])
        max_subslots = max([r['subslot_count'] for r in slot_results])
        unique_subslot_types = len(all_subslots_found)
        
        slot_utilization[slot_name] = {
            'total_tests': len(test_sentences),
            'total_subslots_detected': total_subslots,
            'max_subslots_in_single_test': max_subslots,
            'unique_subslot_types': unique_subslot_types,
            'subslot_types_found': sorted(list(all_subslots_found)),
            'utilization_rate': f"{unique_subslot_types}/10"
        }
        
        print(f"\n📊 {slot_name}スロット統計:")
        print(f"   総サブスロット検出数: {total_subslots}")
        print(f"   最大サブスロット数(単一テスト): {max_subslots}")
        print(f"   サブスロット種類数: {unique_subslot_types}/10")
        print(f"   検出サブスロット種類: {', '.join(sorted(list(all_subslots_found)))}")
        
        results[slot_name] = slot_results
    
    # 全体統計
    print(f"\n{'='*80}")
    print("🎉 包括テスト完了 - 全体統計")
    print(f"{'='*80}")
    
    total_unique_types = 0
    perfect_slots = []
    
    for slot_name, stats in slot_utilization.items():
        utilization_percent = (stats['unique_subslot_types'] / 10) * 100
        print(f"{slot_name:3s}: {stats['utilization_rate']:5s} ({utilization_percent:5.1f}%) - "
              f"検出種類: {', '.join(stats['subslot_types_found'])}")
        
        total_unique_types += stats['unique_subslot_types']
        
        if stats['unique_subslot_types'] == 10:
            perfect_slots.append(slot_name)
    
    overall_utilization = (total_unique_types / (8 * 10)) * 100  # 8スロット × 10サブスロット
    
    print(f"\n🎯 全体活用率: {total_unique_types}/80 ({overall_utilization:.1f}%)")
    
    if perfect_slots:
        print(f"🎉 完全活用達成スロット: {', '.join(perfect_slots)}")
    
    need_improvement = [s for s, stats in slot_utilization.items() 
                       if stats['unique_subslot_types'] < 7]
    if need_improvement:
        print(f"⚠️  改善が必要なスロット: {', '.join(need_improvement)}")
    
    return results, slot_utilization

def analyze_missing_subslots():
    """未検出サブスロットの分析"""
    print("\n🔍 未検出サブスロット分析")
    print("=" * 50)
    
    all_subslot_types = ['sub-s', 'sub-v', 'sub-o1', 'sub-o2', 
                        'sub-c1', 'sub-c2', 'sub-m1', 'sub-m2', 'sub-m3', 'sub-aux']
    
    # 各スロットで検出されるべき典型的サブスロット
    expected_subslots = {
        'S': ['sub-s', 'sub-m1', 'sub-m2', 'sub-aux', 'sub-c1'],
        'O1': all_subslot_types,  # O1は全対応済み
        'O2': ['sub-o2', 'sub-s', 'sub-v', 'sub-m1', 'sub-m2'],
        'C1': ['sub-c1', 'sub-m1', 'sub-m2', 'sub-aux', 'sub-v'],
        'C2': ['sub-c2', 'sub-m1', 'sub-m2', 'sub-aux', 'sub-v'],
        'M1': ['sub-m1', 'sub-s', 'sub-v', 'sub-o1', 'sub-aux'],
        'M2': ['sub-m2', 'sub-s', 'sub-v', 'sub-o1', 'sub-aux'],
        'M3': ['sub-m3', 'sub-s', 'sub-v', 'sub-o1', 'sub-aux']
    }
    
    for slot, expected in expected_subslots.items():
        print(f"{slot}: 期待サブスロット = {', '.join(expected)}")
    
    return expected_subslots

def suggest_improvements():
    """改善提案生成"""
    print("\n💡 改善提案")
    print("=" * 40)
    
    improvements = [
        "1. 前置詞句の詳細分析強化（O2, M1, M2, M3用）",
        "2. 関係代名詞節の完全サブスロット展開",
        "3. 動名詞・不定詞句のサブスロット分解",
        "4. 複合修飾語の階層的分析",
        "5. 補語種類の詳細分類（C1/C2強化）",
        "6. 副詞句の意味分類による適切配置",
        "7. 従属節内のサブスロット再帰処理"
    ]
    
    for improvement in improvements:
        print(f"📝 {improvement}")

if __name__ == "__main__":
    # 包括テスト実行
    results, utilization = comprehensive_slot_test()
    
    # 分析と改善提案
    analyze_missing_subslots()
    suggest_improvements()
    
    print(f"\n{'='*80}")
    print("🎯 次のステップ: 検出率の低いスロットの専用強化実装")
    print("📊 目標: 全8スロットで80/80 (100%) サブスロット活用達成")
    print("="*80)
