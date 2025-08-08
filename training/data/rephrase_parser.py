import json
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional

class RephraseParser:
    """Rephrase文要素分解システム"""
    
    def __init__(self, rules_file: str):
        with open(rules_file, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)
        
        # スロット順序
        self.slot_order = self.rules["slot_order"]
        
    def parse_sentence(self, sentence: str) -> Dict[str, str]:
        """文を文要素に分解"""
        # 基本的な文要素分解
        result = {slot: "" for slot in self.slot_order}
        
        # クリーニング
        sentence = sentence.strip().rstrip('.!?')
        
        # 疑問文チェック（Where did...）
        if sentence.startswith("Where"):
            result["M3"] = "Where"
            sentence = sentence[5:].strip()
            
            # did構文
            if sentence.startswith("did"):
                result["Aux"] = "did"
                sentence = sentence[3:].strip()
                
                # 主語抽出
                parts = sentence.split()
                if parts:
                    result["S"] = parts[0]
                    sentence = " ".join(parts[1:])
                    
                    # 動詞抽出（原形）
                    if sentence.startswith("get"):
                        result["V"] = "get"
                        sentence = sentence[3:].strip()
                        
                        # 目的語
                        if sentence:
                            result["O1"] = sentence
                            
        # 命令文チェック（You, give...）
        elif sentence.startswith("You,"):
            result["S"] = "You"
            sentence = sentence[4:].strip()
            
            # 動詞抽出
            if sentence.startswith("give"):
                result["V"] = "give"
                sentence = sentence[4:].strip()
                
                # give O1 to O2 構文
                if " to " in sentence:
                    parts = sentence.split(" to ")
                    result["O1"] = parts[0].strip()
                    if len(parts) > 1:
                        remaining = parts[1].strip()
                        # 副詞を分離
                        adverbs = ["straight", "clearly", "honestly", "directly"]
                        for adv in adverbs:
                            if remaining.endswith(adv):
                                result["M2"] = adv
                                result["O2"] = remaining[:-len(adv)].strip()
                                break
                        else:
                            result["O2"] = remaining
                            
        # modal構文（Would you...）
        elif sentence.startswith("Would"):
            result["Aux"] = "Would"
            sentence = sentence[5:].strip()
            
            if sentence.startswith("you") or sentence.startswith("I") or sentence.startswith("she") or sentence.startswith("they"):
                parts = sentence.split()
                result["S"] = parts[0]
                sentence = " ".join(parts[1:])
                
                # 動詞抽出
                if sentence.startswith("hold"):
                    result["V"] = "hold"
                    sentence = sentence[4:].strip()
                    
                    # 目的語と丁寧語
                    if sentence.endswith(", please"):
                        result["M2"] = "please"
                        sentence = sentence[:-8].strip()
                    
                    result["O1"] = sentence
                    
        # Could構文
        elif sentence.startswith("Could"):
            result["Aux"] = "Could"
            sentence = sentence[5:].strip()
            
            parts = sentence.split()
            if parts:
                result["S"] = parts[0]
                sentence = " ".join(parts[1:])
                
                if sentence.startswith("write"):
                    result["V"] = "write"
                    sentence = sentence[5:].strip()
                    
                    # write O1 down構文
                    if " down" in sentence:
                        parts = sentence.split(" down")
                        result["O1"] = parts[0].strip()
                        result["M2"] = "down"
                        
                        if len(parts) > 1 and parts[1].strip().endswith(", please"):
                            result["M3"] = "please"
                            
        # 否定文（I haven't seen...）
        elif "haven't" in sentence or "can't" in sentence:
            parts = sentence.split()
            if parts:
                result["S"] = parts[0]
                
                if "haven't" in sentence:
                    result["Aux"] = "haven't"
                    # haven't seen構文
                    if "seen" in sentence:
                        result["V"] = "seen"
                        # seen O1 for時間
                        seen_idx = sentence.find("seen") + 4
                        remaining = sentence[seen_idx:].strip()
                        
                        if " for " in remaining:
                            obj_part, time_part = remaining.split(" for ", 1)
                            result["O1"] = obj_part.strip()
                            result["M3"] = "for " + time_part.strip()
                        else:
                            result["O1"] = remaining
                            
                elif "can't" in sentence:
                    result["Aux"] = "can't"
                    if "afford" in sentence:
                        result["V"] = "afford"
                        # afford O1
                        afford_idx = sentence.find("afford") + 6
                        result["O1"] = sentence[afford_idx:].strip()
                        
        # 過去形（He/She entered, left, reached...）
        elif any(sentence.startswith(subj) for subj in ["He ", "She ", "Tom ", "They ", "Sarah "]):
            parts = sentence.split()
            result["S"] = parts[0]
            
            if len(parts) > 1:
                verb = parts[1]
                result["V"] = verb
                
                if verb in ["entered"]:
                    result["O1"] = " ".join(parts[2:])
                elif verb in ["left", "reached"]:
                    # 場所 + 時間
                    remaining = " ".join(parts[2:])
                    # 時間表現を分離
                    time_phrases = ["a few days ago", "last week", "yesterday", "this morning", 
                                  "the next morning", "that evening", "at noon", "at midnight"]
                    for time_phrase in time_phrases:
                        if time_phrase in remaining:
                            place_part = remaining.replace(time_phrase, "").strip()
                            result["O1"] = place_part
                            result["M3"] = time_phrase
                            break
                    else:
                        result["O1"] = remaining
                elif verb in ["mentioned"]:
                    result["O1"] = " ".join(parts[2:])
                elif verb in ["resembles"]:
                    result["O1"] = " ".join(parts[2:])
                elif verb in ["married"]:
                    result["O1"] = " ".join(parts[2:])
                elif verb.startswith("got"):
                    if "married with" in sentence:
                        result["V"] = "got married with"
                        married_idx = sentence.find("married with") + 12
                        result["O1"] = sentence[married_idx:].strip()
                elif verb.endswith("'s") or "'s been" in sentence:
                    # She's been married to...
                    if "been married to" in sentence:
                        result["Aux"] = "has been"
                        result["V"] = "married to"
                        # 時間表現を分離
                        for_idx = sentence.find(" for ")
                        if for_idx > 0:
                            obj_part = sentence[sentence.find("married to") + 10:for_idx].strip()
                            time_part = sentence[for_idx:]
                            result["O1"] = obj_part
                            result["M3"] = time_part
                elif verb.endswith("'ll"):
                    # He'll answer...
                    result["Aux"] = "will"
                    result["V"] = "answer"
                    remaining = " ".join(parts[2:])
                    
                    # 時間表現を分離
                    time_words = ["soon", "tomorrow", "later", "tonight"]
                    for time_word in time_words:
                        if remaining.endswith(time_word):
                            obj_part = remaining[:-len(time_word)].strip()
                            result["O1"] = obj_part
                            result["M3"] = time_word
                            break
                    else:
                        result["O1"] = remaining
                        
        # 現在形（I/You/We/They + 動詞）
        else:
            parts = sentence.split()
            if parts:
                result["S"] = parts[0]
                
                if len(parts) > 1:
                    verb = parts[1]
                    result["V"] = verb
                    
                    if verb == "lie":
                        # lie on場所
                        if "on" in sentence:
                            on_idx = sentence.find("on")
                            result["M3"] = sentence[on_idx:]
                    elif verb == "got":
                        result["O1"] = " ".join(parts[2:])
                    elif verb == "want":
                        result["O1"] = " ".join(parts[2:])
                    elif verb == "believe":
                        result["O1"] = " ".join(parts[2:])
                    elif verb == "approach":
                        result["O1"] = " ".join(parts[2:])
                    elif verb == "discuss":
                        result["O1"] = " ".join(parts[2:])
                    elif verb in ["reminds"]:
                        result["O1"] = " ".join(parts[2:])
                        
        return result
    
    def process_all_sentences(self, sentences_file: str) -> List[Dict]:
        """全例文を処理"""
        # 88例文ファイルを読み込み
        with open(sentences_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        
        for set_id, set_data in data["expanded_examples"].items():
            for i, sentence in enumerate(set_data["expanded"]):
                parsed = self.parse_sentence(sentence)
                
                result_row = {
                    "set_id": set_id,
                    "sentence_id": f"{set_id}_{i+1:02d}",
                    "original_sentence": sentence,
                    **parsed
                }
                
                results.append(result_row)
                
        return results
    
    def export_to_excel(self, results: List[Dict], output_file: str):
        """Excel形式で出力"""
        df = pd.DataFrame(results)
        
        # 列順序を整理
        columns = ["set_id", "sentence_id", "original_sentence"] + self.slot_order
        df = df[columns]
        
        # Excelファイルに保存
        df.to_excel(output_file, index=False, sheet_name="Rephrase文要素分解")
        
        return df

# 実行
if __name__ == "__main__":
    # パーサー初期化
    rules_path = r"c:\Users\yurit\Downloads\Rephraseプロジェクト20250529\例文セットDB作成システム\rephrase_rules_v1.0.json"
    parser = RephraseParser(rules_path)
    
    # 88例文を処理
    results = parser.process_all_sentences("expanded_examples_88.json")
    
    # Excel出力
    df = parser.export_to_excel(results, "rephrase_parsed_88_sentences.xlsx")
    
    print(f"✅ 処理完了: {len(results)}文を分解")
    print(f"📊 出力ファイル: rephrase_parsed_88_sentences.xlsx")
    
    # 結果のプレビュー
    print("\n🔍 分解結果プレビュー:")
    for i in range(min(5, len(results))):
        result = results[i]
        print(f"\n例文: {result['original_sentence']}")
        for slot in parser.slot_order:
            if result[slot]:
                print(f"  {slot}: {result[slot]}")
