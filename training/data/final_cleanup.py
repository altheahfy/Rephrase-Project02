#!/usr/bin/env python3
"""
Final Cleanup - Phase 2
本当に必要なファイルのみ残す最終整理
"""
import os
import shutil
from pathlib import Path

def final_cleanup():
    """最終整理の実行"""
    base_path = Path(".")
    
    print("🔥 FINAL CLEANUP - Phase 2")
    print("=" * 50)
    
    # 作業完了後に不要になったファイル
    completed_work_files = [
        "file_cleanup.py",                      # 整理作業完了
        "comprehensive_grammar_test.py",        # テスト完了（結果は引き継ぎ書に記載済み）
        "individual_vs_coordination_test.py",   # 理論矛盾検証完了
        "multi_engine_test_final.py",           # 協調システムテスト完了
        "coordination_strategy_test.py",        # 協調戦略テスト完了
        "boundary_expansion_integration_test.py", # 統合テスト完了
        "grammar_coverage_calculator.py",       # カバレッジ計算完了
        "ファイル整理完了レポート_2025-08-13.md", # 一時レポート
    ]
    
    # ドキュメント類で統合可能なもの  
    redundant_docs = [
        "ACTIVE_ENGINE_LIST.md",               # 仕様書に統合済み
        "GRAMMAR_COVERAGE_ANALYSIS.md",        # 引き継ぎ書に統合済み  
        "QUESTION_ENGINE_SPECIFICATION.md",    # エンジン固有仕様（不要）
        "GRAMMAR_PATTERN_IMPLEMENTATION_PLAN.md", # 実装完了（不要）
        "引き継ぎ書_2025-08-12_Modal_Engine_完全統合.md", # 古い引き継ぎ書
    ]
    
    # データファイルで使われていないもの
    unused_data_files = [
        "V自動詞第1文型.json",                # 使用確認できず
        "第3,4文型.json",                      # 使用確認できず  
        "絶対順序考察.xlsx",                   # 考察完了
        "（小文字化した最初の5文型フルセット）例文入力元.xlsx", # 開発時のみ使用
        "（第4文型）例文入力元.xlsx",          # 開発時のみ使用
        "例文入力元.xlsx",                     # 開発時のみ使用
        "Excel_Generator.py",                  # Excel生成（開発時のみ）
    ]
    
    # フェーズ2アーカイブディレクトリ作成
    phase2_archive = Path("final_cleanup_archive_2025-08-13")
    if not phase2_archive.exists():
        phase2_archive.mkdir()
        print(f"📁 Created Phase 2 archive directory: {phase2_archive}")
    
    total_moved = 0
    
    # 1. 作業完了ファイルをアーカイブ
    print("\n✅ Archiving completed work files...")
    for file in completed_work_files:
        if Path(file).exists():
            shutil.move(file, phase2_archive / file)
            print(f"   📦 Moved: {file}")
            total_moved += 1
        else:
            print(f"   ⚠️  Not found: {file}")
    
    # 2. 冗長なドキュメントをアーカイブ
    print("\n📚 Archiving redundant documentation...")
    for file in redundant_docs:
        if Path(file).exists():
            shutil.move(file, phase2_archive / file)
            print(f"   📦 Moved: {file}")
            total_moved += 1
    
    # 3. 未使用データファイルをアーカイブ
    print("\n📊 Archiving unused data files...")
    for file in unused_data_files:
        if Path(file).exists():
            shutil.move(file, phase2_archive / file)
            print(f"   📦 Moved: {file}")
            total_moved += 1
    
    print(f"\n🎯 ESSENTIAL FILES REMAINING:")
    
    essential_files = {
        "Core System": [
            "grammar_master_controller_v2.py",
            "boundary_expansion_lib.py", 
            "sublevel_pattern_lib.py"
        ],
        "Configuration": [
            "preset_config.json",
            "rephrase_rules_v2.0.json",
            "slot_order_data.json"
        ],
        "Documentation": [
            "引き継ぎ書_2025-08-13_エンジン選択ロジック修正.md",
            "specifications/文要素分解システム設計仕様書_v2.0_Ultimate.md",
            "README.md"
        ],
        "Development": [
            "development_archive/",
            "docs/",
            "monitoring/"
        ]
    }
    
    for category, files in essential_files.items():
        print(f"\n📂 {category}:")
        for file in files:
            if Path(file).exists():
                print(f"   ✅ {file}")
            else:
                print(f"   ⚠️  Missing: {file}")
    
    print(f"\n🔥 Final cleanup completed!")
    print(f"📦 Additional {total_moved} files archived")
    print(f"🎯 System now contains ONLY essential files")
    
    # engines フォルダの状況確認
    engines_path = Path("engines")
    if engines_path.exists():
        engine_files = [f for f in engines_path.iterdir() if f.is_file() and f.suffix == ".py"]
        print(f"\n⚙️  Active engines: {len(engine_files)} files")
        for engine in sorted(engine_files):
            print(f"   ✅ {engine.name}")

if __name__ == "__main__":
    final_cleanup()
