#!/usr/bin/env python3
"""
spaCy vs CompleteRephraseParsingEngine 比較検証システム
完全な依存関係抽出と現在システムの差分分析
"""

import spacy
from CompleteRephraseParsingEngine import CompleteRephraseParsingEngine
import json
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict

class SpacySystemComparator:
    def __init__(self):
        print("✅ spaCy語彙認識エンジン初期化完了")
        self.nlp = spacy.load("en_core_web_sm")
        self.engine = CompleteRephraseParsingEngine()
        self.dependency_stats = defaultdict(int)
        self.pos_stats = defaultdict(int)
        
    def extract_complete_spacy_analysis(self, sentence: str) -> Dict[str, Any]:
        """spaCyによる完全な依存関係・構造解析"""
        doc = self.nlp(sentence)
        
        analysis = {
            'sentence': sentence,
            'tokens': [],
            'dependencies': {},
            'noun_phrases': [],
            'verb_phrases': [],
            'prepositional_phrases': [],
            'subjects': [],
            'objects': [],
            'modifiers': [],
            'auxiliaries': [],
            'complements': []
        }
        
        # 全トークン解析
        for token in doc:
            token_info = {
                'text': token.text,
                'lemma': token.lemma_,
                'pos': token.pos_,
                'tag': token.tag_,
                'dep': token.dep_,
                'head_text': token.head.text,
                'head_pos': token.head.pos_,
                'children': [child.text for child in token.children],
                'is_alpha': token.is_alpha,
                'is_stop': token.is_stop,
                'shape': token.shape_
            }
            analysis['tokens'].append(token_info)
            
            # 統計更新
            self.dependency_stats[token.dep_] += 1
            self.pos_stats[token.pos_] += 1
            
        # 依存関係別分類
        for token in doc:
            dep_key = f"{token.dep_}_{token.pos_}"
            if dep_key not in analysis['dependencies']:
                analysis['dependencies'][dep_key] = []
            
            analysis['dependencies'][dep_key].append({
                'text': token.text,
                'lemma': token.lemma_,
                'head': token.head.text,
                'full_phrase': self._extract_spacy_phrase(token)
            })
            
            # 文法役割別分類
            if token.dep_ in ['nsubj', 'nsubjpass', 'csubj', 'csubjpass']:
                analysis['subjects'].append({
                    'text': token.text,
                    'dep': token.dep_,
                    'full_phrase': self._extract_spacy_phrase(token)
                })
            elif token.dep_ in ['dobj', 'iobj', 'pobj']:
                analysis['objects'].append({
                    'text': token.text,
                    'dep': token.dep_,
                    'full_phrase': self._extract_spacy_phrase(token)
                })
            elif token.dep_ in ['amod', 'advmod', 'prep', 'poss', 'det']:
                analysis['modifiers'].append({
                    'text': token.text,
                    'dep': token.dep_,
                    'modifies': token.head.text,
                    'full_phrase': self._extract_spacy_phrase(token)
                })
            elif token.dep_ in ['aux', 'auxpass']:
                analysis['auxiliaries'].append({
                    'text': token.text,
                    'dep': token.dep_,
                    'assists': token.head.text
                })
            elif token.dep_ in ['acomp', 'xcomp', 'ccomp']:
                analysis['complements'].append({
                    'text': token.text,
                    'dep': token.dep_,
                    'full_phrase': self._extract_spacy_phrase(token)
                })
        
        return analysis
    
    def _extract_spacy_phrase(self, token) -> str:
        """spaCyトークンから完全なフレーズを抽出"""
        if token.pos_ == 'NOUN':
            # 名詞句抽出
            phrase_tokens = []
            
            # 左側修飾語（所有格、形容詞、限定詞など）
            for child in token.children:
                if child.i < token.i and child.dep_ in ['det', 'amod', 'compound', 'nummod', 'poss']:
                    phrase_tokens.append(child)
            
            phrase_tokens.append(token)
            
            # 右側修飾語
            for child in token.children:
                if child.i > token.i and child.dep_ in ['amod', 'compound']:
                    phrase_tokens.append(child)
            
            phrase_tokens.sort(key=lambda x: x.i)
            return ' '.join([t.text for t in phrase_tokens])
            
        elif token.pos_ == 'VERB':
            # 動詞句抽出（助動詞含む）
            phrase_tokens = []
            
            # 助動詞
            for child in token.children:
                if child.dep_ in ['aux', 'auxpass'] and child.i < token.i:
                    phrase_tokens.append(child)
            
            phrase_tokens.append(token)
            
            # 句動詞粒子
            for child in token.children:
                if child.dep_ == 'prt':
                    phrase_tokens.append(child)
            
            phrase_tokens.sort(key=lambda x: x.i)
            return ' '.join([t.text for t in phrase_tokens])
        
        elif token.pos_ == 'ADP':  # 前置詞
            # 前置詞句抽出
            phrase_tokens = [token]
            for child in token.children:
                if child.dep_ == 'pobj':
                    phrase_tokens.append(child)
                    # 前置詞の目的語の修飾語も含める
                    phrase_tokens.extend([gc for gc in child.children 
                                        if gc.dep_ in ['det', 'amod', 'poss']])
            
            phrase_tokens.sort(key=lambda x: x.i)
            return ' '.join([t.text for t in phrase_tokens])
        
        else:
            return token.text
    
    def get_current_system_analysis(self, sentence: str) -> Dict[str, Any]:
        """現在のCompleteRephraseParsingEngineによる解析"""
        try:
            result = self.engine.analyze_sentence(sentence)
            return {
                'sentence': sentence,
                'parsing_successful': True,
                'slots': result.get('slots', {}),
                'rules_applied': result.get('rules_applied', []),
                'sentence_pattern': result.get('sentence_pattern', ''),
                'debug_info': result.get('debug_info', {})
            }
        except Exception as e:
            return {
                'sentence': sentence,
                'parsing_successful': False,
                'error': str(e),
                'slots': {},
                'rules_applied': [],
                'sentence_pattern': '',
                'debug_info': {}
            }
    
    def compare_systems(self, sentences: List[str]) -> Dict[str, Any]:
        """両システムの包括的比較分析"""
        comparison_results = {
            'sentences_analyzed': len(sentences),
            'spacy_coverage': {},
            'current_system_coverage': {},
            'gaps_identified': [],
            'dependency_distribution': dict(self.dependency_stats),
            'pos_distribution': dict(self.pos_stats),
            'detailed_comparisons': []
        }
        
        for sentence in sentences:
            print(f"\n🔍 分析中: '{sentence}'")
            
            # spaCy完全解析
            spacy_analysis = self.extract_complete_spacy_analysis(sentence)
            
            # 現在システム解析
            current_analysis = self.get_current_system_analysis(sentence)
            
            # 比較結果
            comparison = self._compare_single_sentence(spacy_analysis, current_analysis)
            comparison_results['detailed_comparisons'].append(comparison)
            
            # ギャップ特定
            gaps = self._identify_gaps(spacy_analysis, current_analysis)
            comparison_results['gaps_identified'].extend(gaps)
        
        # 全体統計
        comparison_results['spacy_coverage'] = self._calculate_spacy_coverage()
        comparison_results['current_system_coverage'] = self._calculate_current_system_coverage(comparison_results['detailed_comparisons'])
        
        return comparison_results
    
    def _compare_single_sentence(self, spacy_analysis: Dict, current_analysis: Dict) -> Dict:
        """単一文の詳細比較"""
        return {
            'sentence': spacy_analysis['sentence'],
            'spacy_elements_count': len(spacy_analysis['tokens']),
            'current_slots_count': len(current_analysis['slots']),
            'spacy_dependencies': list(spacy_analysis['dependencies'].keys()),
            'current_rules_applied': current_analysis['rules_applied'],
            'spacy_subjects': spacy_analysis['subjects'],
            'spacy_objects': spacy_analysis['objects'],
            'spacy_modifiers': spacy_analysis['modifiers'],
            'current_slots': current_analysis['slots'],
            'parsing_successful': current_analysis['parsing_successful']
        }
    
    def _identify_gaps(self, spacy_analysis: Dict, current_analysis: Dict) -> List[Dict]:
        """システム間のギャップ特定"""
        gaps = []
        
        # spaCyが検出したが現在システムが見逃した要素
        spacy_elements = set()
        for dep_key, elements in spacy_analysis['dependencies'].items():
            for element in elements:
                spacy_elements.add(f"{element['text']}_{dep_key}")
        
        current_elements = set()
        for slot, content in current_analysis['slots'].items():
            if content:  # 空でない場合のみ
                current_elements.add(f"{content}_{slot}")
        
        # 現在システムで未検出の依存関係
        for dep_key in spacy_analysis['dependencies']:
            if dep_key not in [f"{slot}" for slot in current_analysis['slots']]:
                gaps.append({
                    'type': 'missing_dependency',
                    'sentence': spacy_analysis['sentence'],
                    'dependency': dep_key,
                    'elements': spacy_analysis['dependencies'][dep_key]
                })
        
        return gaps
    
    def _calculate_spacy_coverage(self) -> Dict:
        """spaCy解析網羅性統計"""
        total_deps = sum(self.dependency_stats.values())
        total_pos = sum(self.pos_stats.values())
        
        return {
            'total_dependencies_found': total_deps,
            'unique_dependency_types': len(self.dependency_stats),
            'dependency_distribution': dict(self.dependency_stats),
            'total_pos_tags': total_pos,
            'unique_pos_types': len(self.pos_stats),
            'pos_distribution': dict(self.pos_stats)
        }
    
    def _calculate_current_system_coverage(self, comparisons: List[Dict]) -> Dict:
        """現在システム網羅性統計"""
        total_sentences = len(comparisons)
        successful_parses = sum(1 for c in comparisons if c['parsing_successful'])
        
        all_slots = set()
        all_rules = set()
        
        for comparison in comparisons:
            all_slots.update(comparison['current_slots'].keys())
            all_rules.update(comparison['current_rules_applied'])
        
        return {
            'total_sentences_analyzed': total_sentences,
            'successful_parses': successful_parses,
            'success_rate': (successful_parses / total_sentences * 100) if total_sentences > 0 else 0,
            'unique_slots_used': list(all_slots),
            'unique_rules_applied': list(all_rules),
            'slots_count': len(all_slots),
            'rules_count': len(all_rules)
        }
    
    def generate_comprehensive_report(self, comparison_results: Dict) -> str:
        """包括的分析レポート生成"""
        report = []
        report.append("=" * 80)
        report.append("🔬 spaCy vs CompleteRephraseParsingEngine 包括的比較分析レポート")
        report.append("=" * 80)
        
        # 全体サマリー
        report.append(f"\n📊 分析概要:")
        report.append(f"  分析文数: {comparison_results['sentences_analyzed']}")
        report.append(f"  spaCy検出依存関係種類: {comparison_results['spacy_coverage']['unique_dependency_types']}")
        report.append(f"  現在システム成功率: {comparison_results['current_system_coverage']['success_rate']:.1f}%")
        report.append(f"  特定されたギャップ: {len(comparison_results['gaps_identified'])}")
        
        # spaCy網羅性詳細
        report.append(f"\n🎯 spaCy依存関係分布:")
        for dep, count in sorted(comparison_results['dependency_distribution'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {dep}: {count}回")
        
        # 現在システム統計
        report.append(f"\n🔧 現在システム統計:")
        report.append(f"  使用スロット: {comparison_results['current_system_coverage']['slots_count']}種類")
        report.append(f"  適用ルール: {comparison_results['current_system_coverage']['rules_count']}種類")
        report.append(f"  スロット一覧: {', '.join(comparison_results['current_system_coverage']['unique_slots_used'])}")
        
        # ギャップ詳細
        if comparison_results['gaps_identified']:
            report.append(f"\n🚨 特定されたギャップ:")
            gap_types = defaultdict(int)
            for gap in comparison_results['gaps_identified']:
                gap_types[gap['type']] += 1
                
            for gap_type, count in gap_types.items():
                report.append(f"  {gap_type}: {count}件")
        
        # 詳細比較（最初の3文のみ表示）
        report.append(f"\n📝 詳細比較サンプル (最初の3文):")
        for i, comparison in enumerate(comparison_results['detailed_comparisons'][:3]):
            report.append(f"\n  例文 {i+1}: '{comparison['sentence']}'")
            report.append(f"    spaCy要素数: {comparison['spacy_elements_count']}")
            report.append(f"    現在スロット数: {comparison['current_slots_count']}")
            report.append(f"    spaCy依存関係: {', '.join(comparison['spacy_dependencies'][:5])}{'...' if len(comparison['spacy_dependencies']) > 5 else ''}")
            report.append(f"    現在ルール: {', '.join(comparison['current_rules_applied'])}")
        
        report.append("\n" + "=" * 80)
        return '\n'.join(report)

def main():
    """メイン実行関数"""
    print("🚀 spaCy vs CompleteRephraseParsingEngine 比較検証開始")
    
    # テスト文セット（多様な文法構造）
    test_sentences = [
        "He resembles his mother.",
        "She gave him a beautiful present.",
        "The big red car parked outside quickly.",
        "I will go to the store tomorrow.",
        "They have been working hard all day.",
        "The book on the table is very interesting.",
        "Turn the music down, please.",
        "If you study hard, you will succeed.",
        "Walking in the park is relaxing.",
        "The man who called yesterday is here."
    ]
    
    # 比較器初期化・実行
    comparator = SpacySystemComparator()
    results = comparator.compare_systems(test_sentences)
    
    # レポート生成・出力
    report = comparator.generate_comprehensive_report(results)
    print(report)
    
    # 結果をJSONファイルに保存
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"spacy_system_comparison_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細結果を保存: {output_file}")
    print("🎉 比較検証完了！")

if __name__ == "__main__":
    main()
