import re

print('🔍 Step15でのspaCy依存関係使用状況分析')
print('=' * 80)

# Step15のコードを読み込み
with open('archive/step15_enhanced_universal.py', 'r', encoding='utf-8') as f:
    step15_code = f.read()

# 全spaCy依存関係ラベル
all_dep_labels = [
    'ROOT', 'acl', 'acomp', 'advcl', 'advmod', 'agent', 'amod', 'appos', 'attr', 
    'aux', 'auxpass', 'case', 'cc', 'ccomp', 'compound', 'conj', 'csubj', 'csubjpass', 
    'dative', 'dep', 'det', 'dobj', 'expl', 'intj', 'mark', 'meta', 'neg', 'nmod', 
    'npadvmod', 'nsubj', 'nsubjpass', 'nummod', 'oprd', 'parataxis', 'pcomp', 'pobj', 
    'poss', 'preconj', 'predet', 'prep', 'prt', 'punct', 'quantmod', 'relcl', 'xcomp'
]

# Step15で使用されている依存関係を検索
used_deps = set()
dep_pattern = r'\.dep_\s*==?\s*["\'](\w+)["\']'
matches = re.findall(dep_pattern, step15_code)

for match in matches:
    used_deps.add(match)

# "in" 演算子での使用も検索
in_pattern = r'\.dep_\s+in\s+\[["\']([^]]+)["\']\]'
in_matches = re.findall(in_pattern, step15_code)
for match in in_matches:
    # カンマ区切りの依存関係を分解
    deps_in_list = re.findall(r'["\'](\w+)["\']', match)
    used_deps.update(deps_in_list)

print(f'📊 Step15で使用されている依存関係数: {len(used_deps)}')
print(f'📊 spaCy全依存関係数: {len(all_dep_labels)}')
print(f'📊 カバレッジ: {len(used_deps)}/{len(all_dep_labels)} ({len(used_deps)/len(all_dep_labels)*100:.1f}%)')

print(f'\n✅ Step15で使用されている依存関係:')
for i, dep in enumerate(sorted(used_deps), 1):
    print(f'{i:2d}. {dep}')

unused_deps = set(all_dep_labels) - used_deps
print(f'\n❌ Step15で未使用の依存関係 ({len(unused_deps)}個):')
for i, dep in enumerate(sorted(unused_deps), 1):
    print(f'{i:2d}. {dep}')

print(f'\n🎯 結論:')
if len(used_deps) == len(all_dep_labels):
    print('✅ Step15は spaCy の全45依存関係を100%活用しています！')
elif len(used_deps) >= 35:
    print('🔥 Step15は spaCy の大部分の依存関係を活用しています（優秀）')
elif len(used_deps) >= 20:
    print('⭐ Step15は spaCy の依存関係を良く活用しています')
else:
    print('⚠️  Step15の spaCy 活用度は改善の余地があります')
