import json

# final_54_test_data.jsonから関係節関連文を抽出
with open('final_test_system/final_54_test_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

relative_tests = []
for test_id, test_case in data['data'].items():
    sentence = test_case['sentence']
    # 関係節キーワードを含む文
    if any(word in sentence.lower() for word in ['who', 'whose', 'which', 'that']):
        # 受動態は除く
        if not any(word in sentence.lower() for word in ['was', 'were', 'been']):
            relative_tests.append({
                'id': test_id,
                'sentence': sentence,
                'expected': test_case['expected']
            })

print(f'関係節関連文（受動態除く）: {len(relative_tests)}件')
print()
for test in relative_tests:
    print(f'Test {test["id"]}: {test["sentence"]}')
    
# Python辞書形式で出力（run_official_test.pyに追加用）
print('\n' + '='*60)
print('run_official_test.pyに追加するテストケース:')
print('='*60)

for test in relative_tests:
    print(f'''        {{
            "id": "{test['id']}",
            "sentence": "{test['sentence']}",
            "expected": {json.dumps(test['expected'], ensure_ascii=False)}
        }},''')
