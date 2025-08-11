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
        """動的スロット抽出：spaCy解析に基づく実際のスロット分割"""
        slots = {}
        
        # ROOT動詞を特定
        root_verb = None
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                root_verb = token
                break
        
        if not root_verb:
            return {}
        
        # Vスロット（メイン動詞）
        slots['V'] = root_verb.text
        
        # Sスロット（主語）：主語とその修飾を含む
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubjpass', 'csubj'] and token.head == root_verb:
                # 主語句全体を抽出（修飾語も含む）
                s_tokens = [token]
                for child in token.subtree:
                    if child != token:
                        s_tokens.append(child)
                s_tokens.sort(key=lambda t: t.i)
                if s_tokens:
                    slots['S'] = doc[s_tokens[0].i:s_tokens[-1].i+1].text
                break
        
        # O1スロット（目的語節）：that節など
        for token in doc:
            if token.dep_ in ['ccomp', 'xcomp'] and token.head == root_verb:
                # 目的語節全体を抽出
                o1_tokens = list(token.subtree)
                o1_tokens.sort(key=lambda t: t.i)
                if o1_tokens:
                    slots['O1'] = doc[o1_tokens[0].i:o1_tokens[-1].i+1].text
                break
        
        # M2, M3スロット（副詞節）：although, because節など
        adv_clauses = []
        for token in doc:
            if token.dep_ in ['advcl'] and token.head == root_verb:
                adv_tokens = list(token.subtree)
                adv_tokens.sort(key=lambda t: t.i)
                if adv_tokens:
                    clause_text = doc[adv_tokens[0].i:adv_tokens[-1].i+1].text
                    adv_clauses.append(clause_text)
        
        # 副詞節をM2, M3に割り当て
        if len(adv_clauses) >= 1:
            slots['M2'] = adv_clauses[0]
        if len(adv_clauses) >= 2:
            slots['M3'] = adv_clauses[1]
        
        return slots
    
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
        """spaCy依存関係解析 - sub-m2精密化対応"""
        assignments = {}
        
        # デバッグ: 依存関係を確認
        print(f"🔍 依存関係解析デバッグ: '{doc.text}'")
        for token in doc:
            print(f"  {token.text:15} | {token.dep_:10} | {token.pos_:5} | head: {token.head.text}")
        
        for token in doc:
            dep = token.dep_
            pos = token.pos_
            
            # 前置詞の特別処理：親トークンと統合
            if dep == 'prep':
                print(f"📌 前置詞統合処理: '{token.text}' -> 親トークン'{token.head.text}'と統合")
                # 前置詞は独立処理せず、親トークンの拡張スパンで自動統合
                continue
            
            # sub-m2の特別処理：副詞のみを単独で認識
            if dep == 'advmod' and pos == 'ADV':
                print(f"📌 sub-m2発見: '{token.text}' (dep={dep}, pos={pos})")
                assignments[token.i] = {
                    'token': token,
                    'subslot': 'sub-m2',
                    'text': token.text,  # 単語のみ、拡張なし
                    'no_expansion': True  # 拡張禁止フラグ
                }
                continue
            
            # 特別処理: 関係節内の動詞
            if dep == 'relcl' and pos == 'VERB':
                target_subslot = 'sub-v'  # 動詞として認識
            elif dep in self.dep_to_subslot:
                target_subslot = self.dep_to_subslot[dep]
            else:
                continue
                
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
        
    def _apply_rephrase_rules(self, doc, assignments):
        """Rephraseルール適用 - 動詞優先度対応強化"""
        result = self._empty_subslots()
        subslot_tokens = defaultdict(list)
        
        # トークンをサブスロット別に分類
        for token_idx, assignment in assignments.items():
            subslot = assignment['subslot']
            token = assignment['token']
            subslot_tokens[subslot].append(token)
        
        # sub-m2の特別処理：advmod副詞を分離
        if 'sub-m2' in subslot_tokens:
            sub_m2_tokens = subslot_tokens['sub-m2']
            advmod_tokens = [t for t in sub_m2_tokens if t.dep_ == 'advmod' and t.pos_ == 'ADV']
            other_tokens = [t for t in sub_m2_tokens if not (t.dep_ == 'advmod' and t.pos_ == 'ADV')]
            
            print(f"🔍 sub-m2分離: advmod={len(advmod_tokens)}個, other={len(other_tokens)}個")
            
            if advmod_tokens:
                # advmod副詞のみでsub-m2を構成（最優先）
                subslot_tokens['sub-m2'] = advmod_tokens
                # 他の要素があれば別のスロットに移動（今回は無視）
                if other_tokens:
                    print(f"🔍 sub-m2から除外: {[t.text for t in other_tokens]}")
            else:
                # advmodがない場合は、sub-m2を空にする
                print(f"🔍 sub-m2にadvmodなし - スロット削除: {[t.text for t in other_tokens]}")
                del subslot_tokens['sub-m2']
        
        # 各サブスロットでトークンを選択・結合
        for subslot, tokens in subslot_tokens.items():
            print(f"🔍 処理中サブスロット: {subslot}, トークン数: {len(tokens)}")
            if tokens:
                if subslot == 'sub-v':
                    # 動詞は特別処理：最も適切な1つを選択
                    result[subslot] = self._select_best_verb(tokens)
                    print(f"🔍 動詞選択: {result[subslot]}")
                elif len(tokens) == 1:
                    token = tokens[0]
                    assignment = assignments.get(token.i, {})
                    
                    print(f"🔍 単一トークン処理: {subslot} = '{token.text}' (dep={token.dep_}, pos={token.pos_})")
                    
                    # 拡張禁止フラグがある場合は事前設定テキストを使用
                    if assignment.get('no_expansion'):
                        result[subslot] = assignment.get('text', token.text)
                        print(f"📌 拡張禁止適用: {subslot} = '{result[subslot]}'")
                    else:
                        # その他は拡張スパン適用
                        print(f"🔍 拡張スパン適用前: {subslot}")
                        result[subslot] = self._get_extended_span(token, doc)
                        print(f"🔍 拡張スパン適用後: {subslot} = '{result[subslot]}'")
                else:
                    # 複数トークン：連続スパン構築
                    tokens.sort(key=lambda t: t.i)
                    start_idx = tokens[0].i
                    end_idx = tokens[-1].i + 1
                    result[subslot] = doc[start_idx:end_idx].text
                    print(f"🔍 複数トークン結合: {subslot} = '{result[subslot]}'")
                    
            else:
                print(f"🔍 空トークン: {subslot}")
        
        return result
    
    def _select_best_verb(self, tokens):
        """動詞の最適選択"""
        # 動詞の優先度定義
        verb_priority = {
            'relcl': 1,    # 関係節動詞（最優先）
            'ROOT': 2,     # 主動詞
            'cop': 3,      # コピュラ
            'aux': 4       # 助動詞（低優先）
        }
        
        # 優先度でソート
        sorted_tokens = sorted(tokens, 
                              key=lambda t: verb_priority.get(t.dep_, 999))
        
        # 最優先の動詞を選択
        best_token = sorted_tokens[0]
        return best_token.text
    
    def _get_extended_span(self, token, doc):
        """拡張スパン構築 - sub-m2過大拡張防止対応"""
        
        # sub-m2の副詞は絶対に拡張しない（最優先ガード）
        if token.dep_ == 'advmod' and token.pos_ == 'ADV':
            print(f"📌 advmod副詞拡張防止: '{token.text}'")
            return token.text
        
        # sub-m2の特別処理：副詞・形容詞の範囲を適切に制限
        if token.dep_ in ['advmod', 'amod'] and token.pos_ in ['ADV', 'ADJ']:
            # 単語レベルまたは最小限の修飾のみ
            span_tokens = [token]
            
            # 限定的な修飾のみ追加（det, compoundなど）
            for child in token.children:
                if child.dep_ in ['det', 'compound'] and child.pos_ in ['DET', 'NOUN']:
                    span_tokens.append(child)
            
            if len(span_tokens) == 1:
                return token.text
            
            # 連続スパンを構築（範囲制限）
            span_tokens.sort(key=lambda t: t.i)
            return doc[span_tokens[0].i:span_tokens[-1].i + 1].text
        
        # 関係代名詞を含む主語句の特別処理
        if token.dep_ == 'nsubj' and any(child.text.lower() in ['who', 'which', 'that'] for child in token.head.children):
            # 関係代名詞句全体を主語として認識
            span_tokens = []
            
            # 主語部分（関係代名詞より前）
            for t in doc:
                if t.i <= token.i:
                    span_tokens.append(t)
                else:
                    break
            
            # 関係代名詞を含める
            for child in token.head.children:
                if child.text.lower() in ['who', 'which', 'that'] and child.i > token.i:
                    span_tokens.append(child)
                    break
            
            if len(span_tokens) > 1:
                span_tokens.sort(key=lambda t: t.i)
                return doc[span_tokens[0].i:span_tokens[-1].i + 1].text
        
        # 通常の拡張スパン処理
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
    
    print('Step18統一Rephraseシステム - 5文型フルセット全例文処理')
    print('=' * 80)
    
    try:
        # 5文型フルセットExcelから全例文を読み込み
        df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
        
        # 例文ID別に原文を取得
        sentences = {}
        for _, row in df.iterrows():
            if pd.notna(row['例文ID']) and pd.notna(row['原文']):
                if row['例文ID'] not in sentences:
                    sentences[row['例文ID']] = row['原文']
        
        print(f"📂 5文型フルセットから{len(sentences)}個の例文を読み込み完了")
        
        # 各例文を処理（全例文処理）
        for i, (ex_id, sentence) in enumerate(sentences.items(), 1):
            print(f"\n{'=' * 80}")
            print(f"📋 [{i}/{len(sentences)}] 処理中: {ex_id}")
            print(f"原文: {sentence}")
            print('=' * 80)
            
            # Step18で処理
            results = system.process_sentence(sentence)
            
            # 結果表示
            print(f'\n✅ {ex_id} 処理結果:')
            print('-' * 60)
            
            for slot_name, slot_data in results.items():
                if slot_data:  # データが存在する場合のみ表示
                    print(f'\n📋 {slot_name}スロット:')
                    if slot_name in system.single_slots:
                        for key, value in slot_data.items():
                            print(f'  {key}: "{value}"')
                    else:
                        for key, value in slot_data.items():
                            if value:
                                print(f'  {key:10}: "{value}"')
        
        print(f"\n{'=' * 80}")
        print(f"🎯 全{len(sentences)}例文の処理完了！")
        print('=' * 80)
        
    except Exception as e:
        print(f"❌ Excel読み込みエラー: {e}")
        print("フォールバック: 単一テスト文で処理")
        
        # フォールバック用固定文
        test_sentence = "That afternoon at the crucial point in the presentation, the manager who had recently taken charge of the project had to make the committee responsible for implementation deliver the final proposal flawlessly even though he was under intense pressure so the outcome would reflect their full potential."
        
        print(f"🎯 Step18処理開始: '{test_sentence[:100]}...'")
        print("=" * 80)
        
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
