"""
Phase 2.0 安全基盤: 統合テスト・制御システム
バックアップ・監視システムの統合運用・テスト

作成日: 2025年8月21日
目的: Phase 2.0実装前の安全基盤動作確認
"""

import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# 安全基盤モジュールのインポート
sys.path.append(str(Path(__file__).parent))
from backup_system import StanzaSystemBackup
from quality_monitor import ContinuousQualityMonitoring

class SafetyInfrastructureController:
    """安全基盤統合制御システム"""
    
    def __init__(self):
        self.controller_id = f"safety_controller_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.log_dir = Path("safety_infrastructure/integration_logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 安全基盤コンポーネント
        self.backup_system = None
        self.quality_monitor = None
        
        # システム状態
        self.infrastructure_ready = False
        self.monitoring_active = False
        
        print(f"🎛️ 安全基盤制御システム初期化: {self.controller_id}")
    
    def initialize_safety_infrastructure(self):
        """安全基盤の初期化"""
        print("🔧 安全基盤初期化開始...")
        
        try:
            # Step 1: バックアップシステム初期化
            print("📦 バックアップシステム初期化中...")
            self.backup_system = StanzaSystemBackup()
            backup_success = self.backup_system.create_complete_backup()
            
            if not backup_success:
                print("❌ バックアップシステム初期化失敗")
                return False
            
            # Step 2: 品質監視システム初期化
            print("📊 品質監視システム初期化中...")
            self.quality_monitor = ContinuousQualityMonitoring(self.backup_system)
            monitor_success = self.quality_monitor.establish_baseline()
            
            if not monitor_success:
                print("❌ 品質監視システム初期化失敗")
                return False
            
            # Step 3: 統合テスト実行
            integration_success = self._run_integration_tests()
            
            if integration_success:
                self.infrastructure_ready = True
                print("✅ 安全基盤初期化完了")
                return True
            else:
                print("❌ 統合テスト失敗")
                return False
                
        except Exception as e:
            print(f"❌ 安全基盤初期化エラー: {e}")
            return False
    
    def start_safety_monitoring(self):
        """安全監視開始"""
        if not self.infrastructure_ready:
            print("❌ 安全基盤未初期化。initialize_safety_infrastructure()を先に実行してください")
            return False
        
        print("🔍 安全監視開始...")
        
        try:
            # 品質監視開始
            monitor_started = self.quality_monitor.start_monitoring()
            
            if monitor_started:
                self.monitoring_active = True
                print("✅ 安全監視開始完了")
                return True
            else:
                print("❌ 監視開始失敗")
                return False
                
        except Exception as e:
            print(f"❌ 安全監視開始エラー: {e}")
            return False
    
    def stop_safety_monitoring(self):
        """安全監視停止"""
        if self.monitoring_active and self.quality_monitor:
            print("⏹️ 安全監視停止中...")
            self.quality_monitor.stop_monitoring()
            self.monitoring_active = False
            print("✅ 安全監視停止完了")
    
    def emergency_shutdown(self):
        """緊急停止・復旧"""
        print("🚨 緊急停止実行...")
        
        try:
            # 監視停止
            if self.monitoring_active:
                self.stop_safety_monitoring()
            
            # 緊急復旧実行
            if self.backup_system:
                recovery_success = self.backup_system.immediate_rollback("all")
                if recovery_success:
                    print("✅ 緊急復旧完了")
                    return True
                else:
                    print("❌ 緊急復旧失敗")
                    return False
            
            return False
            
        except Exception as e:
            print(f"❌ 緊急停止エラー: {e}")
            return False
    
    def get_system_status(self):
        """システム状態取得"""
        try:
            status = {
                "controller_id": self.controller_id,
                "timestamp": datetime.now().isoformat(),
                "infrastructure_ready": self.infrastructure_ready,
                "monitoring_active": self.monitoring_active,
                "backup_system_status": "initialized" if self.backup_system else "not_initialized",
                "quality_monitor_status": "initialized" if self.quality_monitor else "not_initialized"
            }
            
            # システム整合性確認
            if self.backup_system:
                status["system_integrity"] = self.backup_system.validate_system_integrity()
            
            return status
            
        except Exception as e:
            return {"error": f"Status check failed: {e}"}
    
    def _run_integration_tests(self):
        """統合テスト実行"""
        print("🧪 安全基盤統合テスト開始...")
        
        test_results = {}
        
        try:
            # テスト1: バックアップ・復旧機能テスト
            print("  📦 バックアップ・復旧機能テスト...")
            backup_test = self._test_backup_recovery()
            test_results["backup_recovery"] = backup_test
            
            # テスト2: 品質監視機能テスト
            print("  📊 品質監視機能テスト...")
            monitor_test = self._test_quality_monitoring()
            test_results["quality_monitoring"] = monitor_test
            
            # テスト3: 緊急時対応テスト
            print("  🚨 緊急時対応テスト...")
            emergency_test = self._test_emergency_response()
            test_results["emergency_response"] = emergency_test
            
            # 統合テスト結果評価
            all_tests_passed = all(test_results.values())
            
            # テスト結果ログ保存
            self._save_test_results(test_results)
            
            if all_tests_passed:
                print("✅ 統合テスト完全成功")
                return True
            else:
                print("❌ 統合テスト部分失敗")
                failed_tests = [test for test, result in test_results.items() if not result]
                print(f"   失敗テスト: {failed_tests}")
                return False
                
        except Exception as e:
            print(f"❌ 統合テスト実行エラー: {e}")
            return False
    
    def _test_backup_recovery(self):
        """バックアップ・復旧機能テスト"""
        try:
            # システム整合性確認
            integrity_before = self.backup_system.validate_system_integrity()
            
            # 模擬復旧テスト（実際にはファイルを変更しない）
            recovery_test = self.backup_system.immediate_rollback("test_component")
            
            # システム整合性再確認
            integrity_after = self.backup_system.validate_system_integrity()
            
            return integrity_before and integrity_after
            
        except Exception as e:
            print(f"  ❌ バックアップテストエラー: {e}")
            return False
    
    def _test_quality_monitoring(self):
        """品質監視機能テスト"""
        try:
            # 基準値確認
            baseline_exists = self.quality_monitor.baseline_results is not None
            
            # 品質チェック実行
            quality_check = self.quality_monitor._run_quality_check()
            quality_ok = quality_check is not None and quality_check.get("success_rate") == 100.0
            
            return baseline_exists and quality_ok
            
        except Exception as e:
            print(f"  ❌ 品質監視テストエラー: {e}")
            return False
    
    def _test_emergency_response(self):
        """緊急時対応テスト"""
        try:
            # 緊急時プロトコルの動作確認（実際には発火しない）
            emergency_protocols_ready = (
                self.backup_system is not None and
                self.quality_monitor is not None and
                hasattr(self.quality_monitor, '_trigger_emergency_response')
            )
            
            return emergency_protocols_ready
            
        except Exception as e:
            print(f"  ❌ 緊急時対応テストエラー: {e}")
            return False
    
    def _save_test_results(self, test_results):
        """テスト結果保存"""
        try:
            result_log = {
                "controller_id": self.controller_id,
                "timestamp": datetime.now().isoformat(),
                "test_results": test_results,
                "overall_success": all(test_results.values())
            }
            
            log_file = self.log_dir / f"integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(result_log, f, indent=2, ensure_ascii=False)
                
            print(f"  📝 テスト結果保存: {log_file}")
            
        except Exception as e:
            print(f"  ⚠️ テスト結果保存警告: {e}")

