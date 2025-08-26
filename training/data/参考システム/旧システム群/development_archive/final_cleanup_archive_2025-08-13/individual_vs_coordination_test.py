#!/usr/bin/env python3
"""
Individual Engine vs Coordination System Test
個別エンジンの直接テスト vs 協調システムテストの矛盾検証
"""

from grammar_master_controller_v2 import GrammarMasterControllerV2
import sys
import os

# 個別エンジンのインポート
sys.path.append('engines')
from engines.basic_five_pattern_engine import BasicFivePatternEngine
from engines.modal_engine import ModalEngine

def test_individual_vs_coordination():
    print("🔍 Individual Engine vs Coordination System Comparison")
    print("=" * 80)
    
    # 失敗した例文を個別エンジンで直接テスト
    failed_examples = {
        'basic_five': [
            "The cat sits.",                    # 協調システムで失敗
            "They made him captain."            # 協調システムで失敗
        ],
        'modal': [
            "You can swim.",                    # 協調システムで失敗  
            "She should study harder."          # 協調システムで失敗
        ]
    }
    
    # 協調システム初期化
    controller = GrammarMasterControllerV2()
    
    print("\n🧪 BASIC FIVE PATTERN ENGINE COMPARISON")
    print("-" * 60)
    
    # 個別基本5文型エンジンテスト
    basic_engine = BasicFivePatternEngine()
    
    for sentence in failed_examples['basic_five']:
        print(f"\n📝 Sentence: '{sentence}'")
        
        # 個別エンジン直接テスト
        print("🔸 Individual Engine (Direct):")
        try:
            direct_result = basic_engine.process_sentence(sentence)
            if direct_result and 'slots' in direct_result and direct_result['slots']:
                print(f"   ✅ SUCCESS | Slots: {len(direct_result['slots'])} | Pattern: {direct_result.get('pattern', 'unknown')}")
                print(f"   📋 Slots: {direct_result['slots']}")
                print(f"   📊 Confidence: {direct_result.get('confidence', 0):.3f}")
            else:
                print(f"   ❌ FAILED | No slots detected")
        except Exception as e:
            print(f"   ❌ ERROR | {e}")
        
        # 協調システムテスト
        print("🔸 Coordination System:")
        try:
            coord_result = controller.process_sentence(sentence)
            if hasattr(coord_result, 'success') and coord_result.success and coord_result.slots:
                print(f"   ✅ SUCCESS | Slots: {len(coord_result.slots)} | Engine: {coord_result.engine_type.value}")
                print(f"   📋 Slots: {coord_result.slots}")
                print(f"   📊 Confidence: {coord_result.confidence:.3f}")
            else:
                print(f"   ❌ FAILED | Success: {getattr(coord_result, 'success', 'unknown')}")
                print(f"   🔍 Engine: {getattr(coord_result, 'engine_type', 'unknown')}")
                print(f"   ⚠️  Error: {getattr(coord_result, 'error', 'No error info')}")
        except Exception as e:
            print(f"   ❌ ERROR | {e}")
    
    print("\n🧪 MODAL ENGINE COMPARISON")
    print("-" * 60)
    
    # 個別法助動詞エンジンテスト
    modal_engine = ModalEngine()
    
    for sentence in failed_examples['modal']:
        print(f"\n📝 Sentence: '{sentence}'")
        
        # 個別エンジン直接テスト
        print("🔸 Individual Engine (Direct):")
        try:
            direct_result = modal_engine.process_sentence(sentence)
            if direct_result and 'slots' in direct_result and direct_result['slots']:
                print(f"   ✅ SUCCESS | Slots: {len(direct_result['slots'])} | Pattern: {direct_result.get('pattern', 'unknown')}")
                print(f"   📋 Slots: {direct_result['slots']}")
                print(f"   📊 Confidence: {direct_result.get('confidence', 0):.3f}")
            else:
                print(f"   ❌ FAILED | No slots detected")
        except Exception as e:
            print(f"   ❌ ERROR | {e}")
        
        # 協調システムテスト
        print("🔸 Coordination System:")
        try:
            coord_result = controller.process_sentence(sentence)
            if hasattr(coord_result, 'success') and coord_result.success and coord_result.slots:
                print(f"   ✅ SUCCESS | Slots: {len(coord_result.slots)} | Engine: {coord_result.engine_type.value}")
                print(f"   📋 Slots: {coord_result.slots}")
                print(f"   📊 Confidence: {coord_result.confidence:.3f}")
            else:
                print(f"   ❌ FAILED | Success: {getattr(coord_result, 'success', 'unknown')}")
                print(f"   🔍 Engine: {getattr(coord_result, 'engine_type', 'unknown')}")
                print(f"   ⚠️  Error: {getattr(coord_result, 'error', 'No error info')}")
        except Exception as e:
            print(f"   ❌ ERROR | {e}")

    print("\n📊 CONCLUSION:")
    print("If individual engines succeed but coordination fails,")
    print("there's a theoretical contradiction in the system.")
    print("=" * 80)

if __name__ == "__main__":
    test_individual_vs_coordination()
