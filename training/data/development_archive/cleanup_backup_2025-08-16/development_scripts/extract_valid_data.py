#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
確認済み正解データを抽出し、新しい54例文セットを構築
"""

import json
import codecs

def extract_valid_data():
    """正常なデータを抽出"""
    
    # 正常なエントリID（不整合チェック結果より）
    valid_ids = []
    for i in range(1, 55):
        if str(i) not in ['20', '21', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '41', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54']:
            valid_ids.append(str(i))
    
    print(f"✅ 使える正常データ: {len(valid_ids)}個")
    print(f"📝 正常ID: {valid_ids}")
    
    # データ読み込み
    with codecs.open('expected_results_progress.json', 'r', 'utf-8') as f:
        data = json.load(f)
    
    valid_data = {}
    for id in valid_ids:
        if id in data['correct_answers'] and data['correct_answers'][id]['expected'] is not None:
            entry = data['correct_answers'][id]
            valid_data[id] = {
                'sentence': entry['sentence'],
                'expected': entry['expected'],
                'notes': entry.get('notes', ''),
                'handler_type': classify_handler_type(entry['sentence'])
            }
    
    print(f"✅ 抽出成功: {len(valid_data)}個")
    
    # ハンドラー別分類
    handler_counts = {}
    for id, data_entry in valid_data.items():
        handler = data_entry['handler_type']
        if handler not in handler_counts:
            handler_counts[handler] = []
        handler_counts[handler].append(id)
    
    print(f"\n📊 ハンドラー別分布:")
    for handler, ids in handler_counts.items():
        print(f"  {handler}: {len(ids)}個 {ids}")
    
    return valid_data

def classify_handler_type(sentence):
    """例文からハンドラータイプを推定"""
    sentence_lower = sentence.lower()
    
    # 関係詞節判定
    if any(word in sentence_lower for word in ['who', 'which', 'that', 'whose', 'where', 'when', 'why', 'how']):
        return 'relative_clause'
    
    # 受動態判定
    if any(phrase in sentence_lower for phrase in ['was ', 'were ', 'is being', 'are being', 'been ', 'by ']):
        return 'passive_voice'
    
    # 副詞修飾判定（簡易）
    if any(word in sentence_lower for word in ['slowly', 'quickly', 'carefully', 'loudly', 'beautifully', 'diligently']):
        return 'adverbial_modifier'
    
    # デフォルトは基本文型
    return 'basic_five_pattern'

def create_new_test_sentences():
    """破損データ用の新例文を生成"""
    
    # 各ハンドラーをバランス良くテストする23個の新例文
    new_sentences = {
        # basic_five_pattern (6個)
        '20': 'Birds fly in the sky.',
        '21': 'Children play games.',
        '32': 'Students read books quietly.',
        '41': 'Teachers explain lessons clearly.',
        '45': 'Musicians play instruments.',
        '46': 'Artists paint beautiful pictures.',
        
        # relative_clause (6個)
        '23': 'The woman who sings is talented.',
        '24': 'The house that stands here is old.',
        '25': 'The child whose toy broke cried.',
        '26': 'The place where we met is special.',
        '27': 'The time when he came was perfect.',
        '28': 'The reason why she left is unknown.',
        
        # passive_voice (6個)
        '29': 'The window was broken yesterday.',
        '30': 'The letter is being written now.',
        '31': 'The cake was made by mother.',
        '47': 'The door was opened carefully.',
        '48': 'The message will be sent tomorrow.',
        '49': 'The problem has been solved.',
        
        # adverbial_modifier (5個)
        '50': 'She walks slowly in the park.',
        '51': 'He speaks clearly and loudly.',
        '52': 'They work hard every day.',
        '53': 'The rain falls gently outside.',
        '54': 'Students study seriously for exams.'
    }
    
    return new_sentences

if __name__ == "__main__":
    print("🔍 確認済み正解データ抽出開始")
    print("=" * 60)
    
    valid_data = extract_valid_data()
    new_sentences = create_new_test_sentences()
    
    print(f"\n📋 補完用新例文:")
    for id, sentence in new_sentences.items():
        print(f"  {id}: {sentence}")
    
    print(f"\n✅ 合計54例文セット準備完了")
    print(f"  - 既存正常データ: {len(valid_data)}個")
    print(f"  - 新規補完例文: {len(new_sentences)}個")
    print(f"  - 総計: {len(valid_data) + len(new_sentences)}個")
