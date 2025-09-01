"""
条件文の節境界識別デバッグツール
失敗している4つのケースの詳細分析
"""

import spacy
from central_controller import CentralController

class ClauseBoundaryDebugger:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.controller = CentralController()
    
    def debug_case(self, case_num, sentence):
        """個別ケースのデバッグ"""
        print(f"\n{'='*60}")
        print(f"🔍 Case {case_num}: {sentence}")
        print(f"{'='*60}")
        
        # spaCy解析結果
        doc = self.nlp(sentence)
        print(f"\n📋 spaCy解析:")
        for token in doc:
            print(f"   {token.i:2d}: '{token.text:10s}' dep={token.dep_:10s} pos={token.pos_:5s} tag={token.tag_:6s} head={token.head.text}")
        
        # 依存関係ツリー構造表示
        print(f"\n🌳 依存関係ツリー:")
        self._print_dependency_tree(doc)
        
        # カンマ分割結果
        print(f"\n✂️ カンマ分割テスト:")
        if ',' in sentence:
            parts = sentence.split(',', 1)
            print(f"   前半: '{parts[0].strip()}'")
            print(f"   後半: '{parts[1].strip()}'")
        else:
            print(f"   カンマなし: '{sentence}'")
        
        # _split_conditional_sentence結果
        print(f"\n🔧 _split_conditional_sentence結果:")
        try:
            if_clause, main_clause = self.controller._split_conditional_sentence(sentence)
            print(f"   条件節: '{if_clause}'")
            print(f"   主節: '{main_clause}'")
            
            # 主節の基本分解テスト
            print(f"\n⚙️ 主節基本分解テスト:")
            basic_result = self.controller._process_basic_decomposition(main_clause)
            print(f"   成功: {basic_result.get('success', False)}")
            if not basic_result.get('success', False):
                print(f"   エラー: {basic_result.get('error', 'Unknown error')}")
            else:
                print(f"   メインスロット: {basic_result.get('main_slots', {})}")
        except Exception as e:
            print(f"   エラー: {e}")
    
    def _print_dependency_tree(self, doc, level=0, visited=None):
        """依存関係ツリーの表示"""
        if visited is None:
            visited = set()
        
        # ROOTを探す
        if level == 0:
            for token in doc:
                if token.dep_ == 'ROOT':
                    self._print_token_tree(token, level, visited)
    
    def _print_token_tree(self, token, level, visited):
        """トークンツリーの再帰表示"""
        if token.i in visited:
            return
        visited.add(token.i)
        
        indent = "  " * level
        print(f"{indent}{token.text} ({token.dep_})")
        
        # 子要素を表示
        for child in token.children:
            self._print_token_tree(child, level + 1, visited)

def main():
    debugger = ClauseBoundaryDebugger()
    
    # 失敗している4つのケース
    failed_cases = {
        141: "Should you need help, please call me.",
        148: "As if I didn't know that already.",
        151: "But for your help, I would have failed.",
        152: "Without your support, we couldn't have succeeded."
    }
    
    for case_num, sentence in failed_cases.items():
        debugger.debug_case(case_num, sentence)

if __name__ == "__main__":
    main()
