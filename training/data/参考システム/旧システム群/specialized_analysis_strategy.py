#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
専門分担型分析戦略
各解析手法を得意分野に特化して使用
"""

import spacy
from typing import Dict, Any, Optional

class SpecializedAnalysisStrategy:
    """解析手法の専門分担管理"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # 専門分担マップ
        self.analysis_assignments = {
            # 品詞分析が得意な分野
            'adverb_detection': 'pos_analysis',
            'passive_voice_pattern': 'pos_analysis', 
            'be_verb_identification': 'pos_analysis',
            'simple_sentence_verb': 'pos_analysis',
            'perfect_tense_aux': 'pos_analysis',
            
            # 依存関係が得意な分野
            'main_verb_in_complex': 'dependency_analysis',
            'relative_clause_structure': 'dependency_analysis',
            'sentence_root': 'dependency_analysis'
        }
    
    def detect_adverbs(self, doc) -> list:
        """副詞検出 - 品詞分析専用"""
        adverbs = []
        for token in doc:
            if token.pos_ == 'ADV':
                adverbs.append({
                    'text': token.text,
                    'index': token.i,
                    'method': 'pos_analysis'
                })
        return adverbs
    
    def detect_passive_voice(self, doc) -> Optional[Dict]:
        """受動態検出 - 品詞分析専用"""
        be_verbs = ['am', 'is', 'are', 'was', 'were', 'be', 'been', 'being']
        
        for i, token in enumerate(doc):
            if token.text.lower() in be_verbs and i + 1 < len(doc):
                next_token = doc[i + 1]
                # 間に副詞があってもスキップして検出
                check_idx = i + 1
                while check_idx < len(doc) and doc[check_idx].pos_ == 'ADV':
                    check_idx += 1
                
                if check_idx < len(doc) and doc[check_idx].tag_ == 'VBN':
                    return {
                        'aux': token.text,
                        'verb': doc[check_idx].text,
                        'pattern': 'passive_voice',
                        'method': 'pos_analysis'
                    }
        return None
    
    def find_main_verb_complex(self, doc) -> Optional[int]:
        """複文の主動詞検出 - 依存関係専用"""
        for token in doc:
            if token.dep_ == 'ROOT':
                return token.i
        return None
    
    def analyze_relative_clause_structure(self, doc) -> Dict:
        """関係節構造分析 - 依存関係専用"""
        structure = {
            'has_relative_clause': False,
            'relative_pronouns': [],
            'relative_verbs': [],
            'main_verb': None,
            'method': 'dependency_analysis'
        }
        
        # 関係代名詞検出
        rel_pronouns = ['who', 'which', 'that', 'whose']
        for token in doc:
            if token.text.lower() in rel_pronouns:
                structure['relative_pronouns'].append({
                    'text': token.text,
                    'index': token.i
                })
                structure['has_relative_clause'] = True
        
        # 関係節動詞と主動詞を依存関係で区別
        for token in doc:
            if token.dep_ == 'relcl':  # 関係節動詞
                structure['relative_verbs'].append({
                    'text': token.text,
                    'index': token.i
                })
            elif token.dep_ == 'ROOT':  # 主動詞
                structure['main_verb'] = {
                    'text': token.text,
                    'index': token.i
                }
        
        return structure
    
    def get_analysis_method(self, task: str) -> str:
        """タスクに適した解析手法を返す"""
        return self.analysis_assignments.get(task, 'pos_analysis')
    
    def analyze_sentence_comprehensive(self, sentence: str) -> Dict[str, Any]:
        """文の包括的分析 - 専門分担使用"""
        doc = self.nlp(sentence)
        
        result = {
            'sentence': sentence,
            'analysis_methods_used': [],
            'components': {}
        }
        
        # 副詞検出（品詞分析）
        adverbs = self.detect_adverbs(doc)
        if adverbs:
            result['components']['adverbs'] = adverbs
            result['analysis_methods_used'].append('pos_analysis')
        
        # 受動態検出（品詞分析）
        passive = self.detect_passive_voice(doc)
        if passive:
            result['components']['passive_voice'] = passive
            result['analysis_methods_used'].append('pos_analysis')
        
        # 関係節構造（依存関係）
        rel_structure = self.analyze_relative_clause_structure(doc)
        if rel_structure['has_relative_clause']:
            result['components']['relative_clause'] = rel_structure
            result['analysis_methods_used'].append('dependency_analysis')
            
            # 複文の主動詞（依存関係）
            main_verb_idx = self.find_main_verb_complex(doc)
            if main_verb_idx is not None:
                result['components']['main_verb'] = {
                    'text': doc[main_verb_idx].text,
                    'index': main_verb_idx,
                    'method': 'dependency_analysis'
                }
        else:
            # 単純文の動詞（品詞分析）
            verbs = [token for token in doc if token.pos_ == 'VERB']
            if verbs:
                result['components']['main_verb'] = {
                    'text': verbs[-1].text,
                    'index': verbs[-1].i,
                    'method': 'pos_analysis'
                }
                result['analysis_methods_used'].append('pos_analysis')
        
        # 使用した手法を重複削除
        result['analysis_methods_used'] = list(set(result['analysis_methods_used']))
        
        return result

# テスト実行
if __name__ == "__main__":
    strategy = SpecializedAnalysisStrategy()
    
    test_sentences = [
        'She sings beautifully.',                                    # 単純文 + 副詞
        'The letter was written by John.',                           # 受動態
        'The man who runs fast is strong.',                          # 関係節
        'The teacher whose class runs efficiently is respected.'     # 複雑な関係節
    ]
    
    print("=== 専門分担型分析テスト ===")
    for sentence in test_sentences:
        result = strategy.analyze_sentence_comprehensive(sentence)
        print(f"\n📝 {sentence}")
        print(f"🔧 使用手法: {', '.join(result['analysis_methods_used'])}")
        
        for component, data in result['components'].items():
            if 'method' in data:
                print(f"  {component}: {data.get('text', data)} (手法: {data['method']})")
            else:
                print(f"  {component}: {data}")
