#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spacy
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController

def debug_case_119():
    """Case 119の詳細デバッグ"""
    sentence = "It depends on if you agree."
    expected = {'3': 'we', '4': 'In less than one hour', '5': 'arrived', '6': 'at the station'}
    
    print(f"🔍 Case 119 デバッグ: '{sentence}'")
    print(f"📊 期待結果: {expected}")
    print("=" * 80)
    
    # spaCy解析
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    
    print("🔍 spaCy依存関係分析:")
    for token in doc:
        print(f"   {token.text}: dep={token.dep_}, pos={token.pos_}, tag={token.tag_}, head={token.head.text}, head_idx={token.head.i}")
    print()
    
    # Central Controller処理
    controller = CentralController()
    result = controller.decompose_sentence(sentence)
    
    print("🚀 CentralController処理結果:")
    print(f"   成功: {result.get('success', False)}")
    if 'slots' in result:
        print(f"   スロット: {result['slots']}")
    if 'metadata' in result:
        print(f"   メタデータ: {result['metadata']}")
    print()
    
    # 問題分析
    print("🔍 問題分析:")
    print("1. この文は条件文（if節）を含む複文")
    print("2. 主文: 'It depends on [something]'")
    print("3. 従属節: 'if you agree'")
    print("4. 期待されるスロット配置:")
    print("   - S: It (主語)")
    print("   - V: depends (動詞)")
    print("   - M2: on if you agree (修飾語句)")
    print()
    
    # より詳細な分析
    print("🔍 期待される処理フロー:")
    print("1. 条件文ハンドラーでif節を処理")
    print("2. 主文 'It depends on [if clause]' を基本構造として抽出")
    print("3. スロット配置: S=It, V=depends, M2=on if you agree")
    print()

if __name__ == "__main__":
    debug_case_119()
