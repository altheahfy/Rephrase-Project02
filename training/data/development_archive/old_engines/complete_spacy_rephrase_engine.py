import spacy
import pandas as pd
from collections import defaultdict

class CompleteSpacyRephraseEngine:
    """
    spaCy依存関係45個完全対応 Rephrase統一分解エンジン
    ① spaCyが全単語の依存関係を解析
    ② エンジンがRephraseルールに基づいてサブスロットに配置
    ③ 100%単語保全を保証
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
        
        # 優先順位（複数候補がある場合）
        self.subslot_priority = {
            'sub-m1': 1,
            'sub-s': 2,
            'sub-aux': 3,
            'sub-m2': 4,
            'sub-v': 5,
            'sub-c1': 6,
            'sub-o1': 7,
            'sub-o2': 8,
            'sub-c2': 9,
            'sub-m3': 10
        }
    
    def decompose(self, phrase):
        """
        統一分解メソッド：spaCy解析 → Rephraseルール適用
        """
        if not phrase or phrase.strip() == "":
            return self._empty_subslots()
        
        phrase = phrase.strip()
        doc = self.nlp(phrase)
        
        # デバッグ：spaCy解析結果表示
        print(f"\n🔍 spaCy解析: '{phrase}'")
        for token in doc:
            print(f"  {token.text:12} | {token.dep_:12} | {token.pos_:8} | {token.head.text}")
        
        # ① spaCy依存関係解析
        token_assignments = self._analyze_dependencies(doc)
        
        # ② Rephraseルール適用
        result = self._apply_rephrase_rules(doc, token_assignments)
        
        # ③ 100%単語保全チェック
        if not self._verify_complete_coverage(phrase, result):
            print(f"⚠️  単語欠落検出: '{phrase}'")
            result = self._recover_missing_words(phrase, doc, result)
        
        return result
    
    def _analyze_dependencies(self, doc):
        """spaCy依存関係を解析してトークン割り当てを決定"""
        assignments = {}
        
        for token in doc:
            dep = token.dep_
            
            # 依存関係をサブスロットにマッピング
            if dep in self.dep_to_subslot:
                target_subslot = self.dep_to_subslot[dep]
                if target_subslot:  # 空文字列でない場合
                    assignments[token.i] = {
                        'token': token,
                        'subslot': target_subslot,
                        'priority': self.subslot_priority.get(target_subslot, 999)
                    }
        
        return assignments
    
    def _apply_rephrase_rules(self, doc, assignments):
        """Rephraseルールに基づいてサブスロットに配置"""
        result = self._empty_subslots()
        subslot_tokens = defaultdict(list)
        
        # トークンをサブスロット別に分類
        for token_idx, assignment in assignments.items():
            subslot = assignment['subslot']
            token = assignment['token']
            subslot_tokens[subslot].append((token, assignment['priority']))
        
        # 各サブスロットで最適なトークンを選択・結合
        for subslot, token_list in subslot_tokens.items():
            if token_list:
                # 優先順位でソート
                token_list.sort(key=lambda x: (x[1], x[0].i))
                
                # スパンを構築（隣接トークンを結合）
                span_text = self._build_coherent_span(token_list, doc)
                result[subslot] = span_text
        
        return result
    
    def _build_coherent_span(self, token_list, doc):
        """文法的に一貫したスパンを構築"""
        if len(token_list) == 1:
            token = token_list[0][0]
            return self._get_extended_span(token, doc)
        
        # 複数トークンの場合、最も代表的なものを選択
        primary_token = token_list[0][0]
        return self._get_extended_span(primary_token, doc)
    
    def _get_extended_span(self, token, doc):
        """トークンとその修飾語を含む拡張スパン"""
        # 子トークン（修飾語）を含める
        span_tokens = [token]
        
        for child in token.children:
            # 重要な修飾語のみ含める
            if child.dep_ in ['det', 'amod', 'compound', 'poss']:
                span_tokens.append(child)
        
        # 位置順にソート
        span_tokens.sort(key=lambda t: t.i)
        
        if len(span_tokens) == 1:
            return token.text
        else:
            # 連続スパンを構築
            start_idx = min(t.i for t in span_tokens)
            end_idx = max(t.i for t in span_tokens) + 1
            return doc[start_idx:end_idx].text
    
    def _verify_complete_coverage(self, original, subslots):
        """100%単語保全確認"""
        original_words = set(w.lower() for w in original.split() if w.strip())
        covered_words = set()
        
        for value in subslots.values():
            if value and value.strip():
                covered_words.update(w.lower() for w in value.split() if w.strip())
        
        missing = original_words - covered_words
        return len(missing) == 0
    
    def _recover_missing_words(self, original, doc, current_result):
        """欠落単語の回復"""
        original_words = set(w.lower() for w in original.split())
        covered_words = set()
        
        for value in current_result.values():
            if value:
                covered_words.update(w.lower() for w in value.split())
        
        missing_words = original_words - covered_words
        
        if missing_words:
            # 欠落単語をsub-m3に追加（フォールバック）
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


# テスト実行
if __name__ == "__main__":
    engine = CompleteSpacyRephraseEngine()
    
    print('🎯 spaCy依存関係45個完全対応 統一分解エンジンテスト')
    print('=' * 100)
    
    # フルセットの重要例文でテスト
    test_cases = [
        "although it was emotionally hard",
        "that he had been trying to avoid Tom",
        "the woman who seemed indecisive",
        "because he was afraid of hurting her feelings",
        "the manager who had recently taken charge of the project"
    ]
    
    for phrase in test_cases:
        print(f'\n' + '='*80)
        print(f'📋 入力: "{phrase}"')
        result = engine.decompose(phrase)
        
        print('\n✅ 分解結果:')
        for key, value in result.items():
            if value:
                print(f'  {key:8}: "{value}"')
        
        # 単語保全確認
        original_words = len(phrase.split())
        covered_words = sum(len(v.split()) for v in result.values() if v)
        
        print(f'\n📊 単語保全: {original_words}語 → {covered_words}語', end='')
        if original_words == covered_words:
            print(' ✅ 100%保全')
        else:
            print(' ❌ 単語数不一致')
