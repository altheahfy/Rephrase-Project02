"""
Phase 1 Universal Slot Position System - Integration Test
統一システムの動作確認と既存システムとの互換性テスト

Test Cases:
1. WhosePattern動作確認
2. PassivePattern動作確認  
3. UniversalSlotPositionManager統合テスト
4. 既存システムとの精度比較
"""

import sys
import os
import logging

# プロジェクトルートを追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 統一システムインポート
from universal_slot_system import UniversalSlotPositionManager
from universal_slot_system.patterns.whose_pattern import WhosePattern
from universal_slot_system.patterns.passive_pattern import PassivePattern

# 既存システムとの比較用
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

import stanza


class Phase1IntegrationTest:
    """Phase 1統合テストクラス"""
    
    def __init__(self):
        self.logger = logging.getLogger("Phase1Test")
        
        # ログ設定
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Stanza初期化
        try:
            self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
            self.logger.info("✅ Stanza初期化完了")
        except Exception as e:
            self.logger.error(f"❌ Stanza初期化エラー: {e}")
            return
            
        # 統一システム初期化
        self.universal_manager = UniversalSlotPositionManager()
        
        # パターン登録
        self._register_patterns()
        
        # 既存システム（比較用）
        self.legacy_mapper = UnifiedStanzaRephraseMapper()
        
        # テストケース
        self.test_sentences = [
            # whose構文テストケース
            "The man whose car is red lives here",
            "The woman whose dog runs fast works there",
            "The person whose house looks good stays nearby",
            
            # 受動態テストケース
            "The result was unexpected",
            "The plan was completed yesterday", 
            "The report was finished by the team",
            
            # 混合テストケース
            "The man whose car was damaged lives here",
        ]
        
    def _register_patterns(self):
        """パターン登録"""
        # WhosePattern登録
        whose_pattern = WhosePattern()
        success1 = self.universal_manager.register_pattern(
            "whose_ambiguous_verb", 
            whose_pattern, 
            priority=90
        )
        
        # PassivePattern登録
        passive_pattern = PassivePattern()
        success2 = self.universal_manager.register_pattern(
            "passive_voice", 
            passive_pattern, 
            priority=85
        )
        
        if success1 and success2:
            self.logger.info("✅ パターン登録完了")
        else:
            self.logger.error("❌ パターン登録失敗")
            
    def run_all_tests(self):
        """全テスト実行"""
        self.logger.info("🚀 Phase 1統合テスト開始")
        
        # 1. 個別パターンテスト
        self.test_whose_pattern()
        self.test_passive_pattern()
        
        # 2. 統合システムテスト
        self.test_universal_manager()
        
        # 3. 既存システムとの比較テスト
        self.test_compatibility()
        
        # 4. パフォーマンステスト
        self.test_performance()
        
        # 5. 統計出力
        self.output_statistics()
        
        self.logger.info("🏁 Phase 1統合テスト完了")
        
    def test_whose_pattern(self):
        """WhosePattern個別テスト"""
        self.logger.info("🧪 WhosePattern個別テスト開始")
        
        whose_pattern = WhosePattern()
        whose_sentences = [
            "The man whose car is red lives here",
            "The woman whose dog runs fast works there",
            "Regular sentence without whose clause"
        ]
        
        for sentence in whose_sentences:
            doc = self.nlp(sentence)
            words = doc.sentences[0].words if doc.sentences else []
            
            # 適用可能性チェック
            is_applicable = whose_pattern.is_applicable(sentence)
            self.logger.debug(f"📝 適用可能性 '{sentence}': {is_applicable}")
            
            if is_applicable:
                # パターン検出
                detection_result = whose_pattern.detect(words, sentence)
                self.logger.debug(f"🔍 検出結果: {detection_result.get('found', False)}")
                
                if detection_result.get('found', False):
                    # 修正適用
                    corrected_doc, metadata = whose_pattern.correct(doc, detection_result)
                    self.logger.debug(f"✅ 修正完了: {metadata}")
                    
    def test_passive_pattern(self):
        """PassivePattern個別テスト"""
        self.logger.info("🧪 PassivePattern個別テスト開始")
        
        passive_pattern = PassivePattern()
        passive_sentences = [
            "The result was unexpected",
            "The plan was completed yesterday",
            "The man is tall"  # 非受動態
        ]
        
        for sentence in passive_sentences:
            doc = self.nlp(sentence)
            words = doc.sentences[0].words if doc.sentences else []
            
            # 適用可能性チェック
            is_applicable = passive_pattern.is_applicable(sentence)
            self.logger.debug(f"📝 適用可能性 '{sentence}': {is_applicable}")
            
            if is_applicable:
                # パターン検出
                detection_result = passive_pattern.detect(words, sentence)
                self.logger.debug(f"🔍 検出結果: {detection_result.get('found', False)}")
                
                if detection_result.get('found', False):
                    # 修正適用
                    corrected_doc, metadata = passive_pattern.correct(doc, detection_result)
                    self.logger.debug(f"✅ 修正完了: {metadata}")
                    
    def test_universal_manager(self):
        """UniversalSlotPositionManager統合テスト"""
        self.logger.info("🧪 UniversalManager統合テスト開始")
        
        for sentence in self.test_sentences:
            self.logger.debug(f"🔄 処理中: '{sentence}'")
            
            doc = self.nlp(sentence)
            
            # 統一システムで処理
            processed_doc, metadata = self.universal_manager.process_all_patterns(doc, sentence)
            
            self.logger.debug(f"📊 処理結果: {metadata}")
            
            # 適用されたパターン数をチェック
            applied_patterns = metadata.get('patterns_applied', [])
            if applied_patterns:
                self.logger.info(f"✅ パターン適用: {applied_patterns}")
            else:
                self.logger.debug("📝 パターン未適用")
                
    def test_compatibility(self):
        """既存システムとの互換性テスト"""
        self.logger.info("🧪 既存システム互換性テスト開始")
        
        compatibility_results = []
        
        for sentence in self.test_sentences:
            self.logger.debug(f"🔄 互換性チェック: '{sentence}'")
            
            doc = self.nlp(sentence)
            
            # 既存システムでの処理
            try:
                legacy_result = self.legacy_mapper.process(sentence)
                legacy_corrections = getattr(legacy_result.get('stanza_doc'), 'human_grammar_corrections', {})
            except Exception as e:
                self.logger.warning(f"既存システムエラー: {e}")
                legacy_corrections = {}
                
            # 統一システムでの処理
            try:
                processed_doc, metadata = self.universal_manager.process_all_patterns(doc, sentence)
                universal_corrections = getattr(processed_doc, 'human_grammar_corrections', {})
            except Exception as e:
                self.logger.warning(f"統一システムエラー: {e}")
                universal_corrections = {}
                
            # 比較
            compatibility = {
                'sentence': sentence,
                'legacy_corrections_count': len(legacy_corrections),
                'universal_corrections_count': len(universal_corrections),
                'compatible': len(legacy_corrections) == len(universal_corrections)
            }
            
            compatibility_results.append(compatibility)
            self.logger.debug(f"📊 互換性: {compatibility}")
            
        # 互換性統計
        compatible_count = sum(1 for r in compatibility_results if r['compatible'])
        total_count = len(compatibility_results)
        compatibility_rate = compatible_count / total_count if total_count > 0 else 0
        
        self.logger.info(f"📊 互換性率: {compatibility_rate:.1%} ({compatible_count}/{total_count})")
        
    def test_performance(self):
        """パフォーマンステスト"""
        self.logger.info("🧪 パフォーマンステスト開始")
        
        import time
        
        # 統一システムの処理時間測定
        start_time = time.time()
        
        for _ in range(10):  # 10回実行
            for sentence in self.test_sentences:
                doc = self.nlp(sentence)
                self.universal_manager.process_all_patterns(doc, sentence)
                
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_sentence = total_time / (10 * len(self.test_sentences))
        
        self.logger.info(f"⚡ 平均処理時間: {avg_time_per_sentence*1000:.2f}ms/文")
        
    def output_statistics(self):
        """統計出力"""
        self.logger.info("📊 統計情報出力")
        
        # 処理統計
        stats = self.universal_manager.get_processing_stats()
        self.logger.info(f"📈 処理統計: {stats}")
        
        # 品質メトリクス
        quality_metrics = self.universal_manager.get_quality_metrics()
        self.logger.info(f"🎯 品質メトリクス: {quality_metrics}")
        
        # 登録パターン一覧
        registered_patterns = self.universal_manager.get_registered_patterns()
        self.logger.info(f"📋 登録パターン: {registered_patterns}")


if __name__ == "__main__":
    # テスト実行
    test = Phase1IntegrationTest()
    test.run_all_tests()
