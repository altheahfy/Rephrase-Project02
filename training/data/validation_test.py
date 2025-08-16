#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正解データとの照合テスト
expected_results_progress.jsonとシステム出力を完全照合
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class ValidationTester:
    def __init__(self):
        """ValidationTester初期化"""
        self.setup_logging()
        self.system = UnifiedStanzaRephraseMapper()
        
        # 4ハンドラー追加
        self.system.add_handler('basic_five_pattern')
        self.system.add_handler('relative_clause')
        self.system.add_handler('passive_voice')
        self.system.add_handler('adverbial_modifier')
        
        self.expected_data = self.load_expected_results()
        
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('validation_test.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_expected_results(self) -> Dict:
        """正解データ読み込み"""
        try:
            with open('expected_results_progress.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"✅ 正解データ読み込み完了: {len(data['correct_answers'])}件")
            return data['correct_answers']
        except Exception as e:
            self.logger.error(f"❌ 正解データ読み込みエラー: {e}")
            return {}
    
    def normalize_slots(self, slots: Dict) -> Dict:
        """スロット正規化（比較用）"""
        if not slots:
            return {}
        
        normalized = {}
        for key, value in slots.items():
            if value is not None and value != "":
                # 空白の正規化
                normalized[key] = str(value).strip()
        
        return normalized
    
    def compare_results(self, expected: Dict, actual: Dict) -> Dict:
        """結果比較"""
        comparison = {
            'main_slots_match': True,
            'sub_slots_match': True,
            'main_slots_diff': {},
            'sub_slots_diff': {},
            'score': 0.0
        }
        
        # メインスロット比較（expected: main_slots, actual: slots）
        expected_main = self.normalize_slots(expected.get('main_slots', {}))
        actual_main = self.normalize_slots(actual.get('slots', {}))
        
        # メインスロット差分チェック
        all_main_keys = set(expected_main.keys()) | set(actual_main.keys())
        main_matches = 0
        
        for key in all_main_keys:
            exp_val = expected_main.get(key, "")
            act_val = actual_main.get(key, "")
            
            if exp_val == act_val:
                main_matches += 1
            else:
                comparison['main_slots_match'] = False
                comparison['main_slots_diff'][key] = {
                    'expected': exp_val,
                    'actual': act_val
                }
        
        # サブスロット比較（both use sub_slots）
        expected_sub = self.normalize_slots(expected.get('sub_slots', {}))
        actual_sub = self.normalize_slots(actual.get('sub_slots', {}))
        
        all_sub_keys = set(expected_sub.keys()) | set(actual_sub.keys())
        sub_matches = 0
        
        for key in all_sub_keys:
            exp_val = expected_sub.get(key, "")
            act_val = actual_sub.get(key, "")
            
            if exp_val == act_val:
                sub_matches += 1
            else:
                comparison['sub_slots_match'] = False
                comparison['sub_slots_diff'][key] = {
                    'expected': exp_val,
                    'actual': act_val
                }
        
        # スコア計算
        total_slots = len(all_main_keys) + len(all_sub_keys)
        if total_slots > 0:
            comparison['score'] = (main_matches + sub_matches) / total_slots
        else:
            comparison['score'] = 1.0
            
        return comparison
    
    def run_validation(self) -> Dict:
        """バリデーション実行"""
        print("🔍 正解データとの照合テスト開始")
        print("=" * 60)
        
        results = {
            'total_tests': 0,
            'perfect_matches': 0,
            'partial_matches': 0,
            'failed_tests': 0,
            'total_score': 0.0,
            'detailed_results': {}
        }
        
        for test_id, expected_data in self.expected_data.items():
            if 'expected' not in expected_data:
                continue
                
            sentence = expected_data['sentence']
            expected_result = expected_data['expected']
            
            print(f"\n🧪 テスト {test_id}: {sentence}")
            print("-" * 50)
            
            # システム実行
            start_time = time.time()
            try:
                actual_result = self.system.process(sentence)
                process_time = time.time() - start_time
                
                # None チェック
                if actual_result is None:
                    print("❌ システムエラー: None result returned")
                    results['failed_tests'] += 1
                    results['total_tests'] += 1
                    continue
                
                # 結果比較
                comparison = self.compare_results(expected_result, actual_result)
                
                # 結果分類
                if comparison['score'] == 1.0:
                    results['perfect_matches'] += 1
                    status = "✅ 完全一致"
                elif comparison['score'] > 0.0:
                    results['partial_matches'] += 1
                    status = f"⚠️  部分一致 ({comparison['score']:.2%})"
                else:
                    results['failed_tests'] += 1
                    status = "❌ 不一致"
                
                print(f"⏱️  処理時間: {process_time:.3f}秒")
                print(f"📊 {status}")
                
                # 差分表示
                if comparison['main_slots_diff']:
                    print("🔍 メインスロット差分:")
                    for key, diff in comparison['main_slots_diff'].items():
                        print(f"  {key}: 期待値='{diff['expected']}' vs 実際='{diff['actual']}'")
                
                if comparison['sub_slots_diff']:
                    print("🔍 サブスロット差分:")
                    for key, diff in comparison['sub_slots_diff'].items():
                        print(f"  {key}: 期待値='{diff['expected']}' vs 実際='{diff['actual']}'")
                
                # 詳細結果保存
                results['detailed_results'][test_id] = {
                    'sentence': sentence,
                    'expected': expected_result,
                    'actual': actual_result,
                    'comparison': comparison,
                    'process_time': process_time
                }
                
                results['total_score'] += comparison['score']
                results['total_tests'] += 1
                
            except Exception as e:
                print(f"❌ システムエラー: {e}")
                results['failed_tests'] += 1
                results['total_tests'] += 1
        
        # 最終統計
        if results['total_tests'] > 0:
            average_score = results['total_score'] / results['total_tests']
        else:
            average_score = 0.0
            
        print("\n" + "=" * 60)
        print("📈 最終統計:")
        print(f"  総テスト数: {results['total_tests']}")
        print(f"  完全一致: {results['perfect_matches']}")
        print(f"  部分一致: {results['partial_matches']}")
        print(f"  不一致: {results['failed_tests']}")
        print(f"  平均スコア: {average_score:.2%}")
        print(f"  正解率: {results['perfect_matches']}/{results['total_tests']} = {results['perfect_matches']/results['total_tests']*100:.1f}%")
        
        return results

def main():
    """メイン関数"""
    try:
        tester = ValidationTester()
        results = tester.run_validation()
        
        # 結果保存
        with open('validation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print("\n🎉 バリデーションテスト完了！")
        print("📁 詳細結果は validation_results.json に保存されました")
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
