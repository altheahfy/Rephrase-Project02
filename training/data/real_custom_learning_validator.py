#!/usr/bin/env python3
"""
学習型54例文バリデーションシステム（実際のcustom_test.py使用版）
AI推測 → ユーザー訂正 → 学習改善のサイクル
"""

import json
import re
import ast
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class RealCustomLearningValidator:
    """学習型バリデーションシステム（実際のcustom_test.py例文版）"""
    
    def __init__(self):
        self.mapper = UnifiedStanzaRephraseMapper(log_level='INFO')
        self.mapper.add_handler('basic_five_pattern')
        self.mapper.add_handler('relative_clause')
        self.mapper.add_handler('adverbial_modifier')
        
        # custom_test.pyから実際の54例文を読み込み
        self.test_sentences = self._load_custom_test_sentences()
        
        # 学習データベース
        self.learning_db = {
            "correction_patterns": [],
            "confidence_scores": {},
            "confirmed_results": {}
        }
    
    def _load_custom_test_sentences(self):
        """custom_test.pyから実際の例文を読み込み"""
        try:
            with open('custom_test.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # your_test_sentences配列を抽出（改良版）
            sentences = []
            in_array = False
            bracket_count = 0
            
            lines = content.split('\n')
            for line in lines:
                if 'your_test_sentences = [' in line:
                    in_array = True
                    bracket_count = line.count('[') - line.count(']')
                    continue
                
                if in_array:
                    bracket_count += line.count('[') - line.count(']')
                    
                    # 文字列リテラルを抽出
                    string_matches = re.findall(r'"([^"]*)"', line)
                    for match in string_matches:
                        sentence = match.strip()
                        if sentence and not sentence.startswith('#') and len(sentence) > 5:
                            sentences.append(sentence)
                    
                    if bracket_count <= 0:
                        break
            
            print(f"✅ custom_test.pyから{len(sentences)}例文を読み込みました")
            return sentences
            
        except Exception as e:
            print(f"⚠️  custom_test.py読み込みエラー: {e}")
            print("📋 フォールバック例文を使用します")
            return [
                "The man who runs fast is strong.",
                "The book which I bought is expensive.",
                "The car which was crashed is red.",
                "The place where we met is beautiful.",
                "The book I read yesterday was boring."
            ]
    
    def generate_initial_expectation(self, sentence_id, sentence):
        """AI初期推測生成"""
        
        print(f"\n📝 例文{sentence_id}: {sentence}")
        
        try:
            # 実際のマッパー処理
            result = self.mapper.process(sentence)
            
            main_slots = result.get('slots', {})
            sub_slots = result.get('sub_slots', {})
            
            # 信頼度計算（学習データベースから）
            confidence = self._calculate_confidence(sentence, main_slots, sub_slots)
            
            ai_expectation = {
                "sentence": sentence,
                "main_slots": main_slots,
                "sub_slots": sub_slots,
                "confidence": confidence,
                "ai_expectation": {
                    "main_slots": main_slots,
                    "sub_slots": sub_slots
                }
            }
            
            print(f"🤖 AI推測結果:")
            print(f"   Main slots: {main_slots}")
            print(f"   Sub slots: {sub_slots}")
            print(f"   信頼度: {confidence:.1f}%")
            
            return ai_expectation
            
        except Exception as e:
            print(f"❌ 処理エラー: {e}")
            return None
    
    def _calculate_confidence(self, sentence, main_slots, sub_slots):
        """信頼度計算（学習履歴ベース）"""
        
        # 基本信頼度
        base_confidence = 50.0
        
        # 学習パターンマッチング
        for pattern in self.learning_db["correction_patterns"]:
            if self._pattern_matches(sentence, pattern):
                # 過去の訂正頻度で信頼度調整
                correction_rate = pattern.get("correction_rate", 0.5)
                base_confidence *= (1 - correction_rate)
        
        # スロット数による信頼度調整
        total_slots = len(main_slots) + len(sub_slots)
        if total_slots > 4:
            base_confidence *= 0.8  # 複雑文は信頼度下降
        
        # 特殊パターン検出
        special_patterns = ["who", "which", "where", "whose", "that"]
        for pattern in special_patterns:
            if pattern in sentence.lower():
                base_confidence *= 0.7  # 関係詞は難しい
                break
        
        return min(95.0, max(20.0, base_confidence))
    
    def _pattern_matches(self, sentence, pattern):
        """パターンマッチング簡易版"""
        # 簡易的な実装（後で改善）
        trigger_words = pattern.get("trigger_words", [])
        for word in trigger_words:
            if word in sentence.lower():
                return True
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
            self.test_sentences[sentence_id-1], 
            ai_expectation, 
            user_correction
        )
        
        if correction_pattern:
            self.learning_db["correction_patterns"].append(correction_pattern)
            print(f"🧠 新パターン学習: {correction_pattern['pattern_name']}")
        
        # 確認済みマーク
        self.learning_db["confirmed_results"][sentence_id]["user_confirmed"] = True
        self.learning_db["confirmed_results"][sentence_id]["user_correction"] = user_correction
        
        print("✅ 学習完了")
    
    def _extract_correction_pattern(self, sentence, ai_result, user_result):
        """訂正パターン抽出"""
        
        pattern = {
            "pattern_name": f"correction_{len(self.learning_db['correction_patterns'])+1}",
            "sentence_example": sentence,
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
    
    def batch_process_with_learning(self, start_idx=1, end_idx=5):
        """学習型バッチ処理"""
        
        print(f"🚀 54例文学習型バリデーション開始（例文{start_idx}-{end_idx}）")
        print("="*60)
        
        for i in range(start_idx-1, min(end_idx, len(self.test_sentences))):
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
    
    def get_learning_stats(self):
        """学習統計情報"""
        return {
            "total_patterns": len(self.learning_db["correction_patterns"]),
            "confirmed_sentences": len([r for r in self.learning_db["confirmed_results"].values() if "user_confirmed" in r]),
            "total_sentences": len(self.test_sentences),
            "patterns": self.learning_db["correction_patterns"]
        }

def demo_real_custom_system():
    """学習型システムのデモ（実際のcustom_test.py使用）"""
    
    validator = RealCustomLearningValidator()
    
    print("🎓 学習型54例文バリデーションシステム（実際のcustom_test.py版）")
    print("="*60)
    print("💡 コンセプト:")
    print("   1. custom_test.pyの実際の54例文を使用")
    print("   2. AIが期待結果を推測")
    print("   3. ユーザーが確認・訂正")
    print("   4. AIが訂正パターンを学習")
    print("   5. 後半になるほど精度向上")
    print("="*60)
    
    # 実際の例文確認
    print(f"\n📖 読み込み例文数: {len(validator.test_sentences)}")
    print("最初の5例文:")
    for i, sentence in enumerate(validator.test_sentences[:5], 1):
        print(f"  {i}. {sentence}")
    
    print("\n" + "="*60)
    
    # 最初の3例文でデモ
    results = validator.batch_process_with_learning(1, 3)
    
    return validator

if __name__ == "__main__":
    demo_real_custom_system()
