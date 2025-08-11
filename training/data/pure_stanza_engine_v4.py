#!/usr/bin/env python3
"""
複文対応Pure Stanza Engine v4 - 階層的clause分解アプローチ
"""

import stanza
import spacy
from typing import Dict, List, Optional, Any, Tuple
import json

class PureStanzaEngine_v4:
    """複文対応Pure Stanza Engine v4"""
    
    def __init__(self):
        self.nlp = None
        self.spacy_nlp = None
        self.sentence_patterns = {}
        self.modifier_mappings = {
            'advmod': 'M2',
            'amod': 'subslot',
            'det': 'subslot',
            'case': 'subslot',
            'nmod': 'M1'
        }
        self.subordinate_relations = ['advcl', 'ccomp', 'xcomp', 'acl:relcl', 'csubj']
        
    def initialize(self):
        """エンジン初期化"""
        print("🎯 PureStanzaEngine v4 初期化中...")
        
        # Stanza初期化
        try:
            self.nlp = stanza.Pipeline(
                lang='en', 
                processors='tokenize,pos,lemma,depparse',
                download_method=None
            )
            print("✅ Stanza準備完了")
        except Exception as e:
            print(f"❌ Stanza初期化エラー: {e}")
            return False
            
        # spaCy初期化
        try:
            self.spacy_nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy準備完了")
        except Exception as e:
            print(f"❌ spaCy初期化エラー: {e}")
            return False
            
        # パターン設定読み込み
        self._load_sentence_patterns()
        print("🏗️ 階層的分解エンジン準備完了 (v4)")
        return True
        
    def _load_sentence_patterns(self):
        """文型パターン設定読み込み"""
        self.sentence_patterns = {
            "SV": {
                "required": ["nsubj", "root"],
                "mapping": {"nsubj": "S", "root": "V"}
            },
            "SVC_BE": {
                "required": ["nsubj", "cop", "root"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            },
            "SVC_LOOKS": {
                "required": ["nsubj", "root"],
                "optional": ["xcomp"],
                "mapping": {"nsubj": "S", "root": "V", "xcomp": "C1"}
            },
            "SVO": {
                "required": ["nsubj", "root", "obj"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1"}
            },
            "SVOO": {
                "required": ["nsubj", "root", "obj", "iobj"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1", "iobj": "O2"}
            },
            "SVOC": {
                "required": ["nsubj", "root", "obj", "xcomp"],
                "mapping": {"nsubj": "S", "root": "V", "obj": "O1", "xcomp": "C2"}
            },
            "S_AUX_V": {
                "required": ["nsubj", "root", "aux"],
                "mapping": {"nsubj": "S", "root": "V", "aux": "Aux"}
            },
            "S_AUX_V_O": {
                "required": ["nsubj", "root", "aux", "obj"],
                "mapping": {"nsubj": "S", "root": "V", "aux": "Aux", "obj": "O1"}
            },
            "PASSIVE": {
                "required": ["nsubj:pass", "root"],
                "mapping": {"nsubj:pass": "S", "root": "V"}
            },
            "PASSIVE_AUX": {
                "required": ["nsubj:pass", "root", "aux:pass"],
                "mapping": {"nsubj:pass": "S", "root": "V", "aux:pass": "Aux"}
            },
            "THERE_BE": {
                "required": ["expl", "root"],
                "mapping": {"expl": "S", "root": "V"}
            },
            "WH_BE": {
                "required": ["nsubj", "cop", "root"],
                "mapping": {"nsubj": "S", "cop": "V", "root": "C1"}
            }
        }
    
    def analyze_complex_sentence(self, text: str) -> Dict[str, Any]:
        """複文の階層的分析"""
        print(f"\n🎯 複文分析開始: '{text}'")
        
        # Stanza解析
        doc = self.nlp(text)
        sent = doc.sentences[0]
        
        # 主節分析
        main_clause_result = self._analyze_main_clause(sent)
        
        # 従属節分析
        subordinate_clauses = self._extract_subordinate_clauses(sent)
        subordinate_results = []
        
        for clause_info in subordinate_clauses:
            clause_result = self._analyze_subordinate_clause(sent, clause_info)
            subordinate_results.append(clause_result)
        
        # 統合結果
        complex_result = {
            "sentence_type": "complex" if subordinate_clauses else "simple",
            "main_clause": main_clause_result,
            "subordinate_clauses": subordinate_results,
            "total_clauses": 1 + len(subordinate_clauses)
        }
        
        return complex_result
    
    def _analyze_main_clause(self, sent) -> Dict[str, Any]:
        """主節の分析"""
        print("\n📋 主節分析:")
        
        # ROOT動詞特定
        root_verb = self._find_root_verb(sent)
        if not root_verb:
            print("❌ ROOT動詞が見つかりません")
            return {}
        
        print(f"📌 主節ROOT: '{root_verb.text}' (POS: {root_verb.upos})")
        
        # 主節の要素のみ抽出（従属節の要素を除外）
        main_clause_words = self._extract_main_clause_words(sent, root_verb)
        
        # 文型パターン識別
        sentence_pattern = self._identify_sentence_pattern_for_words(main_clause_words, root_verb)
        if not sentence_pattern:
            print("❌ 主節の文型パターンが見つかりません")
            return {}
        
        print(f"🔍 主節パターン: {sentence_pattern}")
        
        # スロット抽出
        slots = self._extract_slots_for_words(main_clause_words, root_verb, sentence_pattern)
        
        return {
            "clause_type": "main",
            "pattern": sentence_pattern,
            "root_verb": root_verb.text,
            "slots": slots
        }
    
    def _extract_subordinate_clauses(self, sent) -> List[Dict[str, Any]]:
        """従属節の抽出"""
        subordinate_clauses = []
        
        for word in sent.words:
            if word.deprel in self.subordinate_relations:
                # 従属節の構成要素を収集
                clause_words = self._collect_clause_words(sent, word)
                
                # 従属接続詞の特定
                connector = self._find_connector(clause_words)
                
                clause_info = {
                    "head_word": word,
                    "relation": word.deprel,
                    "words": clause_words,
                    "connector": connector
                }
                subordinate_clauses.append(clause_info)
                print(f"🔍 従属節検出: {word.text} ({word.deprel}) - 接続詞: {connector}")
        
        return subordinate_clauses
    
    def _analyze_subordinate_clause(self, sent, clause_info: Dict[str, Any]) -> Dict[str, Any]:
        """個別の従属節分析"""
        head_word = clause_info["head_word"]
        clause_words = clause_info["words"]
        
        print(f"\n📋 従属節分析: {head_word.text} ({clause_info['relation']})")
        
        # 従属節内での文型パターン識別
        pattern = self._identify_sentence_pattern_for_words(clause_words, head_word)
        if not pattern:
            print("❌ 従属節の文型パターンが見つかりません")
            return {}
        
        print(f"🔍 従属節パターン: {pattern}")
        
        # スロット抽出
        slots = self._extract_slots_for_words(clause_words, head_word, pattern)
        
        return {
            "clause_type": "subordinate",
            "relation": clause_info["relation"],
            "connector": clause_info["connector"],
            "pattern": pattern,
            "root_verb": head_word.text,
            "slots": slots
        }
    
    def _extract_main_clause_words(self, sent, root_verb) -> List[Any]:
        """主節の単語のみ抽出（従属節を除外）"""
        main_words = []
        subordinate_heads = [w for w in sent.words if w.deprel in self.subordinate_relations]
        subordinate_word_ids = set()
        
        # 従属節に属する単語IDを収集
        for sub_head in subordinate_heads:
            subordinate_word_ids.update(self._get_subtree_word_ids(sent, sub_head))
        
        # 主節の単語のみ抽出
        for word in sent.words:
            if word.id not in subordinate_word_ids:
                main_words.append(word)
        
        return main_words
    
    def _collect_clause_words(self, sent, head_word) -> List[Any]:
        """従属節の構成単語を収集"""
        clause_words = []
        subtree_ids = self._get_subtree_word_ids(sent, head_word)
        
        for word in sent.words:
            if word.id in subtree_ids:
                clause_words.append(word)
        
        return clause_words
    
    def _get_subtree_word_ids(self, sent, head_word) -> set:
        """指定した語を頂点とする部分木の単語IDを取得"""
        subtree_ids = {head_word.id}
        
        # 再帰的に子ノードを追加
        def add_children(word_id):
            for word in sent.words:
                if word.head == word_id and word.id not in subtree_ids:
                    subtree_ids.add(word.id)
                    add_children(word.id)
        
        add_children(head_word.id)
        return subtree_ids
    
    def _find_connector(self, clause_words) -> str:
        """従属接続詞を特定"""
        for word in clause_words:
            if word.deprel == 'mark':
                return word.text
        return ""
    
    # 以下、既存のv3メソッドを適用
    def _find_root_verb(self, sent) -> Optional[Any]:
        """ROOT動詞を特定"""
        for word in sent.words:
            if word.deprel == 'root':
                return word
        return None
    
    def _identify_sentence_pattern_for_words(self, words: List[Any], root_verb) -> Optional[str]:
        """指定した単語群での文型パターン識別"""
        word_relations = [w.deprel for w in words]
        
        for pattern_name, pattern_config in self.sentence_patterns.items():
            required = pattern_config["required"]
            optional = pattern_config.get("optional", [])
            
            # 必須要素チェック
            if all(rel in word_relations for rel in required):
                print(f"✅ マッチしたパターン: {pattern_name}")
                return pattern_name
        
        return None
    
    def _extract_slots_for_words(self, words: List[Any], root_verb, pattern_name: str) -> Dict[str, str]:
        """指定した単語群でのスロット抽出"""
        pattern_config = self.sentence_patterns[pattern_name]
        mapping = pattern_config["mapping"]
        
        slots = {}
        aux_words = []
        
        for word in words:
            if word.deprel in mapping:
                slot_name = mapping[word.deprel]
                
                if slot_name == "Aux":
                    aux_words.append(word)
                    continue
                
                print(f"📍 {slot_name}検出: '{word.text}' (deprel: {word.deprel})")
                slots[slot_name] = word.text
        
        # Aux統合
        if aux_words:
            aux_texts = [word.text for word in sorted(aux_words, key=lambda w: w.id)]
            aux_combined = " ".join(aux_texts)
            print(f"📍 Aux検出: '{aux_combined}' (統合: {len(aux_words)}個)")
            slots["Aux"] = aux_combined
        
        return slots

def test_complex_analysis():
    """複文分析テスト"""
    engine = PureStanzaEngine_v4()
    if not engine.initialize():
        return
    
    test_sentences = [
        "He succeeded even though he was under intense pressure.",
        "She passed the test because she is very intelligent.",
        "The man who is tall walks quickly.",
        "I know that he is happy."
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*80}")
        print(f"テスト文: {sentence}")
        print('='*80)
        
        result = engine.analyze_complex_sentence(sentence)
        
        print(f"\n📊 分析結果:")
        print(f"文型: {result.get('sentence_type', 'unknown')}")
        print(f"節数: {result.get('total_clauses', 0)}")
        
        # 主節結果
        main_clause = result.get('main_clause', {})
        if main_clause:
            print(f"\n🏛️ 主節:")
            print(f"  パターン: {main_clause.get('pattern', 'N/A')}")
            print(f"  スロット: {main_clause.get('slots', {})}")
        
        # 従属節結果
        for i, sub_clause in enumerate(result.get('subordinate_clauses', [])):
            print(f"\n🔗 従属節 {i+1}:")
            print(f"  接続: {sub_clause.get('connector', 'N/A')} ({sub_clause.get('relation', 'N/A')})")
            print(f"  パターン: {sub_clause.get('pattern', 'N/A')}")
            print(f"  スロット: {sub_clause.get('slots', {})}")

if __name__ == "__main__":
    test_complex_analysis()
