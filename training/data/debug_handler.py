#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BasicFivePatternHandler デバッグ版
"""

import spacy
from typing import Dict, Any, List, Optional

class DebugBasicFivePatternHandler:
    """5文型用デバッグ版ハンドラー"""
    
    def __init__(self):
        """初期化"""
        self.nlp = spacy.load('en_core_web_sm')
        
        # 5文型パターン定義
        self.patterns = {
            'SV': ['S', 'V'],                    # 第1文型
            'SVC': ['S', 'V', 'C1'],             # 第2文型  
            'SVO': ['S', 'V', 'O1'],             # 第3文型
            'SVOO': ['S', 'V', 'O1', 'O2'],      # 第4文型
            'SVOC': ['S', 'V', 'O1', 'C2']       # 第5文型
        }
        
        # 文型判定用動詞分類
        self.verb_types = {
            'linking': ['be', 'seem', 'become', 'appear', 'look', 'sound', 'feel', 'taste', 'smell', 'remain', 'stay', 'turn', 'grow'],
            'transitive': ['love', 'like', 'see', 'hear', 'make', 'take', 'give', 'send', 'show', 'read', 'play', 'study'],
            'ditransitive': ['give', 'send', 'show', 'tell', 'teach', 'buy', 'make', 'get', 'find', 'offer'],
            'causative': ['make', 'let', 'have', 'get', 'help', 'see', 'hear', 'watch', 'call', 'find', 'consider']
        }
    
    def process(self, text: str) -> Dict[str, Any]:
        """処理メイン（デバッグ版）"""
        print(f"🔍 デバッグ処理開始: {text}")
        
        try:
            doc = self.nlp(text)
            print(f"📊 Token詳細:")
            for i, token in enumerate(doc):
                print(f"  [{i}] {token.text:>8} | {token.pos_:>8} | {token.tag_:>12} | {token.lemma_}")
            
            # 基本要素抽出
            elements = self._extract_basic_elements_debug(doc)
            print(f"📋 抽出要素: {elements}")
            
            # パターン識別
            pattern = self._identify_pattern(elements, doc)
            print(f"🎯 識別パターン: {pattern}")
            
            return {
                'success': True,
                'slots': elements,
                'pattern_type': pattern,
                'debug_info': {
                    'tokens': [(t.text, t.pos_, t.lemma_) for t in doc]
                }
            }
            
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            return {
                'success': False,
                'error': str(e),
                'slots': {}
            }
    
    def _extract_basic_elements_debug(self, doc) -> Dict[str, str]:
        """基本要素抽出（デバッグ版）"""
        print(f"🔧 基本要素抽出開始")
        elements = {}
        
        # 主語候補（文頭の名詞句全体を抽出）
        subject_tokens = []
        for token in doc:
            print(f"  主語処理: {token.text} ({token.pos_})")
            if token.pos_ in ['DET', 'ADJ', 'NOUN', 'PRON', 'PROPN']:
                subject_tokens.append(token.text)
                print(f"    → 主語候補に追加")
            elif token.pos_ in ['VERB', 'AUX']:
                print(f"    → 動詞発見、主語終了")
                break  # 動詞に到達したら主語終了
            elif subject_tokens:  # 主語候補があり、動詞以外に到達したら終了
                print(f"    → 主語終了")
                break
        
        if subject_tokens:
            elements['S'] = ' '.join(subject_tokens)
            print(f"✅ 主語: {elements['S']}")
        
        # 動詞抽出と位置特定
        verb_idx = None
        for i, token in enumerate(doc):
            print(f"  動詞処理: {token.text} ({token.pos_}, lemma={token.lemma_})")
            if token.pos_ == 'VERB' and not token.lemma_ in ['be']:
                elements['V'] = token.text
                verb_idx = i
                print(f"    → メイン動詞発見: {token.text} (位置{i})")
                break
            elif token.pos_ == 'AUX' and token.lemma_ == 'be':
                elements['V'] = token.text
                verb_idx = i
                print(f"    → be動詞発見: {token.text} (位置{i})")
                break
        
        if verb_idx is None:
            print(f"❌ 動詞が見つかりません")
            return elements
        
        # 動詞後の要素を詳細分析
        post_verb_tokens = [token for token in doc[verb_idx + 1:] if token.pos_ != 'PUNCT']
        print(f"📝 動詞後トークン: {[t.text for t in post_verb_tokens]}")
        
        if not post_verb_tokens:
            print(f"ℹ️ 動詞後要素なし")
            return elements
        
        # 動詞の種類判定（連結動詞かどうか）
        verb_lemma = doc[verb_idx].lemma_
        is_linking_verb = verb_lemma in self.verb_types['linking']
        print(f"🔗 動詞判定: {verb_lemma} → 連結動詞: {is_linking_verb}")
        
        # 要素分類
        elements_found = []
        current_phrase = []
        
        for token in post_verb_tokens:
            print(f"  後処理: {token.text} ({token.pos_})")
            if token.pos_ in ['DET', 'ADJ', 'NOUN', 'PRON', 'PROPN']:
                current_phrase.append(token.text)
                print(f"    → 句に追加: {current_phrase}")
            elif current_phrase:  # 句の終了
                phrase_text = ' '.join(current_phrase)
                print(f"    → 句終了: {phrase_text}")
                
                # 最後のトークンのPOSで判定
                last_token_pos = None
                for t in post_verb_tokens:
                    if t.text == current_phrase[-1]:
                        last_token_pos = t.pos_
                        break
                
                print(f"    → 最後のトークンPOS: {last_token_pos}")
                
                if last_token_pos == 'ADJ':
                    elements_found.append(('ADJ', phrase_text))
                    print(f"    → ADJ要素として記録")
                else:
                    elements_found.append(('NOUN', phrase_text))
                    print(f"    → NOUN要素として記録")
                current_phrase = []
        
        # 最後の句を処理
        if current_phrase:
            phrase_text = ' '.join(current_phrase)
            print(f"  最終句処理: {phrase_text}")
            
            last_token_pos = None
            for t in post_verb_tokens:
                if t.text == current_phrase[-1]:
                    last_token_pos = t.pos_
                    break
            
            print(f"    → 最後のトークンPOS: {last_token_pos}")
            
            if last_token_pos == 'ADJ':
                elements_found.append(('ADJ', phrase_text))
                print(f"    → ADJ要素として記録")
            else:
                elements_found.append(('NOUN', phrase_text))
                print(f"    → NOUN要素として記録")
        
        print(f"📊 発見要素: {elements_found}")
        
        # 文型判定とスロット配置
        noun_count = len([e for e in elements_found if e[0] == 'NOUN'])
        adj_count = len([e for e in elements_found if e[0] == 'ADJ'])
        
        print(f"📈 要素数: NOUN={noun_count}, ADJ={adj_count}")
        print(f"🔗 連結動詞: {is_linking_verb}")
        
        if is_linking_verb and adj_count > 0:
            # 第2文型: 連結動詞 + 形容詞
            adj_elements = [e[1] for e in elements_found if e[0] == 'ADJ']
            elements['C1'] = adj_elements[0]
            print(f"✅ 第2文型(形容詞補語): C1={elements['C1']}")
            
        elif is_linking_verb and noun_count > 0:
            # 第2文型: 連結動詞 + 名詞（補語）
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['C1'] = noun_elements[0]
            print(f"✅ 第2文型(名詞補語): C1={elements['C1']}")
            
        elif noun_count == 1 and adj_count == 0:
            # 第3文型: 他動詞 + 目的語
            noun_elements = [e[1] for e in elements_found if e[0] == 'NOUN']
            elements['O1'] = noun_elements[0]
            print(f"✅ 第3文型: O1={elements['O1']}")
            
        else:
            print(f"ℹ️ その他のパターン（実装中）")
        
        print(f"🎯 最終要素: {elements}")
        return elements
    
    def _identify_pattern(self, elements: Dict[str, str], doc) -> Optional[str]:
        """パターン識別"""
        if 'S' in elements and 'V' in elements:
            if 'C1' in elements:
                return 'SVC'  # 第2文型
            elif 'O1' in elements:
                if 'O2' in elements:
                    return 'SVOO'  # 第4文型
                elif 'C2' in elements:
                    return 'SVOC'  # 第5文型
                else:
                    return 'SVO'  # 第3文型
            else:
                return 'SV'   # 第1文型
        return None

# テスト実行
if __name__ == "__main__":
    handler = DebugBasicFivePatternHandler()
    result = handler.process("She looks happy.")
    print(f"\n🎯 最終結果: {result}")
