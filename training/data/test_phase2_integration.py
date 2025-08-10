#!/usr/bin/env python3
"""
🚀 フェーズ2統合機能テストスイート
80%カバレッジ達成確認用テスト
"""

import json
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_phase2_features():
    """フェーズ2の7種類依存関係拡張機能をテスト"""
    print("🧪 フェーズ2統合機能テスト開始")
    print("=" * 60)
    
    engine = CompleteRephraseParsingEngine()
    
    # フェーズ2テストケース（文構造拡張）
    test_sentences = [
        # nmod（名詞修飾語）テスト
        "The book on the table is mine.",
        "A man with a beard walked in.",
        
        # xcomp（動詞補語）テスト
        "I want to go home.",
        "She decided to study abroad.",
        
        # ccomp（節補語）テスト
        "I believe that he is right.",
        "She said that it was raining.",
        
        # auxpass（受動助動詞）テスト
        "The cake was eaten by John.",
        "The problem is being solved.",
        
        # agent（動作主）テスト
        "The book was written by Shakespeare.",
        "The door was opened by the wind.",
        
        # pcomp（前置詞補語）テスト
        "I am interested in learning Japanese.",
        "She is good at playing piano.",
        
        # dative（与格目的語）テスト
        "Give me the book.",
        "Send her a letter.",
    ]
    
    phase2_detection_count = 0
    total_tests = len(test_sentences)
    
    for i, sentence in enumerate(test_sentences, 1):
        print(f"\n📝 テスト{i:2d}: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # フェーズ2機能の検出確認
            phase2_features = []
            
            # enhanced_dataでフェーズ2機能をチェック
            if 'enhanced_data' in result:
                enhanced = result['enhanced_data']
                
                if enhanced.get('nmod_phrases'):
                    phase2_features.append(f"nmod({len(enhanced['nmod_phrases'])})")
                    
                if enhanced.get('xcomp_clauses'):
                    phase2_features.append(f"xcomp({len(enhanced['xcomp_clauses'])})")
                    
                if enhanced.get('ccomp_clauses'):
                    phase2_features.append(f"ccomp({len(enhanced['ccomp_clauses'])})")
                    
                if enhanced.get('auxpass_auxiliaries'):
                    phase2_features.append(f"auxpass({len(enhanced['auxpass_auxiliaries'])})")
                    
                if enhanced.get('agent_phrases'):
                    phase2_features.append(f"agent({len(enhanced['agent_phrases'])})")
                    
                if enhanced.get('pcomp_complements'):
                    phase2_features.append(f"pcomp({len(enhanced['pcomp_complements'])})")
                    
                if enhanced.get('dative_objects'):
                    phase2_features.append(f"dative({len(enhanced['dative_objects'])})")
            
            if phase2_features:
                phase2_detection_count += 1
                print(f"✅ フェーズ2検出: {', '.join(phase2_features)}")
                
                # メインスロット確認
                slots = result.get('rephrase_slots', {})
                if slots:
                    filled_slots = [k for k, v in slots.items() if v and v != '...']
                    print(f"📊 スロット充填: {len(filled_slots)}個 - {', '.join(filled_slots)}")
            else:
                print("⚠️  フェーズ2機能未検出")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
    
    # 統計報告
    print("\n" + "=" * 60)
    print(f"🎯 フェーズ2統合テスト結果")
    print(f"📊 フェーズ2検出率: {phase2_detection_count}/{total_tests} = {phase2_detection_count/total_tests*100:.1f}%")
    
    if phase2_detection_count >= total_tests * 0.8:
        print("🎉 フェーズ2統合成功！80%カバレッジ達成！")
    else:
        print("⚠️  80%カバレッジ未達成、調整が必要です")
    
    print("=" * 60)

def test_cumulative_coverage():
    """累積カバレッジテスト（フェーズ1+フェーズ2）"""
    print("\n🔄 累積カバレッジテスト開始")
    print("=" * 40)
    
    engine = CompleteRephraseParsingEngine()
    
    # 包括的テスト文
    comprehensive_tests = [
        "The big red car that was bought by John is parked outside.",
        "I want to believe that she will come and help us tomorrow.",
        "The book on the shelf was written by a famous author.",
        "She decided to study hard and pass the difficult exam.",
        "Give me the keys and show her the way to the station.",
    ]
    
    total_features = 0
    detected_features = 0
    
    for i, sentence in enumerate(comprehensive_tests, 1):
        print(f"\n📝 包括テスト{i}: {sentence}")
        
        try:
            result = engine.analyze_sentence(sentence)
            
            # 全機能カウント
            sentence_features = []
            
            if 'enhanced_data' in result:
                enhanced = result['enhanced_data']
                
                # フェーズ1機能
                for feature in ['compound_words', 'coordinated_phrases', 'negations', 'numerical_modifiers']:
                    if enhanced.get(feature):
                        sentence_features.append(feature)
                        
                # フェーズ2機能
                for feature in ['nmod_phrases', 'xcomp_clauses', 'ccomp_clauses', 'auxpass_auxiliaries', 'agent_phrases', 'pcomp_complements', 'dative_objects']:
                    if enhanced.get(feature):
                        sentence_features.append(feature)
            
            detected_features += len(sentence_features)
            total_features += 7  # 各文で期待される最大機能数
            
            print(f"🔍 検出機能: {len(sentence_features)}個")
            for feature in sentence_features:
                print(f"   - {feature}")
                
        except Exception as e:
            print(f"❌ エラー: {str(e)}")
    
    coverage_rate = (detected_features / total_features) * 100 if total_features > 0 else 0
    print(f"\n📊 総合カバレッジ: {detected_features}/{total_features} = {coverage_rate:.1f}%")

if __name__ == "__main__":
    test_phase2_features()
    test_cumulative_coverage()
    print("\n🎯 フェーズ2統合テスト完了")
