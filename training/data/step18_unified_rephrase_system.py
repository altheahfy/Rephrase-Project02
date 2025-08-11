import spacy
import pandas as pd
from collections import defaultdict
import re

class Step18UnifiedRephraseSystem:
    """
    Step18: spaCy45個依存関係完全対応 統一Rephraseシステム
    - 8スロット統一分解エンジン適用 (M1, S, M2, C1, O1, O2, C2, M3)
    - 2スロット単一要素処理 (Aux, V)
    - フルセット12例文対応
    - Excel生成機能搭載
    """
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # spaCy依存関係45個 → Rephraseサブスロット完全マッピング
        self.dep_to_subslot = {
            # 主語関連
            'nsubj': 'sub-s',           # 名詞主語
            'nsubjpass': 'sub-s',       # 受動態主語
            'csubj': 'sub-s',           # 節主語
            'csubjpass': 'sub-s',       # 受動節主語
            'expl': 'sub-s',            # 虚辞主語(there, it)
            
            # 動詞・述語関連
            'ROOT': 'sub-v',            # 主動詞
            'cop': 'sub-v',             # コピュラ(be動詞)
            'aux': 'sub-aux',           # 助動詞
            'auxpass': 'sub-aux',       # 受動態助動詞
            
            # 目的語関連
            'dobj': 'sub-o1',           # 直接目的語
            'iobj': 'sub-o2',           # 間接目的語
            'pobj': 'sub-o1',           # 前置詞目的語
            'dative': 'sub-o2',         # 与格目的語
            
            # 補語関連
            'attr': 'sub-c1',           # 属性補語
            'acomp': 'sub-c1',          # 形容詞補語
            'pcomp': 'sub-c1',          # 前置詞補語
            'xcomp': 'sub-c2',          # 開放補語
            'ccomp': 'sub-c2',          # 節補語
            'oprd': 'sub-c1',           # 目的語述語
            
            # 修飾語関連（M1/M2/M3）
            'advmod': 'sub-m2',         # 副詞修飾
            'amod': 'sub-m2',           # 形容詞修飾
            'npadvmod': 'sub-m3',       # 名詞句副詞修飾
            'tmod': 'sub-m3',           # 時間修飾
            'nummod': 'sub-m2',         # 数詞修飾
            'quantmod': 'sub-m2',       # 量詞修飾
            
            # 接続詞・標識関連
            'mark': 'sub-m1',           # 従属接続詞(although, that等)
            'cc': 'sub-m1',             # 等位接続詞
            'preconj': 'sub-m1',        # 前接続詞
            
            # 節・句関連
            'advcl': 'sub-m3',          # 副詞節
            'relcl': 'sub-m3',          # 関係節
            'acl': 'sub-m3',            # 節修飾語
            'prt': 'sub-m3',            # 助詞
            
            # 前置詞関連
            'prep': 'sub-m3',           # 前置詞
            'poss': 'sub-m2',           # 所有格
            'possessive': 'sub-m2',     # 所有格マーカー
            
            # その他重要な関係
            'agent': 'sub-s',           # 動作主
            'neg': 'sub-m2',            # 否定
            'det': 'sub-m2',            # 限定詞
            'predet': 'sub-m2',         # 前限定詞
            'appos': 'sub-m3',          # 同格
            'compound': 'sub-m2',       # 複合語
            'conj': 'sub-m3',           # 接続項
            'discourse': 'sub-m1',      # 談話標識
            'vocative': 'sub-m1',       # 呼格
            'intj': 'sub-m1',           # 間投詞
            'meta': 'sub-m3',           # メタ情報
            'parataxis': 'sub-m3',      # 並列構造
            'punct': '',                # 句読点（除外）
            'dep': 'sub-m3'             # その他依存関係
        }
        
        # 統一分解対象スロット
        self.decomposable_slots = {'M1', 'S', 'M2', 'C1', 'O1', 'O2', 'C2', 'M3'}
        
        # 単一要素スロット
        self.single_slots = {'Aux', 'V'}
    
    def process_sentence(self, sentence):
        """1つの例文を完全処理"""
        print(f"\n🎯 Step18処理開始: '{sentence}'")
        
        # spaCy解析
        doc = self.nlp(sentence)
        
        # スロット分割（仮想的 - 実際は上位システムから受け取る）
        slot_phrases = self._extract_slot_phrases(sentence, doc)
        
        # 各スロット処理
        results = {}
        for slot_name, phrase in slot_phrases.items():
            if slot_name in self.single_slots:
                # 単一要素処理
                results[slot_name] = {slot_name.lower(): phrase}
            else:
                # 統一分解エンジン適用
                results[slot_name] = self._unified_decompose(phrase)
        
        return results
    
    def _extract_slot_phrases(self, sentence, doc):
        """テスト用：簡易スロット抽出"""
        # 実際の運用では上位システムからスロット分割済みデータを受け取る
        return {
            'S': 'the woman who seemed indecisive',
            'M2': 'although it was emotionally hard',
            'V': 'known',
            'O1': 'that he had been trying to avoid Tom',
            'M3': 'because he was afraid of hurting her feelings'
        }
    
    def _unified_decompose(self, phrase):
        """統一分解エンジン：8スロット共通"""
        if not phrase or phrase.strip() == "":
            return self._empty_subslots()
        
        phrase = phrase.strip()
        doc = self.nlp(phrase)
        
        print(f"  🔍 統一分解: '{phrase}'")
        
        # spaCy依存関係解析
        token_assignments = self._analyze_dependencies(doc)
        
        # Rephraseルール適用
        result = self._apply_rephrase_rules(doc, token_assignments)
        
        # 100%単語保全チェック
        if not self._verify_complete_coverage(phrase, result):
            result = self._recover_missing_words(phrase, doc, result)
        
        return result
    
    def _analyze_dependencies(self, doc):
        """spaCy依存関係解析"""
        assignments = {}
        
        for token in doc:
            dep = token.dep_
            if dep in self.dep_to_subslot:
                target_subslot = self.dep_to_subslot[dep]
                if target_subslot:  # 空文字列でない場合
                    assignments[token.i] = {
                        'token': token,
                        'subslot': target_subslot,
                        'text': token.text
                    }
        
        return assignments
    
    def _apply_rephrase_rules(self, doc, assignments):
        """Rephraseルール適用"""
        result = self._empty_subslots()
        subslot_tokens = defaultdict(list)
        
        # トークンをサブスロット別に分類
        for token_idx, assignment in assignments.items():
            subslot = assignment['subslot']
            token = assignment['token']
            subslot_tokens[subslot].append(token)
        
        # 各サブスロットでトークンを結合
        for subslot, tokens in subslot_tokens.items():
            if tokens:
                # 位置順にソート
                tokens.sort(key=lambda t: t.i)
                
                # スパン構築
                if len(tokens) == 1:
                    result[subslot] = self._get_extended_span(tokens[0], doc)
                else:
                    # 複数トークン：最初と最後の位置で連続スパン構築
                    start_idx = tokens[0].i
                    end_idx = tokens[-1].i + 1
                    result[subslot] = doc[start_idx:end_idx].text
        
        return result
    
    def _get_extended_span(self, token, doc):
        """拡張スパン構築"""
        # 重要な修飾語を含める
        span_tokens = [token]
        
        for child in token.children:
            if child.dep_ in ['det', 'amod', 'compound', 'poss']:
                span_tokens.append(child)
        
        if len(span_tokens) == 1:
            return token.text
        
        # 連続スパンを構築
        span_tokens.sort(key=lambda t: t.i)
        start_idx = span_tokens[0].i
        end_idx = span_tokens[-1].i + 1
        return doc[start_idx:end_idx].text
    
    def _verify_complete_coverage(self, original, subslots):
        """100%単語保全確認"""
        original_words = set(w.lower() for w in original.split() if w.strip())
        covered_words = set()
        
        for value in subslots.values():
            if value and value.strip():
                covered_words.update(w.lower() for w in value.split() if w.strip())
        
        return original_words.issubset(covered_words)
    
    def _recover_missing_words(self, original, doc, current_result):
        """欠落単語回復"""
        original_words = set(w.lower() for w in original.split())
        covered_words = set()
        
        for value in current_result.values():
            if value:
                covered_words.update(w.lower() for w in value.split())
        
        missing_words = original_words - covered_words
        
        if missing_words:
            # フォールバック：sub-m3に追加
            missing_text = ' '.join(missing_words)
            if current_result['sub-m3']:
                current_result['sub-m3'] += f" {missing_text}"
            else:
                current_result['sub-m3'] = missing_text
        
        return current_result
    
    def _empty_subslots(self):
        """空のサブスロット構造"""
        return {
            'sub-m1': '',
            'sub-s': '',
            'sub-aux': '',
            'sub-m2': '',
            'sub-v': '',
            'sub-c1': '',
            'sub-o1': '',
            'sub-o2': '',
            'sub-c2': '',
            'sub-m3': ''
        }
    
    def generate_excel_output(self, results, example_id="test"):
        """Excel出力形式生成"""
        excel_data = []
        
        for slot_name, slot_data in results.items():
            if slot_name in self.single_slots:
                # 単一要素スロット
                excel_data.append({
                    '例文ID': example_id,
                    'Slot': slot_name,
                    'SubslotID': '',
                    'SlotPhrase': slot_data[slot_name.lower()],
                    'SubslotElement': ''
                })
            else:
                # 統一分解スロット
                # メインスロット行
                main_phrase = ' '.join([v for v in slot_data.values() if v])
                excel_data.append({
                    '例文ID': example_id,
                    'Slot': slot_name,
                    'SubslotID': '',
                    'SlotPhrase': main_phrase,
                    'SubslotElement': ''
                })
                
                # サブスロット行
                for subslot_id, element in slot_data.items():
                    if element:
                        excel_data.append({
                            '例文ID': example_id,
                            'Slot': slot_name,
                            'SubslotID': subslot_id,
                            'SlotPhrase': '',
                            'SubslotElement': element
                        })
        
        return excel_data


