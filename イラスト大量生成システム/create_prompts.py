import json
import re

# 新しく必要な単語リスト（先ほどの結果から）
needed_words = [
    'absent', 'academic', 'administrator', 'afternoon', 'alarm', 'analyze', 'appeared',
    'avoid', 'avoided', 'became', 'become', 'believed', 'briefing', 'building',
    'capable', 'catch', 'central', 'challenges', 'clarity', 'clouded', 'completed',
    'complex', 'composure', 'confidence', 'confident', 'counting', 'critical',
    'crucial', 'cruelty', 'data', 'days', 'decisive', 'dependable', 'determined',
    'direct', 'doubt', 'earlier', 'echoed', 'employee', 'encourage', 'engineer',
    'enhance', 'everyone', 'exhausting', 'experiment', 'facing', 'fatigue',
    'feared', 'figured', 'filled', 'final', 'flawlessly', 'full', 'given',
    'growth', 'hard', 'help', 'hesitation', 'instant', 'instructor', 'joined',
    'known', 'laboratory', 'lacked', 'leader', 'lessons', 'lingered', 'long',
    'make', 'math', 'mentally', 'meticulously', 'mind', 'missed', 'moment',
    'near', 'new', 'notice', 'occurred', 'offered', 'out', 'outage', 'outline',
    'people', 'point', 'policy', 'power', 'prepared', 'previous', 'prior',
    'privious', 'publication', 'recently', 'reflect', 'remarkable', 'reputation',
    'research', 'responded', 'responsible', 'returned', 'room', 'scientist',
    'seemed', 'severe', 'shown', 'silence', 'spoke', 'staff', 'students',
    'suggestions', 'support', 'taken', 'think', 'thoughts', 'tom', 'transferred',
    'trying', 'uncertainty', 'unexpected', 'voice', 'waiting', 'wanted', 'week',
    'working'
]

# 5つのAIツールに分割
chunk_size = len(needed_words) // 5
ai_tools = {
    'ChatGPT': needed_words[0:chunk_size],
    'Gemini': needed_words[chunk_size:chunk_size*2],
    'Bing_Image_Creator': needed_words[chunk_size*2:chunk_size*3],
    'Ideogram': needed_words[chunk_size*3:chunk_size*4],
    'Playground': needed_words[chunk_size*4:]
}

# 各単語に対するイラストコンセプト
word_concepts = {
    # 職業・人物
    'administrator': '事務的な作業をしている人（書類を持ち、メガネをかけた人）',
    'employee': '会社員（スーツを着た人、IDカードを付けている）',
    'engineer': '技術者（ヘルメットをかぶり、設計図を持つ人）',
    'instructor': '指導者（黒板の前で説明している人）',
    'leader': 'リーダー（前に立ち、手を上げて指示している人）',
    'scientist': '科学者（白衣を着て、試験管を持つ人）',
    'students': '学生たち（制服を着た複数の人）',
    
    # 感情・状態
    'absent': '空の椅子（誰もいない状態）',
    'confidence': '胸を張って立つ人（自信に満ちた表情）',
    'confident': '堂々とした姿勢の人（手を腰に当てて立つ）',
    'doubt': '首をかしげて困った表情の人（？マークが頭上に）',
    'fatigue': '疲れた表情で肩を落とした人（汗をかいている）',
    'feared': '恐怖で震えている人（手で顔を覆っている）',
    'hesitation': '迷っている人（ドアの前で立ち止まっている）',
    'uncertainty': '不安そうな表情で腕を組む人（眉間にしわ）',
    
    # 行動・動作
    'analyze': '虫眼鏡でグラフを見ている人',
    'avoid': '障害物を避けて歩く人（矢印で迂回を示す）',
    'catch': 'ボールをキャッチする人（手を伸ばしている）',
    'counting': '指で数を数えている人（指を立てている）',
    'encourage': '肩を叩いて励ます人（温かい表情）',
    'enhance': '何かを改良している人（道具を使って作業）',
    'experiment': '実験をしている人（フラスコと試験管）',
    'reflect': '鏡を見て考えている人（手を顎に当てて）',
    'research': '本を読んで調べている人（積まれた本と共に）',
    'think': '考えている人（手を頭に当て、思考の雲が浮かぶ）',
    'trying': '努力している人（汗をかいて頑張っている）',
    'waiting': '時計を見ながら待っている人（腕時計を確認）',
    'working': '仕事をしている人（デスクで作業中）',
    
    # 場所・物
    'afternoon': '太陽が傾いた空（時計が午後3時頃を指す）',
    'building': '高層ビル（シンプルな建物の外観）',
    'laboratory': '実験室（実験台とフラスコがある部屋）',
    'room': '部屋（ドアと窓がある四角い空間）',
    'alarm': '目覚まし時計（ベルが鳴っている様子）',
    'data': 'グラフと数字（棒グラフや円グラフ）',
    'publication': '本や雑誌（開いた本のページ）',
    
    # 抽象概念
    'academic': '卒業帽と卒業証書',
    'briefing': 'プレゼンテーション（画面と発表者）',
    'challenges': '山を登る人（困難を克服する象徴）',
    'clarity': '澄んだ水晶や透明なガラス',
    'complex': '複雑な歯車（絡み合った機械）',
    'composure': '落ち着いた表情で瞑想する人',
    'critical': '重要マーク（！マークと時計）',
    'crucial': '鍵（重要性を示す）',
    'growth': '成長する植物（芽から大きな木へ）',
    'policy': '規則書（ルールブック）',
    'power': '電球（アイデアや力の象徴）',
    'reputation': '星の評価（5つ星）',
    'silence': '静寂を示す人（人差し指を口に当てる）',
    'support': '支える人（倒れそうな人を支える）',
    'voice': '話している人（口から音波が出ている）'
}

