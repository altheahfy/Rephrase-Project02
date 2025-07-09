#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

# 修正が必要な語形変化のマッピング
corrections = {
    # 不規則動詞
    "know": {
        "meta_tags": ["know", "knows", "knowing", "knew", "known"],
        "description": "知る"
    },
    "early": {
        "meta_tags": ["early", "earlier", "earliest"],
        "description": "早い"
    },
    "take": {
        "meta_tags": ["take", "takes", "taking", "took", "taken"],
        "description": "取る"
    },
    "make": {
        "meta_tags": ["make", "makes", "making", "made"],
        "description": "作る"
    },
    "come": {
        "meta_tags": ["come", "comes", "coming", "came"],
        "description": "来る"
    },
    "go": {
        "meta_tags": ["go", "goes", "going", "went", "gone"],
        "description": "行く"
    },
    "see": {
        "meta_tags": ["see", "sees", "seeing", "saw", "seen"],
        "description": "見る"
    },
    "get": {
        "meta_tags": ["get", "gets", "getting", "got", "gotten"],
        "description": "得る"
    },
    "do": {
        "meta_tags": ["do", "does", "doing", "did", "done"],
        "description": "する"
    },
    "have": {
        "meta_tags": ["have", "has", "having", "had"],
        "description": "持つ"
    },
    "be": {
        "meta_tags": ["be", "am", "is", "are", "being", "was", "were", "been"],
        "description": "である"
    },
    "become": {
        "meta_tags": ["become", "becomes", "becoming", "became"],
        "description": "なる"
    },
    "begin": {
        "meta_tags": ["begin", "begins", "beginning", "began", "begun"],
        "description": "始める"
    },
    "find": {
        "meta_tags": ["find", "finds", "finding", "found"],
        "description": "見つける"
    },
    "think": {
        "meta_tags": ["think", "thinks", "thinking", "thought"],
        "description": "考える"
    },
    "feel": {
        "meta_tags": ["feel", "feels", "feeling", "felt"],
        "description": "感じる"
    },
    "tell": {
        "meta_tags": ["tell", "tells", "telling", "told"],
        "description": "話す"
    },
    "say": {
        "meta_tags": ["say", "says", "saying", "said"],
        "description": "言う"
    },
    "put": {
        "meta_tags": ["put", "puts", "putting"],
        "description": "置く"
    },
    "let": {
        "meta_tags": ["let", "lets", "letting"],
        "description": "させる"
    },
    "run": {
        "meta_tags": ["run", "runs", "running", "ran"],
        "description": "走る"
    },
    "write": {
        "meta_tags": ["write", "writes", "writing", "wrote", "written"],
        "description": "書く"
    },
    "read": {
        "meta_tags": ["read", "reads", "reading"],
        "description": "読む"
    },
    "leave": {
        "meta_tags": ["leave", "leaves", "leaving", "left"],
        "description": "去る"
    },
    "build": {
        "meta_tags": ["build", "builds", "building", "built"],
        "description": "建てる"
    },
    "buy": {
        "meta_tags": ["buy", "buys", "buying", "bought"],
        "description": "買う"
    },
    "bring": {
        "meta_tags": ["bring", "brings", "bringing", "brought"],
        "description": "持ってくる"
    },
    "catch": {
        "meta_tags": ["catch", "catches", "catching", "caught"],
        "description": "捕まえる"
    },
    "teach": {
        "meta_tags": ["teach", "teaches", "teaching", "taught"],
        "description": "教える"
    },
    "learn": {
        "meta_tags": ["learn", "learns", "learning", "learned", "learnt"],
        "description": "学ぶ"
    },
    "send": {
        "meta_tags": ["send", "sends", "sending", "sent"],
        "description": "送る"
    },
    "spend": {
        "meta_tags": ["spend", "spends", "spending", "spent"],
        "description": "費やす"
    },
    "meet": {
        "meta_tags": ["meet", "meets", "meeting", "met"],
        "description": "会う"
    },
    "hear": {
        "meta_tags": ["hear", "hears", "hearing", "heard"],
        "description": "聞く"
    },
    "keep": {
        "meta_tags": ["keep", "keeps", "keeping", "kept"],
        "description": "保つ"
    },
    "lose": {
        "meta_tags": ["lose", "loses", "losing", "lost"],
        "description": "失う"
    },
    "win": {
        "meta_tags": ["win", "wins", "winning", "won"],
        "description": "勝つ"
    },
    "cut": {
        "meta_tags": ["cut", "cuts", "cutting"],
        "description": "切る"
    },
    "hit": {
        "meta_tags": ["hit", "hits", "hitting"],
        "description": "打つ"
    },
    "set": {
        "meta_tags": ["set", "sets", "setting"],
        "description": "設定する"
    },
    "sit": {
        "meta_tags": ["sit", "sits", "sitting", "sat"],
        "description": "座る"
    },
    "stand": {
        "meta_tags": ["stand", "stands", "standing", "stood"],
        "description": "立つ"
    },
    "understand": {
        "meta_tags": ["understand", "understands", "understanding", "understood"],
        "description": "理解する"
    },
    "hold": {
        "meta_tags": ["hold", "holds", "holding", "held"],
        "description": "持つ"
    },
    "wear": {
        "meta_tags": ["wear", "wears", "wearing", "wore", "worn"],
        "description": "着る"
    },
    "break": {
        "meta_tags": ["break", "breaks", "breaking", "broke", "broken"],
        "description": "壊す"
    },
    "choose": {
        "meta_tags": ["choose", "chooses", "choosing", "chose", "chosen"],
        "description": "選ぶ"
    },
    "speak": {
        "meta_tags": ["speak", "speaks", "speaking", "spoke", "spoken"],
        "description": "話す"
    },
    "drive": {
        "meta_tags": ["drive", "drives", "driving", "drove", "driven"],
        "description": "運転する"
    },
    "fall": {
        "meta_tags": ["fall", "falls", "falling", "fell", "fallen"],
        "description": "落ちる"
    },
    "fly": {
        "meta_tags": ["fly", "flies", "flying", "flew", "flown"],
        "description": "飛ぶ"
    },
    "forget": {
        "meta_tags": ["forget", "forgets", "forgetting", "forgot", "forgotten"],
        "description": "忘れる"
    },
    "grow": {
        "meta_tags": ["grow", "grows", "growing", "grew", "grown"],
        "description": "成長する"
    },
    "throw": {
        "meta_tags": ["throw", "throws", "throwing", "threw", "thrown"],
        "description": "投げる"
    },
    "drink": {
        "meta_tags": ["drink", "drinks", "drinking", "drank", "drunk"],
        "description": "飲む"
    },
    "eat": {
        "meta_tags": ["eat", "eats", "eating", "ate", "eaten"],
        "description": "食べる"
    },
    "sleep": {
        "meta_tags": ["sleep", "sleeps", "sleeping", "slept"],
        "description": "眠る"
    },
    "swim": {
        "meta_tags": ["swim", "swims", "swimming", "swam", "swum"],
        "description": "泳ぐ"
    },
    "sing": {
        "meta_tags": ["sing", "sings", "singing", "sang", "sung"],
        "description": "歌う"
    },
    "draw": {
        "meta_tags": ["draw", "draws", "drawing", "drew", "drawn"],
        "description": "描く"
    },
    "ride": {
        "meta_tags": ["ride", "rides", "riding", "rode", "ridden"],
        "description": "乗る"
    },
    "shut": {
        "meta_tags": ["shut", "shuts", "shutting"],
        "description": "閉める"
    },
    "cost": {
        "meta_tags": ["cost", "costs", "costing"],
        "description": "費用がかかる"
    },
    "hurt": {
        "meta_tags": ["hurt", "hurts", "hurting"],
        "description": "傷つける"
    },
    # 比較級・最上級を持つ形容詞
    "good": {
        "meta_tags": ["good", "better", "best"],
        "description": "良い"
    },
    "bad": {
        "meta_tags": ["bad", "worse", "worst"],
        "description": "悪い"
    },
    "big": {
        "meta_tags": ["big", "bigger", "biggest"],
        "description": "大きい"
    },
    "small": {
        "meta_tags": ["small", "smaller", "smallest"],
        "description": "小さい"
    },
    "old": {
        "meta_tags": ["old", "older", "oldest"],
        "description": "古い"
    },
    "new": {
        "meta_tags": ["new", "newer", "newest"],
        "description": "新しい"
    },
    "easy": {
        "meta_tags": ["easy", "easier", "easiest"],
        "description": "簡単な"
    },
    "hard": {
        "meta_tags": ["hard", "harder", "hardest"],
        "description": "難しい"
    },
    "fast": {
        "meta_tags": ["fast", "faster", "fastest"],
        "description": "速い"
    },
    "slow": {
        "meta_tags": ["slow", "slower", "slowest"],
        "description": "遅い"
    },
    "high": {
        "meta_tags": ["high", "higher", "highest"],
        "description": "高い"
    },
    "low": {
        "meta_tags": ["low", "lower", "lowest"],
        "description": "低い"
    },
    "long": {
        "meta_tags": ["long", "longer", "longest"],
        "description": "長い"
    },
    "short": {
        "meta_tags": ["short", "shorter", "shortest"],
        "description": "短い"
    },
    "young": {
        "meta_tags": ["young", "younger", "youngest"],
        "description": "若い"
    }
}

def fix_meta_tags():
    try:
        # image_meta_tags.jsonを読み込み
        meta_tags_path = './image_meta_tags.json'
        
        if not os.path.exists(meta_tags_path):
            print(f"エラー: {meta_tags_path} が見つかりません")
            return
        
        with open(meta_tags_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed_count = 0
        
        # 各画像のメタタグをチェック・修正
        for item in data:
            base_name = item['image_file'].replace('.png', '')
            
            if base_name in corrections:
                print(f"修正中: {base_name}")
                print(f"  変更前: {item['meta_tags']}")
                
                item['meta_tags'] = corrections[base_name]['meta_tags']
                item['description'] = corrections[base_name]['description']
                
                print(f"  変更後: {item['meta_tags']}")
                fixed_count += 1
        
        # バックアップを作成
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = f'./image_meta_tags_backup_{timestamp}.json'
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"バックアップを作成しました: {backup_path}")
        
        # 修正版を保存
        with open(meta_tags_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n修正完了: {fixed_count}個の語形変化を修正しました")
        
    except Exception as error:
        print(f'修正中にエラーが発生しました: {error}')

if __name__ == '__main__':
    fix_meta_tags()
