#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine

def test_quickly_missing():
    """quicklyがM2に分類されない問題を調査"""
    
    engine = CompleteRephraseParsingEngine()
    
    test_sentence = "He has recovered quickly from a serious injury."
    print(f"=== テスト文: {test_sentence} ===")
    
    result = engine.analyze_sentence(test_sentence)
    
    print(f"\n📋 スロット分析:")
    if 'slots' in result:
        for slot, candidates in result['slots'].items():
            if not candidates:
                continue
            print(f"\n  {slot}:")
            for candidate in candidates:
                if isinstance(candidate, dict):
                    value = candidate.get('value', '')
                    print(f"    - '{value}'")
    
    # quicklyがどこに分類されているかチェック
    print(f"\n🔍 'quickly' の分類確認:")
    found_quickly = False
    if 'slots' in result:
        for slot, candidates in result['slots'].items():
            for candidate in candidates:
                if isinstance(candidate, dict):
                    value = candidate.get('value', '')
                    if 'quickly' in value.lower():
                        print(f"  ✅ '{value}' が {slot} に分類されています")
                        found_quickly = True
    
    if not found_quickly:
        print(f"  ❌ 'quickly' がどのスロットにも見つかりません")
        
        # spaCy解析の詳細を確認
        print(f"\n🔍 spaCy 解析詳細:")
        import spacy
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(test_sentence)
        
        for token in doc:
            print(f"  '{token.text}' [POS: {token.pos_}, Tag: {token.tag_}, Dep: {token.dep_, token.dep_}, Head: {token.head.text}]")

if __name__ == "__main__":
    test_quickly_missing()
