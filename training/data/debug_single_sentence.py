#!/usr/bin/env python3
"""単一文のテスト（Excel_Generator.py）"""

from Excel_Generator import ExcelGeneratorV2

def test_single_sentence():
    generator = ExcelGeneratorV2()
    
    # 1つの文をテスト
    test_sentence = "I saw the building."
    print(f"テスト文: {test_sentence}")
    
    try:
        result = generator.analyze_and_add_sentence(test_sentence)
        print(f"戻り値: {result} (型: {type(result)})")
        
        if result:
            print("✅ 処理成功")
        else:
            print("❌ 処理失敗")
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        import traceback
        traceback.print_exc()
            
    except Exception as e:
        print(f"例外発生: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_sentence()
