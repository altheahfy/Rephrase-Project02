from dynamic_grammar_mapper import DynamicGrammarMapper
import logging
logging.basicConfig(level=logging.DEBUG)

mapper = DynamicGrammarMapper()
sentence = 'The student who studies diligently always succeeds academically.'

print('=== 文章分析結果 ===')
result = mapper.analyze_sentence(sentence)
print('main_slots:', result.get('main_slots', {}))
print('sub_slots:', result.get('sub_slots', {}))
print()
print('=== 主語スロット確認 ===')
if 'S' in result.get('main_slots', {}):
    s_content = result['main_slots']['S']
    print(f'S スロット内容: "{s_content}"')
    print(f'S スロット長さ: {len(s_content)}')
    if s_content == '':
        print('✓ 正しい：Sスロットは空文字列（サブスロットあり）')
    else:
        print('✗ 間違い：Sスロットが空文字列ではない')
else:
    print('ERROR: S スロットが見つかりません')
