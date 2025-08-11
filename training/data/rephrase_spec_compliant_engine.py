"""
正しいRephrase仕様準拠エンジン v4.0
- PhraseType = "clause"/"phrase" → 上位スロット空化
- 関係詞節はサブスロット内で処理（別従属節として分離しない）
- Step18参照による正確な実装
"""

import stanza
import spacy
from typing import Dict, List, Any, Optional, Tuple
import json
import re
from dataclasses import dataclass

@dataclass
class SlotResult:
    """スロット分解結果"""
    main_content: str = ""  # 上位スロット内容（空化対象）
    subslots: Dict[str, str] = None  # サブスロット内容
    phrase_type: str = "word"  # word/phrase/clause
    is_empty_upper: bool = False  # 上位スロット空化フラグ
    
    def __post_init__(self):
        if self.subslots is None:
            self.subslots = {}

class RephraseSpecCompliantEngine:
    """Rephrase仕様準拠エンジン"""
    
    def __init__(self):
        print("🚀 Rephrase仕様準拠エンジン v4.0 初期化中...")
        
        # NLPツール初期化
        try:
            self.nlp_stanza = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
            print("✅ Stanza初期化完了")
        except Exception as e:
            print(f"⚠️ Stanza初期化失敗: {e}")
            self.nlp_stanza = None
        
        try:
            self.nlp_spacy = spacy.load('en_core_web_sm')
            print("✅ spaCy初期化完了")
        except Exception as e:
            print(f"⚠️ spaCy初期化失敗: {e}")
            self.nlp_spacy = None
        
        # Step18参照用マッピング
        self.step18_reference = self._load_step18_reference()
        
        print("✅ 初期化完了\n")
    
    def _load_step18_reference(self) -> Dict:
        """Step18の既知パターンをロード"""
        return {
            "manager_pattern": {
                "sentence": "The experienced manager who had recently taken charge completed the project successfully.",
                "expected_result": {
                    "S": {
                        "sub-s": "manager who",
                        "sub-aux": "had", 
                        "sub-m2": "recently",
                        "sub-o1": "charge",
                        "sub-v": "taken"
                    },
                    "V": {"v": "completed"}
                }
            }
        }
    
    def decompose_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        文を90スロット構造に分解（Rephrase仕様準拠）
        """
        print(f"🔍 分解開始: {sentence}")
        
        # Phase 1: パターン認識（Stanza基盤）
        stanza_analysis = self._analyze_with_stanza(sentence)
        
        # Phase 2: 構造認識（spaCy補完）
        structure_analysis = self._analyze_structure(sentence, stanza_analysis)
        
        # Phase 3: スロット割り当て（Rephrase仕様準拠）
        slot_assignment = self._assign_slots_rephrase_compliant(sentence, structure_analysis)
        
        # Phase 4: 上位スロット空化処理
        final_result = self._apply_upper_slot_emptying(slot_assignment)
        
        print(f"✅ 分解完了: {len(final_result)}スロット")
        return final_result
    
    def _analyze_with_stanza(self, sentence: str) -> Dict:
        """Phase 1: Stanzaによる基本分析"""
        if not self.nlp_stanza:
            return {"tokens": [], "dependencies": []}
        
        try:
            doc = self.nlp_stanza(sentence)
            
            analysis = {
                "tokens": [],
                "dependencies": [],
                "sentences": []
            }
            
            for sent in doc.sentences:
                sent_data = {
                    "text": sent.text,
                    "words": []
                }
                
                for word in sent.words:
                    word_data = {
                        "text": word.text,
                        "lemma": word.lemma,
                        "pos": word.pos,
                        "head": word.head,
                        "deprel": word.deprel,
                        "id": word.id
                    }
                    analysis["tokens"].append(word_data)
                    sent_data["words"].append(word_data)
                    
                    # 依存関係を記録
                    if word.head != 0:  # rootでない場合
                        analysis["dependencies"].append({
                            "child": word_data,
                            "parent_id": word.head,
                            "relation": word.deprel
                        })
                
                analysis["sentences"].append(sent_data)
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Stanza分析エラー: {e}")
            return {"tokens": [], "dependencies": []}
    
    def _analyze_structure(self, sentence: str, stanza_analysis: Dict) -> Dict:
        """Phase 2: spaCyによる構造分析"""
        if not self.nlp_spacy:
            return stanza_analysis
        
        try:
            doc = self.nlp_spacy(sentence)
            
            # 関係詞節の識別
            relative_clauses = []
            for token in doc:
                if token.text.lower() in ['who', 'which', 'that']:
                    # 関係詞から節の終わりまでを特定
                    clause_tokens = [token]
                    current = token
                    
                    # 関係詞節の範囲を特定
                    for child in token.children:
                        if child.dep_ in ['nsubj', 'aux', 'advmod', 'dobj', 'pobj']:
                            clause_tokens.append(child)
                    
                    relative_clauses.append({
                        'start': min(t.i for t in clause_tokens),
                        'end': max(t.i for t in clause_tokens),
                        'text': ' '.join([t.text for t in sorted(clause_tokens, key=lambda x: x.i)]),
                        'head_noun': token.head.text if token.head else None
                    })
            
            # 構造情報を追加
            structure = stanza_analysis.copy()
            structure.update({
                "relative_clauses": relative_clauses,
                "named_entities": [(ent.text, ent.label_) for ent in doc.ents],
                "noun_phrases": [chunk.text for chunk in doc.noun_chunks]
            })
            
            return structure
            
        except Exception as e:
            print(f"⚠️ spaCy分析エラー: {e}")
            return stanza_analysis
    
    def _assign_slots_rephrase_compliant(self, sentence: str, analysis: Dict) -> Dict[str, SlotResult]:
        """Phase 3: Rephrase仕様準拠スロット割り当て（Step18ベース自動分解）"""
        
        # Step18ベースの真の自動分解エンジンを使用
        step18_result = self._step18_auto_decompose(sentence)
        
        # Step18結果をSlotResult形式に変換
        return self._convert_step18_to_slot_result(step18_result)
    
    def _step18_auto_decompose(self, sentence: str) -> Dict[str, Dict[str, str]]:
        """Step18ベースの真の自動分解エンジン"""
        print("🎯 Step18ベース自動分解開始")
        
        if not self.nlp_spacy:
            print("⚠️ spaCy未初期化 - 空結果を返します")
            return {}
        
        doc = self.nlp_spacy(sentence)
        
        # 依存関係-サブスロットマッピング（Step18と同じ）
        dep_to_subslot = {
            'nsubj': 'sub-s',
            'nsubjpass': 'sub-s', 
            'aux': 'sub-aux',
            'auxpass': 'sub-aux',
            'dobj': 'sub-o1',
            'iobj': 'sub-o2',
            'attr': 'sub-c1',
            'ccomp': 'sub-c2',
            'xcomp': 'sub-c2',
            'advmod': 'sub-m2',
            'amod': 'sub-m3',
            'prep': 'sub-m3', 
            'pobj': 'sub-o1',
            'pcomp': 'sub-c2',
            'mark': 'sub-m1',
            'relcl': 'sub-m3',
            'acl': 'sub-m3'
        }
        
        # ROOT動詞特定
        root_verb = None
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ in ['VERB', 'AUX']:
                root_verb = token
                break
        
        if not root_verb:
            print("⚠️ ROOT動詞が見つかりません")
            return {}
        
        print(f"🎯 ROOT動詞: '{root_verb.text}'")
        
        # 完全スロット分解（Step18ロジック）
        slots = {}
        
        # Sスロット抽出（関係詞節対応）
        s_slot = self._extract_s_slot_step18(doc, root_verb, dep_to_subslot)
        if s_slot:
            slots['S'] = s_slot
        
        # Vスロット抽出
        v_slot = self._extract_v_slot_step18(root_verb)
        if v_slot:
            slots['V'] = v_slot
        
        # その他のスロットも同様に抽出...
        # 簡略化のため、まずS, Vのみ実装
        
        return slots
    
    
    def _extract_s_slot_step18(self, doc, root_verb, dep_to_subslot) -> Optional[Dict[str, str]]:
        """Step18ベースのSスロット抽出"""
        print("� Sスロット抽出（Step18ベース）")
        
        # ROOT動詞の主語を探す
        main_subject = None
        for child in root_verb.children:
            if child.dep_ in ['nsubj', 'nsubjpass']:
                main_subject = child
                break
        
        if not main_subject:
            return None
        
        print(f"📌 主語発見: '{main_subject.text}'")
        
        # 主語の関係節処理
        from collections import defaultdict
        s_tokens = defaultdict(list)
        
        # 主語の子要素収集
        for child in main_subject.children:
            if child.dep_ == 'relcl':  # 関係節
                print(f"📌 関係節発見: '{child.text}'")
                
                # 関係節内のサブスロット
                for rel_child in child.children:
                    dep = rel_child.dep_
                    if dep in dep_to_subslot:
                        subslot = dep_to_subslot[dep]
                        s_tokens[subslot].append(rel_child)
                
                # 関係節動詞自体
                s_tokens['sub-v'].append(child)
        
        # 主語自体（スパン拡張適用）
        s_tokens['sub-s'].append(main_subject)
        print(f"📌 主語トークン追加: '{main_subject.text}' (dep={main_subject.dep_})")
        
        # ROOT動詞のaux収集（Sスロット用）
        for child in root_verb.children:
            if child.dep_ in ['aux', 'auxpass']:
                s_tokens['sub-aux'].append(child)
        
        if s_tokens:
            return self._build_subslots_step18(s_tokens, doc)
        
        return None
    
    def _extract_v_slot_step18(self, root_verb) -> Dict[str, str]:
        """Step18ベースのVスロット抽出"""
        print("🔍 Vスロット抽出（Step18ベース）")
        return {'v': root_verb.text}
    
    def _build_subslots_step18(self, slot_tokens, doc) -> Dict[str, str]:
        """Step18ベースのサブスロット構築"""
        subslots = {}
        
        for subslot_name, tokens in slot_tokens.items():
            if not tokens:
                continue
            
            if len(tokens) == 1:
                token = tokens[0]
                print(f"  🔍 単一トークン処理: {subslot_name} = '{token.text}' (dep={token.dep_})")
                
                # 前置詞統合チェック
                integrated = self._integrate_prepositions_step18(token, doc)
                if integrated:
                    subslots[subslot_name] = integrated
                else:
                    # スパン拡張
                    span = self._expand_span_step18(token, doc)
                    subslots[subslot_name] = span
            else:
                # 複数トークン結合
                text = ' '.join([t.text for t in sorted(tokens, key=lambda x: x.i)])
                subslots[subslot_name] = text
        
        return subslots
    
    def _integrate_prepositions_step18(self, token, doc) -> Optional[str]:
        """Step18ベースの前置詞統合処理"""
        # 名詞 + 前置詞句統合（Sスロットのsub-o1用）
        if token.pos_ == 'NOUN' and token.dep_ == 'dobj':
            prep_parts = []
            
            for child in token.children:
                if child.dep_ == 'prep':
                    prep_text = child.text
                    
                    # 前置詞の目的語
                    for prep_child in child.children:
                        if prep_child.dep_ == 'pobj':
                            obj_span = self._expand_span_step18(prep_child, doc)
                            prep_text += f" {obj_span}"
                    
                    prep_parts.append(prep_text)
            
            if prep_parts:
                return f"{token.text} {' '.join(prep_parts)}"
        
        return None
    
    def _expand_span_step18(self, token, doc) -> str:
        """Step18ベースのスパン拡張処理"""
        expand_deps = ['det', 'poss', 'compound', 'amod']
        
        start = token.i
        end = token.i
        
        print(f"  🔍 スパン拡張: '{token.text}' (dep={token.dep_})")
        
        # 基本的な子要素の拡張
        for child in token.children:
            if child.dep_ in expand_deps:
                print(f"    ✅ 基本拡張対象: '{child.text}'")
                start = min(start, child.i)
                end = max(end, child.i)
        
        # 関係節の場合は関係代名詞のみ含める
        for child in token.children:
            if child.dep_ == 'relcl':
                print(f"    🔍 関係節処理: '{child.text}'")
                # 関係代名詞(who)のみ探して含める
                for relcl_child in child.children:
                    if relcl_child.dep_ == 'nsubj' and relcl_child.pos_ == 'PRON':  # who
                        print(f"    ✅ 関係代名詞含める: '{relcl_child.text}'")
                        start = min(start, relcl_child.i)
                        end = max(end, relcl_child.i)
                        break
        
        result = ' '.join([doc[i].text for i in range(start, end + 1)])
        print(f"  📌 拡張結果: '{result}'")
        return result
    
    def _convert_step18_to_slot_result(self, step18_result: Dict[str, Dict[str, str]]) -> Dict[str, SlotResult]:
        """Step18結果をSlotResult形式に変換"""
        converted = {}
        
        for slot_name, subslots in step18_result.items():
            if subslots:  # サブスロットがある場合
                converted[slot_name] = SlotResult(
                    main_content="",  # 上位スロット空化
                    phrase_type="clause",  # サブスロットがあるため clause
                    is_empty_upper=True,
                    subslots=subslots
                )
            else:  # 単純なスロットの場合
                # この場合の処理（必要に応じて実装）
                pass
        
        return converted
    
    def _apply_upper_slot_emptying(self, slot_assignment: Dict[str, SlotResult]) -> Dict[str, Any]:
        """Phase 4: 上位スロット空化処理"""
        print("🔄 上位スロット空化処理実行")
        
        final_result = {}
        
        for slot_name, slot_result in slot_assignment.items():
            if slot_result.is_empty_upper or slot_result.phrase_type in ["clause", "phrase"]:
                # 上位スロット空化 - サブスロットのみ出力
                if slot_result.subslots:
                    final_result[slot_name] = slot_result.subslots
                    print(f"   {slot_name}: 上位空化 → {len(slot_result.subslots)}個のサブスロット")
                else:
                    # サブスロットがない場合はスキップ
                    print(f"   {slot_name}: 上位空化対象だがサブスロット無し → スキップ")
            else:
                # 通常のスロット - 上位内容を保持
                if slot_result.main_content:
                    final_result[slot_name] = {
                        slot_name.lower(): slot_result.main_content
                    }
                    print(f"   {slot_name}: 上位保持 → {slot_result.main_content}")
        
        return final_result

def test_rephrase_compliant_engine():
    """テスト実行"""
    engine = RephraseSpecCompliantEngine()
    
    # Step18参照テスト
    test_sentence = "The experienced manager who had recently taken charge completed the project successfully."
    
    print("=" * 80)
    print("🧪 Rephrase仕様準拠エンジン テスト")
    print("=" * 80)
    
    result = engine.decompose_sentence(test_sentence)
    
    print("\n📋 分解結果:")
    for slot, content in result.items():
        if isinstance(content, dict):
            print(f"  {slot}:")
            for key, value in content.items():
                print(f"    {key}: {value}")
        else:
            print(f"  {slot}: {content}")
    
    # Step18との比較
    expected = {
        "S": {
            "sub-s": "the experienced manager who",
            "sub-aux": "had",
            "sub-m2": "recently",
            "sub-v": "taken", 
            "sub-o1": "charge"
        },
        "V": {"v": "completed"}
    }
    
    print("\n🔍 Step18との比較:")
    print("期待値:")
    for slot, content in expected.items():
        print(f"  {slot}: {content}")
    
    print("\n結果:")
    for slot, content in result.items():
        print(f"  {slot}: {content}")

if __name__ == "__main__":
    test_rephrase_compliant_engine()
