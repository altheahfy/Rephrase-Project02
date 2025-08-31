# 関係節デバッグ用スクリプト
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from central_controller import CentralController

# テストケース43を実行
controller = CentralController()
sentence = "The man who runs fast is strong."

print(f"=== 関係節テスト: {sentence} ===")
result = controller.process_sentence(sentence)

print("\n=== main_slots ===")
print(result.get('main_slots', {}))

print("\n=== sub_slots ===") 
print(result.get('sub_slots', {}))

print("\n=== ordered_slots ===")
print(result.get('ordered_slots', {}))

print("\n=== 完全な結果構造 ===")
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
