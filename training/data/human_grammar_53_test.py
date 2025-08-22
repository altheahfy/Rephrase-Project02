#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人間文法認識システム専用テスト（53例文版）- 統一形式対応

このスクリプトは人間文法認識システムのみを使って53例文を処理し、
既存のcompare_results.pyで検証可能な統一形式で結果を出力します。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# プロジェクトルートを設定
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

def run_human_grammar_batch_test():
    """人間文法認識システムで53例文をバッチ処理（統一形式）"""
    
    print("=" * 70)
    print("🧠 人間文法認識システム専用バッチテスト（統一形式）")
    print("=" * 70)
    
    # 53例文のテストデータをロード
    test_data_path = project_root / "final_test_system" / "final_54_test_data.json"
    if not test_data_path.exists():
        print(f"❌ テストデータが見つかりません: {test_data_path}")
        return
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # データ構造を変換
    test_sentences = []
    for key, test_case in raw_data['data'].items():
        test_sentences.append(test_case['sentence'])
    
    print(f"📝 テスト対象文数: {len(test_sentences)}")
    print()
    
    # マッパーを初期化（人間専用テストモード）
    mapper = UnifiedStanzaRephraseMapper(test_mode='human_only')
    
    # バッチ処理実行
    batch_results = []
    start_time = datetime.now()
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"🔍 処理中 {i:2d}/{len(test_sentences)}: {sentence}")
        
        try:
            # 人間文法認識のみで処理
            result = mapper.process(sentence)
            
            # 統一形式に変換（既存システムと同じ形式）
            batch_result = {
                'sentence': sentence,
                'status': 'success',
                'analysis_result': {
                    'sentence': sentence,
                    'slots': result.get('slots', {}),          # main_slots → slots  
                    'sub_slots': result.get('sub_slots', {}),  # sub_slots はそのまま
                    'grammar_info': {
                        'detected_patterns': [],
                        'handler_contributions': {}
                    },
                    'processing_time': result.get('meta', {}).get('processing_time', 0.0)
                },
                'processing_time': result.get('meta', {}).get('processing_time', 0.0),
                'meta': {
                    'sentence_id': i,
                    'test_mode': 'human_only',
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            batch_results.append(batch_result)
            
            # 進捗表示
            if i % 10 == 0:
                print(f"   📊 進捗: {i}/{len(test_sentences)} 完了")
                
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")
            # エラーの場合は空結果を追加
            batch_results.append({
                'sentence': sentence,
                'status': 'error',
                'analysis_result': {
                    'sentence': sentence,
                    'slots': {},
                    'sub_slots': {},
                    'grammar_info': {
                        'detected_patterns': [],
                        'handler_contributions': {}
                    },
                    'processing_time': 0.0
                },
                'processing_time': 0.0,
                'meta': {
                    'sentence_id': i,
                    'test_mode': 'human_only',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
            })
    
    end_time = datetime.now()
    
    # 統一形式でファイル出力（compare_results.py用）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = project_root / f"human_grammar_batch_results_{timestamp}.json"
    
    # バッチ結果をcompare_results.py互換の辞書形式に変換
    results_dict = {}
    for i, result in enumerate(batch_results, 1):
        test_id = str(i)  # "1", "2", "3"... の形式で final_54_test_data.json と一致
        results_dict[test_id] = result
    
    # 既存のバッチ処理結果と同じ形式で出力
    output_data = {
        'meta': {
            'test_type': 'human_grammar_recognition_batch',
            'total_sentences': len(batch_results),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_time': str(end_time - start_time),
            'system_version': 'unified_mapper_v1.0_human_only'
        },
        'results': results_dict
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 70)
    print("📊 バッチテスト完了")
    print("=" * 70)
    print(f"✅ 処理済み文数: {len(batch_results)}")
    print(f"📁 結果ファイル: {output_path}")
    
    # 統計情報
    total_time = sum(r.get('processing_time', 0) for r in batch_results)
    avg_time = total_time / len(batch_results) if batch_results else 0
    print(f"⏱️ 合計処理時間: {total_time:.3f}秒")
    print(f"⏱️ 平均処理時間: {avg_time:.4f}秒/文")
    
    # エラー統計
    error_count = sum(1 for r in batch_results if 'error' in r.get('meta', {}))
    if error_count > 0:
        print(f"⚠️ エラー発生文数: {error_count}/{len(batch_results)}")
    
    # スロット分解成功統計
    slot_success_count = sum(1 for r in batch_results if r.get('slots') or r.get('sub_slots'))
    slot_success_rate = (slot_success_count / len(batch_results)) * 100 if batch_results else 0
    print(f"🎯 スロット分解成功: {slot_success_count}/{len(batch_results)} ({slot_success_rate:.1f}%)")
    
    print()
    print("📋 次のステップ:")
    print(f"1. compare_results.py --results {output_path.name} で期待値との比較")
    print("2. compare_results.py --results {} --detail で詳細分析".format(output_path.name))
    print("3. 人間文法認識システムの改善箇所を特定")
    
    return output_path

if __name__ == "__main__":
    result_file = run_human_grammar_batch_test()
    if result_file:
        print(f"\n🚀 今すぐ実行可能:")
        print(f"   python compare_results.py --results {result_file.name}")
        print(f"   python compare_results.py --results {result_file.name} --detail")
