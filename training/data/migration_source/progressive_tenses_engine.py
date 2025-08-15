#!/usr/bin/env python3
"""
Progressive Tenses Engine - 正しいRephrase式実装
進行形エンジン - be動詞 + -ing構文の正しい処理

Correct Rephrase Slot System:
"I am eating." → S: I, Aux: am, V: eating
"She was running fast." → S: She, Aux: was, V: running, M1: fast
"They are playing football." → S: They, Aux: are, V: playing, O1: football
"""

import stanza
from typing import Dict, List, Optional, Any
import re

class ProgressiveTensesEngine:
    """進行形エンジン - 正しいRephrase準拠版"""
    
    def __init__(self):
        print("🚀 進行形エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # be動詞リスト
        self.be_verbs = {'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """正しい進行形スロット分解"""
        print(f"🔄 進行形構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 進行形検出
        progressive_info = self._analyze_progressive_structure(sent)
        if progressive_info:
            return self._process_progressive_construction(sent, progressive_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_progressive_structure(self, sent) -> Optional[Dict]:
        """進行形構造の検出"""
        progressive_features = {
            'be_verb': None,        # be動詞 (Aux)
            'main_verb': None,      # -ing動詞 (V)
            'subject': None,        # 主語 (S)
            'type': None            # 進行形の種類
        }
        
        # 構造要素の検出
        for word in sent.words:
            # 主語検出
            if word.deprel == 'nsubj':
                progressive_features['subject'] = word
                
            # be動詞検出（助動詞として）
            elif (word.lemma == 'be' and 
                  word.upos == 'AUX' and 
                  word.text.lower() in self.be_verbs):
                progressive_features['be_verb'] = word
                
            # -ing動詞検出（現在分詞）
            elif (word.upos == 'VERB' and 
                  word.text.endswith('ing')):
                progressive_features['main_verb'] = word
        
        # 進行形判定
        if (progressive_features['be_verb'] and 
            progressive_features['main_verb'] and 
            progressive_features['subject']):
            
            # 進行形タイプの判定
            be_form = progressive_features['be_verb'].text.lower()
            if be_form in ['am', 'is', 'are']:
                progressive_features['type'] = 'present_continuous'
            elif be_form in ['was', 'were']:
                progressive_features['type'] = 'past_continuous'
            else:
                progressive_features['type'] = 'complex_continuous'
                
            print(f"  📋 進行形検出:")
            print(f"    パターン: {progressive_features['type']}")
            print(f"    主語: {progressive_features['subject'].text}")
            print(f"    be動詞: {progressive_features['be_verb'].text}")
            print(f"    メイン動詞: {progressive_features['main_verb'].text}")
            return progressive_features
        
        return None
    
    def _process_progressive_construction(self, sent, progressive_info) -> Dict[str, str]:
        """進行形の正しいスロット分解"""
        result = {}
        
        subject = progressive_info['subject']
        be_verb = progressive_info['be_verb']
        main_verb = progressive_info['main_verb']
        
        print(f"  🎯 正しいRephrase式分解:")
        
        # 基本スロット配置
        result['S'] = self._build_subject_phrase(sent, subject)
        result['Aux'] = be_verb.text  # be動詞は助動詞スロット
        result['V'] = main_verb.text  # -ing動詞はメイン動詞スロット
        
        # 追加要素の検出
        for word in sent.words:
            if word.head == main_verb.id:
                if word.deprel == 'obj':
                    # 目的語
                    result['O1'] = self._build_object_phrase(sent, word)
                elif word.deprel in ['advmod', 'obl']:
                    # 修飾語
                    if 'M1' not in result:
                        result['M1'] = word.text
                    elif 'M2' not in result:
                        result['M2'] = word.text
                    else:
                        result['M3'] = word.text
        
        print(f"    S (主語): {result.get('S', '')}")
        print(f"    Aux (助動詞): {result.get('Aux', '')}")
        print(f"    V (動詞): {result.get('V', '')}")
        if 'O1' in result:
            print(f"    O1 (目的語): {result.get('O1', '')}")
        for key in ['M1', 'M2', 'M3']:
            if key in result:
                print(f"    {key} (修飾語): {result[key]}")
        
        print(f"  ✅ 正しい進行形分解: {result}")
        return result
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """非進行形文の処理"""
        print("  📝 非進行形処理")
        result = {}
        
        # 基本的なスロット抽出
        for word in sent.words:
            if word.deprel == 'nsubj':
                result['S'] = word.text
            elif word.deprel == 'root' and word.upos == 'VERB':
                result['V'] = word.text
            elif word.deprel == 'obj':
                result['O1'] = word.text
        
        return result
    
    def _build_subject_phrase(self, sent, subject_word) -> str:
        """主語句の構築"""
        phrase_parts = []
        
        # 冠詞・形容詞の収集
        for word in sent.words:
            if word.head == subject_word.id:
                if word.deprel == 'det':
                    phrase_parts.append((word.id, word.text))
                elif word.deprel in ['amod', 'nmod']:
                    phrase_parts.append((word.id, word.text))
        
        # 語順でソート
        phrase_parts.sort(key=lambda x: x[0])
        
        # 主語句の組み立て
        if phrase_parts:
            modifiers = [part[1] for part in phrase_parts]
            return ' '.join(modifiers + [subject_word.text])
        else:
            return subject_word.text
    
    def _build_object_phrase(self, sent, object_word) -> str:
        """目的語句の構築"""
        phrase_parts = []
        
        # 冠詞・形容詞の収集
        for word in sent.words:
            if word.head == object_word.id:
                if word.deprel == 'det':
                    phrase_parts.append((word.id, word.text))
                elif word.deprel in ['amod', 'nmod']:
                    phrase_parts.append((word.id, word.text))
        
        # 語順でソート
        phrase_parts.sort(key=lambda x: x[0])
        
        # 目的語句の組み立て
        if phrase_parts:
            modifiers = [part[1] for part in phrase_parts]
            return ' '.join(modifiers + [object_word.text])
        else:
            return object_word.text
