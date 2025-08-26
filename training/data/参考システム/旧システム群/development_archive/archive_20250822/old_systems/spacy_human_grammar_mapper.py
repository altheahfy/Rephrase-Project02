#!/usr/bin/env python3
"""
spaCy辞書 + 人間文法認識システム
現在のシステムからの移植版
"""

import spacy
import logging
from typing import Dict, List, Any, Optional, Tuple

class SpacyHumanGrammarMapper:
    """
    spaCy辞書 + 人間文法認識による英語5文型スロット分解システム
    """
    
    def __init__(self):
        """初期化"""
        # spaCy辞書システム初期化
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy辞書システム初期化完了")
        except OSError:
            print("❌ spaCy英語モデルが見つかりません")
            raise
        
        # ログ設定
        self.logger = logging.getLogger(__name__)
        
        # 人間文法認識パラメータ
        self.confidence_threshold = 0.8
        
    def analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        文章を解析してRephraseスロット構造を生成
        
        Args:
            sentence (str): 解析対象の文章
            
        Returns:
            Dict[str, Any]: Rephraseスロット構造
        """
        try:
            # 1. spaCy語彙解析（辞書機能）
            lexical_info = self._extract_lexical_knowledge(sentence)
            
            # 2. 人間文法認識（構造認識）
            grammar_pattern = self._human_grammar_recognition(lexical_info)
            
            # 3. Rephraseスロット生成
            rephrase_slots = self._generate_rephrase_slots(lexical_info, grammar_pattern)
            
            return rephrase_slots
            
        except Exception as e:
            self.logger.error(f"文章解析エラー: {e}")
            return self._create_error_result(sentence, str(e))
    
    def _extract_lexical_knowledge(self, sentence: str) -> Dict[str, Any]:
        """
        spaCy辞書から語彙知識を抽出
        """
        doc = self.nlp(sentence)
        
        lexical_info = {
            'tokens': [],
            'sentence': sentence,
            'spacy_doc': doc
        }
        
        for token in doc:
            token_info = {
                'text': token.text,
                'pos': token.pos_,           # 主要品詞 (NOUN, VERB, etc.)
                'tag': token.tag_,           # 詳細品詞 (NNS, VBZ, etc.)
                'lemma': token.lemma_,       # 原形
                'morph': str(token.morph),   # 形態情報
                'is_stop': token.is_stop,    # ストップワード
                'is_alpha': token.is_alpha,  # アルファベット
                'index': token.i             # 位置
            }
            lexical_info['tokens'].append(token_info)
        
        self.logger.info(f"語彙解析完了: {len(lexical_info['tokens'])}語彙")
        return lexical_info
    
    def _human_grammar_recognition(self, lexical_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        人間文法認識による構造パターン検出
        優先順位: 複雑な文型（SVOO, SVOC）→ 単純な文型（SVO, SVC, SV）
        """
        tokens = lexical_info['tokens']
        
        # 優先順位順に検出（複雑→単純）
        
        # 第5文型（SVOC）検出 - 最優先
        svoc_result = self._detect_svoc_pattern_human(tokens)
        if svoc_result['detected']:
            return svoc_result
        
        # 第4文型（SVOO）検出
        svoo_result = self._detect_svoo_pattern_human(tokens)
        if svoo_result['detected']:
            return svoo_result
        
        # 第3文型（SVO）検出
        svo_result = self._detect_svo_pattern_human(tokens)
        if svo_result['detected']:
            return svo_result
        
        # 第2文型（SVC）検出
        svc_result = self._detect_svc_pattern_human(tokens)
        if svc_result['detected']:
            return svc_result
        
        # 第1文型（SV）検出 - 最後
        sv_result = self._detect_sv_pattern_human(tokens)
        if sv_result['detected']:
            return sv_result
        
        # デフォルト結果
        return {
            'detected': False,
            'pattern': 'UNKNOWN',
            'confidence': 0.0,
            'elements': {},
            'error': '文型パターンを認識できませんでした'
        }
    
    def _detect_sv_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        第1文型（SV）人間文法認識
        
        人間の認識: [主語] + [自動詞] = 第1文型
        """
        if len(tokens) < 2:
            return {'detected': False, 'pattern': 'SV', 'confidence': 0.0}
        
        # 基本パターン: 2語（主語 + 動詞）
        if len(tokens) == 2:
            token1, token2 = tokens[0], tokens[1]
            
            # 主語候補判定（人間基準）
            is_subject = self._is_subject_human(token1)
            # 自動詞候補判定（人間基準）
            is_intransitive_verb = self._is_intransitive_verb_human(token2)
            
            if is_subject and is_intransitive_verb:
                return {
                    'detected': True,
                    'pattern': 'SV',
                    'confidence': 0.95,
                    'elements': {
                        'subject': token1,
                        'verb': token2
                    },
                    'slots': ['S', 'V'],
                    'slot_phrases': [token1['text'], token2['text']]
                }
        
        # 3語パターン: 冠詞 + 名詞 + 動詞
        elif len(tokens) == 3:
            token1, token2, token3 = tokens[0], tokens[1], tokens[2]
            
            # The dog runs パターン
            if (self._is_determiner_human(token1) and 
                self._is_noun_human(token2) and 
                self._is_intransitive_verb_human(token3)):
                
                return {
                    'detected': True,
                    'pattern': 'SV',
                    'confidence': 0.90,
                    'elements': {
                        'subject': f"{token1['text']} {token2['text']}",
                        'verb': token3
                    },
                    'slots': ['S', 'V'],
                    'slot_phrases': [f"{token1['text']} {token2['text']}", token3['text']]
                }
        
        return {'detected': False, 'pattern': 'SV', 'confidence': 0.0}
    
    def _detect_svc_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        第2文型（SVC）人間文法認識
        
        人間の認識: [主語] + [連結動詞] + [補語] = 第2文型
        """
        # 句読点を除外したトークンリストを作成
        content_tokens = [t for t in tokens if t['pos'] != 'PUNCT']
        
        if len(content_tokens) < 3:
            return {'detected': False, 'pattern': 'SVC', 'confidence': 0.0}
        
        # 3語パターン: S + 連結動詞 + C
        if len(content_tokens) == 3:
            subject, verb, complement = content_tokens[0], content_tokens[1], content_tokens[2]
            
            if (self._is_subject_human(subject) and 
                self._is_linking_verb_human(verb) and 
                self._is_complement_human(complement)):
                
                return {
                    'detected': True,
                    'pattern': 'SVC',
                    'confidence': 0.95,
                    'elements': {
                        'subject': subject,
                        'verb': verb,
                        'complement': complement
                    },
                    'slots': ['S', 'V', 'C'],
                    'slot_phrases': [subject['text'], verb['text'], complement['text']]
                }
        
        # 4語パターン: The + 名詞 + 連結動詞 + 補語
        elif len(content_tokens) == 4:
            det, noun, verb, complement = content_tokens[0], content_tokens[1], content_tokens[2], content_tokens[3]
            
            if (self._is_determiner_human(det) and 
                self._is_noun_human(noun) and 
                self._is_linking_verb_human(verb) and 
                self._is_complement_human(complement)):
                
                subject_text = f"{det['text']} {noun['text']}"
                
                return {
                    'detected': True,
                    'pattern': 'SVC',
                    'confidence': 0.90,
                    'elements': {
                        'subject': subject_text,
                        'verb': verb,
                        'complement': complement
                    },
                    'slots': ['S', 'V', 'C'],
                    'slot_phrases': [subject_text, verb['text'], complement['text']]
                }
        
        return {'detected': False, 'pattern': 'SVC', 'confidence': 0.0}
    
    def _detect_svo_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第3文型（SVO）人間文法認識 - 主語 + 他動詞 + 目的語"""
        if len(tokens) < 3:
            return {'detected': False, 'pattern': 'SVO', 'confidence': 0.0}
        
        # 基本パターン: S + V + O
        for i in range(len(tokens) - 2):
            if (self._is_subject_human(tokens[i]) and 
                self._is_transitive_verb_human(tokens[i + 1]) and 
                self._is_object_human(tokens[i + 2])):
                
                return {
                    'detected': True,
                    'pattern': 'SVO',
                    'confidence': 0.90,
                    'elements': {
                        'subject': tokens[i],
                        'verb': tokens[i + 1],
                        'object': tokens[i + 2]
                    },
                    'slots': ['S', 'V', 'O'],
                    'slot_phrases': [tokens[i]['text'], tokens[i + 1]['text'], tokens[i + 2]['text']]
                }
        
        return {'detected': False, 'pattern': 'SVO', 'confidence': 0.0}
    
    def _detect_svoo_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """第4文型（SVOO）人間文法認識 - 主語 + 動詞 + 間接目的語 + 直接目的語"""
        if len(tokens) < 4:
            return {'detected': False, 'pattern': 'SVOO', 'confidence': 0.0}
        
        # 基本パターン: S + V + O1 + O2
        for i in range(len(tokens) - 3):
            if (self._is_subject_human(tokens[i]) and 
                self._is_ditransitive_verb_human(tokens[i + 1]) and 
                self._is_object_human(tokens[i + 2]) and 
                self._is_object_human(tokens[i + 3])):
                
                return {
                    'detected': True,
                    'pattern': 'SVOO',
                    'confidence': 0.85,
                    'elements': {
                        'subject': tokens[i],
                        'verb': tokens[i + 1],
                        'indirect_object': tokens[i + 2],
                        'direct_object': tokens[i + 3]
                    },
                    'slots': ['S', 'V', 'O', 'O'],
                    'slot_phrases': [tokens[i]['text'], tokens[i + 1]['text'], tokens[i + 2]['text'], tokens[i + 3]['text']]
                }
        
        return {'detected': False, 'pattern': 'SVOO', 'confidence': 0.0}
    
    def _detect_svoc_pattern_human(self, tokens: List[Dict]) -> Dict[str, Any]:
        """
        第5文型（SVOC）人間文法認識
        
        人間の認識: [主語] + [使役動詞] + [目的語] + [補語] = 第5文型
        """
        if len(tokens) < 4:
            return {'detected': False, 'pattern': 'SVOC', 'confidence': 0.0}
        
        # 4語パターン: S + V + O + C
        if len(tokens) == 4:
            subject, verb, obj, complement = tokens[0], tokens[1], tokens[2], tokens[3]
            
            if (self._is_subject_human(subject) and 
                self._is_factitive_verb_human(verb) and 
                self._is_object_human(obj) and 
                self._is_complement_human(complement)):
                
                return {
                    'detected': True,
                    'pattern': 'SVOC',
                    'confidence': 0.90,
                    'elements': {
                        'subject': subject,
                        'verb': verb,
                        'object': obj,
                        'complement': complement
                    },
                    'slots': ['S', 'V', 'O', 'C'],
                    'slot_phrases': [subject['text'], verb['text'], obj['text'], complement['text']]
                }
        
        # 5語パターン: S + V + the + O + C
        elif len(tokens) == 5:
            subject, verb, det, obj, complement = tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]
            
            if (self._is_subject_human(subject) and 
                self._is_factitive_verb_human(verb) and 
                self._is_determiner_human(det) and 
                self._is_noun_human(obj) and 
                self._is_complement_human(complement)):
                
                object_text = f"{det['text']} {obj['text']}"
                
                return {
                    'detected': True,
                    'pattern': 'SVOC',
                    'confidence': 0.85,
                    'elements': {
                        'subject': subject,
                        'verb': verb,
                        'object': object_text,
                        'complement': complement
                    },
                    'slots': ['S', 'V', 'O', 'C'],
                    'slot_phrases': [subject['text'], verb['text'], object_text, complement['text']]
                }
        
        return {'detected': False, 'pattern': 'SVOC', 'confidence': 0.0}
    
    # 人間基準判定関数群
    def _is_subject_human(self, token: Dict) -> bool:
        """人間基準での主語判定"""
        return token['pos'] in ['NOUN', 'PRON', 'PROPN']
    
    def _is_noun_human(self, token: Dict) -> bool:
        """人間基準での名詞判定"""
        return token['pos'] in ['NOUN', 'PROPN']
    
    def _is_determiner_human(self, token: Dict) -> bool:
        """人間基準での冠詞・限定詞判定"""
        return token['pos'] == 'DET'
    
    def _is_intransitive_verb_human(self, token: Dict) -> bool:
        """人間基準での自動詞判定"""
        return token['pos'] == 'VERB' and token['tag'] in ['VBP', 'VBZ', 'VB']
    
    def _is_be_verb_human(self, token: Dict) -> bool:
        """人間基準でのbe動詞判定"""
        return (token['pos'] in ['AUX', 'VERB'] and 
                token['lemma'].lower() in ['be', 'am', 'is', 'are', 'was', 'were'])
    
    def _is_linking_verb_human(self, token: Dict) -> bool:
        """人間基準での連結動詞判定（be動詞 + その他連結動詞）"""
        linking_verbs = {
            'be', 'am', 'is', 'are', 'was', 'were',  # be動詞
            'become', 'became', 'get', 'seem', 'appear', 'look', 'sound', 
            'feel', 'taste', 'smell', 'remain', 'stay', 'turn', 'grow'
        }
        return (token['pos'] in ['AUX', 'VERB'] and 
                token['lemma'].lower() in linking_verbs)
    
    def _is_transitive_verb_human(self, token: Dict) -> bool:
        """人間基準での他動詞判定"""
        return token['pos'] == 'VERB' and token['tag'] in ['VBP', 'VBZ', 'VB', 'VBD']
    
    def _is_ditransitive_verb_human(self, token: Dict) -> bool:
        """人間基準での授与動詞判定（give, tell, show等）"""
        ditransitive_verbs = {
            'give', 'tell', 'show', 'send', 'teach', 'offer', 'bring',
            'buy', 'bought', 'get', 'pass', 'hand', 'lend', 'sell', 'pay'
        }
        return (token['pos'] == 'VERB' and 
                token['lemma'].lower() in ditransitive_verbs)
    
    def _is_factitive_verb_human(self, token: Dict) -> bool:
        """人間基準での使役動詞判定（make, call, consider等）"""
        factitive_verbs = {
            'make', 'call', 'consider', 'find', 'keep', 'leave',
            'paint', 'color', 'dye', 'name', 'elect', 'choose'
        }
        return (token['pos'] == 'VERB' and 
                token['lemma'].lower() in factitive_verbs)
    
    def _is_object_human(self, token: Dict) -> bool:
        """人間基準での目的語判定"""
        return token['pos'] in ['NOUN', 'PRON', 'PROPN']
    
    def _is_complement_human(self, token: Dict) -> bool:
        """人間基準での補語判定"""
        # 基本的な補語品詞
        if token['pos'] in ['ADJ', 'NOUN', 'PROPN']:
            return True
        
        # 色名は名詞でも補語として機能
        color_words = {
            'red', 'blue', 'green', 'yellow', 'black', 'white', 
            'brown', 'pink', 'purple', 'orange', 'gray', 'grey'
        }
        if token['lemma'].lower() in color_words:
            return True
        
        return False
    
    def _generate_rephrase_slots(self, lexical_info: Dict, grammar_pattern: Dict) -> Dict[str, Any]:
        """
        Rephraseスロット構造生成（現在システム互換）
        """
        if not grammar_pattern['detected']:
            return self._create_error_result(lexical_info['sentence'], 
                                           grammar_pattern.get('error', '文型認識失敗'))
        
        # Rephrase完全互換スロット構造
        slots = grammar_pattern['slots']
        slot_phrases = grammar_pattern['slot_phrases']
        
        result = {
            'Slot': slots,
            'SlotPhrase': slot_phrases,
            'Slot_display_order': list(range(1, len(slots) + 1)),
            'display_order': list(range(1, len(slots) + 1)),
            'PhraseType': self._determine_phrase_types(slots),
            'SubslotID': list(range(len(slots))),
            
            # 解析情報
            'pattern_detected': grammar_pattern['pattern'],
            'confidence': grammar_pattern['confidence'],
            'analysis_method': 'spacy_human_grammar',
            'lexical_tokens': len(lexical_info['tokens'])
        }
        
        return result
    
    def _determine_phrase_types(self, slots: List[str]) -> List[str]:
        """スロットに対応する句型を決定"""
        phrase_types = []
        for slot in slots:
            if slot == 'S':
                phrase_types.append('名詞句')
            elif slot == 'V':
                phrase_types.append('動詞句')
            elif slot == 'O':
                phrase_types.append('名詞句')
            elif slot == 'C':
                phrase_types.append('補語句')
            else:
                phrase_types.append('未分類')
        return phrase_types
    
    def _create_error_result(self, sentence: str, error_msg: str) -> Dict[str, Any]:
        """エラー結果生成"""
        return {
            'Slot': [],
            'SlotPhrase': [],
            'Slot_display_order': [],
            'display_order': [],
            'PhraseType': [],
            'SubslotID': [],
            'error': error_msg,
            'sentence': sentence,
            'analysis_method': 'spacy_human_grammar'
        }

def test_spacy_human_grammar_system():
    """spaCy人間文法認識システムのテスト"""
    print("=== spaCy辞書 + 人間文法認識システム 5文型テスト ===\n")
    
    # システム初期化
    mapper = SpacyHumanGrammarMapper()
    
    # 5文型テスト文章
    test_sentences = [
        # 第1文型（SV）
        "Children play",
        "The dog runs", 
        "Birds fly",
        
        # 第2文型（SVC）
        "She is happy",
        "The book is interesting",
        "He became a doctor",
        
        # 第3文型（SVO）
        "I like apples",
        "She reads books",
        "They watch movies",
        
        # 第4文型（SVOO）
        "I give him a book",
        "She told me the truth",
        "He showed us the way",
        
        # 第5文型（SVOC）
        "We call him Tom",
        "I consider her smart",
        "They made me happy"
    ]
    
    results = {}
    total_success = 0
    
    for sentence in test_sentences:
        print(f"--- '{sentence}' ---")
        result = mapper.analyze_sentence(sentence)
        
        if 'error' in result:
            print(f"❌ エラー: {result['error']}")
            results[sentence] = 'FAILED'
        else:
            print(f"✅ パターン: {result['pattern_detected']}")
            print(f"   確信度: {result['confidence']:.1%}")
            print(f"   スロット: {result['Slot']}")
            print(f"   句: {result['SlotPhrase']}")
            print(f"   句型: {result['PhraseType']}")
            results[sentence] = 'SUCCESS'
            total_success += 1
        print()
    
    # 統計表示
    success_rate = total_success / len(test_sentences) * 100
    print(f"=== 5文型認識結果統計 ===")
    print(f"成功率: {success_rate:.1f}% ({total_success}/{len(test_sentences)})")
    
    # パターン別統計
    patterns = {'SV': 0, 'SVC': 0, 'SVO': 0, 'SVOO': 0, 'SVOC': 0}
    for sentence, status in results.items():
        if status == 'SUCCESS':
            result = mapper.analyze_sentence(sentence)
            pattern = result['pattern_detected']
            patterns[pattern] += 1
    
    print("\nパターン別成功数:")
    for pattern, count in patterns.items():
        print(f"  {pattern}: {count}個")
    
    return results

def interactive_test():
    """インタラクティブテスト機能"""
    print("=== spaCy人間文法認識システム - インタラクティブテスト ===")
    print("文章を入力してエンターを押してください（'quit'で終了）")
    print()
    
    mapper = SpacyHumanGrammarMapper()
    
    while True:
        try:
            sentence = input("📝 文章を入力: ").strip()
            
            if sentence.lower() in ['quit', 'exit', 'q']:
                print("テストを終了します。")
                break
            
            if not sentence:
                print("❌ 文章を入力してください。")
                continue
            
            print(f"\n--- 解析中: '{sentence}' ---")
            
            # 解析実行
            result = mapper.analyze_sentence(sentence)
            
            if 'error' in result:
                print(f"❌ エラー: {result['error']}")
            else:
                print("✅ 解析成功!")
                print(f"   🔍 検出パターン: {result['pattern_detected']}")
                print(f"   📊 確信度: {result['confidence']:.1%}")
                print(f"   🏷️  スロット: {result['Slot']}")
                print(f"   📝 スロット句: {result['SlotPhrase']}")
                print(f"   🏗️  句型: {result['PhraseType']}")
                
                # 語彙解析詳細
                print("\n   📚 語彙解析詳細:")
                lexical_info = mapper._extract_lexical_knowledge(sentence)
                for token in lexical_info['tokens']:
                    print(f"      {token['text']}: {token['pos']} ({token['tag']}) [lemma: {token['lemma']}]")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\nテストを中断しました。")
            break
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test()
    else:
        test_spacy_human_grammar_system()
