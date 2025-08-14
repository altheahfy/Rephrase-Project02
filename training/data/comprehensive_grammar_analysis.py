#!/usr/bin/env python3
"""
包括的文法解析システム - 節以外の文法要素も検出

現在のシステムでは見逃されている文法要素：
1. 倒置構造 (Inversion)
2. 時制・相 (Tense/Aspect)
3. 強調構造 (Emphasis)
4. 否定構造 (Negation patterns)
5. 条件構造 (Conditional patterns)
"""

import spacy
import stanza
from hierarchical_grammar_detector_v4 import HierarchicalGrammarDetector

class ComprehensiveGrammarDetector:
    def __init__(self):
        print("🔧 Comprehensive Grammar Detector 初期化中...")
        self.nlp_spacy = spacy.load("en_core_web_sm")
        stanza.download('en', quiet=True)
        self.nlp_stanza = stanza.Pipeline('en', quiet=True)
        self.v4_detector = HierarchicalGrammarDetector()
    
    def analyze_comprehensive_grammar(self, sentence):
        """包括的文法解析"""
        print(f"\n🔍 包括的解析: {sentence}")
        print("=" * 60)
        
        doc = self.nlp_spacy(sentence)
        
        result = {
            'sentence': sentence,
            'basic_pattern': None,
            'special_structures': [],
            'tense_aspect': None,
            'emphasis': [],
            'negation': [],
            'word_order': 'normal',
            'complexity_score': 0
        }
        
        # 1. 基本パターン検出（V4使用）
        try:
            v4_result = self.v4_detector.detect_hierarchical_grammar(sentence)
            result['basic_pattern'] = v4_result.main_pattern
        except:
            result['basic_pattern'] = 'unknown'
        
        # 2. 語順分析（倒置検出）
        result['word_order'] = self._detect_word_order(doc)
        
        # 3. 時制・相分析
        result['tense_aspect'] = self._detect_tense_aspect(doc)
        
        # 4. 強調構造検出
        result['emphasis'] = self._detect_emphasis(doc)
        
        # 5. 否定構造検出
        result['negation'] = self._detect_negation(doc)
        
        # 6. 特殊構造検出
        result['special_structures'] = self._detect_special_structures(doc)
        
        # 7. 複雑度スコア計算
        result['complexity_score'] = self._calculate_complexity(result)
        
        self._print_analysis(result)
        return result
    
    def _detect_word_order(self, doc):
        """語順パターン検出"""
        # ROOT動詞を探す
        root_verb = None
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                root_verb = token
                break
        
        if not root_verb:
            return 'no_verb'
        
        # 主語の位置チェック
        subject_before_verb = False
        aux_before_subject = False
        
        for token in doc:
            if token.dep_ == "nsubj":
                if token.i < root_verb.i:
                    subject_before_verb = True
                break
        
        # 助動詞が主語より前にあるかチェック
        for token in doc:
            if token.pos_ == "AUX" and token.dep_ == "aux":
                subj_tokens = [t for t in doc if t.dep_ == "nsubj"]
                if subj_tokens and token.i < subj_tokens[0].i:
                    aux_before_subject = True
                break
        
        # 文頭の副詞や否定語チェック
        first_meaningful = None
        for token in doc:
            if token.pos_ not in ["PUNCT", "SPACE"]:
                first_meaningful = token
                break
        
        if first_meaningful:
            # 否定副詞で始まる倒置
            if first_meaningful.text.lower() in ['never', 'rarely', 'seldom', 'hardly', 'scarcely', 'little', 'not', 'nowhere']:
                if aux_before_subject:
                    return 'negative_inversion'
            
            # 条件節の倒置 (Had I known...)
            if first_meaningful.pos_ == "AUX" and first_meaningful.text.lower() in ['had', 'were', 'should', 'could']:
                return 'conditional_inversion'
            
            # only構造の倒置
            if first_meaningful.text.lower() == 'only':
                return 'only_inversion'
        
        return 'normal' if subject_before_verb else 'inverted'
    
    def _detect_tense_aspect(self, doc):
        """時制・相の検出"""
        aux_verbs = []
        main_verbs = []
        
        for token in doc:
            if token.pos_ == "AUX":
                aux_verbs.append(token.text.lower())
            elif token.pos_ == "VERB":
                main_verbs.append((token.text, token.tag_))
        
        # 完了時制検出
        if 'have' in aux_verbs or 'has' in aux_verbs or 'had' in aux_verbs:
            past_participles = [v for v, tag in main_verbs if tag in ['VBN']]
            if past_participles:
                if 'had' in aux_verbs:
                    return 'past_perfect'
                elif 'have' in aux_verbs or 'has' in aux_verbs:
                    return 'present_perfect'
        
        # 進行時制検出
        if 'be' in [token.lemma_.lower() for token in doc if token.pos_ == "AUX"]:
            present_participles = [v for v, tag in main_verbs if tag in ['VBG']]
            if present_participles:
                return 'progressive'
        
        # 未来時制検出
        if 'will' in aux_verbs or 'shall' in aux_verbs:
            return 'future'
        
        # 条件法検出
        if 'would' in aux_verbs or 'could' in aux_verbs or 'should' in aux_verbs:
            return 'conditional'
        
        return 'simple'
    
    def _detect_emphasis(self, doc):
        """強調構造検出"""
        emphasis = []
        
        # 強調副詞
        emphasis_adverbs = ['very', 'extremely', 'absolutely', 'completely', 'totally', 'really', 'quite', 'rather', 'indeed', 'certainly']
        for token in doc:
            if token.text.lower() in emphasis_adverbs:
                emphasis.append(f"emphasis_adverb: {token.text}")
        
        # Do強調
        for token in doc:
            if token.text.lower() == 'do' and token.pos_ == 'AUX' and token.dep_ != 'aux':
                emphasis.append("do_emphasis")
        
        # It is ... that構文
        tokens_text = [t.text.lower() for t in doc]
        if 'it' in tokens_text and 'is' in tokens_text and 'that' in tokens_text:
            emphasis.append("cleft_sentence")
        
        return emphasis
    
    def _detect_negation(self, doc):
        """否定構造検出"""
        negation = []
        
        # 基本否定
        for token in doc:
            if token.dep_ == "neg":
                negation.append(f"simple_negation: {token.text}")
        
        # 否定副詞
        neg_adverbs = ['never', 'rarely', 'seldom', 'hardly', 'scarcely', 'barely']
        for token in doc:
            if token.text.lower() in neg_adverbs:
                negation.append(f"negative_adverb: {token.text}")
        
        # 否定句
        neg_phrases = ['not only', 'by no means', 'under no circumstances', 'in no way']
        sentence_lower = doc.text.lower()
        for phrase in neg_phrases:
            if phrase in sentence_lower:
                negation.append(f"negative_phrase: {phrase}")
        
        return negation
    
    def _detect_special_structures(self, doc):
        """特殊構造検出"""
        structures = []
        
        # 省略構造
        if len([t for t in doc if t.pos_ == "VERB"]) == 0:
            structures.append("ellipsis")
        
        # 感嘆構造
        if any(token.text in ['What', 'How'] for token in doc):
            structures.append("exclamation")
        
        # 疑問構造
        if doc.text.endswith('?'):
            structures.append("question")
        
        # 命令構造
        if doc[0].pos_ == "VERB" and len([t for t in doc if t.dep_ == "nsubj"]) == 0:
            structures.append("imperative")
        
        return structures
    
    def _calculate_complexity(self, result):
        """複雑度スコア計算"""
        score = 0
        
        # 語順の複雑さ
        if result['word_order'] != 'normal':
            score += 2
        
        # 時制の複雑さ
        if result['tense_aspect'] in ['present_perfect', 'past_perfect', 'conditional']:
            score += 2
        elif result['tense_aspect'] in ['progressive', 'future']:
            score += 1
        
        # 強調・否定
        score += len(result['emphasis']) * 1
        score += len(result['negation']) * 1
        
        # 特殊構造
        score += len(result['special_structures']) * 1
        
        return score
    
    def _print_analysis(self, result):
        """分析結果出力"""
        print(f"📊 基本パターン: {result['basic_pattern']}")
        print(f"📊 語順: {result['word_order']}")
        print(f"📊 時制・相: {result['tense_aspect']}")
        
        if result['emphasis']:
            print(f"📊 強調: {', '.join(result['emphasis'])}")
        
        if result['negation']:
            print(f"📊 否定: {', '.join(result['negation'])}")
        
        if result['special_structures']:
            print(f"📊 特殊構造: {', '.join(result['special_structures'])}")
        
        print(f"📊 複雑度スコア: {result['complexity_score']}")

