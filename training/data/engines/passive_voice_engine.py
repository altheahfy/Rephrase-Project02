#!/usr/bin/env python3
"""
Passive Voice Engine - 受動態構文処理（統合型）
Stanza構造解析による受動態の完全処理

統合型アーキテクチャー:
1. 上位スロット配置 + サブスロット分解を単一エンジンで処理
2. 受動態：動作主をM1位置 + sub-m1（by句のみ）、Auxスロット活用
3. Rephraseルール準拠：大文字上位スロット + 小文字サブスロット
4. 情報保持とデバッグ効率の両立
"""

import stanza
from typing import Dict, List, Optional, Any

class PassiveVoiceEngine:
    """受動態構文エンジン（統合型）"""
    
    def __init__(self):
        print("🚀 受動態構文エンジン初期化中...")
        self.nlp = stanza.Pipeline('en', verbose=False)
        
        # 上位スロット配置マッピング
        self.slot_mapping = {
            'simple_passive': None,     # 単純受動態: 特別な上位配置なし
            'agent_passive': 'M1'       # by句付き: M1位置にby句配置
        }
        print("✅ 初期化完了")
    
    def process(self, text: str) -> Dict[str, str]:
        """統合型メイン処理（独立文用）"""
        print(f"🔍 受動態構文解析: '{text}'")
        
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 受動態検出
        passive_info = self._analyze_passive_structure(sent)
        if passive_info:
            return self._process_complete_passive_construction(sent, passive_info)
        else:
            return self._process_simple_sentence(sent)
    
    def process_as_subslot(self, sent, target_verb=None) -> Dict[str, str]:
        """サブスロット専用処理（従属節内受動態用）"""
        print(f"  🔧 サブスロット受動態処理開始")
        
        # 受動態検出
        passive_info = self._analyze_passive_structure(sent)
        if passive_info:
            return self._process_passive_as_subslot(sent, passive_info)
        else:
            # 能動態の場合のサブスロット処理
            return self._process_active_as_subslot(sent, target_verb)
    
    def _process_passive_as_subslot(self, sent, passive_info) -> Dict[str, str]:
        """受動態のサブスロット分解"""
        result = {}
        auxiliary = passive_info['auxiliary']
        main_verb = passive_info['main_verb']
        subject = passive_info['subject']
        agent_phrase = passive_info['agent_phrase']
        
        print(f"    📋 サブスロット受動態分解:")
        
        # サブスロット配置
        result['sub-s'] = self._build_subject_phrase(sent, subject)
        result['sub-aux'] = self._build_auxiliary_phrase(sent, auxiliary)
        result['sub-v'] = main_verb.text
        
        # by句がある場合
        if agent_phrase:
            agent_word = passive_info['agent']
            result['sub-m1'] = agent_phrase
            result['sub-o1'] = agent_word.text if agent_word else agent_phrase.replace('by ', '')
        
        print(f"    ✅ サブスロット結果: {result}")
        return result
    
    def _process_active_as_subslot(self, sent, target_verb=None) -> Dict[str, str]:
        """能動態のサブスロット分解"""
        result = {}
        
        # ターゲット動詞が指定されている場合
        main_verb = target_verb if target_verb else self._find_main_verb(sent)
        
        if main_verb:
            result['sub-v'] = main_verb.text
            
            # 基本要素
            for word in sent.words:
                if word.head == main_verb.id:
                    if word.deprel == 'nsubj':
                        result['sub-s'] = word.text
                    elif word.deprel == 'obj':
                        result['sub-o1'] = word.text
        
        return result
    
    def _analyze_passive_structure(self, sent) -> Optional[Dict]:
        """受動態構造の統合分析"""
        passive_features = {
            'auxiliary': None,    # be動詞
            'main_verb': None,    # 過去分詞
            'subject': None,      # 主語
            'agent': None,        # by句
            'agent_phrase': None, # by句全体
            'type': None          # 受動態の種類
        }
        
        # 典型的な過去分詞リスト（形容詞として解析される可能性がある）
        common_past_participles = {
            'fed', 'done', 'made', 'seen', 'built', 'written', 'taken', 'given',
            'broken', 'stolen', 'found', 'lost', 'sold', 'bought', 'taught',
            'caught', 'brought', 'thought', 'sent', 'kept', 'left', 'told',
            'heard', 'felt', 'held', 'met', 'read', 'paid', 'laid', 'said',
            'put', 'cut', 'hit', 'set', 'let', 'shut', 'hurt', 'cost', 'beat',
            'eaten', 'driven', 'shown', 'known', 'grown', 'thrown', 'blown',
            'drawn', 'worn', 'torn', 'born', 'sworn', 'chosen', 'frozen',
            'spoken', 'broken', 'woken', 'stolen'
        }
        
        # 構造要素の検出
        for word in sent.words:
            # 受動態主語検出（標準 + 代替）
            if word.deprel == 'nsubj:pass':
                passive_features['subject'] = word
            elif word.deprel == 'nsubj':  # 形容詞受動態の場合
                passive_features['subject'] = word
                
            # 受動態補助動詞検出（標準 + 代替）
            elif word.deprel == 'aux:pass':
                passive_features['auxiliary'] = word
            elif word.deprel == 'cop' and word.lemma == 'be':  # 連結詞be動詞
                passive_features['auxiliary'] = word
                
            # 主動詞検出（標準 + 代替）
            elif word.deprel == 'root' and word.upos == 'VERB':
                passive_features['main_verb'] = word
            elif (word.deprel == 'root' and word.upos == 'ADJ' and 
                  word.text.lower() in common_past_participles):  # 形容詞として解析された過去分詞
                passive_features['main_verb'] = word
                
            # by句動作主検出
            elif word.deprel == 'obl:agent':
                passive_features['agent'] = word
                # by句全体を構築
                passive_features['agent_phrase'] = self._build_agent_phrase(sent, word)
        
        # 受動態判定
        if (passive_features['auxiliary'] and 
            passive_features['main_verb'] and 
            passive_features['subject']):
            
            if passive_features['agent']:
                passive_features['type'] = 'agent_passive'
            else:
                passive_features['type'] = 'simple_passive'
                
            print(f"  📋 受動態検出:")
            print(f"    主語: {passive_features['subject'].text}")
            print(f"    補助動詞: {passive_features['auxiliary'].text}")
            print(f"    主動詞: {passive_features['main_verb'].text}")
            print(f"    動作主: {passive_features['agent'].text if passive_features['agent'] else 'なし'}")
            print(f"    種類: {passive_features['type']}")
            return passive_features
        
        return None
    
    def _process_complete_passive_construction(self, sent, passive_info) -> Dict[str, str]:
        """受動態構文の完全処理 - 統合型"""
        result = {}
        auxiliary = passive_info['auxiliary']
        main_verb = passive_info['main_verb']
        subject = passive_info['subject']
        agent_phrase = passive_info['agent_phrase']
        passive_type = passive_info['type']
        
        print(f"  🎯 統合処理開始: {passive_type}受動態")
        
        # 基本要素の配置
        result['S'] = self._build_subject_phrase(sent, subject)
        result['Aux'] = self._build_auxiliary_phrase(sent, auxiliary)
        result['V'] = main_verb.text
        
        # 上位スロット配置 + サブスロット分解
        if passive_type == 'agent_passive' and agent_phrase:
            # by句全体を上位スロットに配置
            result['M1'] = agent_phrase
            # 動作主のみをサブスロットに分解
            agent_word = passive_info['agent']
            result['sub-m1'] = agent_word.text if agent_word else agent_phrase.replace('by ', '')
            print(f"    上位配置: M1 = '{agent_phrase}'")
            print(f"    サブスロット配置: sub-m1 = '{result['sub-m1']}'")
        
        print(f"  ✅ 統合型完全分解: {result}")
        return result
    
    def _build_agent_phrase(self, sent, agent_word):
        """by句全体の構築"""
        if not agent_word:
            return None
        
        # by前置詞を探す
        by_preposition = None
        for word in sent.words:
            if word.text.lower() == 'by' and word.head == agent_word.id:
                by_preposition = word
                break
        
        if by_preposition:
            # byから動作主まで（修飾語含む）
            phrase_words = self._get_phrase_words(sent, by_preposition, agent_word)
            return ' '.join(w.text for w in sorted(phrase_words, key=lambda x: x.id))
        
        return f"by {agent_word.text}"
    
    def _get_phrase_words(self, sent, start_word, end_word):
        """句を構成する単語を収集"""
        phrase_words = [start_word, end_word]
        
        # end_wordの修飾語を追加
        for word in sent.words:
            if word.head == end_word.id and word.deprel in ['det', 'amod', 'nmod']:
                phrase_words.append(word)
        
        return phrase_words
    
    def _build_subject_phrase(self, sent, subject):
        """主語句の構築"""
        subject_words = [subject]
        
        # 主語の修飾語を収集
        for word in sent.words:
            if word.head == subject.id and word.deprel in ['det', 'amod', 'nmod']:
                subject_words.append(word)
        
        return ' '.join(w.text for w in sorted(subject_words, key=lambda x: x.id))
    
    def _build_auxiliary_phrase(self, sent, auxiliary):
        """補助動詞句の構築（完了・進行形対応）"""
        aux_words = []
        
        # 他の補助動詞も収集
        for word in sent.words:
            if word.upos == 'AUX' and word.head == auxiliary.head:
                aux_words.append(word)
        
        if aux_words:
            return ' '.join(w.text for w in sorted(aux_words, key=lambda x: x.id))
        
        return auxiliary.text
    
    def _find_main_verb(self, sent):
        """主動詞を検出"""
        for word in sent.words:
            if word.deprel == 'root' and word.upos == 'VERB':
                return word
        return None
        
    def _process_simple_sentence(self, sent):
        """単純文の処理"""
        print("  📝 単純文処理")
        result = {}
        
        # ルート動詞を探す
        main_verb = self._find_main_verb(sent)
        
        if main_verb:
            result['V'] = main_verb.text
            
            # 基本的な主語・目的語
            for word in sent.words:
                if word.head == main_verb.id:
                    if word.deprel == 'nsubj':
                        result['S'] = word.text
                    elif word.deprel == 'obj':
                        result['O1'] = word.text
        
        return result
