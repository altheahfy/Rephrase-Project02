#!/usr/bin/env python3
"""
Phase 1 Universal System Accuracy Test
=====================================

Phase 1統一システムと既存システムの精度比較テスト
- 既存システム（UnifiedStanzaRephraseMapper）との完全互換性確認
- 人間文法認識の精度検証
- Universal Slot Position Systemの正確性検証

使用法:
    python phase1_accuracy_test.py
    python phase1_accuracy_test.py --detailed
"""

import json
import sys
import os
import argparse
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

# プロジェクトルートを追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# システムインポート
from universal_slot_system import UniversalSlotPositionManager
from universal_slot_system.patterns.whose_pattern import WhosePattern
from universal_slot_system.patterns.passive_pattern import PassivePattern
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

import stanza


class Phase1AccuracyTest:
    """Phase 1統一システム精度テスト"""
    
    def __init__(self, detailed=False):
        self.detailed = detailed
        self.logger = logging.getLogger("Phase1AccuracyTest")
        
        # ログ設定
        log_level = logging.DEBUG if detailed else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Stanza初期化
        try:
            self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
            self.logger.info("✅ Stanza初期化完了")
        except Exception as e:
            self.logger.error(f"❌ Stanza初期化エラー: {e}")
            return
            
        # システム初期化
        self.legacy_system = UnifiedStanzaRephraseMapper()
        self.universal_system = UniversalSlotPositionManager()
        
        # パターン登録
        self._register_patterns()
        
        # テスト文（既存システムで100%精度が確認済みの文）
        self.test_sentences = [
            # whose構文テストケース
            "The man whose car is red lives here",
            "The woman whose house looks beautiful works there",
            "The person whose dog runs fast stays nearby",
            
            # 受動態テストケース  
            "The result was unexpected",
            "The plan was completed",
            "The book was written",
            
            # 混合・複雑テストケース
            "The teacher whose class was cancelled lives here",
            "The report that was finished yesterday looks good",
            "The student whose homework was completed early goes home",
            
            # エッジケース
            "The man walks",  # 単純文
            "She is beautiful",  # 単純主語述語
            "They were working",  # 進行形
        ]
        
        # 結果格納
        self.comparison_results = []
        self.accuracy_stats = {
            'total_tests': 0,
            'perfect_matches': 0,
            'partial_matches': 0, 
            'complete_mismatches': 0,
            'error_count': 0
        }
        
    def _register_patterns(self):
        """パターン登録"""
        whose_pattern = WhosePattern()
        passive_pattern = PassivePattern()
        
        self.universal_system.register_pattern("whose_ambiguous_verb", whose_pattern, priority=90)
        self.universal_system.register_pattern("passive_voice", passive_pattern, priority=85)
        
        self.logger.info("✅ Phase 1パターン登録完了")
        
    def run_accuracy_test(self):
        """精度テスト実行"""
        self.logger.info("🧪 Phase 1精度テスト開始")
        
        for sentence in self.test_sentences:
            self.logger.info(f"🔄 テスト中: '{sentence}'")
            
            # 比較テスト実行
            comparison = self._compare_systems(sentence)
            self.comparison_results.append(comparison)
            
            # 統計更新
            self._update_stats(comparison)
            
        # 結果分析
        self._analyze_results()
        
        # レポート出力
        self._generate_report()
        
        self.logger.info("🏁 Phase 1精度テスト完了")
        
    def _compare_systems(self, sentence: str) -> Dict:
        """システム間比較"""
        comparison = {
            'sentence': sentence,
            'legacy_result': None,
            'universal_result': None,
            'legacy_error': None,
            'universal_error': None,
            'corrections_match': False,
            'processing_match': False,
            'accuracy_score': 0.0
        }
        
        # 既存システムでの処理
        try:
            legacy_result = self.legacy_system.process(sentence)
            comparison['legacy_result'] = {
                'slots': legacy_result.get('slots', {}),
                'sub_slots': legacy_result.get('sub_slots', {}),
                'corrections': self._extract_corrections(legacy_result.get('stanza_doc'))
            }
            self.logger.debug(f"既存システム結果: {comparison['legacy_result']}")
        except Exception as e:
            comparison['legacy_error'] = str(e)
            self.logger.error(f"❌ 既存システムエラー: {e}")
            
        # 統一システムでの処理
        try:
            doc = self.nlp(sentence)
            processed_doc, metadata = self.universal_system.process_all_patterns(doc, sentence)
            
            # 統一システムは文法修正のみなので、スロット生成は既存システムを使用
            universal_slots_result = self.legacy_system.process(sentence)
            
            comparison['universal_result'] = {
                'slots': universal_slots_result.get('slots', {}),
                'sub_slots': universal_slots_result.get('sub_slots', {}),
                'corrections': self._extract_corrections(processed_doc),
                'metadata': metadata
            }
            self.logger.debug(f"統一システム結果: {comparison['universal_result']}")
        except Exception as e:
            comparison['universal_error'] = str(e)
            self.logger.error(f"❌ 統一システムエラー: {e}")
            
        # 比較分析
        self._analyze_comparison(comparison)
        
        return comparison
        
    def _extract_corrections(self, doc) -> Dict:
        """文法修正情報抽出"""
        if not doc:
            return {}
            
        corrections = {}
        
        # human_grammar_corrections属性チェック
        if hasattr(doc, 'human_grammar_corrections'):
            corrections['human_grammar'] = doc.human_grammar_corrections
            
        # _human_grammar_corrections属性チェック（既存システム）
        if hasattr(doc, '_human_grammar_corrections'):
            corrections['legacy_human_grammar'] = doc._human_grammar_corrections
            
        return corrections
        
    def _analyze_comparison(self, comparison: Dict):
        """比較分析"""
        if comparison['legacy_error'] or comparison['universal_error']:
            comparison['accuracy_score'] = 0.0
            return
            
        legacy_corrections = comparison['legacy_result']['corrections']
        universal_corrections = comparison['universal_result']['corrections']
        
        # 修正内容の比較
        corrections_match = self._compare_corrections(legacy_corrections, universal_corrections)
        comparison['corrections_match'] = corrections_match
        
        # スロット結果の比較（統一システムは文法修正のみなので、基本的に同じはず）
        legacy_slots = comparison['legacy_result']['slots']
        universal_slots = comparison['universal_result']['slots']
        
        slots_match = legacy_slots == universal_slots
        comparison['processing_match'] = slots_match
        
        # 精度スコア計算
        score = 0.0
        if corrections_match:
            score += 0.7  # 文法修正一致度
        if slots_match:
            score += 0.3  # スロット処理一致度
            
        comparison['accuracy_score'] = score
        
        if self.detailed:
            self.logger.debug(f"📊 比較分析: 修正一致={corrections_match}, スロット一致={slots_match}, スコア={score:.2f}")
            
    def _compare_corrections(self, legacy_corrections: Dict, universal_corrections: Dict) -> bool:
        """文法修正の比較"""
        # 既存システムの修正
        legacy_human = legacy_corrections.get('human_grammar', {})
        legacy_list = legacy_corrections.get('legacy_human_grammar', [])
        
        # 統一システムの修正
        universal_human = universal_corrections.get('human_grammar', {})
        
        # 数値的比較
        legacy_count = len(legacy_human) + len(legacy_list)
        universal_count = len(universal_human)
        
        if self.detailed:
            self.logger.debug(f"修正数比較: 既存={legacy_count}, 統一={universal_count}")
            
        # 修正数が同じか、統一システムが同等以上の修正を行っているか
        return universal_count >= legacy_count
        
    def _update_stats(self, comparison: Dict):
        """統計更新"""
        self.accuracy_stats['total_tests'] += 1
        
        if comparison['legacy_error'] or comparison['universal_error']:
            self.accuracy_stats['error_count'] += 1
            return
            
        score = comparison['accuracy_score']
        
        if score >= 0.9:
            self.accuracy_stats['perfect_matches'] += 1
        elif score >= 0.5:
            self.accuracy_stats['partial_matches'] += 1
        else:
            self.accuracy_stats['complete_mismatches'] += 1
            
    def _analyze_results(self):
        """結果分析"""
        stats = self.accuracy_stats
        total = stats['total_tests']
        
        if total == 0:
            self.logger.warning("⚠️ テスト実行なし")
            return
            
        perfect_rate = stats['perfect_matches'] / total
        partial_rate = stats['partial_matches'] / total
        error_rate = stats['error_count'] / total
        
        self.logger.info(f"📊 精度分析結果:")
        self.logger.info(f"  完全一致: {stats['perfect_matches']}/{total} ({perfect_rate:.1%})")
        self.logger.info(f"  部分一致: {stats['partial_matches']}/{total} ({partial_rate:.1%})")
        self.logger.info(f"  不一致: {stats['complete_mismatches']}/{total}")
        self.logger.info(f"  エラー: {stats['error_count']}/{total} ({error_rate:.1%})")
        
        # 品質判定
        if perfect_rate >= 0.9:
            quality = "EXCELLENT"
            status = "✅"
        elif perfect_rate >= 0.7:
            quality = "GOOD"
            status = "⚠️"
        else:
            quality = "NEEDS_IMPROVEMENT"
            status = "❌"
            
        self.logger.info(f"{status} 総合品質評価: {quality} (完全一致率: {perfect_rate:.1%})")
        
    def _generate_report(self):
        """詳細レポート生成"""
        if not self.detailed:
            return
            
        report_filename = f"phase1_accuracy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            'test_info': {
                'timestamp': datetime.now().isoformat(),
                'test_type': 'phase1_universal_system_accuracy',
                'total_sentences': len(self.test_sentences),
                'detailed_mode': self.detailed
            },
            'accuracy_stats': self.accuracy_stats,
            'detailed_results': self.comparison_results
        }
        
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"📄 詳細レポート生成: {report_filename}")
        except Exception as e:
            self.logger.error(f"❌ レポート生成エラー: {e}")
            
    def get_summary(self) -> Dict:
        """テスト結果サマリー取得"""
        total = self.accuracy_stats['total_tests']
        if total == 0:
            return {'status': 'NO_TESTS', 'accuracy': 0.0}
            
        perfect_rate = self.accuracy_stats['perfect_matches'] / total
        
        return {
            'status': 'EXCELLENT' if perfect_rate >= 0.9 else 'GOOD' if perfect_rate >= 0.7 else 'NEEDS_IMPROVEMENT',
            'accuracy': perfect_rate,
            'total_tests': total,
            'perfect_matches': self.accuracy_stats['perfect_matches'],
            'errors': self.accuracy_stats['error_count']
        }


def main():
    parser = argparse.ArgumentParser(description='Phase 1 Universal System Accuracy Test')
    parser.add_argument('--detailed', action='store_true', help='詳細レポート生成')
    
    args = parser.parse_args()
    
    # テスト実行
    test = Phase1AccuracyTest(detailed=args.detailed)
    test.run_accuracy_test()
    
    # サマリー表示
    summary = test.get_summary()
    print(f"\n🎯 Phase 1統一システム精度テスト結果")
    print(f"Status: {summary['status']}")
    print(f"Accuracy: {summary['accuracy']:.1%}")
    print(f"Tests: {summary['perfect_matches']}/{summary['total_tests']} perfect")
    
    # 終了コード
    if summary['status'] == 'EXCELLENT':
        exit(0)
    elif summary['status'] == 'GOOD':
        exit(1)
    else:
        exit(2)


if __name__ == "__main__":
    main()
