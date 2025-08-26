#!/usr/bin/env python3
"""
File Cleanup and Organization Script
古いバージョン・テスト用一時ファイル・不要ファイルの整理
"""
import os
import shutil
from pathlib import Path

def organize_files():
    """ファイル整理の実行"""
    base_path = Path(".")
    
    print("🧹 File Cleanup and Organization")
    print("=" * 50)
    
    # 1. 古いバージョンファイル
    old_versions = [
        "grammar_master_controller.py",  # v1 (古いバージョン)
        "grammar_master_controller_v2_no_phase2.py",  # 不要バージョン
        "multi_engine_coordination_v3.py",  # 古い協調システム
        "multi_engine_coordinator_fix.py",  # 修正版（統合済み）
    ]
    
    # 2. テスト・デバッグ用一時ファイル
    test_temp_files = [
        "architecture_analysis.py",
        "comparison_analysis.py", 
        "concrete_comparison_demo.py",
        "corrected_coverage_analysis.py",
        "current_system_test.py",
        "debug_slot_processing.py",
        "debug_sublevel_pattern_lib.py",
        "debug_test.py",
        "engine_coverage_analysis.py",
        "engine_responsibility_clarification.py",
        "engine_selection_debug.py",
        "enhancement_roadmap.py",
        "integration_status_analysis.py",
        "integration_test.py",
        "missing_structure_analysis.py",
        "multi_sentence_analysis.py",
        "phase1_slot_specific_expansion_test.py",
        "phase2_sublevel_pattern_test.py",
        "pure_stanza_components_analysis.py",
        "pure_stanza_migration_analysis.py",
        "real_coverage_tester.py",
        "real_usage_frequency_calculator.py",
        "slot_verification.py",
        "sublevel_pattern_placement_analysis.py",
        "test_enhanced_engine.py",
        "test_question_complete.py",
        "test_question_corrected.py",
        "test_question_detailed.py",
        "test_question_integration.py",
        "verify_actual_capabilities.py",
    ]
    
    # 3. 結果・ログファイル
    result_files = [
        "phase2_sublevel_integration_results.json",
        "ultimate_grammar_engine.log",
    ]
    
    # 4. Engines内の古いファイル
    engine_old_files = [
        "engines/simple_relative_engine_old.py",
        "engines/simple_relative_engine_unified.py", 
        "engines/stanza_based_conjunction_engine_old.py",
        "engines/stanza_based_conjunction_engine_unified.py",
        "engines/basic_five_pattern_engine_enhanced.py",  # 統合済み
        "engines/pure_stanza_engine_v3_1_unified.py",  # 古いシステム
        "engines/test_boundary_effects.py",  # テストファイル
    ]
    
    # アーカイブディレクトリ作成
    archive_dir = Path("cleanup_archive_2025-08-13")
    if not archive_dir.exists():
        archive_dir.mkdir()
        print(f"📁 Created archive directory: {archive_dir}")
    
    # 1. 古いバージョンファイルをアーカイブ
    print("\n🗂️  Archiving old version files...")
    for file in old_versions:
        if Path(file).exists():
            shutil.move(file, archive_dir / file)
            print(f"   ✅ Moved: {file} → archive")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    # 2. テスト・デバッグファイルをアーカイブ
    print("\n🧪 Archiving test/debug files...")
    for file in test_temp_files:
        if Path(file).exists():
            shutil.move(file, archive_dir / file)
            print(f"   ✅ Moved: {file} → archive")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    # 3. 結果・ログファイルをアーカイブ
    print("\n📊 Archiving result/log files...")
    for file in result_files:
        if Path(file).exists():
            shutil.move(file, archive_dir / file)
            print(f"   ✅ Moved: {file} → archive")
    
    # 4. Engines内の古いファイルをアーカイブ
    print("\n⚙️  Archiving old engine files...")
    engine_archive = archive_dir / "engines"
    if not engine_archive.exists():
        engine_archive.mkdir()
    
    for file in engine_old_files:
        if Path(file).exists():
            filename = Path(file).name
            shutil.move(file, engine_archive / filename)
            print(f"   ✅ Moved: {file} → archive/engines/")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    # 5. __pycache__ フォルダのクリーンアップ
    print("\n🧽 Cleaning __pycache__ directories...")
    for pycache in Path(".").rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"   ✅ Removed: {pycache}")
    
    print("\n📋 Current active files after cleanup:")
    important_files = [
        "grammar_master_controller_v2.py",  # メインコントローラ
        "boundary_expansion_lib.py",        # 境界拡張ライブラリ  
        "sublevel_pattern_lib.py",          # サブレベルパターンライブラリ
        "comprehensive_grammar_test.py",    # 包括テストスイート
        "individual_vs_coordination_test.py", # 理論矛盾検証
        "multi_engine_test_final.py",       # マルチエンジンテスト
        "引き継ぎ書_2025-08-13_エンジン選択ロジック修正.md",  # 最新引き継ぎ書
    ]
    
    for file in important_files:
        if Path(file).exists():
            print(f"   ✅ Active: {file}")
        else:
            print(f"   ⚠️  Missing: {file}")
    
    print(f"\n🎉 Cleanup completed! Archived {len(old_versions + test_temp_files + result_files + engine_old_files)} files")
    print(f"📁 Archive location: {archive_dir.absolute()}")

if __name__ == "__main__":
    organize_files()
