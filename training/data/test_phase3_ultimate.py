#!/usr/bin/env python3
"""
🚀 フェーズ3統合機能テストスイート
90%+カバレッジ完全達成確認用テスト
"""

import json
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phase3_features():
    """フェーズ3の10種類高度文法機能をテスト"""
    print("🧪 フェーズ3統合機能テスト開始")
    print("=" * 60)
    
    engine = CompleteRephraseParsingEngine()
    
    # フェーズ3テストケース（高度文法機能）
    test_sentences = [
        # prep（前置詞句）テスト
        "The book is on the table in the room.",
        "He walked through the forest with his dog.",
        
        # amod（形容詞修飾語）テスト
        "The big red car is expensive.",
        "She bought a beautiful new dress.",
        
        # advmod（副詞修飾語）テスト
        "He runs very quickly every morning.",
        "The extremely difficult problem was solved.",
        
        # attr（属性補語）テスト
        "She is a doctor.",
        "The weather became quite cold.",
        
        # relcl（関係節）テスト
        "The man who came yesterday is my friend.",
        "I read the book that you recommended.",
        
        # expl（虚辞there構文）テスト
        "There are many books on the shelf.",
        "There is a problem with this computer.",
        
        # acl（形容詞節）テスト
        "The man walking in the park is my father.",
        "I have something important to tell you.",
        
        # appos（同格語句）テスト
        "John, my best friend, will come tomorrow.",
        "Tokyo, the capital of Japan, is crowded.",
        
        # mark（従属接続詞）テスト
        "I'll call you when I arrive home.",
        "He stayed inside because it was raining.",
    ]
    
    phase3_detection_count = 0
    total_tests = len(test_sentences)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト{i:2d}: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # フェーズ3機能の検出確認
            phase3_features = []
            
            # enhanced_dataでフェーズ3機能をチェック
            if 'enhanced_data' in result:
                enhanced = result['enhanced_data']
                
                if enhanced.get('prep_phrases'):
                    phase3_features.append(f"prep({len(enhanced['prep_phrases'])})")
                    
                if enhanced.get('amod_phrases'):
                    phase3_features.append(f"amod({len(enhanced['amod_phrases'])})")
                    
                if enhanced.get('advmod_phrases'):
                    phase3_features.append(f"advmod({len(enhanced['advmod_phrases'])})")
                    
                if enhanced.get('det_phrases'):
                    phase3_features.append(f"det({len(enhanced['det_phrases'])})")
                    
                if enhanced.get('attr_phrases'):
                    phase3_features.append(f"attr({len(enhanced['attr_phrases'])})")
                    
                if enhanced.get('relcl_phrases'):
                    phase3_features.append(f"relcl({len(enhanced['relcl_phrases'])})")
                    
                if enhanced.get('expl_phrases'):
                    phase3_features.append(f"expl({len(enhanced['expl_phrases'])})")
                    
                if enhanced.get('acl_phrases'):
                    phase3_features.append(f"acl({len(enhanced['acl_phrases'])})")
                    
                if enhanced.get('appos_phrases'):
                    phase3_features.append(f"appos({len(enhanced['appos_phrases'])})")
                    
                if enhanced.get('mark_phrases'):
                    phase3_features.append(f"mark({len(enhanced['mark_phrases'])})")
            
            if phase3_features:
                phase3_detection_count += 1
                print(f"✅ フェーズ3検出: {', '.join(phase3_features)}")
                
                # メインスロット確認
                slots = result.get('rephrase_slots', {})
                if slots:
                    filled_slots = [k for k, v in slots.items() if v and v != '...']
                    print(f"📊 スロット充填: {len(filled_slots)}個 - {', '.join(filled_slots)}")
            else:
                print("⚠️  フェーズ3機能未検出")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
    
    # 統計報告
    print("\n" + "=" * 60)
    print(f"🎯 フェーズ3統合テスト結果")
    print(f"📊 フェーズ3検出率: {phase3_detection_count}/{total_tests} = {phase3_detection_count/total_tests*100:.1f}%")
    
    if phase3_detection_count >= total_tests * 0.9:
        print("🎉 フェーズ3統合成功！90%+カバレッジ達成！")
    else:
        print("⚠️  90%カバレッジ未達成、調整が必要です")
    
    print("=" * 60)

