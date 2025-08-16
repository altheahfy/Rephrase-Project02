#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4ハンドラー完全性テスト用の高度な23例文セット
ハンドラー間の境界処理と複合パターンをテスト
"""

def create_advanced_test_sentences():
    """4ハンドラーの完全性をテストする高度な例文セット"""
    
    advanced_sentences = {
        # ========== ハンドラー複合テスト ==========
        
        # 20-22: relative_clause + passive_voice 複合
        '20': 'The book which was carefully written by Shakespeare is famous.',
        '21': 'The car that was quickly repaired yesterday runs smoothly.',
        '32': 'The letter which was slowly typed by the secretary arrived today.',
        
        # 23-25: relative_clause + adverbial_modifier 複合  
        '23': 'The student who studies diligently always succeeds academically.',
        '24': 'The teacher whose class runs efficiently is respected greatly.',
        '25': 'The doctor who works carefully saves lives successfully.',
        
        # 26-28: passive_voice + adverbial_modifier 複合
        '26': 'The window was gently opened by the morning breeze.',
        '27': 'The message is being carefully written by the manager.',
        '28': 'The problem was quickly solved by the expert team.',
        
        # ========== 境界ケーステスト ==========
        
        # 29-31: 複雑な関係詞節（whose/where/when）
        '29': 'The house whose roof was damaged badly needs immediate repair.',
        '30': 'The place where we met accidentally became our favorite spot.',
        '31': 'The time when everything changed dramatically was unexpected.',
        
        # 41: 進行形受動態
        '41': 'The building is being constructed very carefully by skilled workers.',
        
        # ========== 基本文型の境界テスト ==========
        
        # 45-46: 第4文型・第5文型の副詞修飾
        '45': 'The teacher explains grammar clearly to confused students daily.',
        '46': 'The manager made the decision quickly and announced it immediately.',
        
        # ========== 高難度複合パターン ==========
        
        # 47-49: 3ハンドラー複合
        '47': 'The report which was thoroughly reviewed by experts was published successfully.',
        '48': 'The student whose essay was carefully corrected improved dramatically.',
        '49': 'The machine that was properly maintained works efficiently every day.',
        
        # ========== エッジケーステスト ==========
        
        # 50-54: 特殊構文・境界処理
        '50': 'The team working overtime completed the project successfully yesterday.',
        '51': 'The woman standing quietly near the door was waiting patiently.',
        '52': 'The children playing happily in the garden were supervised carefully.',
        '53': 'The documents being reviewed thoroughly will be approved soon.',
        '54': 'The artist whose paintings were exhibited internationally became famous rapidly.'
    }
    
    return advanced_sentences

def analyze_test_coverage():
    """テストカバレッジ分析"""
    
    sentences = create_advanced_test_sentences()
    
    coverage = {
        'relative_clause': [],
        'passive_voice': [],
        'adverbial_modifier': [],
        'complex_combinations': []
    }
    
    for id, sentence in sentences.items():
        analysis = []
        
        # 関係詞節検出
        if any(word in sentence.lower() for word in ['who', 'which', 'that', 'whose', 'where', 'when']):
            analysis.append('relative_clause')
            coverage['relative_clause'].append(id)
        
        # 受動態検出
        if any(phrase in sentence.lower() for phrase in ['was ', 'were ', 'is being', 'are being', 'been ']):
            analysis.append('passive_voice')
            coverage['passive_voice'].append(id)
        
        # 副詞修飾検出
        if any(word in sentence.lower() for word in ['carefully', 'quickly', 'slowly', 'diligently', 'efficiently', 'gently', 'thoroughly', 'properly', 'successfully', 'dramatically', 'immediately', 'patiently', 'happily', 'internationally', 'rapidly']):
            analysis.append('adverbial_modifier')
            coverage['adverbial_modifier'].append(id)
        
        # 複合パターン
        if len(analysis) >= 2:
            coverage['complex_combinations'].append(f"{id}({'+'.join(analysis)})")
    
    return coverage

if __name__ == "__main__":
    print("🚀 4ハンドラー完全性テスト用 高度例文セット")
    print("=" * 60)
    
    sentences = create_advanced_test_sentences()
    coverage = analyze_test_coverage()
    
    print("📋 高度テスト例文一覧:")
    for id, sentence in sentences.items():
        print(f"  {id}: {sentence}")
    
    print(f"\n📊 テストカバレッジ分析:")
    print(f"  🔗 relative_clause: {len(coverage['relative_clause'])}例文")
    print(f"  🔄 passive_voice: {len(coverage['passive_voice'])}例文") 
    print(f"  ⚡ adverbial_modifier: {len(coverage['adverbial_modifier'])}例文")
    print(f"  🎯 複合パターン: {len(coverage['complex_combinations'])}例文")
    
    print(f"\n🎯 複合パターン詳細:")
    for combo in coverage['complex_combinations']:
        print(f"    {combo}")
    
    print(f"\n✅ 4ハンドラー境界処理・複合パターンテスト準備完了")
