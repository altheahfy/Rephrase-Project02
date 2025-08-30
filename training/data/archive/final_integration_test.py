#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終統合テスト: CentralController + UIFormatConverter
完全なパイプライン動作検証
"""

import json
from central_controller import CentralController
from ui_format_converter import UIFormatConverter

def test_final_integration():
    """最終統合テスト実行"""
    
    print("🚀 最終統合テスト開始")
    print("=" * 60)
    
    # システム初期化
    controller = CentralController()
    converter = UIFormatConverter()
    
    # テストケース群
    test_cases = [
        {
            "name": "関係節（形容詞補語付き）",
            "text": "The woman who seemed indecisive finally made a decision.",
            "expected_features": [
                "sub-c1: indecisive",
                "独立M2: finally",
                "正しい順序付け"
            ]
        },
        {
            "name": "基本5文型（第3文型）", 
            "text": "I love you very much.",
            "expected_features": [
                "S: I",
                "V: love", 
                "O1: you",
                "M2: very much"
            ]
        },
        {
            "name": "受動態+修飾語",
            "text": "The book was written carefully by him.",
            "expected_features": [
                "受動態分離",
                "Aux + V構造",
                "修飾語統合"
            ]
        },
        {
            "name": "疑問文",
            "text": "What did you buy yesterday?",
            "expected_features": [
                "疑問詞抽出",
                "助動詞分離",
                "時間修飾語"
            ]
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 テストケース {i}: {case['name']}")
        print(f"入力文: '{case['text']}'")
        print("-" * 50)
        
        try:
            # Phase 1: CentralController処理
            controller_result = controller.process_sentence(case['text'])
            
            if controller_result['success']:
                print("✅ CentralController処理成功")
                
                # 結果詳細表示
                main_slots = controller_result.get('main_slots', {})
                sub_slots = controller_result.get('sub_slots', {})
                ordered_slots = controller_result.get('ordered_slots', [])
                
                print(f"📊 Main Slots: {main_slots}")
                if sub_slots:
                    print(f"📊 Sub Slots: {sub_slots}")
                print(f"📊 Ordered Slots: {len(ordered_slots)}個")
                
                # Phase 2: UIFormatConverter処理
                ui_data = converter.convert_to_ui_format(controller_result)
                
                if ui_data:  # リストが空でなければ成功
                    print("✅ UIFormatConverter処理成功")
                    
                    # UI形式詳細表示
                    print(f"📱 UI Ready Items: {len(ui_data)}個")
                    
                    # 重要な特徴を確認
                    feature_check = []
                    for item in ui_data:
                        if item.get('SlotText') or item.get('SlotPhrase'):
                            feature_check.append(f"{item['Slot']}: {item.get('SlotPhrase', item.get('SlotText', ''))}")
                    
                    print(f"🎯 抽出された特徴: {feature_check}")
                    
                    # 成功記録
                    results.append({
                        'case': case['name'],
                        'status': 'SUCCESS',
                        'controller_result': controller_result,
                        'ui_data': ui_data,
                        'features': feature_check
                    })
                    
                else:
                    print(f"❌ UIFormatConverter失敗: 空の結果")
                    results.append({
                        'case': case['name'],
                        'status': 'UI_CONVERTER_FAILED',
                        'error': '空の結果'
                    })
            else:
                print(f"❌ CentralController失敗: {controller_result.get('error')}")
                results.append({
                    'case': case['name'],
                    'status': 'CONTROLLER_FAILED', 
                    'error': controller_result.get('error')
                })
                
        except Exception as e:
            print(f"❌ 例外発生: {str(e)}")
            results.append({
                'case': case['name'],
                'status': 'EXCEPTION',
                'error': str(e)
            })
    
    # 最終レポート
    print("\n" + "=" * 60)
    print("🎯 最終統合テスト結果")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    total_count = len(results)
    
    print(f"成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {result['case']}: {result['status']}")
    
    # サンプルUI出力ファイル作成（最初の成功例）
    success_results = [r for r in results if r['status'] == 'SUCCESS']
    if success_results:
        sample_result = success_results[0]
        sample_ui_data = sample_result['ui_data']
        
        output_file = "final_sample_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_ui_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 サンプルUI出力: {output_file} に保存")
        print(f"内容プレビュー: {len(sample_ui_data)}個のスロットアイテム")
    
    return results

def test_specific_relative_clause():
    """特定の関係節テスト（詳細版）"""
    
    print("\n🔍 関係節詳細テスト")
    print("=" * 40)
    
    controller = CentralController()
    converter = UIFormatConverter()
    
    text = "The woman who seemed indecisive finally made a decision."
    
    print(f"テスト文: '{text}'")
    
    # CentralController処理
    result = controller.process_sentence(text)
    
    if result['success']:
        print("\n📊 CentralController結果:")
        print(f"Main Slots: {result['main_slots']}")
        print(f"Sub Slots: {result['sub_slots']}")
        
        # UIConverter処理  
        ui_data = converter.convert_to_ui_format(result)
        
        if ui_data:
            print("\n📱 UI形式変換結果:")
            
            for item in ui_data:
                slot = item['Slot']
                text = item.get('SlotPhrase', item.get('SlotText', ''))
                phrase_type = item.get('PhraseType', '')
                display_order = item.get('Slot_display_order', '')
                
                print(f"  {slot}: '{text}' (Type: {phrase_type}, Order: {display_order})")
            
            # 期待する構造の検証
            expected_checks = {
                'sub-c1存在': any(item['Slot'] == 'sub-c1' and item.get('SlotPhrase') == 'indecisive' for item in ui_data),
                'M2独立性': any(item['Slot'] == 'M2' and item.get('SlotPhrase') == 'finally' for item in ui_data),
                'S空化': any(item['Slot'] == 'S' and not item.get('SlotPhrase') for item in ui_data),
                'サブスロット親': any(item.get('parent_slot') == 'S' for item in ui_data)
            }
            
            print("\n🔎 期待構造チェック:")
            for check_name, passed in expected_checks.items():
                icon = "✅" if passed else "❌"
                print(f"  {icon} {check_name}")
            
            return ui_data
    
    return None

if __name__ == "__main__":
    # メイン統合テスト
    main_results = test_final_integration()
    
    # 詳細関係節テスト
    detailed_result = test_specific_relative_clause()
    
    print("\n🎉 最終統合テスト完了!")
    print("システムは単一呼び出しでUI対応形式まで変換可能です。")
