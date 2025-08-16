#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
パターン認識型バリデーションシステム
少数の手動確認から多数のテストケースを自動推論
"""

import json
import re
from unified_stanza_rephrase_mapper import UnifiedStanzaRephraseMapper

class PatternInferenceValidator:
    """パターン認識・推論型バリデーター"""
    
    def __init__(self):
        self.mapper = UnifiedStanzaRephraseMapper()
        self.mapper.add_handler('basic_five_pattern')
        self.mapper.add_handler('relative_clause')
        self.mapper.add_handler('adverbial_modifier')
        
        # 確認済みパターンデータベース
        self.confirmed_patterns = {}
        
        # パターン推論ルール
        self.inference_rules = {
            "where_clause_pattern": {
                "trigger": r"where.*is.*in",
                "expected_structure": {
                    "main_slots": {"S": "", "V": "is", "C2": "in [LOCATION]"},
                    "sub_slots": {"sub-m3": "[NOUN] where", "sub-s": "I", "sub-aux": "was", "sub-v": "[VERB]"}
                },
                "confidence": 0.8
            }
        }
    
    def register_confirmed_pattern(self, test_name, sentence, confirmed_result, pattern_type):
        """手動確認済みパターンを登録"""
        self.confirmed_patterns[test_name] = {
            "sentence": sentence,
            "result": confirmed_result,
            "pattern_type": pattern_type,
            "confirmed_by": "manual_inspection"
        }
        
        # パターンから推論ルールを更新
        self._update_inference_rules(sentence, confirmed_result, pattern_type)
        
        print(f"✅ パターン登録: {test_name} ({pattern_type})")
    
    def _update_inference_rules(self, sentence, result, pattern_type):
        """確認済み結果から推論ルールを更新"""
        # 例：where構文パターンの推論ルール更新
        if "where" in sentence and "is" in sentence:
            self.inference_rules["where_clause_pattern"]["confidence"] = 0.9
            print(f"🧠 推論ルール更新: where構文パターンの信頼度向上")
    
    def infer_expected_result(self, sentence):
        """パターン認識による期待結果推論"""
        
        # 登録済みパターンとの類似度チェック
        for test_name, pattern_data in self.confirmed_patterns.items():
            similarity = self._calculate_similarity(sentence, pattern_data["sentence"])
            if similarity > 0.7:
                # 類似パターンからの推論
                inferred = self._adapt_pattern(sentence, pattern_data["result"])
                return {
                    "expected": inferred,
                    "confidence": similarity,
                    "based_on": test_name,
                    "method": "pattern_similarity"
                }
        
        # 推論ルールによる推論
        for rule_name, rule in self.inference_rules.items():
            if re.search(rule["trigger"], sentence, re.IGNORECASE):
                inferred = self._apply_inference_rule(sentence, rule)
                return {
                    "expected": inferred,
                    "confidence": rule["confidence"],
                    "based_on": rule_name,
                    "method": "rule_inference"
                }
        
        return {"expected": None, "confidence": 0, "method": "no_inference"}
    
    def _calculate_similarity(self, sentence1, sentence2):
        """文章類似度計算（簡易版）"""
        words1 = set(sentence1.lower().split())
        words2 = set(sentence2.lower().split())
        
        # Jaccard類似度
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def _adapt_pattern(self, new_sentence, reference_result):
        """類似パターンを新しい文章に適応"""
        # 簡易的な適応（実際にはより洗練された処理が必要）
        adapted = json.loads(json.dumps(reference_result))  # deep copy
        
        # 文章固有の要素を抽出・置換
        words = new_sentence.split()
        
        # 例：場所名の置換
        for i, word in enumerate(words):
            if word.endswith('.'):
                location = word[:-1]
                if 'C2' in adapted.get('main_slots', {}):
                    if adapted['main_slots']['C2'].startswith('in '):
                        adapted['main_slots']['C2'] = f"in {location}"
        
        return adapted
    
    def _apply_inference_rule(self, sentence, rule):
        """推論ルールを適用"""
        template = rule["expected_structure"]
        adapted = json.loads(json.dumps(template))  # deep copy
        
        # テンプレートの変数を実際の値に置換
        words = sentence.split()
        
        # 場所名抽出
        location = None
        for i, word in enumerate(words):
            if word.endswith('.') or i == len(words) - 1:
                location = word.rstrip('.')
                break
        
        if location and 'main_slots' in adapted and 'C2' in adapted['main_slots']:
            adapted['main_slots']['C2'] = adapted['main_slots']['C2'].replace('[LOCATION]', location)
        
        return adapted
    
    def smart_validate(self, test_name, sentence):
        """スマートバリデーション（推論+実行+検証）"""
        
        print(f"🧪 スマートバリデーション: {test_name}")
        print(f"📝 文章: {sentence}")
        
        # 1. 推論による期待結果生成
        inference = self.infer_expected_result(sentence)
        
        if inference["expected"] is None:
            print("⚠️ パターン推論失敗 - 手動確認が必要")
            return {"status": "manual_required", "sentence": sentence}
        
        print(f"🧠 推論結果 (信頼度: {inference['confidence']:.2f}, 根拠: {inference['based_on']})")
        
        # 2. 実際の実行
        try:
            actual_result = self.mapper.process(sentence)
            actual_main = actual_result.get('slots', {})
            actual_sub = actual_result.get('sub_slots', {})
            
            # 3. 推論結果との比較
            expected = inference["expected"]
            expected_main = expected.get('main_slots', {})
            expected_sub = expected.get('sub_slots', {})
            
            validation_results = []
            all_correct = True
            
            # メインスロット検証
            for slot, expected_value in expected_main.items():
                actual_value = actual_main.get(slot, "MISSING")
                is_correct = actual_value == expected_value
                if not is_correct:
                    all_correct = False
                
                validation_results.append({
                    'slot': slot,
                    'expected': expected_value,
                    'actual': actual_value,
                    'correct': is_correct
                })
            
            # サブスロット検証
            for slot, expected_value in expected_sub.items():
                actual_value = actual_sub.get(slot, "MISSING")
                is_correct = actual_value == expected_value
                if not is_correct:
                    all_correct = False
                
                validation_results.append({
                    'slot': slot,
                    'expected': expected_value,
                    'actual': actual_value,
                    'correct': is_correct
                })
            
            # 結果判定
            passed = sum(1 for r in validation_results if r['correct'])
            total = len(validation_results)
            success_rate = passed / total if total > 0 else 0
            
            print(f"📊 結果: {passed}/{total} 項目一致 (成功率: {success_rate:.1%})")
            
            if success_rate >= 0.8:  # 80%以上で合格
                print(f"✅ 推論バリデーション成功！ (信頼度: {inference['confidence']:.2f})")
                return {"status": "validated", "success_rate": success_rate, "inference": inference}
            else:
                print(f"⚠️ 推論バリデーション失敗 - 手動確認推奨")
                print("❌ 不一致項目:")
                for r in validation_results:
                    if not r['correct']:
                        print(f"   {r['slot']}: '{r['actual']}' → '{r['expected']}'")
                return {"status": "manual_recommended", "details": validation_results}
        
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
            return {"status": "error", "error": str(e)}

def demo_pattern_inference():
    """パターン推論デモ"""
    
    validator = PatternInferenceValidator()
    
    print("🧠 パターン認識型バリデーションシステム デモ")
    print("="*60)
    
    # Step 1: 手動確認済みパターンを登録（Test30から）
    validator.register_confirmed_pattern(
        test_name="test30",
        sentence="The house where I was born is in Tokyo.",
        confirmed_result={
            "main_slots": {"S": "", "V": "is", "C2": "in Tokyo"},
            "sub_slots": {"sub-m3": "The house where", "sub-s": "I", "sub-aux": "was", "sub-v": "born"}
        },
        pattern_type="where_clause_location"
    )
    
    print("\n" + "="*60)
    
    # Step 2: 類似パターンの自動推論テスト
    similar_sentences = [
        "The school where I studied is in Paris.",
        "The restaurant where we met is in London.",
        "The hotel where they stayed is in Rome."
    ]
    
    for i, sentence in enumerate(similar_sentences, 1):
        print(f"\n--- 類似パターン推論テスト {i} ---")
        result = validator.smart_validate(f"auto_test_{i}", sentence)
        
        if result["status"] == "validated":
            print(f"🎉 自動バリデーション成功！")
        elif result["status"] == "manual_recommended":
            print(f"🔍 手動確認推奨")
        else:
            print(f"📋 手動確認必須")
    
    return validator

if __name__ == "__main__":
    demo_pattern_inference()