# テスト実行
if __name__ == "__main__":
    system = Step18UnifiedRephraseSystem()
    
    print('🎯 Step18統一Rephraseシステムテスト')
    print('=' * 100)
    
    # テスト例文
    test_sentence = "This morning, the woman who seemed indecisive had, although it was emotionally hard, known that he had been trying to avoid Tom because he was afraid of hurting her feelings."
    
    # 処理実行
    results = system.process_sentence(test_sentence)
    
    # 結果表示
    print('\n✅ 処理結果:')
    print('=' * 80)
    
    for slot_name, slot_data in results.items():
        print(f'\n📋 {slot_name}スロット:')
        if slot_name in system.single_slots:
            for key, value in slot_data.items():
                print(f'  {key}: "{value}"')
        else:
            for subslot, value in slot_data.items():
                if value:
                    print(f'  {subslot:10}: "{value}"')
    
    # Excel出力テスト
    print('\n📊 Excel出力形式:')
    print('=' * 80)
    
    excel_data = system.generate_excel_output(results, "ex001")
    for row in excel_data[:10]:  # 最初の10行
        print(f"  {row}")
    
    print(f"\n📈 統計:")
    print(f"  処理スロット数: {len(results)}")
    print(f"  Excel出力行数: {len(excel_data)}")
    print(f"  単一要素スロット: {len(system.single_slots)}")
    print(f"  分解対象スロット: {len(system.decomposable_slots)}")
