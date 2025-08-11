import pandas as pd
import spacy
from collections import defaultdict

# Step18システムをインポート
from step18_unified_rephrase_system import Step18UnifiedRephraseSystem

class FullsetTester:
    """
    フルセット例文テスト・修正システム
    1例文ずつ処理→エラー発見→修正
    """
    
    def __init__(self):
        self.system = Step18UnifiedRephraseSystem()
        
    def load_fullset_data(self):
        """フルセットExcelを読み込み"""
        df = pd.read_excel('（小文字化した最初の5文型フルセット）例文入力元.xlsx')
        
        # 例文IDごとにデータを整理
        examples = {}
        example_ids = [eid for eid in df['例文ID'].unique() if pd.notna(eid)]
        
        for example_id in example_ids:
            example_data = df[df['例文ID'] == example_id]
            
            # 原文取得
            original_rows = example_data[example_data['原文'].notna()]
            original = original_rows['原文'].iloc[0] if len(original_rows) > 0 else ''
            
            # スロット別データ整理
            slots = {}
            for _, row in example_data.iterrows():
                if pd.notna(row['Slot']):
                    slot_name = row['Slot']
                    
                    if slot_name not in slots:
                        slots[slot_name] = {
                            'phrase': '',
                            'subslots': {}
                        }
                    
                    # スロット原句
                    if pd.isna(row['SubslotID']) and pd.notna(row['SlotPhrase']):
                        slots[slot_name]['phrase'] = row['SlotPhrase']
                    
                    # サブスロット
                    elif pd.notna(row['SubslotID']) and pd.notna(row['SubslotElement']):
                        slots[slot_name]['subslots'][row['SubslotID']] = row['SubslotElement']
            
            examples[example_id] = {
                'original': original,
                'slots': slots
            }
        
        return examples
    
    def test_single_example(self, example_id, example_data):
        """1例文をテスト"""
        print(f'\n🎯 例文テスト: {example_id}')
        print('=' * 100)
        
        original = example_data['original']
        expected_slots = example_data['slots']
        
        print(f'📋 原文: {original}')
        print()
        
        # 各スロットを個別テスト
        results = {}
        for slot_name, slot_info in expected_slots.items():
            phrase = slot_info['phrase']
            expected_subslots = slot_info['subslots']
            
            print(f'🔍 {slot_name}スロットテスト: "{phrase}"')
            
            if slot_name in ['Aux', 'V']:
                # 単一要素スロット
                actual_result = {slot_name.lower(): phrase}
                print(f'  単一要素: {slot_name.lower()} = "{phrase}"')
            else:
                # 統一分解エンジン適用
                actual_result = self.system._unified_decompose(phrase)
                
                print(f'  期待サブスロット:')
                for sub_id, sub_element in expected_subslots.items():
                    print(f'    {sub_id:10}: "{sub_element}"')
                
                print(f'  実際サブスロット:')
                for sub_id, sub_element in actual_result.items():
                    if sub_element:
                        print(f'    {sub_id:10}: "{sub_element}"')
                
                # 差分チェック
                self._check_differences(expected_subslots, actual_result, slot_name)
            
            results[slot_name] = actual_result
            print()
        
        return results
    
    def _check_differences(self, expected, actual, slot_name):
        """期待値vs実際値の差分チェック"""
        print(f'  🔍 差分チェック:')
        
        # 期待値にあって実際値にないもの
        missing = []
        for sub_id, expected_value in expected.items():
            if sub_id not in actual or not actual[sub_id]:
                missing.append((sub_id, expected_value))
        
        # 実際値にあって期待値にないもの
        extra = []
        for sub_id, actual_value in actual.items():
            if actual_value and sub_id not in expected:
                extra.append((sub_id, actual_value))
        
        # 値が異なるもの
        different = []
        for sub_id, expected_value in expected.items():
            if sub_id in actual and actual[sub_id] and actual[sub_id] != expected_value:
                different.append((sub_id, expected_value, actual[sub_id]))
        
        # レポート
        if not missing and not extra and not different:
            print(f'    ✅ 完全一致!')
        else:
            if missing:
                print(f'    ❌ 欠落: {missing}')
            if extra:
                print(f'    ⚠️  追加: {extra}')
            if different:
                print(f'    🔄 差異: {different}')
    
    def run_fullset_test(self, max_examples=None):
        """フルセットテスト実行"""
        print('🎯 フルセット12例文テスト開始')
        print('=' * 100)
        
        # データ読み込み
        examples = self.load_fullset_data()
        print(f'📊 読み込み完了: {len(examples)}例文')
        
        # 1例文ずつテスト
        test_count = 0
        for example_id, example_data in examples.items():
            if max_examples and test_count >= max_examples:
                break
                
            try:
                results = self.test_single_example(example_id, example_data)
                test_count += 1
                
                # 停止確認
                if test_count < len(examples):
                    input(f'\n⏸️  {example_id}完了。次の例文に進む？ (Enter)')
                
            except Exception as e:
                print(f'❌ エラー発生 {example_id}: {e}')
                import traceback
                traceback.print_exc()
                break
        
        print(f'\n🎯 テスト完了: {test_count}例文処理')


# テスト実行
if __name__ == "__main__":
    tester = FullsetTester()
    
    print('🎯 フルセット例文テスト・修正システム')
    print('=' * 100)
    print('各例文を1つずつ処理し、エラーを発見・修正していきます')
    print()
    
    # 最初の3例文でテスト開始
    tester.run_fullset_test(max_examples=3)
