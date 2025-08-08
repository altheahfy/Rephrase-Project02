"""
実際のAI文法分解処理のシミュレーション
どのようにルール辞書を使って判断しているか
"""

import json
import re
from typing import List, Dict, Tuple

class RuleBasedParser:
    """ルール辞書を使った文法分解エンジン"""
    
    def __init__(self, rules_file: str):
        """ルール辞書読み込み"""
        with open(rules_file, 'r', encoding='utf-8') as f:
            self.rules_data = json.load(f)
        
        self.rules = self.rules_data['rules']
        self.slot_order = self.rules_data['slot_order']
        
        print(f"📚 ルール辞書読み込み完了: {len(self.rules)}個のルール")
    
    def tokenize(self, sentence: str) -> List[str]:
        """文を単語に分解"""
        # 简単な分解（実際はより複雑）
        sentence = sentence.replace("'", "'")  # 特殊文字正規化
        tokens = re.findall(r"\b\w+'\w+|\b\w+|[.,!?]", sentence)
        return tokens
    
    def find_matching_rules(self, token: str, context: List[str]) -> List[Dict]:
        """トークンにマッチするルールを検索"""
        matching_rules = []
        
        for rule in self.rules:
            if self.rule_matches(rule, token, context):
                matching_rules.append(rule)
        
        # 優先度でソート
        matching_rules.sort(key=lambda r: r.get('priority', 0), reverse=True)
        return matching_rules
    
    def rule_matches(self, rule: Dict, token: str, context: List[str]) -> bool:
        """ルールがトークンにマッチするかチェック"""
        trigger = rule.get('trigger', {})
        
        # 直接トークンマッチ
        if 'token' in trigger:
            if trigger['token'].lower() == token.lower():
                return True
        
        # 語幹マッチ
        if 'lemma' in trigger:
            if token.lower() in [l.lower() for l in trigger['lemma']]:
                return True
        
        # 形態マッチ
        if 'form' in trigger:
            if token.lower() in [f.lower() for f in trigger['form']]:
                return True
        
        # パターンマッチ（簡易版）
        if 'pattern' in trigger:
            if re.search(trigger['pattern'], token.lower()):
                return True
                
        return False
    
    def apply_heuristics(self, token: str, position: int, tokens: List[str]) -> Tuple[str, str]:
        """ルールにマッチしない場合のヒューリスティック判断"""
        
        # 代名詞判定
        pronouns_s = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
        pronouns_o = ['me', 'him', 'her', 'us', 'them']
        
        if token.lower() in pronouns_s:
            return 'S', 'word'
        elif token.lower() in pronouns_o:
            return 'O1', 'word'
        
        # 位置ベース判定
        if position == 0:  # 文頭
            return 'S', 'word'
        
        # 動詞的要素の判定（簡易）
        verb_endings = ['ed', 'ing', 's']
        if any(token.lower().endswith(end) for end in verb_endings):
            return 'V', 'word'
        
        # デフォルト
        return 'O1', 'word'
    
    def parse_sentence(self, sentence: str) -> List[Dict]:
        """文を分解してスロット分類"""
        
        print(f"\n🔍 '{sentence}' の分解プロセス:")
        print("-" * 40)
        
        tokens = self.tokenize(sentence)
        print(f"1️⃣ トークン分解: {tokens}")
        
        results = []
        
        for i, token in enumerate(tokens):
            if token in ['.', ',', '!', '?']:  # 句読点スキップ
                continue
                
            print(f"\n2️⃣ '{token}' の分類:")
            
            # ルールマッチング
            matching_rules = self.find_matching_rules(token, tokens)
            
            if matching_rules:
                # 最優先ルールを適用
                best_rule = matching_rules[0]
                slot = best_rule['assign']['slot']
                phrase_type = best_rule['assign']['type']
                print(f"   📋 ルール適用: {best_rule['id']} → {slot}({phrase_type})")
            else:
                # ヒューリスティック判断
                slot, phrase_type = self.apply_heuristics(token, i, tokens)
                print(f"   🧠 ヒューリスティック判断: → {slot}({phrase_type})")
            
            results.append({
                'token': token,
                'slot': slot,
                'phrase_type': phrase_type,
                'position': i
            })
        
        return results
    
    def demonstrate_parsing(self):
        """分解デモンストレーション"""
        
        test_sentences = [
            "I can't afford it.",
            "Where did you get it?",
            "She got married with a bald man."
        ]
        
        for sentence in test_sentences:
            results = self.parse_sentence(sentence)
            
            print(f"\n3️⃣ 最終結果:")
            for result in results:
                print(f"   {result['slot']}: '{result['token']}' ({result['phrase_type']})")
            
            print("=" * 50)

def main():
    print("🚀 Rephraseルール辞書システム実演")
    print("=" * 50)
    
    # パーサー初期化
    parser = RuleBasedParser('rephrase_rules_v1.0.json')
    
    # デモンストレーション実行
    parser.demonstrate_parsing()
    
    print("\n💡 重要なポイント:")
    print("1. ルール辞書による自動分類が基本")
    print("2. ルールがない場合はヒューリスティック（経験的判断）")
    print("3. 優先度による競合解決")
    print("4. 文脈情報の活用")
    print("5. ユーザーフィードバックによる継続改善")
    
    print("\n🔄 改善サイクル:")
    print("エラー発見 → ルール追加/修正 → 再テスト → 精度向上")

if __name__ == "__main__":
    main()
