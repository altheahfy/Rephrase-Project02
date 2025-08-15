#!/usr/bin/env python3
"""
Participial Construction Engine - 分詞構文処理
Stanzaの構造を活用した分詞構文の完全分解（統合型）

核心原則:
1. advcl関係の分詞動詞を検出
2. 現在分詞(VBG)と過去分詞(VBN/ADJ)の区別  
3. 分詞句全体の上位スロット配置
4. 分詞句内部のサブスロット分解
5. 主節要素との統合処理
"""

import stanza
from typing import Dict, List, Optional, Any

class ParticipleEngine:
    """分詞構文エンジン（統合型）"""
    
    def __init__(self):
        print("🚀 分詞構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 分詞構文の種類分類
        self.participle_types = {
            'present': ['VBG'],  # 現在分詞: running, walking
            'past': ['VBN', 'ADJ'],  # 過去分詞: tired, surprised (形容詞化も含む)
            'perfect': ['VBG']  # 完了分詞: having + VBN
        }
        
        # 上位スロット配置規則
        self.slot_mapping = {
            'temporal': 'M3',     # 時間的分詞構文
            'causal': 'M1',       # 理由的分詞構文  
            'conditional': 'M1',  # 条件的分詞構文
            'general': 'M1'       # 一般的分詞構文
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """メイン処理 - 統合型完全分解"""
        print(f"🔍 分詞構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 分詞構文の構造解析
        participle_info = self._analyze_participle_structure(sent)
        
        if participle_info:
            return self._process_complete_participle_construction(sent, participle_info)
        else:
            return self._process_simple_sentence(sent)
    
    def _analyze_participle_structure(self, sent) -> Optional[Dict]:
        """分詞構文の構造分析"""
        structure_info = {
            'participle_verb': None,    # 分詞動詞
            'main_verb': None,         # 主動詞
            'participle_type': None,   # 分詞の種類
            'participle_phrase': [],   # 分詞句全体
        }
        
        # 1. advcl関係の分詞動詞を検出
        for word in sent.words:
            if word.deprel == 'advcl':
                print(f"    🔍 advcl検出: {word.text} ({word.upos}), lemma: {word.lemma}")
                # 分詞かどうか確認（より寛容な条件）
                is_participle = (
                    word.upos in ['VBG', 'VBN', 'VERB'] or  # VERB も含める
                    (word.upos == 'ADJ' and self._is_participial_adjective(word, sent))
                )
                
                if is_participle:
                    structure_info['participle_verb'] = word
                    structure_info['participle_type'] = self._classify_participle_type(word, sent)
                    
                    # 主動詞を特定（advcl の head）
                    if word.head > 0:
                        structure_info['main_verb'] = sent.words[word.head - 1]
                    
                    # 分詞句の範囲を特定
                    structure_info['participle_phrase'] = self._extract_participle_phrase(sent, word)
                    
                    print(f"  📋 分詞構文検出:")
                    print(f"    分詞動詞: {word.text} ({word.upos}) - {structure_info['participle_type']}")
                    print(f"    主動詞: {structure_info['main_verb'].text if structure_info['main_verb'] else '?'}")
                    print(f"    分詞句: {' '.join([w.text for w in structure_info['participle_phrase']])}")
                    return structure_info
                else:
                    print(f"    ❌ 分詞ではない: {word.text} ({word.upos})")
        
        return None
    
    def _is_participial_adjective(self, word, sent) -> bool:
        """形容詞が分詞由来かどうか判定"""
        # 簡易的な判定：一般的な分詞形容詞
        participial_adjectives = {
            'tired', 'surprised', 'excited', 'interested', 'bored', 
            'confused', 'worried', 'amazed', 'shocked', 'pleased'
        }
        return word.lemma.lower() in participial_adjectives
    
    def _classify_participle_type(self, word, sent) -> str:
        """分詞の種類を分類"""
        # lemma による判定を追加
        lemma = word.lemma.lower()
        
        # 現在分詞の判定（-ing形）
        if word.text.endswith('ing') or word.upos == 'VBG':
            # having + VBN の完了分詞構文かチェック
            if lemma == 'have':
                # 次の語が VBN かチェック
                for child_word in sent.words:
                    if child_word.head == word.id and child_word.upos == 'VBN':
                        return 'perfect'
            return 'present'
            
        # 過去分詞の判定（-ed形や不規則活用）
        elif word.upos in ['VBN', 'ADJ'] or self._is_past_participle_form(word.text):
            return 'past'
            
        # VERB タグで分詞の場合
        elif word.upos == 'VERB':
            if word.text.endswith('ing'):
                return 'present'
            elif self._is_past_participle_form(word.text):
                return 'past'
        
        return 'unknown'
    
    def _is_past_participle_form(self, word_text: str) -> bool:
        """過去分詞形かどうか判定"""
        # 一般的な過去分詞形の語尾
        past_participle_endings = ['ed', 'en', 'n', 't']
        # 不規則動詞の過去分詞（例）
        irregular_past_participles = {
            'surprised', 'tired', 'excited', 'broken', 'written', 'taken', 'given',
            'seen', 'done', 'gone', 'come', 'run', 'sung', 'drunk', 'begun'
        }
        
        word_lower = word_text.lower()
        return (any(word_lower.endswith(ending) for ending in past_participle_endings) or
                word_lower in irregular_past_participles)
    
    def _extract_participle_phrase(self, sent, participle_verb) -> List:
        """分詞句の範囲を抽出"""
        phrase_words = []
        
        # 分詞動詞自体を追加
        phrase_words.append(participle_verb)
        
        # 分詞動詞に依存する語を再帰的に収集
        def collect_dependents(head_id):
            dependents = []
            for word in sent.words:
                if word.head == head_id:
                    dependents.append(word)
                    # 再帰的に孫も収集
                    dependents.extend(collect_dependents(word.id))
            return dependents
        
        dependents = collect_dependents(participle_verb.id)
        phrase_words.extend(dependents)
        
        # 語順でソート
        phrase_words.sort(key=lambda w: w.id)
        
        # カンマまでの範囲で切る
        filtered_words = []
        for word in phrase_words:
            if word.text == ',':
                break
            filtered_words.append(word)
        
        return filtered_words
    
    def _process_complete_participle_construction(self, sent, participle_info) -> Dict[str, str]:
        """分詞構文の完全処理 - 統合型"""
        participle_verb = participle_info['participle_verb']
        main_verb = participle_info['main_verb']
        participle_type = participle_info['participle_type']
        phrase_words = participle_info['participle_phrase']
        
        result = {}
        
        print(f"  🎯 統合処理開始: {participle_type}分詞構文")
        
        # 1. 分詞句全体を上位スロットに配置
        participle_phrase = self._build_complete_participle_phrase(sent, participle_info)
        upper_slot = self._determine_upper_slot_position(participle_info, sent)
        
        if upper_slot:
            result[upper_slot] = participle_phrase
            print(f"    上位配置: {upper_slot} = '{participle_phrase}'")
        
        # 2. 分詞句をサブスロットに分解
        sub_elements = self._decompose_participle_phrase_to_subslots(sent, participle_verb, phrase_words)
        result.update(sub_elements)
        
        # 3. 主節の他の要素を処理
        if main_verb:
            main_elements = self._extract_main_clause_elements(sent, main_verb, phrase_words)
            result.update(main_elements)
        
        print(f"  ✅ 統合型完全分解: {result}")
        return result
    
    def _build_complete_participle_phrase(self, sent, participle_info) -> str:
        """分詞句全体を構築"""
        phrase_words = participle_info['participle_phrase']
        phrase_parts = []
        
        # 分詞句の語を順序通りに追加
        for word in phrase_words:
            phrase_parts.append(word.text)
        
        return ' '.join(phrase_parts).lower()
    
    def _determine_upper_slot_position(self, participle_info, sent) -> str:
        """上位スロット位置の決定"""
        # 分詞構文の意味的分類
        participle_verb = participle_info['participle_verb']
        participle_type = participle_info['participle_type']
        
        # 時間的表現を含む場合はM3
        if self._has_time_expression(participle_info['participle_phrase']):
            return 'M3'
        
        # 理由・原因を表す場合はM1
        if participle_type in ['past', 'perfect']:
            return 'M1'
        
        # 一般的な分詞構文はM1
        return 'M1'
    
    def _has_time_expression(self, phrase_words) -> bool:
        """時間表現を含むかチェック"""
        time_indicators = ['when', 'while', 'after', 'before', 'during', 'yesterday', 'today', 'now']
        phrase_text = ' '.join([w.text.lower() for w in phrase_words])
        return any(indicator in phrase_text for indicator in time_indicators)
    
    def _process_participle_construction(self, sent, participle_info) -> Dict[str, str]:
        """分詞構文の処理 - Rephraseルール準拠"""
        participle_verb = participle_info['participle_verb']
        main_verb = participle_info['main_verb']
        participle_type = participle_info['participle_type']
        phrase_words = participle_info['participle_phrase']
        
        result = {}
        
        # 1. 上位スロット判定 - 分詞構文はM1位置
        print(f"  📍 分詞構文 → M1位置（サブスロット展開）")
        
        # 2. 分詞句をサブスロットに分解
        sub_elements = self._decompose_participle_phrase_to_subslots(sent, participle_verb, phrase_words)
        result.update(sub_elements)
        
        # 3. 主節の処理
        if main_verb:
            main_elements = self._extract_main_clause_elements(sent, main_verb, phrase_words)
            result.update(main_elements)
        
        print(f"  ✅ Rephraseルール準拠分解: {result}")
        return result
    
    def _decompose_participle_phrase_to_subslots(self, sent, participle_verb, phrase_words) -> Dict[str, str]:
        """分詞句をサブスロットに分解 - 正確なRephraseルール適用"""
        sub_elements = {}
        phrase_ids = {w.id for w in phrase_words}
        
        # 1. 分詞動詞の処理
        sub_elements['sub-v'] = participle_verb.text.lower()
        
        # 2. having の処理（aux として依存している場合）
        for word in sent.words:
            if word.id in phrase_ids and word.head == participle_verb.id and word.deprel == 'aux':
                if word.text.lower() == 'having':
                    sub_elements['sub-aux'] = word.text.lower()
        
        # 3. 前置詞句の処理
        prep_phrases = self._extract_prepositional_phrases(sent, participle_verb, phrase_ids)
        if prep_phrases:
            # 最初の前置詞句を sub-m2 に
            sub_elements['sub-m2'] = prep_phrases[0]
        
        # 4. 目的語・補語の処理
        for word in sent.words:
            if word.id in phrase_ids and word.id != participle_verb.id:
                if word.head == participle_verb.id:
                    if word.deprel == 'obj':
                        sub_elements['sub-o1'] = word.text.lower()
                    elif word.deprel == 'iobj':
                        sub_elements['sub-o2'] = word.text.lower()
                    elif word.deprel in ['advmod'] and not prep_phrases:
                        # 前置詞句以外の副詞（fastなど）
                        if 'sub-m1' not in sub_elements:
                            sub_elements['sub-m1'] = word.text.lower()
                        else:
                            sub_elements['sub-m2'] = word.text.lower()
        
        return sub_elements
    
    def _extract_prepositional_phrases(self, sent, participle_verb, phrase_ids) -> List[str]:
        """前置詞句を抽出"""
        prep_phrases = []
        
        # 分詞動詞に依存する前置詞句を探す
        for word in sent.words:
            if word.id in phrase_ids and word.head == participle_verb.id:
                if word.deprel in ['obl', 'nmod', 'obl:agent']:
                    # この語から前置詞句を構築
                    phrase = self._build_prepositional_phrase_v2(sent, word, phrase_ids)
                    prep_phrases.append(phrase)
        
        return prep_phrases
    
    def _build_prepositional_phrase_v2(self, sent, head_word, phrase_ids) -> str:
        """前置詞句を正確に構築"""
        phrase_parts = []
        
        # 前置詞を探す
        preposition = None
        for word in sent.words:
            if word.head == head_word.id and word.deprel == 'case' and word.id in phrase_ids:
                preposition = word.text
                break
        
        if preposition:
            phrase_parts.append(preposition)
        
        # 修飾語を探す（順序付け）
        modifiers = []
        for word in sent.words:
            if word.head == head_word.id and word.deprel in ['det', 'amod'] and word.id in phrase_ids:
                modifiers.append((word.id, word.text))
        
        # ID順にソート
        modifiers.sort()
        for _, text in modifiers:
            phrase_parts.append(text)
        
        # 主語を追加
        phrase_parts.append(head_word.text)
        
        return ' '.join(phrase_parts).lower()
    
    def _extract_main_clause_elements(self, sent, main_verb, participle_phrase_words) -> Dict[str, str]:
        """主節の要素を抽出（分詞句以外の部分）"""
        elements = {}
        phrase_ids = {w.id for w in participle_phrase_words}
        
        # 主動詞の処理
        if main_verb.upos == 'VERB':
            elements['v'] = main_verb.text
        elif main_verb.upos == 'AUX':
            elements['aux'] = main_verb.text
        
        # 主動詞に依存する要素を抽出
        for word in sent.words:
            # 分詞句の一部は除外
            if word.id in phrase_ids:
                continue
            
            if word.head == main_verb.id:
                if word.deprel == 'nsubj':
                    elements['s'] = word.text
                elif word.deprel == 'obj':
                    elements['o1'] = word.text
                elif word.deprel == 'iobj':
                    elements['o2'] = word.text
                elif word.deprel in ['advmod', 'obl'] and word.text != ',':
                    elements['m1'] = word.text
                elif word.deprel in ['amod', 'attr'] and word.upos == 'ADJ':
                    elements['c1'] = word.text
        
        return elements
    
    def _process_simple_sentence(self, sent) -> Dict[str, str]:
        """単純文の処理（分詞構文なし）"""
        print("  📝 単純文処理")
        
        # root動詞を探す
        main_verb = None
        for word in sent.words:
            if word.deprel == 'root':
                main_verb = word
                break
        
        if main_verb:
            return self._extract_main_clause_elements(sent, main_verb, [])
        
        return {"error": "動詞未検出"}

def test_participle_engine():
    """テスト実行"""
    engine = ParticipleEngine()
    
    test_cases = [
        "Running fast, he won the race",
        "Tired from work, she went to bed",
        "Having finished homework, he watched TV",
        "Surprised by the news, they celebrated",
        "Walking to school, I met my friend",
        "He won the race running fast",  # 後置分詞句
        "She slept peacefully"  # 分詞構文なし
    ]
    
    print("\n" + "="*60)
    print("🧪 分詞構文エンジン テスト（統合型）")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【Test {i}】 '{test}'")
        result = engine.process(test)
        
        print("📊 完全分解結果:")
        # 上位スロットを先に表示
        upper_slots = {k: v for k, v in result.items() if not k.startswith('sub-') and k != 'error'}
        sub_slots = {k: v for k, v in result.items() if k.startswith('sub-')}
        
        if upper_slots:
            print("  【上位スロット】")
            for key, value in sorted(upper_slots.items()):
                print(f"    {key}: {value}")
        
        if sub_slots:
            print("  【サブスロット】")
            for key, value in sorted(sub_slots.items()):
                print(f"    {key}: {value}")
        
        if 'error' in result:
            print(f"  ❌ エラー: {result['error']}")

def test_participle_engine_legacy():
    """レガシーテスト実行"""
    engine = ParticipleEngine()
    
    test_cases = [
        "Running fast, he won the race",
        "Tired from work, she went to bed", 
        "Having finished homework, he watched TV",
        "Surprised by the news, they celebrated",
        "Walking to school, I met my friend",
        "He won the race running fast",  # 後置分詞句
        "She slept peacefully"  # 分詞構文なし
    ]
    
    print("\n" + "="*50)
    print("🧪 分詞構文エンジン テスト（レガシー）")
    print("="*50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n【Test {i}】 '{test}'")
        result = engine.process(test)
        
        print("📊 結果:")
        for key, value in result.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_participle_engine()