def main():
    detector = ComprehensiveGrammarDetector()
    
    # テスト文
    test_sentences = [
        "Never have I seen such a beautiful sunset.",
        "Little did I know what would happen.",
        "Had I known earlier, I would have acted.",
        "Not only is he smart, but he is also kind.",
        "Rarely do we see such dedication.",
        "Under no circumstances should you do this.",
        "I have been working here for five years.",
        "She is extremely talented.",
        "What a beautiful day it is!",
        "Do tell me the truth.",
    ]
    
    results = []
    for sentence in test_sentences:
        result = detector.analyze_comprehensive_grammar(sentence)
        results.append(result)
    
    print("\n" + "="*80)
    print("📈 総合評価")
    print("="*80)
    
    # 複雑度別分類
    simple_sentences = [r for r in results if r['complexity_score'] <= 1]
    moderate_sentences = [r for r in results if 1 < r['complexity_score'] <= 3]
    complex_sentences = [r for r in results if r['complexity_score'] > 3]
    
    print(f"🟢 シンプル (スコア≤1): {len(simple_sentences)}")
    print(f"🟡 中程度 (スコア2-3): {len(moderate_sentences)}")  
    print(f"🔴 複雑 (スコア>3): {len(complex_sentences)}")
    
    # 現在のV4/V5.1では見逃される構造
    missed_structures = 0
    for result in results:
        if (result['word_order'] != 'normal' or 
            result['tense_aspect'] not in ['simple'] or
            result['emphasis'] or result['negation']):
            missed_structures += 1
    
    print(f"\n🚨 現在のシステムで見逃される複雑構造: {missed_structures}/{len(results)} ({missed_structures/len(results)*100:.1f}%)")

if __name__ == "__main__":
    main()
