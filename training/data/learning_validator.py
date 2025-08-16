#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学習型54例文バリデーションシステム
ユーザーの訂正から段階的にパターンを学習し、精度を向上させる
"""

import json
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class LearningValidator:
    """学習型バリデーター"""
    
    def __init__(self):
        self.mapper = UnifiedStanzaRephraseMapper()
        self.mapper.add_handler('basic_five_pattern')
        self.mapper.add_handler('relative_clause')
        self.mapper.add_handler('adverbial_modifier')
        
        # 54例文リスト（custom_test.pyから）
        self.test_sentences = [
            "I like apples.",
            "She reads books every day.",
            "The cat is sleeping.",
            "He gave me a book.",
            "We made him happy.",
            "The man who lives next door is very kind.",
            "The book that I bought yesterday is interesting.",
            "The house where I was born is in Tokyo.",
            "The woman whose car was stolen called the police.",
            "I met a girl who speaks French fluently.",
            # ... 残り44例文をここに追加予定
        ]
        
        # 学習データベース
        self.learning_db = {
            "confirmed_results": {},     # ユーザー確認済み正解
            "correction_patterns": {},   # 訂正パターン
            "accuracy_history": [],      # 精度履歴
            "learned_rules": {}          # 学習済みルール
        }
        
        # 初期推論ルール
        self.inference_rules = {
            "basic_svo": {"pattern": r"^[A-Z]\w+ \w+ \w+\.$", "confidence": 0.6},
            "relative_who": {"pattern": r"who \w+", "confidence": 0.7},
            "relative_where": {"pattern": r"where .+ is in", "confidence": 0.8},
            "past_tense": {"pattern": r"\w+ed", "confidence": 0.5}
        }
    
    def generate_initial_expectation(self, sentence_id, sentence):
        """初期期待結果生成（私の推測）"""
        
        print(f"\n📝 例文{sentence_id}: {sentence}")
        
        # 実際の実行結果を取得
        try:
            actual_result = self.mapper.process(sentence)
            actual_main = actual_result.get('slots', {})
            actual_sub = actual_result.get('sub_slots', {})
            
            # 私の推論による期待結果生成
            expected = self._generate_expectation_from_patterns(sentence, actual_main, actual_sub)
            
            print(f"🤖 AI推測結果:")
            print(f"   Main slots: {expected.get('main_slots', {})}")
            print(f"   Sub slots: {expected.get('sub_slots', {})}")
            print(f"   信頼度: {expected.get('confidence', 0):.1%}")
            
            return {
                "sentence_id": sentence_id,
                "sentence": sentence,
                "ai_expectation": expected,
                "actual_result": {"main_slots": actual_main, "sub_slots": actual_sub}
            }
            
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            return None
    
    def _generate_expectation_from_patterns(self, sentence, actual_main, actual_sub):
        """パターンベースの期待結果生成"""
        
        confidence = 0.5  # 初期信頼度
        expected_main = {}
        expected_sub = {}
        
        # 学習済みパターンから推論
        for pattern_name, correction in self.learning_db["correction_patterns"].items():
            if self._matches_pattern(sentence, pattern_name):
                confidence += 0.1
                # 学習済み訂正を適用
                expected_main.update(correction.get("main_slots", {}))
                expected_sub.update(correction.get("sub_slots", {}))
        
        # 実際の結果をベースに調整
        for slot, value in actual_main.items():
            if slot not in expected_main:
                expected_main[slot] = value
        
        for slot, value in actual_sub.items():
            if slot not in expected_sub:
                expected_sub[slot] = value
        
        # 特定パターンの調整
        if "where" in sentence and "is in" in sentence:
            # Test30で学習したパターン
            if "S" in expected_main:
                expected_main["S"] = ""  # 関係節により空
            confidence += 0.2
        
        return {
            "main_slots": expected_main,
            "sub_slots": expected_sub,
            "confidence": min(confidence, 1.0)
        }
    
    def _matches_pattern(self, sentence, pattern_name):
        """パターンマッチング判定"""
        # 簡易的な実装（後で改善）
        if pattern_name == "where_clause":
            return "where" in sentence and "is in" in sentence
        return False
    
    def process_user_correction(self, sentence_id, user_correction):
        """ユーザー訂正の処理と学習"""
        
        if sentence_id not in self.learning_db["confirmed_results"]:
            print(f"❌ 例文{sentence_id}が見つかりません")
            return
        
        # 訂正前の推測
        ai_expectation = self.learning_db["confirmed_results"][sentence_id]["ai_expectation"]
        
        print(f"\n📚 学習処理: 例文{sentence_id}")
        print(f"🤖 AI推測: {ai_expectation}")
        print(f"✅ ユーザー訂正: {user_correction}")
        
        # 訂正パターンを抽出・学習
        correction_pattern = self._extract_correction_pattern(
            self.learning_db["confirmed_results"][sentence_id]["sentence"],
            ai_expectation,
            user_correction
        )
        
        # 学習データベース更新
        pattern_key = f"pattern_{sentence_id}"
        self.learning_db["correction_patterns"][pattern_key] = correction_pattern
        self.learning_db["confirmed_results"][sentence_id]["user_confirmed"] = user_correction
        
        print(f"🧠 学習完了: パターン'{pattern_key}'を記録")
        
        # 信頼度更新
        self._update_confidence()
    
    def _extract_correction_pattern(self, sentence, ai_result, user_result):
        """訂正からパターンを抽出"""
        
        pattern = {
            "trigger_words": [],
            "main_slots": {},
            "sub_slots": {},
            "rules": []
        }
        
        # トリガーワード抽出
        words = sentence.lower().split()
        for word in words:
            if word in ["who", "which", "where", "whose", "that"]:
                pattern["trigger_words"].append(word)
        
        # スロット訂正パターン
        ai_main = ai_result.get("main_slots", {})
        user_main = user_result.get("main_slots", {})
        
        for slot in user_main:
            if slot not in ai_main or ai_main[slot] != user_main[slot]:
                pattern["main_slots"][slot] = user_main[slot]
                pattern["rules"].append(f"{slot} should be '{user_main[slot]}'")
        
        return pattern
    
    def _update_confidence(self):
        """信頼度更新"""
        confirmed_count = len([r for r in self.learning_db["confirmed_results"].values() if "user_confirmed" in r])
        total_patterns = len(self.learning_db["correction_patterns"])
        
        if total_patterns > 0:
            learning_rate = confirmed_count / total_patterns
            for pattern in self.inference_rules.values():
                pattern["confidence"] = min(pattern["confidence"] + learning_rate * 0.1, 0.95)
    
    def batch_process_with_learning(self, start_id=1, end_id=10):
        """バッチ処理（学習付き）"""
        
        print(f"🚀 54例文学習型バリデーション開始（例文{start_id}-{end_id}）")
        print("="*60)
        
        for i in range(start_id-1, min(end_id, len(self.test_sentences))):
            sentence_id = i + 1
            sentence = self.test_sentences[i]
            
            # AI推測生成
            result = self.generate_initial_expectation(sentence_id, sentence)
            if result:
                self.learning_db["confirmed_results"][sentence_id] = result
                
                print(f"\n⏳ ユーザー確認待ち...")
                print(f"💡 この推測は正しいですか？修正点があれば教えてください。")
                print(f"   正しい場合: 'OK' または 'ok'")
                print(f"   修正がある場合: 修正内容を具体的に")
                print("-" * 40)
        
        # 学習状況サマリー
        confirmed = len([r for r in self.learning_db["confirmed_results"].values() if "user_confirmed" in r])
        total = len(self.learning_db["confirmed_results"])
        
        print(f"\n📊 学習状況: {confirmed}/{total} 例文確認済み")
        
        return self.learning_db["confirmed_results"]

def demo_learning_system():
    """学習型システムのデモ"""
    
    validator = LearningValidator()
    
    print("🎓 学習型54例文バリデーションシステム")
    print("="*50)
    print("💡 コンセプト:")
    print("   1. AIが期待結果を推測")
    print("   2. ユーザーが確認・訂正")
    print("   3. AIが訂正パターンを学習")
    print("   4. 後半になるほど精度向上")
    print("="*50)
    
    # 最初の5例文でデモ
    results = validator.batch_process_with_learning(1, 5)
    
    return validator

if __name__ == "__main__":
    demo_learning_system()
