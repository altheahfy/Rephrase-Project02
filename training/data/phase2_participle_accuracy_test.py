#!/usr/bin/env python3
"""
Phase 2 ParticiplePattern 精度テストシステム
==========================================

分詞構文処理の統一システム検証
- present participle (working, standing)
- past participle (written, spoken)
- compound participle (being reviewed)
- adjectival vs adverbial usage detection

予想改善効果: +7% (ロードマップ目標)
"""

import sys
import os
import json
import stanza
from datetime import datetime

# プロジェクトルートをパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Phase2テスト対象をインポート
sys.path.insert(0, os.path.join(project_root, 'training', 'data'))
from universal_slot_system.universal_manager import UniversalSlotPositionManager
from universal_slot_system.patterns.participle_pattern import ParticiplePattern
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper
import logging


class Phase2ParticipleTest:
    def __init__(self):
        self.setup_logging()
        
        # Stanza解析システム初期化
        print("🔧 Stanza英語モデル初期化中...")
        try:
            self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', use_gpu=False)
            print("✅ Stanza初期化完了")
            self.logger.info("✅ Stanza初期化完了")
        except Exception as e:
            print(f"⚠️ Stanza初期化エラー: {e}")
            self.nlp = None
            
        # システム初期化
        self.legacy_system = UnifiedStanzaRephraseMapper()
        self.universal_system = UniversalSlotPositionManager()
        self.participle_pattern = ParticiplePattern()
        
        # パターン登録
        self._register_patterns()
        
    def setup_logging(self):
        """ログ設定"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('Phase2ParticipleTest')
        
    def _register_patterns(self):
        """パターン登録 (Phase 1 + Phase 2)"""
        # Phase 1パターン
        from universal_slot_system.patterns.whose_pattern import WhosePattern
        from universal_slot_system.patterns.passive_pattern import PassivePattern
        from universal_slot_system.patterns.relative_clause_pattern import RelativeClausePattern
        
        whose_pattern = WhosePattern()
        passive_pattern = PassivePattern()
        relative_pattern = RelativeClausePattern()
        
        # Phase 2パターン  
        self.universal_system.register_pattern('whose_pattern', whose_pattern, priority=1)
        self.universal_system.register_pattern('passive_pattern', passive_pattern, priority=2)
        self.universal_system.register_pattern('relative_clause_pattern', relative_pattern, priority=3)
        self.universal_system.register_pattern('participle_pattern', self.participle_pattern, priority=4)
        
        # 分詞構文テスト例文（ロードマップから特定）
        self.test_sentences = [
            # 現在分詞（形容詞的用法）
            {
                "sentence": "The man working overtime is tired",
                "expected_pattern": "participle_clause",
                "focus": "present_participle_adjectival"
            },
            # 現在分詞（副詞的用法）
            {
                "sentence": "She stood quietly watching the sunset",
                "expected_pattern": "participle_clause", 
                "focus": "present_participle_adverbial"
            },
            # 過去分詞（形容詞的用法）
            {
                "sentence": "The book written carefully is popular",
                "expected_pattern": "participle_clause",
                "focus": "past_participle_adjectival"
            },
            # 複合分詞構文
            {
                "sentence": "The report being reviewed thoroughly needs changes",
                "expected_pattern": "participle_clause",
                "focus": "compound_participle"
            },
            # 現在分詞（動作説明）
            {
                "sentence": "Running quickly he caught the train",
                "expected_pattern": "participle_clause",
                "focus": "present_participle_action"
            },
            # 過去分詞（状態説明）
            {
                "sentence": "Broken completely the machine stopped working",
                "expected_pattern": "participle_clause",
                "focus": "past_participle_state"
            },
            # 複合パターン（being + 過去分詞）
            {
                "sentence": "The document being written now is important",
                "expected_pattern": "participle_clause",
                "focus": "being_participle"
            },
            # 分詞 + 副詞修飾
            {
                "sentence": "Standing silently in the corner he observed",
                "expected_pattern": "participle_clause",
                "focus": "participle_with_adverb"
            },
            # 過去分詞（受動的意味）
            {
                "sentence": "The letter sent yesterday arrived late",
                "expected_pattern": "participle_clause",
                "focus": "past_participle_passive"
            },
            # 現在分詞（能動的意味）
            {
                "sentence": "The dog barking loudly disturbed neighbors",
                "expected_pattern": "participle_clause",
                "focus": "present_participle_active"
            },
            # 複雑な分詞構文
            {
                "sentence": "Walking slowly through the park she enjoyed nature",
                "expected_pattern": "participle_clause",
                "focus": "complex_participle_adverbial"
            },
            # 分詞の連続使用
            {
                "sentence": "Working hard studying English he improved quickly",
                "expected_pattern": "participle_clause",
                "focus": "multiple_participles"
            }
        ]
        
        self.results = []
        
    def run_tests(self):
        """分詞構文テスト実行"""
        
        print("🔍 Phase 2 ParticiplePattern 精度テスト開始")
        print(f"📝 テスト例文数: {len(self.test_sentences)}")
        print("=" * 60)
        
        perfect_matches = 0
        
        for i, test_data in enumerate(self.test_sentences, 1):
            sentence = test_data["sentence"]
            expected_pattern = test_data["expected_pattern"]
            focus = test_data["focus"]
            
            print(f"\n🧪 テスト #{i}: {focus}")
            print(f"📄 例文: {sentence}")
            
            # 統一システムでの処理
            try:
                # Stanza解析
                if self.nlp:
                    analysis_doc = self.nlp(sentence)
                else:
                    analysis_doc = None
                    
                # Legacy system処理 (比較用)
                legacy_result = self.legacy_system.process(sentence)
                legacy_slots = legacy_result.get('slots', {}) if legacy_result else {}
                
                # Universal system処理 
                unified_result = self.universal_system.process_all_patterns(analysis_doc, sentence)
                
                if isinstance(unified_result, tuple) and len(unified_result) == 2:
                    unified_slots, confidence = unified_result
                else:
                    unified_slots = unified_result if unified_result else {}
                    confidence = 0.0
                    
                # ParticiplePattern特有の処理
                participle_detected = self.participle_pattern.detect(analysis_doc, sentence)
                participle_result = None
                if participle_detected:
                    participle_result = self.participle_pattern.correct(analysis_doc, sentence)
                
                # 結果評価
                evaluation = self._evaluate_result(
                    sentence, legacy_slots, unified_slots, participle_detected, 
                    participle_result, expected_pattern, focus
                )
                
                print(f"✅ 分詞検出: {'成功' if participle_detected else '失敗'}")
                # JSON serializable な形式でスロット表示
                unified_slots_json = {}
                if unified_slots:
                    for key, value in unified_slots.items():
                        if isinstance(value, str):
                            unified_slots_json[key] = value
                        else:
                            unified_slots_json[key] = str(value)
                            
                print(f"📊 統一スロット: {json.dumps(unified_slots_json, ensure_ascii=False, indent=2) if unified_slots_json else 'None'}")
                print(f"🎯 フォーカス評価: {evaluation['focus_score']}/10")
                print(f"📈 総合評価: {evaluation['overall_grade']}")
                
                if evaluation['is_perfect']:
                    perfect_matches += 1
                    print("🌟 完全一致!")
                
                self.results.append({
                    "test_id": i,
                    "sentence": sentence,
                    "focus": focus,
                    "legacy_slots": legacy_slots,
                    "unified_slots": unified_slots,
                    "participle_detected": participle_detected,
                    "participle_result": participle_result,
                    "evaluation": evaluation
                })
                
            except Exception as e:
                print(f"❌ エラー: {str(e)}")
                self.results.append({
                    "test_id": i,
                    "sentence": sentence,
                    "focus": focus,
                    "error": str(e),
                    "evaluation": {"is_perfect": False, "overall_grade": "FAILED"}
                })
        
        # 最終結果表示
        self._display_final_results(perfect_matches)
        
        # 結果保存
        self._save_results()
        
    def _evaluate_result(self, sentence, legacy_slots, unified_slots, participle_detected, 
                        participle_result, expected_pattern, focus):
        """結果評価ロジック"""
        
        evaluation = {
            "is_perfect": False,
            "focus_score": 0,
            "overall_grade": "FAILED",
            "details": {}
        }
        
        # 1. 分詞検出の精度 (30%)
        if participle_detected:
            evaluation["focus_score"] += 3
            evaluation["details"]["detection"] = "✅"
        else:
            evaluation["details"]["detection"] = "❌"
        
        # 2. 統一システムとの統合 (40%)
        if unified_slots and isinstance(unified_slots, dict):
            if any(slot for slot in unified_slots.values() if slot):
                evaluation["focus_score"] += 4
                evaluation["details"]["integration"] = "✅"
            else:
                evaluation["details"]["integration"] = "⚠️"
        else:
            evaluation["details"]["integration"] = "❌"
            
        # 3. 分詞特有の処理結果 (30%)
        if participle_result and isinstance(participle_result, tuple):
            enhanced_slots, confidence = participle_result
            if (enhanced_slots and 'sub_slots' in enhanced_slots and 
                'participle_clause' in enhanced_slots.get('sub_slots', {})):
                evaluation["focus_score"] += 3
                evaluation["details"]["participle_processing"] = "✅"
            else:
                evaluation["details"]["participle_processing"] = "⚠️"
        else:
            evaluation["details"]["participle_processing"] = "❌"
        
        # 総合評価
        if evaluation["focus_score"] >= 9:
            evaluation["overall_grade"] = "EXCELLENT"
            evaluation["is_perfect"] = True
        elif evaluation["focus_score"] >= 7:
            evaluation["overall_grade"] = "GOOD"
        elif evaluation["focus_score"] >= 5:
            evaluation["overall_grade"] = "FAIR"
        else:
            evaluation["overall_grade"] = "POOR"
            
        return evaluation
    
    def _display_final_results(self, perfect_matches):
        """最終結果表示"""
        
        total_tests = len(self.test_sentences)
        success_rate = (perfect_matches / total_tests) * 100
        
        print("\n" + "=" * 60)
        print("📊 **Phase 2 ParticiplePattern テスト結果サマリー**")
        print("=" * 60)
        print(f"✅ 完全一致: {perfect_matches}/{total_tests} ({success_rate:.1f}%)")
        
        # 品質評価
        if success_rate >= 90:
            quality_rating = "🌟 EXCELLENT (Phase 2 目標達成!)"
        elif success_rate >= 80:
            quality_rating = "✅ GOOD (改善の余地あり)"
        elif success_rate >= 70:
            quality_rating = "⚠️ FAIR (要改善)"
        else:
            quality_rating = "❌ POOR (大幅な改善が必要)"
            
        print(f"🎯 総合品質評価: {quality_rating}")
        
        # フォーカス別分析
        focus_analysis = {}
        for result in self.results:
            if 'focus' in result:
                focus = result['focus']
                if focus not in focus_analysis:
                    focus_analysis[focus] = {'total': 0, 'success': 0}
                focus_analysis[focus]['total'] += 1
                if result.get('evaluation', {}).get('is_perfect', False):
                    focus_analysis[focus]['success'] += 1
        
        print("\n📋 フォーカス別パフォーマンス:")
        for focus, stats in focus_analysis.items():
            rate = (stats['success'] / stats['total']) * 100
            print(f"  • {focus}: {stats['success']}/{stats['total']} ({rate:.0f}%)")
        
        print("\n🎯 Phase 2 次期展開: AdverbialPattern実装準備完了")
        
    def _save_results(self):
        """結果をJSONファイルに保存"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase2_participle_accuracy_report_{timestamp}.json"
        filepath = os.path.join(project_root, "training", "data", filename)
        
        report_data = {
            "test_info": {
                "timestamp": timestamp,
                "phase": "Phase 2 - ParticiplePattern",
                "test_count": len(self.test_sentences),
                "focus": "participle_clause_integration"
            },
            "accuracy_stats": {
                "total_tests": len(self.test_sentences),
                "perfect_matches": sum(1 for r in self.results if r.get('evaluation', {}).get('is_perfect', False)),
                "partial_matches": 0,  # Phase 2では完全一致のみカウント
                "complete_mismatches": sum(1 for r in self.results if not r.get('evaluation', {}).get('is_perfect', False)),
                "error_count": sum(1 for r in self.results if 'error' in r)
            },
            "detailed_results": self.results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
            
        print(f"\n💾 詳細レポート保存: {filename}")


if __name__ == "__main__":
    test_system = Phase2ParticipleTest()
    test_system.run_tests()
