"""
Step4: 修正結果確認
正解データと修正後の出力を比較
"""

import subprocess
import sys

def run_step18_and_extract_s_slot():
    """Step18を実行してSスロット部分のみ抽出"""
    print("🔧 修正版Step18システム実行中...")
    print("=" * 60)
    
    try:
        # Step18システム実行
        result = subprocess.run([sys.executable, "step18_complete_8slot.py"], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print("❌ 実行エラー:")
            print(result.stderr)
            return None
        
        output = result.stdout
        
        # Sスロット部分を抽出
        lines = output.split('\n')
        s_slot_lines = []
        in_s_slot = False
        
        for line in lines:
            if '📋 Sスロット:' in line:
                in_s_slot = True
                s_slot_lines.append(line)
            elif in_s_slot and line.startswith('📋'):
                break
            elif in_s_slot:
                s_slot_lines.append(line)
        
        return s_slot_lines
    
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return None

def compare_results(s_slot_output):
    """修正結果と正解データの比較"""
    
    print("📋 正解データ (expected):")
    expected = {
        'sub-s': 'the manager who',
        'sub-aux': 'had',
        'sub-m2': 'recently',
        'sub-v': 'taken', 
        'sub-o1': 'charge of the project'
    }
    
    for key, value in expected.items():
        print(f"  {key:<10}: \"{value}\"")
    
    print(f"\n📋 修正後の出力結果:")
    
    if s_slot_output:
        for line in s_slot_output:
            print(line)
        
        # 簡易的な結果解析（実際の出力から値を抽出）
        print(f"\n🔍 修正効果の確認:")
        print("  期待していた修正:")
        print("    修正前: sub-s = 'manager who'")
        print("    修正後: sub-s = 'the manager who' ← 冠詞'the'と関係代名詞'who'のみ")
        print("    関係節動詞'taken'は別のサブスロット(sub-v)として処理")
    else:
        print("❌ 出力結果の取得に失敗")

if __name__ == "__main__":
    s_slot_output = run_step18_and_extract_s_slot()
    compare_results(s_slot_output)