# 基本プロンプトテンプレート
base_prompt = "A simple black-and-white line art illustration showing {concept}. The style should be clean, minimalistic cartoon-like drawing with clear black outlines on a white background. No colors, no shading, just clean line art suitable for educational vocabulary learning."

# AIツール別の特徴的なプロンプト調整
ai_specific_adjustments = {
    'ChatGPT': "Simple and clear educational illustration. ",
    'Gemini': "Clean line drawing for language learning. ",
    'Bing_Image_Creator': "Black and white educational clipart style. ",
    'Ideogram': "Minimalist line art for vocabulary teaching. ",
    'Playground': "Simple cartoon-style educational illustration. "
}

# プロンプト生成
print("=== AI別単語割り当てとプロンプト ===\n")

for ai_name, words in ai_tools.items():
    print(f"### {ai_name} ({len(words)}個の単語)")
    print(f"調整: {ai_specific_adjustments[ai_name]}")
    print("---")
    
    for word in words:
        concept = word_concepts.get(word, f"a visual representation of '{word}'")
        prompt = ai_specific_adjustments[ai_name] + base_prompt.format(concept=concept)
        print(f"**{word}**: {prompt}")
    
    print(f"\n{'='*50}\n")

# 概念別グループ化も表示
print("=== 概念別グループ化 ===\n")

concept_groups = {
    '職業・人物': ['administrator', 'employee', 'engineer', 'instructor', 'leader', 'scientist', 'students'],
    '感情・状態': ['absent', 'confidence', 'confident', 'doubt', 'fatigue', 'feared', 'hesitation', 'uncertainty'],
    '行動・動作': ['analyze', 'avoid', 'catch', 'counting', 'encourage', 'enhance', 'experiment', 'reflect', 'research', 'think', 'trying', 'waiting', 'working'],
    '場所・物': ['afternoon', 'building', 'laboratory', 'room', 'alarm', 'data', 'publication'],
    '抽象概念': ['academic', 'briefing', 'challenges', 'clarity', 'complex', 'composure', 'critical', 'crucial', 'growth', 'policy', 'power', 'reputation', 'silence', 'support', 'voice']
}

for group_name, words in concept_groups.items():
    print(f"### {group_name}")
    available_words = [w for w in words if w in needed_words]
    if available_words:
        for word in available_words:
            concept = word_concepts.get(word, f"a visual representation of '{word}'")
            print(f"- {word}: {concept}")
    print()
