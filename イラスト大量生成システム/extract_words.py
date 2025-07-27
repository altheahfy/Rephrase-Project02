import json
import re

# JSONファイルを読み込み
with open(r'c:\Users\yurit\Downloads\Rephraseプロジェクト進捗ファイル20250529\完全トレーニングUI完成フェーズ３\project-root\Rephrase-Project\slot_order_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 単語抽出用のセット
all_words = set()

# イラスト化に適さない単語（冠詞、前置詞、助動詞、疑問詞など）
skip_words = {
    'a', 'an', 'the', 'and', 'or', 'but', 'so', 'for', 'nor', 'yet',
    'at', 'in', 'on', 'by', 'with', 'from', 'to', 'of', 'about', 'over', 'under',
    'above', 'below', 'through', 'during', 'before', 'after', 'since', 'until',
    'between', 'among', 'against', 'toward', 'upon', 'within', 'without',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might',
    'can', 'could', 'must', 'ought',
    'what', 'where', 'when', 'why', 'how', 'who', 'whom', 'whose', 'which',
    'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
    'our', 'their', 'me', 'you', 'him', 'her', 'us', 'them', 'it',
    'i', 'he', 'she', 'we', 'they',
    'not', 'no', 'yes', 'if', 'unless', 'whether', 'as', 'than', 'while',
    'although', 'because', 'since', 'so', 'that', 'though', 'even', 'just',
    'only', 'also', 'too', 'very', 'quite', 'rather', 'much', 'many', 'more',
    'most', 'less', 'least', 'some', 'any', 'all', 'both', 'either', 'neither',
    'each', 'every', 'few', 'little', 'several', 'such', 'own', 'same', 'other',
    'another', 'next', 'last', 'first', 'second', 'third', 'enough', 'already',
    'still', 'yet', 'again', 'once', 'twice', 'here', 'there', 'now', 'then',
    'today', 'tomorrow', 'yesterday', 'soon', 'late', 'early', 'never', 'always',
    'often', 'sometimes', 'usually', 'rarely', 'seldom', 'hardly', 'barely',
    'nearly', 'almost', 'quite', 'really', 'actually', 'truly', 'certainly',
    'probably', 'perhaps', 'maybe', 'possibly', 'definitely', 'surely',
    'absolutely', 'completely', 'totally', 'entirely', 'fully', 'partly',
    'mainly', 'mostly', 'generally', 'especially', 'particularly', 'specifically'
}

# 各エントリから単語を抽出
for entry in data:
    # SlotPhraseから単語を抽出
    if entry.get('SlotPhrase'):
        words = re.findall(r'\b[a-zA-Z]+\b', entry['SlotPhrase'].lower())
        for word in words:
            if word not in skip_words and len(word) > 2:  # 2文字以下の単語は除外
                all_words.add(word)
    
    # SubslotElementから単語を抽出
    if entry.get('SubslotElement'):
        words = re.findall(r'\b[a-zA-Z]+\b', entry['SubslotElement'].lower())
        for word in words:
            if word not in skip_words and len(word) > 2:
                all_words.add(word)

# 既存のイラストファイル名を取得
existing_images = set()
import os
image_dir = r'c:\Users\yurit\Downloads\Rephraseプロジェクト進捗ファイル20250529\完全トレーニングUI完成フェーズ３\project-root\Rephrase-Project\slot_images\common'
if os.path.exists(image_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith('.png'):
            # ファイル名から拡張子を除去し、アンダースコアをスペースに変換
            base_name = filename[:-4].replace('_', ' ').lower()
            existing_images.add(base_name)

# 必要なイラストを特定
needed_words = sorted(all_words - existing_images)

print("=== 抽出された全単語 ===")
for word in sorted(all_words):
    print(word)

print(f"\n=== 既存のイラスト ({len(existing_images)}個) ===")
for img in sorted(existing_images):
    print(img)

print(f"\n=== 追加で必要な単語 ({len(needed_words)}個) ===")
for word in needed_words:
    print(word)
