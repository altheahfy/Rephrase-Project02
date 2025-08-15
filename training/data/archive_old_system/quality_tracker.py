#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rephrase システム品質管理・進捗トラッキングツール
毎日の作業後に実行して、改善状況を記録
"""

import json
import datetime
from typing import Dict, List
from simple_unified_rephrase_integrator import SimpleUnifiedRephraseSlotIntegrator
from sub_slot_decomposer import SubSlotDecomposer

class QualityTracker:
    """品質改善トラッキングシステム"""
    
    def __init__(self):
        self.integrator = SimpleUnifiedRephraseSlotIntegrator()
        self.decomposer = SubSlotDecomposer()
        self.history_file = "quality_tracking_history.json"
        
        # 標準テストケース
        self.test_categories = {
            "basic": [
                "I study English.",
                "The cat sat.",
                "She is happy."
            ],
            "relative_clause": [
                "The book that I bought is good.",
                "The person who called me was John.",
                "The car which we saw was red."
            ],
            "causative": [
                "I made him study English.",
                "She let me use her car.", 
                "He had me clean the room."
            ],
            "temporal_conditional": [
                "When I arrived, he was sleeping.",
                "If it rains, we will stay home.",
                "Before she left, she called me."
            ],
            "complex": [
                "I think that he is smart.",
                "Having finished homework, I went out.",
                "The man walking there is my father."
            ]
        }
    
    def run_quality_assessment(self) -> Dict:
        """品質評価実行"""
        print("🔍 品質評価実行中...")
        
        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "categories": {}
        }
        
        total_success = 0
        total_tests = 0
        
        for category, sentences in self.test_categories.items():
            print(f"\n📂 カテゴリ: {category}")
            category_success = 0
            category_tests = len(sentences)
            category_details = []
            
            for sentence in sentences:
                try:
                    # メインスロット分解
                    main_result = self.integrator.process(sentence)
                    main_slots = main_result.get('slots', {})
                    
                    # サブスロット分解
                    sub_results = self.decomposer.decompose_complex_slots(main_slots)
                    
                    # 🔧 修正: より厳密な成功判定
                    main_meaningful = any(
                        slot.strip() for slot in main_slots.values() 
                        if slot and isinstance(slot, str)
                    )
                    
                    # サブスロット分解の詳細評価
                    sub_meaningful = False
                    sub_details = {}
                    
                    for slot_name, sub_results_list in sub_results.items():
                        if sub_results_list:
                            for sub_result in sub_results_list:
                                if hasattr(sub_result, 'sub_slots') and sub_result.sub_slots:
                                    if any(v.strip() for v in sub_result.sub_slots.values() if v):
                                        sub_meaningful = True
                                        sub_details[slot_name] = sub_result.sub_slots
                    
                    # 関係詞節を含む文の特別評価
                    has_relative_clause = any(
                        word in sentence.lower() 
                        for word in ['that', 'which', 'who', 'whom', 'whose']
                    )
                    
                    if has_relative_clause:
                        # 関係詞節がある場合はサブスロット分解必須
                        success = main_meaningful and sub_meaningful
                    else:
                        # 通常文はメインスロットのみで判定
                        success = main_meaningful
                    if success:
                        category_success += 1
                        total_success += 1
                    
                    category_details.append({
                        "sentence": sentence,
                        "success": success,
                        "main_slots": {k: v for k, v in main_slots.items() if v},
                        "sub_slots": sub_details,
                        "has_relative_clause": has_relative_clause,
                        "sub_meaningful": sub_meaningful
                    })
                    
                    print(f"  {'✅' if success else '❌'} {sentence}")
                    
                except Exception as e:
                    print(f"  ❌ {sentence} - エラー: {e}")
                    category_details.append({
                        "sentence": sentence,
                        "success": False,
                        "error": str(e)
                    })
                
                total_tests += 1
            
            category_accuracy = (category_success / category_tests) * 100
            results["categories"][category] = {
                "accuracy": category_accuracy,
                "success_count": category_success,
                "total_count": category_tests,
                "details": category_details
            }
            
            print(f"  📊 {category}: {category_accuracy:.1f}% ({category_success}/{category_tests})")
        
        overall_accuracy = (total_success / total_tests) * 100
        results["overall_accuracy"] = overall_accuracy
        results["total_success"] = total_success
        results["total_tests"] = total_tests
        
        print(f"\n🎯 総合精度: {overall_accuracy:.1f}% ({total_success}/{total_tests})")
        
        return results
    
    def save_history(self, results: Dict):
        """履歴保存"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
        
        history.append(results)
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"📝 結果を {self.history_file} に保存しました")
    
    def show_progress_trend(self):
        """進捗トレンド表示"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError:
            print("📊 履歴データが見つかりません")
            return
        
        if len(history) < 2:
            print("📊 比較するデータが不足しています")
            return
        
        print("\n📈 進捗トレンド:")
        print("=" * 50)
        
        for i, record in enumerate(history[-5:], 1):  # 最新5件
            timestamp = record.get("timestamp", "不明")
            accuracy = record.get("overall_accuracy", 0)
            date = timestamp.split('T')[0] if 'T' in timestamp else timestamp
            print(f"{i:2d}. {date}: {accuracy:.1f}%")
        
        # 改善幅計算
        if len(history) >= 2:
            latest = history[-1]["overall_accuracy"]
            previous = history[-2]["overall_accuracy"]
            improvement = latest - previous
            
            if improvement > 0:
                print(f"\n🚀 改善: +{improvement:.1f}% 向上！")
            elif improvement < 0:
                print(f"\n⚠️ 後退: {improvement:.1f}% 低下")
            else:
                print(f"\n➡️ 維持: 変化なし")
    
    def generate_daily_report(self):
        """日次レポート生成"""
        results = self.run_quality_assessment()
        self.save_history(results)
        self.show_progress_trend()
        
        # 改善提案
        print("\n💡 改善提案:")
        for category, data in results["categories"].items():
            if data["accuracy"] < 90:
                print(f"  🎯 {category}: {data['accuracy']:.1f}% - 改善が必要")
                
                # 失敗ケース分析
                failed_cases = [d for d in data["details"] if not d["success"]]
                if failed_cases:
                    print(f"    失敗ケース: {len(failed_cases)}件")
                    for case in failed_cases[:2]:  # 最初の2件表示
                        print(f"      - {case['sentence']}")

def main():
    """メイン実行"""
    print("🔍 Rephrase システム品質管理ツール")
    print("=" * 50)
    
    tracker = QualityTracker()
    tracker.generate_daily_report()
    
    print("\n📋 次のアクション:")
    print("  1. 失敗ケースを詳細分析")
    print("  2. 該当コードを修正")  
    print("  3. 再度このツールで検証")
    print("  4. 改善が確認できたら次のPhaseへ")

if __name__ == "__main__":
    main()
