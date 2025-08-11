# 開発アーカイブ分類表

## 保持予定（再利用・重要ファイル）
- pure_stanza_engine_v2.py         # 現在のStanza統合エンジン
- step18_complete_8slot.py          # Step18資産移植元
- Excel_Generator.py                # データ生成
- preset_config.json                # 設定
- rephrase_rules_v2.0.json         # ルール定義
- slot_order_data.json             # スロット順序
- V自動詞第1文型.json              # 文型データ
- 第3,4文型.json                   # 文型データ
- 例文入力元.xlsx                  # 正解データ
- 例文入力元_分解結果_v2_20250810_113552.xlsx # 正解データ

## アーカイブ対象（開発過程の作業ファイル）

### analysis_scripts/
- analyze_*.py系統（20個程度）
- check_*.py系統（15個程度）
- compare_*.py系統
- investigate_*.py系統

### test_scripts/ 
- test_*.py系統（15個程度）
- comprehensive_step_test.py
- fullset_tester.py

### debug_scripts/
- debug_*.py系統
- simple_*.py系統
- verify_*.py系統

### old_engines/
- step16_*, step17_*系統
- complete_spacy_rephrase_engine.py
- stanza_rephrase_hybrid.py
- universal_decompose_engine.py
- その他の古いエンジン

## 削除対象（一時デバッグファイル）
- __pycache__/ 
- .gitignore
