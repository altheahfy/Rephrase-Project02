"""
Step1: managerトークンのスパン拡張デバッグ確認
"""

import spacy
from collections import defaultdict

# 簡易版Step18でmanagerの処理のみデバッグ
def debug_manager_span():
    nlp = spacy.load('en_core_web_sm')
    
    # ex007から該当部分のみ抽出
    fragment = "the manager who had recently taken charge of the project"
    doc = nlp(fragment)
    
    print("🔍 managerトークンの依存関係構造:")
    
    manager_token = None
    for token in doc:
        if token.text == 'manager':
            manager_token = token
            break
    
    if manager_token:
        print(f"  manager: dep={manager_token.dep_}, pos={manager_token.pos_}")
        print(f"  manager の子要素:")
        
        for child in manager_token.children:
            print(f"    '{child.text}': dep={child.dep_}, pos={child.pos_}")
        
        print(f"\n🔍 現在のスパン拡張ロジックでの処理:")
        
        # 現在のexpand_depsリスト
        expand_deps = ['det', 'poss', 'compound', 'amod', 'relcl']
        
        start = manager_token.i
        end = manager_token.i
        
        print(f"  初期範囲: [{start}, {end}] = '{doc[start:end+1]}'")
        
        for child in manager_token.children:
            print(f"  子要素 '{child.text}' (dep={child.dep_}):")
            if child.dep_ in expand_deps:
                print(f"    ✅ 拡張対象 - 範囲更新")
                start = min(start, child.i)
                end = max(end, child.i)
                print(f"    新範囲: [{start}, {end}] = '{doc[start:end+1]}'")
            else:
                print(f"    ❌ 拡張対象外")
        
        final_span = ' '.join([doc[i].text for i in range(start, end + 1)])
        print(f"\n📌 最終スパン結果: '{final_span}'")
        
        # 期待値との比較
        expected = "the manager who"
        if final_span == expected:
            print(f"✅ 期待値と一致")
        else:
            print(f"❌ 期待値不一致")
            print(f"   期待: '{expected}'")
            print(f"   実際: '{final_span}'")
            
            # 不一致の原因分析
            if 'the' not in final_span:
                print(f"   原因: 'the'が含まれていない")
                
                the_token = None
                for token in doc:
                    if token.text == 'the':
                        the_token = token
                        break
                
                if the_token:
                    print(f"   'the'の情報: dep={the_token.dep_}, head='{the_token.head.text}'")
                    if the_token.dep_ == 'det' and the_token.head == manager_token:
                        print(f"   'the'は正しくmanagerの子要素(det)として認識されている")
                        print(f"   問題: expand_depsに'det'が含まれているが拡張されない理由を調査必要")

if __name__ == "__main__":
    debug_manager_span()
