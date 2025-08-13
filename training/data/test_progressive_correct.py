#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Progressive Tenses Engine 正しい実装テスト
"""

from engines.progressive_tenses_engine import ProgressiveTensesEngine

def main():
    engine = ProgressiveTensesEngine()

    test_cases = [
        # 基本進行形
        'I am eating.',                         # S: I, Aux: am, V: eating
        'She is running.',                      # S: She, Aux: is, V: running  
        'They are watching TV.',                # S: They, Aux: are, V: watching, O1: TV
        'We were studying English.',            # S: We, Aux: were, V: studying, O1: English
        
        # 修飾語付き進行形
        'The cat is sleeping peacefully.',      # S: The cat, Aux: is, V: sleeping, M1: peacefully
        'She was running very fast.',           # S: She, Aux: was, V: running, M1: very, M2: fast
        'They are playing football now.',       # S: They, Aux: are, V: playing, O1: football, M1: now
        
        # 複雑な進行形
        'The students are writing letters to their friends.',  # 複数要素
        
        # 非進行形（比較用）
        'I eat apples.',                        # S: I, V: eat, O1: apples (進行形なし)
        'She runs fast.',                       # S: She, V: runs, M1: fast (進行形なし)
    ]

    print('=== 🔄 進行形エンジン正しい実装テスト ===')
    print('正しい分解: S=主語, Aux=be動詞, V=-ing動詞, O1=目的語, M1=修飾語')
    print()
    
    for text in test_cases:
        print(f'入力: {text}')
        try:
            result = engine.process(text)
            print(f'結果: {result}')
            
            # スロット内容詳細表示
            for key, value in result.items():
                print(f'  {key}: "{value}"')
            
            # 正しい分解の確認
            if 'am eating' in text or 'is eating' in text:
                if result.get('Aux') in ['am', 'is'] and result.get('V') == 'eating':
                    print('  ✅ 正しい進行形分解！')
                else:
                    print('  ❌ 間違った分解')
            
        except Exception as e:
            print(f'エラー: {e}')
            import traceback
            traceback.print_exc()
        
        print()

if __name__ == "__main__":
    main()