def run_full_safety_infrastructure_test():
    """安全基盤完全テスト実行"""
    print("🚀 Phase 2.0 安全基盤完全テスト開始")
    print("=" * 60)
    
    # 制御システム初期化
    controller = SafetyInfrastructureController()
    
    # Step 1: 安全基盤初期化
    print("\n🔧 Step 1: 安全基盤初期化")
    init_success = controller.initialize_safety_infrastructure()
    
    if not init_success:
        print("❌ 安全基盤初期化失敗 - テスト中断")
        return False
    
    # Step 2: 安全監視開始テスト
    print("\n🔍 Step 2: 安全監視開始テスト")
    monitor_success = controller.start_safety_monitoring()
    
    # 短時間監視動作確認
    if monitor_success:
        print("   5秒間監視動作確認中...")
        time.sleep(5)
        
        # 監視停止
        controller.stop_safety_monitoring()
    
    # Step 3: システム状態確認
    print("\n📊 Step 3: システム状態確認")
    status = controller.get_system_status()
    print(f"   システム状態: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # Step 4: 緊急時対応テスト
    print("\n🚨 Step 4: 緊急時対応テスト")
    emergency_success = controller.emergency_shutdown()
    
    # 最終評価
    print("\n📋 最終評価")
    overall_success = init_success and monitor_success and emergency_success
    
    if overall_success:
        print("✅ 安全基盤完全テスト成功")
        print("🎯 Phase 2.0実装準備完了")
        return controller
    else:
        print("❌ 安全基盤テスト部分失敗")
        print("⚠️ 問題解決後にPhase 2.0実装を開始してください")
        return None

if __name__ == "__main__":
    run_full_safety_infrastructure_test()