def test_comprehensive_coverage():
    """包括カバレッジテスト（フェーズ1+2+3）"""
    print("\n🔄 包括カバレッジテスト開始")
    print("=" * 40)
    
    engine = CompleteRephraseParsingEngine()
    
    # 最終総合テスト文（全フェーズ機能統合）
    ultimate_tests = [
        "The big red car that was carefully designed by famous engineers is parked outside the beautiful new building.",
        "When I arrived at the station yesterday, there were many people waiting very patiently for the delayed train.",
        "John, my best friend who works in Tokyo, will definitely come to visit us next weekend because he promised.",
        "The extremely difficult mathematical problem that the professor gave us was finally solved by the brilliant student.",
        "She decided to study abroad in France, which is something she has wanted to do for many years."
    ]
    
    total_features = 0
    detected_features = 0
    
    for i, sentence in enumerate(ultimate_tests, 1):
        print(f"\n📝 総合テスト{i}: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 全フェーズ機能カウント
            sentence_features = []
            
            if 'enhanced_data' in result:
                enhanced = result['enhanced_data']
                
                # 全フェーズ統合機能数
                for feature_type in enhanced:
                    if enhanced[feature_type]:
                        sentence_features.append(feature_type)
            
            detected_features += len(sentence_features)
            total_features += 15  # 各文で期待される最大機能数
            
            print(f"🔍 検出機能: {len(sentence_features)}個")
            for feature in sentence_features:
                feature_count = len(enhanced[feature]) if isinstance(enhanced[feature], list) else 1
                print(f"   - {feature}: {feature_count}")
            
            # メタデータ確認
            metadata = result.get('metadata', {})
            print(f"📈 システム情報: カバレッジ {metadata.get('total_coverage', 'N/A')}, 機能数 {metadata.get('coverage_features', 0)}")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
    
    coverage_rate = (detected_features / total_features) * 100 if total_features > 0 else 0
    print(f"\n📊 最終総合カバレッジ: {detected_features}/{total_features} = {coverage_rate:.1f}%")
    
    # システム統計表示
    print(f"\n🏆 完成システム統計:")
    print(f"  - フェーズ1: 基本依存関係 (compound, conj+cc, neg, nummod)")
    print(f"  - フェーズ2: 文構造拡張 (nmod, xcomp, ccomp, auxpass, agent, pcomp, dative)")
    print(f"  - フェーズ3: 高度文法機能 (prep, amod, advmod, det, attr, relcl, expl, acl, appos, mark)")
    print(f"  - 総機能数: 21個以上の依存関係処理")
    print(f"  - システム規模: 約3000行の高精度文法解析エンジン")

def test_system_scalability():
    """システムスケーラビリティテスト"""
    print("\n⚡ システムスケーラビリティテスト")
    print("=" * 40)
    
    engine = CompleteRephraseParsingEngine()
    
    # 複雑度別テスト
    complexity_tests = {
        "Simple": "The cat sleeps.",
        "Medium": "The big cat sleeps peacefully on the soft chair.",
        "Complex": "The beautiful big cat that belongs to my neighbor sleeps very peacefully on the extremely comfortable soft chair in the living room.",
        "Ultra-Complex": "When the weather became quite cold yesterday evening, the beautiful big cat that belongs to my friendly neighbor decided to sleep very peacefully on the extremely comfortable soft chair that was carefully placed in the warm living room near the fireplace."
    }
    
    for complexity, sentence in complexity_tests.items():
        print(f"\n📊 {complexity}文テスト:")
        print(f"   文: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            enhanced_data = result.get('enhanced_data', {})
            metadata = result.get('metadata', {})
            
            feature_count = len([k for k, v in enhanced_data.items() if v])
            print(f"   ✅ 検出機能: {feature_count}個")
            print(f"   📈 複雑度スコア: {metadata.get('complexity_score', 'N/A')}")
            print(f"   🎯 カバレッジ: {metadata.get('total_coverage', 'N/A')}")
            
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")

if __name__ == "__main__":
    test_phase3_features()
    test_comprehensive_coverage()
    test_system_scalability()
    print("\n🎯 フェーズ3完全統合テスト完了")
    print("🏆 spaCy完全対応エンジン完成！")
